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

def container_list_raw():
    return wrap_json([{"containerID": c[0], "hostname": c[1], "ipList": c[2]} for c in dqs.list_containers()])

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
    cache_key = "service_by_id_%s" % id
    return cache_exec(cache_key, service_tasks_by_id_raw, [service_id])

run(host='localhost', port=8080)
