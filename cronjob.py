import sys
import redis

r = redis.Redis(host="localhost")
key = 'heatState'

if sys.argv[1] == "on":
    r.set(key, "True")
elif sys.argv[1] == "off":
    r.set(key, "False")


