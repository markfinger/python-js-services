from optional_django import conf


class Verbosity(object):
    SILENT = 0
    CONNECT = 100  # Output when connections are opened
    PROCESS_START = 200  # Output when managers and managed hosts are started
    PROCESS_STOP = 300  # Output when managers and managed hosts are sent `stop` signals
    SERVICE_CALL = 400  # Output when services are called
    ALL = 500  # Output everything


class Conf(conf.Conf):
    # If True, turns on caching and deactivates the manager
    # If False, turns off caching and activates a basic process manager
    # which handle the host
    PRODUCTION = True

    # A path that will resolve to a node binary
    PATH_TO_NODE = 'node'

    # An absolute path to the directory containing the codebase for the
    # JavaScript library "service-host"
    PATH_TO_NODE_MODULES = None

    # An absolute path to the config file used for the `service_host.host`
    # singletons which services will use by default
    CONFIG_FILE = None

    # If True, the host will cache the output of the services until it expires.
    # This can be overridden on by services by adding `cachable = False` to the
    # subclass of `Service`, or by adding `cache: false` to the config file's
    # object for that particular service
    CACHE = PRODUCTION

    # By default this will print to the terminal whenever processes are started or
    # connected to. If you want to suppress all output, set it to
    # `service_host.conf.Verbosity.SILENT`
    VERBOSITY = Verbosity.PROCESS_START

    """
    DO *NOT* USE THE MANAGER IN PRODUCTION
    --------------------------------------

    If set to True, a manager process will be used to start and stop host processes.
    The manager runs at the port used by the config - either the defined or default
    one - and whenever a request comes in to start a host, it will either start
    it up or simply inform the python process where to find it.

    Do *not* use the manager in production, it exists purely to solve issues relating
    to the typical development environment:

    - Many of the typical JS services involve processes which have an initial overhead,
     but are performant after the first run, compilers are the usual example. Using a
     persistent process enables services to maintain a warm cache of the project's
     assets.

    - Running a persistent node process involves manually starting a node process
     with the proper incantation, which adds unwanted overhead on staff that are not
     familiar with the technology.

    - If the node process is started programmatically as a child of the python process,
     it will be need to be restarted with the the python process. Given the frequent
     restarts of python development servers, this delays the immediate feedback
     resulting from code changes.

    - If you run the node process as a detached child, this introduces additional
     overheads as you need to ensure that the process is inevitably stopped. The
     manager does this automatically, once a connection has been closed for a
     certain time period.

    The manager comes with certain downsides:

    - It is complicated to get access to the stdout/stderr of either the manager or
     the host. Hence, if the host goes down outside of a request cycle, there is no
     indication as to the reasons why.
    - The manager runs the host on a "random" port allocated by the OS, this introduces
     an unlikely, but technically possible, opportunity for a port collision to occur.

    To avoid these issues, you can simply run the host as a normal process, by calling
    `node node_modules/.bin/service-host path/to/services.config.js`, which will run
    a host directly on the port expected, and allow you to view the host's stdout and
    stderr.
    """
    USE_MANAGER = not PRODUCTION

    # When the python process exits, the manager is informed to stop the host once this
    # timeout has expired. If the python process is only restarting, the manager will
    # cancel the timeout once it has reconnected. If the python process is shutting down
    # for good, the manager will inevitably stop the host's process.
    ON_EXIT_MANAGED_HOSTS_STOP_TIMEOUT = 60 * 1000  # 1 minute

settings = Conf()