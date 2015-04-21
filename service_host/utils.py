from .service_host import ServiceHost
from .manager import Manager
from .managed_service_host import ManagedServiceHost


def singleton_host_and_manager(**kwargs):
    conf = {
        'path_to_node': kwargs['path_to_node'],
        'path_to_node_modules': kwargs['path_to_node_modules'],
        'config_file': kwargs['config_file'],
    }

    if kwargs['use_manager']:
        manager = Manager(**conf)

        # Managers run as persistent processes, so it may already be running
        if not manager.is_running():
            manager.start()

        manager.connect()

        host = ManagedServiceHost(manager=manager)
        host.start()
        host.connect()

        return host, manager

    host = ServiceHost(**conf)

    # In production environments, the host should be run as an external process
    # under a supervisor system. Hence we only connect to it, and verify that it
    # is using the config that we expect
    host.connect()

    return host, None