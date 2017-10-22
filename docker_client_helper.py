from config import *
import docker
import os

class DockerClientHelper:
    def __init__(self):
        pass 

    @staticmethod
    def get_client(node_name, ip):
        node_cert_dir = os.path.join(CERT_BASE_DIR, node_name)
        cert = os.path.join(node_cert_dir, 'cert.pem')
        key = os.path.join(node_cert_dir, 'key.pem')
        url = "tcp://%s:2376" % ip

        print cert, key 
        tls_config = docker.tls.TLSConfig(
            client_cert=(cert, key)
        )

        return docker.DockerClient(base_url=url, tls=tls_config)

    @staticmethod
    def get_swarm_manager_client():
        return DockerClientHelper.get_client(NODE_SWARM_MANAGER, IP_SWARM_MANAGER)
