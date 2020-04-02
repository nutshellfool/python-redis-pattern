import redis
from flask import Flask

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


if __name__ == '__main__':
    app.run()
