from docker_query_service import DockerQueryService

dqs = DockerQueryService()
 
# [(serviceId, serviceName)]
print dqs.list_services()

# [(taskID, nodeID, containerID)]
print dqs.list_tasks() 

# [(nodeID, nodeName, nodeIP)]
print dqs.list_nodes()

# (nodeID, nodeName, nodeIP)
print dqs.get_node("qkhb3pzfcktm80pntsj24nuy7")

# [(containerID, hostname, [ip_list])]
print dqs.list_containers() 

## [(containerID, hostname, [ip_list])]
print dqs.get_containers_by_node_id("u2unvchn99gph46ve7x114vxc")

