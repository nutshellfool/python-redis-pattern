import redis
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)


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
    key = request.args.get('key')
    value = request.args.get('value')
    not_exist_update_only = request.args.get('nx', False)
    exist_update_only = request.args.get('xx', False)
    expire_in_seconds = request.args.get('ex', None)
    expire_in_milli_seconds = request.args.get('px', None)

    if not key or not value:
        return "not valid parameter"
    result = r.set(key, value, expire_in_seconds, expire_in_milli_seconds, not_exist_update_only, exist_update_only)

    return jsonify({"result": result})


@app.route('/redis/string/key', methods=["GET"])
def redis_string_get_command():
    key = request.args.get('key')
    result = r.get(key)
    return jsonify({"result": result})


@app.route('/redis/list/append', methods=["POST"])
def redis_list_append_command():
    list_name = request.args.get('list_name')
    value = request.args.get('value')
    head = request.args.get('head', False)

    if None in {list_name, value}:
        return "not valid parameter"

    result = r.lpush(list_name, value) if head else r.rpush(list_name, value)
    return jsonify({'value': result})


@app.route('/redis/list/pop', methods=['POST'])
def redis_list_pop_command():
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


if __name__ == '__main__':
    app.run()
