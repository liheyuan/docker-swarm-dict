import os

# docker machine location
#CERT_BASE_DIR = "/home/coder4/.docker/machine/machines/"
CERT_BASE_DIR = "/etc/dsd/machines/"
# docker swarm manager node
#NODE_SWARM_MANAGER = "node-1"
NODE_SWARM_MANAGER = os.environ["NODE_SWARM_MANAGER"] 
# docker swarm manager ip
#IP_SWARM_MANAGER = "192.168.99.100"
IP_SWARM_MANAGER = os.environ["IP_SWARM_MANAGER"]
