import math
import time
import uuid
from http import HTTPStatus

import redis
from flask import Flask
from flask import jsonify
from flask import request
from redlock import Redlock, Lock, MultipleRedlockException

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
rl = Redlock([{"host": "localhost", "port": 6379, "db": 0}, ])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/redis/echo')
def redis_echo_command():
    """
    Demonstration of redis command "echo"

    Returns:
        str the result of command "echo foo'
    """
    return r.echo("foo")


@app.route('/redis/string/key', methods=["POST"])
def redis_string_set_command():
    request_data = request.get_json()
    if not request_data:
        return "not valid post body"
    key = request_data.get('key')
    value = request_data.get('value')
    not_exist_update_only = request_data.get('nx', False)
    exist_update_only = request_data.get('xx', False)
    expire_in_seconds = request_data.get('ex', None)
    expire_in_milli_seconds = request_data.get('px', None)

    if not key or not value:
        return "not valid parameter"
    result = r.set(key, value, expire_in_seconds, expire_in_milli_seconds,
                   not_exist_update_only, exist_update_only)

    return jsonify({"result": result})


@app.route('/redis/string/key/<string:key>', methods=["GET"])
def redis_string_get_command(key):
    # key = request.args.get('key')
    result = r.get(key)
    return jsonify({"result": result.decode('utf-8')})


@app.route('/redis/list/append', methods=["POST"])
def redis_list_append_command():
    request_data = request.get_json()
    if not request_data:
        return "not valid post body"

    list_name = request_data.get('list_name')
    value = request_data.get('value')
    head = request_data.get('head', False)

    if None in {list_name, value}:
        return "not valid parameter"

    result = r.lpush(list_name, value) if head else r.rpush(list_name, value)
    return jsonify({'value': result})


@app.route('/redis/list/pop', methods=['POST'])
def redis_list_pop_command():
    request_data = request.get_json()
    if not request_data:
        return "not valid post body"

    list_name = request.args.get('list_name')
    value = request.args.get('value')
    head = request.args.get('head', False)
    if None in {list_name, value}:
        return jsonify({"message": "not valid parameter"})
    list_len = r.llen(list_name)
    if not list_len:
        return jsonify({"message": "empty list"})
    result = r.lpop(list_name) if head else r.rpop(list_name)
    return jsonify({'value': str(result, 'utf-8')})


@app.route('/redis/geo/hash', methods=['GET'])
def redis_geo_hash_command():
    key = request.args.get('key')
    member_name = request.args.get('member')
    if None in {key, member_name}:
        return jsonify({"message": "not a valid parameter"})
    result = r.geohash(key, member_name)
    return jsonify({"value": result})


@app.route('/redis/geo/radius', methods=["GET"])
def redis_geo_radius_command():
    key = request.args.get('key')
    longitude = request.args.get('lon')
    latitude = request.args.get('lat')
    nearby_distance = request.args.get('distance', 10000)

    if None in {key, longitude, latitude}:
        return jsonify({"message": "not a valid parameter"})
    result = r.georadius(key, longitude, latitude, nearby_distance)
    return jsonify({"value": result})


# distributed lock useage
@app.route('/redis/distributed/lock', methods=['GET'])
def redis_distributed_lock():
    lock_name = request.args.get('lock_name')
    lock_timeout = request.args.get('lock_timeout')
    acquire_timeout = request.args.get('require_timeout')

    if not lock_name:
        return jsonify({'code': HTTPStatus.BAD_REQUEST.value,
                        'message': 'lock_name required'})
    if not lock_timeout:
        lock_timeout = 10
    if not acquire_timeout:
        acquire_timeout = 10

    acquire_result = acquire_lock_with_timeout(r, lock_name,
                                               int(acquire_timeout),
                                               int(lock_timeout))
    if not acquire_result:
        return jsonify({"message": "acquire lock fail (timeout)"})

    return jsonify({"lockid": acquire_result})


@app.route('/redis/distributed/unlock', methods=['GET'])
def redis_distributed_unlock():
    lock_name = request.args.get('lock_name')
    lock_id = request.args.get('lock_id')
    if not (lock_name and lock_id):
        return jsonify({'code': HTTPStatus.BAD_REQUEST.value,
                        'message': 'necessary parameter(s) required'})
    release_result = release_lock(r, lock_name, lock_id)
    return jsonify({'code': HTTPStatus.OK.value, 'release': release_result})


def acquire_lock_with_timeout(
        conn, lockname, acquire_timeout=10, lock_timeout=10):
    identifier = str(uuid.uuid4())  # A
    _lock_name = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))  # D

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.set(_lock_name, identifier, ex=lock_timeout, nx=True):
            return identifier

        # the following code are equivalence with Directive:
        #
        # set(key, value, ex=xx, nx=True)

        # if conn.setnx(lockname, identifier):  # B
        #     conn.expire(lockname, lock_timeout)  # B
        #     return identifier
        elif conn.ttl(lockname) < 0:  # C
            conn.expire(lockname, lock_timeout)  # C

        time.sleep(.001)

    return False


def to_bytes(x):
    return x.encode() if isinstance(x, str) else x


def release_lock(conn, lock_name, identifier):
    pipe = conn.pipeline(True)
    _lock_name = 'lock:' + lock_name
    identifier = to_bytes(identifier)

    while True:
        try:
            pipe.watch(_lock_name)  # A
            if pipe.get(_lock_name) == identifier:  # A
                pipe.multi()  # B
                pipe.delete(_lock_name)  # B
                pipe.execute()  # B
                return True  # B

            pipe.unwatch()
            break

        except redis.exceptions.WatchError:  # C
            pass  # C

    return False  # D


@app.route('/redis/redlock/lock', methods=['GET'])
def redlock_acquire():
    lock_name = request.args.get('lock_name')
    lock_timeout = request.args.get('lock_timeout')

    if not lock_name:
        return jsonify({'code': HTTPStatus.BAD_REQUEST.value,
                        'message': 'lock_name required'})
    if not lock_timeout:
        lock_timeout = 10000

    acquire_result = rl.lock(lock_name, lock_timeout)
    if not acquire_result:
        return jsonify({"message": "acquire lock fail (timeout)"})

    return jsonify({"lock_name": acquire_result.resource,
                    "lock_key": acquire_result.key.decode('utf-8'),
                    "validity": str(acquire_result.validity)})


@app.route('/redis/redlock/unlock', methods=['GET'])
def redlock_release():
    lock_name = request.args.get('lock_name')
    lock_id = request.args.get('lock_key')
    validity = request.args.get('validity')
    if not (lock_name and lock_id and validity):
        return jsonify({'code': HTTPStatus.BAD_REQUEST.value,
                        'message': 'necessary parameter(s) required'})
    release_result = True
    try:
        rl.unlock(
            Lock(validity, lock_name, lock_id))
    except MultipleRedlockException:
        release_result = False

    return jsonify({'code': HTTPStatus.OK.value, 'release': release_result})


if __name__ == '__main__':
    app.run()
