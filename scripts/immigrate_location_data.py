import pymysql
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '000000',
    'db': 'chores',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**config)
conn.autocommit(1)

try:

    with conn.cursor() as cursor:
        cursor.execute("SELECT name, adcode, lnglat FROM system_region2 where type=3;")
        result = cursor.fetchall()

        for item in result:
            lon_lat_pair = item.get('lnglat').split(",")
            # r.geoadd('district:cn', lon_lat_pair[0], lon_lat_pair[1],item.get('name'))

finally:
    conn.close()
