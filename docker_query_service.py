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
    def extract_node_info(self, node):
        return (node.id, node.attrs.get("Description", {}).get("Hostname", ""), node.attrs.get("Status", {}).get("Addr", ""))

    # [(nodeID, nodeName, nodeIP)]
    def list_nodes(self):
        return [self.extract_node_info(node) for node in self.sm_client.nodes.list()]

    # (nodeID, nodeName, nodeIP)
    def get_node(self, node_id):
        node = self.sm_client.nodes.get(node_id)
        return self.extract_node_info(node) 

    # [(nodeID, nodeName, nodeIP)]
    def extract_container_info(self, attrs):
        return (attrs.get("Id", ""), attrs.get("Config", {}).get("Hostname", ""), [x for x in get_recursively(attrs, "IPAddress") if len(x) > 0])

    # [(containerID, hostname, [ip_list])]
    def get_containers(self, node_name, node_ip):
        containerList = []
        node_client = DockerClientHelper.get_client(node_name, node_ip)
        for container in node_client.containers.list():
            attrs = container.attrs
            containerList.append(self.extract_container_info(attrs))
        return containerList

    # [(containerID, hostname, [ip_list])]
    def get_containers_by_node_id(self, node_id):
        containerList = []
        node = self.get_node(node_id)
        node_name = node[1]
        node_ip = node[2]
        node_client = DockerClientHelper.get_client(node_name, node_ip)
        for container in node_client.containers.list():
            attrs = container.attrs
            containerList.append(self.extract_container_info(attrs))
        return containerList

    # [(containerID, hostname, [ip_list])]
    def list_containers(self):
        containerList = []
        for (nodeID, nodeName, nodeIP) in self.list_nodes():
            containerList.extend(self.get_containers(nodeName, nodeIP))
        return containerList
