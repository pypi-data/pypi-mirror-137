# Python utilities and subsytems for Heptapod Runner

[Heptapod Runner](https://foss.heptapod.net/heptapod/heptapod-runner)
is the fork of [GitLab Runner](https://docs.gitlab.com/runner/) meant to
work for [Heptapod](https://heptapod.net) and [GitLab](https://gitlab.com)
instances.

The facilities provided in this package are part of the Heptapod Runner
extended distribution, aiming to provide additional options. They also
share the same
[source code repository](https://foss.heptapod.net/heptapod/heptapod-runner)
with Heptapod Runner.

They are not to be confused with the main Heptapod Runner program, which
is a standalone programm written in Go (like GitLab Runner) that does not have
any dependency on `python-heptapod-runner`.

Python was selected for fast prototyping and because it is lingua franca in
the Mercurial community, but It is possible that some of facilities end up
being rewritten in another language.

## `heptapod-paas-runner-register`

This interactive program can be used to bootstrap the configuration for
`heptapod-paas-runner`.

**Warning:** in all cases, the configuration has to be manually completed
afterwards.

It takes care notably of the registration against
the GitLab or Heptapod instance, hence playing a similar role as the
`gitlab-runner register` command.

It will just append a new `[[runners]` section if the configuration file
already exists.

### Caveats for configuration file creation

- The parent directory of the configuration file path has to exist,
  be writable by the system user doing the registration
- The resulting configuration file has to be readable by
  the system user for `heptapod-paas-runner`.
- The parent directory of the state file path has to be writable by the
  system user for  `heptapod-paas-runner`.


## `heptapod-paas-runner`

The purpose of this program is to provide on-demand provisioning while
following the expected workflows of PAAS systems:

- Docker hosts are provisioned only after jobs have been acquired from the
  coordinator
- actual job launch involves pushing a Dockerfile to a Git repository that
  controls the Docker host.

### Process and state management

#### Simple invocation

`heptapod-paas-runner` takes a single positional argument: the path to
its configuration file (see the section about `heptapod-paas-runner-register`
above)

Several options are available and can be displayed with:

```
heptapod-paas-runner --help
```

#### Graceful restart and state management

Heptapod PAAS Runner tracks the jobs it has launched
in order to deprovision the resources once they are finished.

To that end, it implements a graceful shutdown when `SIGTERM` is
received (this is the default stop signal used by many process managers,
including systemd).

Upon signal reception, it will

- stop acquiring new jobs
- finish operations that can't be interrupted (launchings, decommissionings)
- write all needed information about currently tracked jobs in a file
- exit

This shutdown sequence is not instantaneous. A waiting time of 2 minutes
should be enough before resorting to more drastic means (this includes margin).

We will probably improve the interruption of the launch sequence, but we
can't go as far as to interrupt a currently running request, as it could
provision untrackable resources.

#### Graceful reload

Currently not supported, a configuration change can be done without losing
information with the grateful restart.

In theory, a proper reload would be less dangerous.

#### Sample systemd unit file

```
[Unit]
Description=Heptapod PAAS Runner
After=network.target

[Install]
WantedBy=multi-user.target

[Service]
User=heptapod-runner
WorkingDirectory=/srv/heptapod-runner
ExecStart=/srv/heptapod-runner/venv/bin/heptapod-paas-runner /etc/heptapod-runner/pass-runner.toml
# We don't need a specific ExecStop, as systemd has a cascading system
# of defaults for the stop signal, with the
# SIGTERM being the ultimate default.

TimeoutStopSec=120
Restart=always
RestartSec=125
```

### The configuration file

`heptapod-paas-runner` uses the same configuration file as the normal
Heptapod (or GitLab) Runner.

Each `runners` section has an `executor` entry that must be one of the PAAS
executors, and consists otherwise of a mix of

- specific PAAS Runner configuration, depending on the executor.
- standard GitLab Runner configuration, forwarded to the final executor,
  unless forced by the PAAS Runner.

The PAAS executors are currently:

- `clever-docker` (see below)
- `local-docker`, for testing and development purposes only

Note: `heptapod-paas-runner` does not have a registration facility yet.
In practice, you can use any `heptapod-runner` or `gitlab-runner` executable
to create a configuration file with an appropriate coordinator token,
and then modify it for `heptapod-paas-runner`. This does not have to be done
on the actual target system.

### Global configuration

The global configuration is not forwarded to the PAAS resources. It is instead
used to tweak `heptapod-paas-runner` itself.


- `concurrency`: same meaning as in standard GitLab Runner configuration,
  controls the total number of jobs that can be acquired in parallel, hence
  of PAAS resources.
- `state_file`: path of the file used to keep tracking running jobs after
  a graceful restart.

### Common properties of the Docker executors

- All standard features (images, services) are supporteed

#### Image management and Dependency Proxy

We don't currently have the means to reuse PAAS resources, hence all jobs
start with fresh downloads of all necessary Docker images.

Partly because of this, the Heptapod PAAS Runner uses the Dependency Proxy
automatically, diverging in that from the standard GitLab Runner Docker
executor.

Practical consequences for job authors:

- do *not* disable the Dependency Proxy for your Group
- if a service has no alias defined in the job, it will be accessible with
  only one of [the two syntaxes normally supported by GitLab Runner](https://docs.gitlab.com/ce/ci/services/#accessing-the-services):

  + if the service image is defined as `postgres:13`, the service container
    can be accessed as usual as `postgres`
  + if the image is defined as `tutum/wordpress`, the service
    container can be accessed as `tutum-wordpress`, but *not*
    `tutum__wordpress`


### The `clever-docker` executor

This runs the job in [Clever Cloud](https://clever-cloud.com).

Clever Cloud is also the company hosting the [public Heptapod instance for
Free and Open Source Software](https://foss.heptapod.net), where Heptapod
is self-hosted and the [commercial Heptapod instance](https://heptapod.host).

There are two modes of operation: single organization and multi-tenant.

#### Common configuration

Required:

- `executor`: `clever-docker`
- `cc_extra_env` subsection. Can be used to pass extra environment to
  the sub-runner spawned on the provisioned resource. Currently
  `CC_ENABLE_HEPTAPOD_RUNNER = "true"` is necessary

Optional:

- `cc_api_url` (defaults to `https://api.clever-cloud.com/v2`):
  Clever Cloud base API URL
- `cc_zone` (defaults to `par`): any zone can be in theory used. In practice,
  the zone better be close to the GitLab / Heptapod instance (the coordinator).
- `cc_default_flavor` (defaults to `M`): the flavor (size) of instances that
  will be launched on Clever Cloud if not specified by the job.

#### Running for a single Clever Cloud Organization

Put these in the Runner configuration

- `cc_multi_tenant`: unspecified or `false`.
- `cc_orga_id`: specify the id of your Clever Cloud Organization, as seen,
  e.g, in its Overview page in the Clever Cloud console.
- `cc_token`: token for the Clever Cloud API, with enough rights to create,
  deploy and delete applications and instances

It doesn't matter whether the Runner is tied to specific Projects, a Group or
a whole GitLab / Heptapod instance: all resources will be attached
(and billed) to the specified Organization.

This is a good fit for a self-hosted Heptapod instance.

Full example:

```toml

concurrent = 8
state_file = "/srv/heptapod-runner/paas-runner-state.json"

[[runners]]
  name = "clever-cloud"
  url = "https://heptapod.example.com"
  token = "D3adNQYu8OCjkYDbwDaG"
  executor = "clever-docker"

  cc_orga_id = "orga_07cf2ef0-c9ad-4f04-b492-94c164f95c76"
  cc_token = "bb52e490-d47e-47a4-b190-73e23eb17111"

  [runners.cc_extra_env]
    CC_ENABLE_HEPTAPOD_RUNNER = "true"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    # A future version of Heptapod PAAS Runner may fill this in automatically.
    # Meanwhile it is possible to use any S3 configuration. Using Clever's
    # Cellar for your CI caches in the same zone is the best for
    # network proximity and bandwidth.
    # (replace with your credentials and bucket of choice)
    ServerAddress = "cellar-c2.services.clever-cloud.com"
    AccessKey = "dEA7gjmYM98gobVi6Y1x"
    SecretKey = "v0tdpjgpsDRqaSvIndvHAXFmjbpEd958gbZuO7yv"
    BucketName = "heptapod-ci"
    [runners.cache.gcs]
  [runners.docker]
    helper_image = "registry.heptapod.net/heptapod/heptapod-runner/helper:x86_64-latest"
    tls_verify = false
    image = "debian:bullseye"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
```

(all tokens and uuids in this example are random values freshly obtained
for this documentation)


#### The multi-tenant mode

In this mode, the runner determines the Clever Cloud Organization and the
associated API token from attributes of the top-level Heptapod Group to which
the Project belongs.

It assumes that something populates those attributes.

This mode of operation is intended for instances such as `heptapod.host`.

Required Runner configuration:

- `cc_multi_tenant`: `true`
- `cc_gitlab_namespace_attributes_token`: a GitLab / Heptapod private token
  with enough rights to query Group custom attributes.

Optional Runner configuration:

- `cc_orga_id_attribute` (defaults to `cc_orga_id`). Name of the custom
  attribute on top-level Groups to use for the Organization ID.
- `cc_orga_token_attribute (defaults to `cc_orga_token`). Name of the custom
  attribute on top-level Groups to use for the Clever API token of the
  Organization.

Full example:

```toml
concurrent = 8
state_file = "/srv/heptapod-runner/paas-runner-state.json"

[[runners]]
  name = "clever-cloud"
  url = "https://heptapod.example.com"
  token = "D3adNQYu8OCjkYDbwDaG"
  executor = "clever-docker"

  cc_multi_tenant = true
  cc_gitlab_namespace_attributes_token = "D7aY5I5SygxA5oyZ11vB"

  [runners.cc_extra_env]
    CC_ENABLE_HEPTAPOD_RUNNER = "true"

  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    # Do not fill in this: it would use the same bucket for all tenants.
    # A future version of Heptapod PAAS Runner will fill this automatically,
    # using the Cellar add-on of each tenant for proper separation.
    [runners.cache.gcs]
  [runners.docker]
    helper_image = "registry.heptapod.net/heptapod/heptapod-runner/helper:x86_64-latest"
    tls_verify = false
    image = "debian:bullseye"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
```

(all tokens in this example are random values freshly obtained for this
documentation)






