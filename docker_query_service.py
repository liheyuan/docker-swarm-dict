from docker_client_helper import DockerClientHelper
from utils import get_recursively

class DockerQueryService:
    def __init__(self):
        self.sm_client = DockerClientHelper.get_swarm_manager_client()
        pass

    # [(serviceId, serviceName)]
    def list_services(self):
        return [(x.id, x.name) for x in self.sm_client.services.list()]

    # [(taskID, (on)nodeID, (with)containerID)]
    def get_tasks(self, service_id):
        taskList = []
	for task in self.sm_client.services.get(service_id).tasks(filters={"desired-state": "running"}):
	    taskList.append((task.get("ID", ""), task.get("NodeID", ""), task.get("Status", {}).get("ContainerStatus", {}).get("ContainerID", "")))
	return taskList

    # [(taskID, (on)nodeID, (with)containerID)]
    def list_tasks(self):
        taskList = []
        for (serviceId, serviceName) in self.list_services():
            taskList.extend(self.get_tasks(serviceId))
        return taskList

    # [(nodeID, nodeName, nodeIP)]
    def list_nodes(self):
        return [(node.id, node.attrs.get("Description", {}).get("Hostname", ""), node.attrs.get("Status", {}).get("Addr", "")) for node in self.sm_client.nodes.list()]

    # [(containerID, hostname, [ip_list])]
    def get_containers(self, node_name, node_ip):
        containerList = []
        node_client = DockerClientHelper.get_client(node_name, node_ip)
        for container in node_client.containers.list():
            attrs = container.attrs
            containerList.append((attrs.get("Id", ""), attrs.get("Config", {}).get("Hostname", ""), [x for x in get_recursively(attrs, "IPAddress") if len(x) > 0]))
        return containerList

    # [(containerID, hostname, [ip_list])]
    def list_containers(self):
        containerList = []
        for (nodeID, nodeName, nodeIP) in self.list_nodes():
            containerList.extend(self.get_containers(nodeName, nodeIP))
        return containerList
