from pathlib import Path
from time import sleep

from pydactyl import PterodactylClient

PTERODACTYL_URL = 'https://pterodactyl.yggdrasil'

api_key_file = Path(__file__).parent.resolve() / 'config/api_key'
with open(api_key_file, 'r') as f:
    api_key = f.read().strip()


class Server:
    client = PterodactylClient(PTERODACTYL_URL, api_key).client

    def __init__(self, identifier) -> None:
        details = self.client.servers.get_server(identifier)

        self.id = identifier
        self.name = details['name']
        self.maintenance = details['is_node_under_maintenance']
        self.resource_limits = details['limits']

        # Convert MiB to GiB
        self.resource_limits['memory'] /= 1024
        self.resource_limits['disk'] /= 1024

    def get_state(self) -> dict:
        usage = self.client.servers.get_server_utilization(self.id)

        return {
            "state": usage['current_state'],
            "cpu": round(usage['resources']['cpu_absolute'], 2), # percent
            "memory": round(usage['resources']['memory_bytes'] / 1073741824, 2), # GiB
            "disk": round(usage['resources']['disk_bytes'] / 1073741824, 2),     # GiB
        }

    def get_usage_string(self) -> str:
        usage = self.get_state()

        if self.resource_limits['memory'] > 0:
            memory = (usage['memory'] / self.resource_limits['memory']) * 100
            memory = f"{round(memory, 2)}%"
        else:
            memory = f"{usage['memory']} GiB"

        if self.resource_limits['disk'] > 0:
            disk = (usage['disk'] / self.resource_limits['disk']) * 100
            disk = f"{round(disk, 2)}%"
        else:
            disk = f"{usage['disk']} GiB"

        return f"CPU: {usage['cpu']}% | RAM: {memory} | DISK: {disk}"
    
    def wait_for_state(self, target: str, timeout=60) -> str:
        """Attempt to wait for a target state.
        
        Arguments:
            target  (str) | state to wait for
                Valid options: running, offline
            timeout (int) | seconds to wait before timing out

        Returns the current state. If timed out, appends (timeout)
        """

        if target not in ('offline', 'running'):
            raise ValueError("Target state must be one of: offline, running")

        time = 0
        state = self.get_state()['state']

        while state != target and time <= timeout:
            sleep(5)
            time += 5

            state = self.get_state()['state']

        if time > timeout:
            state += ' (timeout)'

        return state
    
    # TODO check overall resource usage/availability
    # TODO if state is 'stopping' wait for stop before sending start signal
    # maybe handle all not running cases ?
    def start(self) -> str:
        current_state = self.get_state()

        if current_state['state'] != 'offline':
            return f"Error: Cannot start server from state: current_state['state']"
        
        self.client.servers.send_power_action(self.id, 'start')
        return self.wait_for_state('running')
    
    def stop(self) -> str:
        current_state = self.get_state()

        if current_state['state'] != 'running':
            return f"Error: Cannot stop server from state: current_state['state']"
        
        self.client.servers.send_power_action(self.id, 'stop')
        return self.wait_for_state('offline')


def server_list() -> list:
    servers = []
    for s in Server.client.servers.list_servers().collect():
        servers.append(Server(s['attributes']['identifier']))

    return servers
