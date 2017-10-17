from docker_query_service import DockerQueryService

dqs = DockerQueryService()
 
# [(serviceId, serviceName)]
print dqs.list_services()

# [(taskID, nodeID, containerID)]
print dqs.list_tasks() 

# [(nodeID, nodeName, nodeIP)]
print dqs.list_nodes()

# [(containerID, hostname, [ip_list])]
print dqs.list_containers() 
