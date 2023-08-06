# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
from overrides import overrides
import requests
import tempfile
import time

from .docker import DockerBuildHelper
from .exceptions import (
    GitLabUnexpectedError,
    PaasProvisioningError,
    PaasResourceError,
)
from .job import get_job_variable
from .runner import PaasRunner

logger = logging.getLogger(__file__)

FLAVOR_JOB_VARIABLE_NAME = 'CI_CLEVER_CLOUD_FLAVOR'
DEFAULT_FLAVOR = 'M'
"""Ultimate default if flavor not specified in job nor runner config."""

CC_ORGA_ID_ATTRIBUTE = 'cc_orga_id'
CC_ORGA_TOKEN_ATTRIBUTE = 'cc_orga_token'


def convert_http_error(http_response):
    """Return error code, message."""
    try:
        resp_data = http_response.json()
        assert resp_data['type'] == 'error'
        # checked with Clever, `id` is definitely an error code
        return resp_data['id'], resp_data['message']
    except Exception:
        return None, http_response.text


class CleverCloudDockerRunner(PaasRunner):

    executor = 'clever-docker'
    _available_flavors = (None, None)
    """dict of available flavors and timestamp of retrieval.
    """

    def __init__(self, config):
        super(CleverCloudDockerRunner, self).__init__(config)
        self.init_cc_global()
        self.init_cc_git()
        self.init_cc_orga()
        self.init_common_app_params()

    def init_cc_global(self):
        self.cc_base_url = self.config.get('cc_api_url',
                                           'https://api.clever-cloud.com/v2')
        self.cc_zone = self.config.get('cc_zone', 'par')
        self.cc_default_flavor = self.config.get('cc_default_flavor',
                                                 DEFAULT_FLAVOR)

    def init_cc_orga(self):
        if self.config.get('cc_multi_tenant'):
            self.fixed_cc_orga = None
        else:
            self.fixed_cc_orga = CleverCloudOrganization(
                self.cc_base_url,
                orga_id=self.config['cc_orga_id'],
                git_user=self.cc_git_user,
                token=self.config['cc_token'])
        self.gl_attributes_token = self.config.get(
            'cc_gitlab_namespace_attributes_token')
        self.cc_orga_id_attribute = self.config.get(
            'cc_orga_id_attribute', CC_ORGA_ID_ATTRIBUTE)
        self.cc_orga_token_attribute = self.config.get(
            'cc_orga_token_attribute', CC_ORGA_TOKEN_ATTRIBUTE)
        self.all_cc_orga_attributes = (self.cc_orga_id_attribute,
                                       self.cc_orga_token_attribute,
                                       )

    @property
    def available_flavors(self):
        """Cached dict of available flavors.

        This is a mapping whose keys are user flavor names, such as `'XL'`
        and values are the actual names expected by Clever Cloud
        (e.g, `'heptapod-runner-XL'`).

        The caching is not really thread-safe, but the worst that can
        happen is several GET requests towards the Clever API if several
        threads realize that the timestamp is outdated at the same time.
        It is very unlikely that these requests would give different results
        and even more unlikely that it would make a difference for the end
        user (using a flavor that just got advertised or that doesn't exist
        anymore. In the first case, the job will be able to run earlier than
        expected, in the second case we're only losing a job that would have
        been invalid mere seconds later).
        """
        available, ts = self._available_flavors
        if available is not None and time.time() - ts < 3600:
            return available

        timestamp = time.time()
        # default values should be the final ones in production,
        # configurability will help us in particular to prototype with
        # the Jenkins flavors.
        flavor_context = self.config.get('cc_flavor_context',
                                         'heptapod-runner')
        params = dict(context=flavor_context)
        resp = requests.get(self.cc_base_url + '/products/flavors',
                            params=params)

        if resp.status_code >= 400:
            # TODO surely this must most of the times
            # be a transient failure. Retry logic?
            error_code, message = convert_http_error(resp)
            raise PaasProvisioningError(action='get-available-flavors',
                                        action_details=params,
                                        transport_code=resp.status_code,
                                        code=error_code,
                                        error_details=message,
                                        executor=self.executor)

        prefix = self.config.get('cc_flavor_name_prefix', flavor_context + '-')
        available = {
            flav['name'][len(prefix):]: flav['name']
            for flav in resp.json()
            if flav['name'].startswith(prefix)}
        logger.info("Retrieved variant flavors. Resulting mapping: %r",
                    available)
        self._available_flavors = available, timestamp
        return available

    def init_cc_git(self):
        self.cc_git_user = self.config.get('cc_auth_user', 'Jenkins')

    def init_common_app_params(self):
        self.common_app_params = {
            # TODO could depend on job rather than runner
            'zone': self.cc_zone,
            'instanceLifetime': 'TASK',
            'instanceType': 'docker',
            'deploy': 'git',
            'instanceVariant': self.config.get(
                'cc_instance_variant_uuid',
                # This is the initial UUID for Heptapod Runner variant
                "70d676a0-a775-4dc9-a43d-3121036e8515"),
            'maxInstances': 1,  # we'll do our own auto scaling
            'minInstances': 1,
        }

    def inner_executor(self):
        return 'docker'

    def is_config_item_for_inner(self, key):
        return (key != 'heptapod_runner_main_image'
                and not key.startswith('cc_'))

    def cc_docker_instance_type(self):
        resp = requests.get(self.cc_base_url + '/products/instances')
        if resp.status_code >= 400:
            error_code, message = convert_http_error(resp)
            raise PaasProvisioningError(action='get-instance-type',
                                        transport_code=resp.status_code,
                                        code=error_code,
                                        error_details=message,
                                        executor=self.executor)

        assert resp.status_code == 200
        docker_types = [inst for inst in resp.json()
                        if inst['name'] == 'Docker']
        # TODO what if several match? Are, e.g., several versions
        # possible at a given time?
        return docker_types[0]

    def cc_select_flavor(self, instance_type, job):
        flavor = get_job_variable(job, FLAVOR_JOB_VARIABLE_NAME)
        if flavor is None:
            flavor = self.cc_default_flavor

        available = self.available_flavors
        cc_flavor = available.get(flavor)
        if cc_flavor is None:
            raise PaasProvisioningError(
                action='check-flavor',
                transport_code=None,
                code=1,
                error_details="Selected flavor %r is not available, "
                "possible choices are %r" % (flavor,
                                             list(self.available_flavors)),
                executor=self.executor,
            )
        return cc_flavor

    def job_cc_orga(self, job):
        orga = self.fixed_cc_orga
        if orga is not None:
            return orga

        return self.cc_orga(self.gitlab_job_top_namespace(job))

    def gitlab_job_top_namespace(self, job):
        return get_job_variable(job, 'CI_PROJECT_ROOT_NAMESPACE')

    def cc_orga(self, gitlab_namespace):
        orga = self.fixed_cc_orga
        if orga is not None:
            return orga

        # perhaps we should have a dedicated PaasAccessError
        # meanwhile, this will be good enough.
        try:
            attrs = self.gitlab_custom_attributes(
                gitlab_namespace,
                self.all_cc_orga_attributes,
                token=self.gl_attributes_token,
            )
        except GitLabUnexpectedError as exc:
            raise PaasProvisioningError(
                executor=self.executor,
                action='find-orga',
                action_details='namespace=%r, '
                'failed attributes request on %r: %s' % (
                    gitlab_namespace,
                    exc.url,
                    exc.message
                ),
                code=exc.status_code)
        try:
            orga_id, orga_token = (attrs[self.cc_orga_id_attribute],
                                   attrs[self.cc_orga_token_attribute])
        except KeyError as exc:
            raise PaasProvisioningError(
                executor=self.executor,
                action='find-orga',
                action_details='namespace=%r, '
                'missing attribute %r' % (gitlab_namespace,
                                          exc.args[0]),
                code=None)

        return CleverCloudOrganization(
            self.cc_base_url,
            gitlab_namespace=gitlab_namespace,
            orga_id=orga_id,
            git_user=self.cc_git_user,
            token=orga_token)

    @overrides
    def provision(self, job):
        # TODO cache instance_type, and reload only if provision ends
        # with errors possibly due to outdated information (including change
        # of flavor availability)
        # (error code for unknown application should be 4004)
        instance_type = self.cc_docker_instance_type()

        req_data = self.common_app_params.copy()
        req_data['instanceVersion'] = instance_type['version']

        flavor = self.cc_select_flavor(instance_type, job)
        req_data['minFlavor'] = req_data['maxFlavor'] = flavor

        req_data['name'] = 'hpd-job-%s-%d' % (self.unique_name, job['id'])
        app = self.job_cc_orga(job).create_app(req_data)

        cc_env = {'CC_MOUNT_DOCKER_SOCKET': 'true'}
        extra_env = self.config.get('cc_extra_env')
        if extra_env:
            cc_env.update(extra_env)

        app.put_env(cc_env)
        return app

    @overrides
    def load_paas_resource(self, data):
        # this maintains compatibility with data dumped without a
        # GitLab namespace for runners with a fixed CC Organization
        gl_namespace = data.get('gitlab_namespace')
        try:
            cc_orga = self.cc_orga(gl_namespace)
        except PaasProvisioningError as exc:
            # In a multi-tenant system, one misconfigured tenant
            # should not crash the whole system.
            logger.error(
                "Failed to load PAAS resource from data %r."
                "Operations on resource, notably decommission, "
                "won't be possible. "
                "action=%r, action_details=%r, code=%r, error_details=%r",
                data, exc.action, exc.action_details,
                exc.code, exc.error_details)
            # we should also not lose data about the resource just
            # because we couldn't resolve the orga this time
            cc_orga = OrganizationNotFound(gl_namespace)

        return cc_orga.load_application(data)

    @overrides
    def launch(self, paas_resource, job_data):
        with tempfile.TemporaryDirectory() as tmp_path:
            build_helper = DockerBuildHelper.from_runner_config(tmp_path,
                                                                self.config)
            build_helper.write_build_context(self, job_data)
            build_helper.git_push(paas_resource.git_push_url)

    @overrides
    def decommission(self, paas_resource):
        app_id = paas_resource.app_id

        resp = paas_resource.orga.delete_app(app_id)
        if resp.status_code >= 400:
            error_code, message = convert_http_error(resp)
            raise PaasResourceError(app_id, self.executor,
                                    action='delete',
                                    action_details=None,
                                    code=error_code,
                                    transport_code=resp.status_code,
                                    error_details=message)
        logger.debug('decommission: successful response %r', resp.text)

    def decommission_all(self, gitlab_namespace=None):
        """Decommission all PAAS resources for this runner.

        This is obviously dangerous and if ever exposed to the CLI or
        users in any way, care must be taken to make sure it can't
        happen by accident.

        :param gitlab_namespace: if specified, will be used to
           find the relevant Organization. Otherwise, :attr:`fixed_cc_orga`
           will be used. If the latter is ``None`` (typically case of a
           multi-tenant Runner), then `ValueError` is raised.

        :returns: the number of decommissionned resources and number of
           ignored ones (not related to this runner).
        """
        if gitlab_namespace is None:
            if self.fixed_cc_orga is None:
                raise ValueError("This Runner %r does not have a fixed "
                                 "Clever Cloud Organization. "
                                 "To decommission all "
                                 "its resources, the path of the GitLab "
                                 "namespace bearing the CC Organization and "
                                 "token must be given." % self.unique_name)
            else:
                cc_orga = self.fixed_cc_orga
        else:
            cc_orga = self.cc_orga(gitlab_namespace)

        logger.warning("Decommissionning all PAAS resources for runner %r"
                       " on Clever Cloud Organization %r",
                       self.unique_name, cc_orga.orga_id)
        rsc_name_prefix = 'hpd-job-%s-' % self.unique_name
        done = 0
        ignored = 0
        for app_data in cc_orga.list_applications():
            if not app_data.get('name', '').startswith(rsc_name_prefix):
                ignored += 1
                continue

            app = cc_orga.application(app_data)
            self.decommission(app)
            done += 1

        logger.info("Decommissionned the %d applications spawned by "
                    "runner %r, and ignored %d unrelated applications "
                    "in the same organization %r",
                    done, self.unique_name, ignored, cc_orga.orga_id)
        return done, ignored


CleverCloudDockerRunner.register()


class CleverCloudOrganization:

    executor = CleverCloudDockerRunner.executor
    """Used in logging and raising of exceptions."""

    def __init__(self, base_api_url, orga_id, token, git_user,
                 gitlab_namespace=None):
        """Information needed to work on Clever API for an Organization.
        """
        self.base_api_url = base_api_url
        self.orga_id = orga_id
        self.git_user = git_user
        self.token = token
        self.gitlab_namespace = gitlab_namespace

        self.url = '/'.join((base_api_url, 'organisations', orga_id))
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + self.token,
        }

    @property
    def applications_url(self):
        return '/'.join((self.url, 'applications'))

    def app_url(self, app_id):
        return '/'.join((self.applications_url, app_id))

    def create_app(self, data):
        """Create an application by calling the proper endpoint.

        :returns: :class:`CleverCloudApplication`
        """
        logger.debug("create_app data=%r", data)
        resp = requests.post(self.applications_url,
                             headers=self.headers,
                             json=data)
        if resp.status_code >= 400:
            # TODO catch error due to outdated version to recompute it
            # and raise something appropriate for other errors.
            # Actual error got due to lack of version is currently in use in
            # test_clever.py for easy reference.
            error_code, message = convert_http_error(resp)
            raise PaasProvisioningError(action='create-app',
                                        action_details=data,
                                        code=error_code,
                                        transport_code=resp.status_code,
                                        error_details=message,
                                        executor=self.executor,
                                        )
        logger.debug("CleverCloud application creation: "
                     "successful response %r", resp.text)

        return self.application(resp.json())

    def application(self, resp_data):
        """Represent an existing CC application from API response data.

        The data can be obtained, e.g., from a creation request, or a listing
        request.
        """
        return CleverCloudApplication(
            orga=self,
            app_id=resp_data['id'],
            deploy_url=resp_data['deployment']['httpUrl'],
            user=self.git_user,
            password=self.token,
        )

    def load_application(self, data):
        """Load application from saved data."""
        return CleverCloudApplication(
            orga=self,
            app_id=data['id'],
            deploy_url=data['deploy_url'],
            user=self.git_user,
            password=self.token,
        )

    def delete_app(self, app_id):
        """Delete an application.

        Kept as a method on the organization, because we need less
        detailed information to delete an application that to use it.
        """
        return requests.delete(self.app_url(app_id),
                               headers=self.headers)

    def list_applications(self):
        """Return the list of all applications.

        This list may include applications that are *not* related to
        a given Runner, or not even CI related: this is the Clever Cloud
        API request result after JSON decoding.
        """
        return requests.get(self.applications_url,
                            headers=self.headers).json()


class OrganizationNotFound(CleverCloudOrganization):
    """Represent a failure to resolve an organization.

    Used to keep track of CleverCloudApplication instances even if
    the corresponding organization could not be resolved (typically after
    a restart on a wrong configuration or while the coordinator is down).
    This is enough to allow various kinds of retry.
    """

    def __init__(self, gitlab_namespace):
        self.gitlab_namespace = gitlab_namespace
        self.git_user = None
        self.token = None
        self.url = None

    def __eq__(self, other):
        return self.gitlab_namespace == other.gitlab_namespace

    def app_url(self, app_id):
        """Always return None to express URL is not known."""

    def delete_app(self, app_id):
        raise PaasResourceError(
            app_id, self.executor,
            action='delete',
            code=22,  # chosen arbitrarily (randint call)
            error_details="Could not find Clever Cloud Organization "
            "credentials for the GitLab namespace %r this resource is "
            "linked to. Earlier logs may have details "
            "about failed attempts." % self.gitlab_namespace,
            )


class CleverCloudApplication:

    def __init__(self, orga, app_id, deploy_url, user, password):
        self.orga = orga
        self.app_id = app_id
        self.api_url = orga.app_url(self.app_id)
        self.deploy_url = deploy_url

        self.git_push_url = deploy_url.replace(
            'https://',
            'https://%s:%s@' % (user, password))

    @property
    def executor(self):
        return self.orga.executor

    @property
    def headers(self):
        return self.orga.headers

    def dump(self):
        # we don't dump credentials. If this is loaded by a Runner,
        # it will reinitialize the credentials, maybe with an updated value.
        return dict(id=self.app_id,
                    gitlab_namespace=self.orga.gitlab_namespace,
                    deploy_url=self.deploy_url)

    def put_env(self, env):
        """Add environment variables to the application.
        """
        resp = requests.put(self.api_url + '/env',
                            json=env,
                            headers=self.headers)

        if resp.status_code >= 400:
            error_code, message = convert_http_error(resp)
            raise PaasResourceError(self.app_id, self.executor,
                                    action='put-env',
                                    action_details=env,
                                    code=error_code,
                                    transport_code=resp.status_code,
                                    error_details=message)
        # success code should be 328.
        logger.debug('CleverCloudApplication.put_env: successful response %r',
                     resp.text)
        return resp
