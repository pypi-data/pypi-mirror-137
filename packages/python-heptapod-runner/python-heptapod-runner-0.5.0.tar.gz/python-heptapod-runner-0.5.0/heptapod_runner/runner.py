# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import requests
from requests.exceptions import RequestException
import toml

from .exceptions import (
    GitLabUnavailableError,
    GitLabUnexpectedError,
)


logger = logging.getLogger(__name__)

INNER_CONFIG_EXCLUDED_ITEMS = ('heptapod_runner_main_image',
                               )
"""Configuration items that are never to be forwarded to running resources.

This collection is for items that should be excluded with all concrete
subclasses of :class:`PaasRunner`.

For per-class specific rules, see :meth:`PaasRunner.is_config_item_for_inner`
"""


class PaasRunner:
    """Abstract base class for one of the `[[runners]]` of the main config.

    Concrete subclasses will be able to provision PAAS resources and
    launch the main Heptapod Runner's command to run one job on them.
    """

    executor = None
    """Executor name for the PAAS runner.

    Must be unique and not one of the executors provided by the main Heptapod
    Runner executable.
    """

    @classmethod
    def register(cls):
        runner_classes[cls.executor] = cls

    @staticmethod
    def create(config):
        """Instantiate with the appropriate class."""
        return runner_classes[config['executor']](config)

    def __init__(self, config):
        self.config = config
        self.gitlab_token = self.config['token']
        # GitLab itself uses the 8 first chars in the token as a unique
        # string identifier.
        self.gitlab_api_url = self.config['url'].rstrip('/') + '/api/v4'
        self.unique_name = self.gitlab_token[:8]

    def inner_executor(self):
        """Return executor for actual use on provisoned PAAS resource.

        To be provided by concrete classes, and must be one of the executors
        provided by the main Heptapod Runner executable.

        This is a method because a given class can use several different
        executors.
        """
        raise NotImplementedError  # pragma no cover

    def is_config_item_for_inner(self, key):
        """Tell if the given item  is to be forwarded to the PAAS resource.

        For instance, configuration items allowing to provision PAAS resources
        should not be made available to a provisioned one, so that an attack
        from a job on the runner on the PAAS resource would not leak means
        to provision infinite resources.

        This method cannot be used to allow items that are in
        :const:`INNER_CONFIG_EXCLUDED_ITEMS`.

        To be extended by concrete classes
        """
        raise NotImplementedError  # pragma no cover

    def dump_inner_config(self, path):
        """Make a full configuration for use on provisioned PAAS resource.

        The produced configuration has a single `[[runner]]` section, with
        the end executor meant for the present Runner.

        It will be used with the `exec-fetched-job` command of Heptapod Runner.
        """
        # TODO should be computed and serialized (to string) only once
        inner_runner = {k: v for k, v in self.config.items()
                        if k not in INNER_CONFIG_EXCLUDED_ITEMS
                        and self.is_config_item_for_inner(k)}
        inner_runner['executor'] = self.inner_executor()
        inner_config = dict(runners=[inner_runner])
        with open(path, 'w') as fobj:
            toml.dump(inner_config, fobj)

    def request_job(self):
        """Request one job from the coordinator

        :return: Job definition (JSON `str`) or `None` if there isn't any.
        """
        url = self.gitlab_api_url + '/jobs/request'
        post_data = dict(token=self.config['token'],
                         info=dict(executor=self.inner_executor(),
                                   features=dict(
                                       # always true (shells/abstract.go)
                                       upload_multiple_artifacts=True,
                                       upload_raw_artifacts=True,
                                       refspecs=True,
                                       artifacts=True,
                                       artifacts_exclude=True,
                                       multi_build_steps=True,
                                       return_exit_code=True,
                                       raw_variables=True,
                                       cache=True,
                                       masking=True,
                                       # true for Docker executor
                                       variables=True,
                                       image=True,
                                       services=True,
                                       session=True,
                                       terminal=True,
                                       # shared seems to be set to True
                                       # for shell, ssh and custom only.
                                       shared=False,
                                       # proxy seems to be set to True
                                       # for kubernetes only.
                                       # TODO evaluate if we shouldn't set
                                       # it for PAAS Runner
                                       proxy=False,
                                       ),
                                   )
                         )
        try:
            resp = requests.post(url, json=post_data)
        except RequestException as exc:
            raise GitLabUnavailableError(url=url, message=str(exc))

        if resp.status_code in (502, 503):
            # to be catched in main loop
            # (don't want to end everything if coordinator is temporarily
            # not available)
            raise GitLabUnavailableError(status_code=resp.status_code,
                                         message=resp.text,
                                         url=url)
        elif resp.status_code >= 400:
            raise GitLabUnexpectedError(status_code=resp.status_code,
                                        params=None,
                                        message=resp.text,
                                        url=url)

        if resp.status_code == 204:  # no job
            return None
        return resp.text

    def is_job_finished(self, job_handle):
        # Using the API endpoint to get a job by its token
        url = self.gitlab_api_url + '/job'
        try:
            resp = requests.get(url, params=dict(job_token=job_handle.token))
        except RequestException as exc:
            raise GitLabUnavailableError(url=url, message=str(exc))
            # TODO raise the usual exceptions, just catch and log from
            # the polling method

        if resp.status_code == 401:
            # of course this is ugly, but assuming we are correct
            # on our call (proper token, on a job that was properly
            # acquired), then geting a 401 means that the job is not
            # running anymore. Doing something more natural may require
            # changes in the Rails app (or next main iteration of the Paas
            # Runner, with a proper HTTP service)
            return True
        elif resp.status_code >= 400:
            raise GitLabUnexpectedError(status_code=resp.status_code,
                                        params=None,
                                        message=resp.text,
                                        url=url)

        # TODO cancel provisioned resource if job is canceled
        status = resp.json().get('status')
        logger.debug("%s status is %r", job_handle, status)
        return status in ('failed', 'success', 'canceled')

    def gitlab_custom_attributes(self, resource_path, keys,
                                 token=None,
                                 resource_type='groups'):
        """Retrieve custom attributes with the given keys.

        :param token: if specified, is used instead of the usual runner token
        :returns: a `dict` with the wished keys. It is *not* guaranteed that
                  all are present.
        """
        if token is None:
            token = self.gitlab_token
        # if there are more than one keys, it is expected to be much
        # more efficient to list all attributes rather than issue as
        # many requests. This can be tweaked later if needed.
        url = '/'.join((self.gitlab_api_url,
                        resource_type,
                        resource_path.replace('/', '%2F'),
                        'custom_attributes'))
        resp = requests.get(url, headers={'Private-Token': token})
        if resp.status_code >= 400:
            raise GitLabUnexpectedError(status_code=resp.status_code,
                                        params=None,
                                        message=resp.text,
                                        url=url)
        return {attr['key']: attr['value'] for attr in resp.json()
                if attr['key'] in keys}

    def report_coordinator_job_failed(self, job_handle, message):
        url = self.gitlab_api_url + '/jobs/%d' % job_handle.job_id
        params = dict(token=job_handle.token,
                      failure_reason=message,
                      exit_code=103,
                      state='failed')
        resp = requests.put(url, json=params)

        if resp.status_code >= 400:
            params['token'] = 'REDACTED'
            raise GitLabUnexpectedError(status_code=resp.status_code,
                                        params=params,
                                        message=resp.text,
                                        url=url)

    def provision(self, job):
        """Provision necessary resources in which to actually run the job.

        To be implemented by subclasses
        """
        raise NotImplementedError('provision')  # pragma no cover

    def launch(self, paas_resource, job_data):
        """Schedule the job to run on the given PAAS resource.

        To be implemented by subclasses
        """
        raise NotImplementedError('laucnh')  # pragma no cover

    def decommission(self, paas_resource):
        """Delete the PAAS resource."""
        raise NotImplementedError('decommission')  # pragma no cover

    def load_paas_resource(self, data):
        """Create a full PAAS resource from minimal extracted data.

        Given a resource ``rsc`` created by this Runner instance,
        ``self.restore_paas_resouce(rsc.export())`` should give back a
        fully functional new resource.

        Typically will be used for state save before shutdown and restoration
        after startup, perhaps using changed configuration accessible from
        the Runner.
        """
        raise NotImplementedError("load_paas_resource")  # pragma no cover


runner_classes = {}
"""Mapping of executor to runner class."""
