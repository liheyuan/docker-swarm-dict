# docker-swarm-ipdict

## Dependency
pip install docker[tls] bottle cachetools

## Local Usage

Modify config.py

```python
# docker machine location
CERT_BASE_DIR = "/home/coder4/.docker/machine/machines/"
# docker swarm manager node
NODE_SWARM_MANAGER = "node-1"
# docker swarm manager ip
IP_SWARM_MANAGER = "192.168.99.100"
```

## Docker usage
```shell
docker run \
  -p8080:8080 \
  --env NODE_SWARM_MANAGER=node-1 \
  --env IP_SWARM_MANAGER=192.168.99.100 \
  --volume $HOME/.docker/machine/machines:/etc/dsd/machines \
  --detach \
  coder4/swarmdict:1.1
```
