from bottle import route, run, response
from docker_query_service import DockerQueryService
from cachetools import TTLCache, cached
import json

dqs = DockerQueryService()

cache = TTLCache(maxsize=1024, ttl=10)

def wrap_json(obj):
    response.content_type = 'application/json'
    return json.dumps(obj)

def cache_exec(key, func, extraArgs):
    if key in cache:
        return cache[key]
    else:
        val = func(*extraArgs)
        cache[key] = val
        return val

def wrap_container(c):
    return {"containerID": c[0], "hostname": c[1], "ipList": c[2]}

def container_list_raw():
    return wrap_json([wrap_container(c) for c in dqs.list_containers()])

@route('/container/list')
def container_list():
    cache_key = "container_list"
    return cache_exec(cache_key, container_list_raw, [])

def service_list_raw():
    return wrap_json([{"serviceID": s[0], "name": s[1]} for s in dqs.list_services()])

@route('/service/list')
def container_list():
    cache_key = "service_list"
    return cache_exec(cache_key, service_list_raw, [])

def service_tasks_by_id_raw(service_id):
    return wrap_json([{"taskID": t[0], "nodeID": t[1], "containerID": t[2]} for t in dqs.get_tasks(service_id)])

@route('/service/id/<service_id>/tasks')
def service_tasks_by_id(service_id):
    cache_key = "service_tasks_by_id_%s" % service_id
    return cache_exec(cache_key, service_tasks_by_id_raw, [service_id])

def node_list_raw():
    return wrap_json([{"nodeID": s[0], "nodeName": s[1], "nodeIP": s[2]} for s in dqs.list_nodes()])

@route('/node/list')
def node_list():
    cache_key = "node_list"
    return cache_exec(cache_key, node_list_raw, [])

def node_containers_by_id_raw(node_id):
    return wrap_json([wrap_container(c) for c in dqs.get_containers_by_node_id(node_id)])

@route('/node/<node_id>/containers')
def node_containers_by_id(node_id):
    cache_key = "node_containers_by_id_%s" % node_id
    return cache_exec(cache_key, node_containers_by_id_raw, [node_id])

run(host="0.0.0.0", port=8080)
