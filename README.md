# Python redis pattern

This is redis classical usage pattern project

## what problems 

Redis is a well-known data structure(key-value) database, 
build-in data structure supports many complex computing scenario.

Too many post and article introduce redis usage in theory not in real word application.

This project will introduce the redis usage in real word by instances.

## what usage patterns in this project

### Overview

It is well-known that redis build-in data structures

* String
* Lists
* Sets
* Sorted Sets
* Hashes
* Bitmap(Bit arrays)
* HyperLogLogs
* Streams


this build-in data structure usage in real life will be the first main part

beside that, redis also be used in distributed system, such as distributed lock.
So the distributed system usage will be the second main part 


### basic usage of build-in data structure

#### String

* cache a side

#### Lists

#### Sets

#### Sorted Sets

* leader board

#### hashes

#### Bitmap

* bloom filter

#### GEO

* GEO nearby information

#### HyperLogLogs

#### Streams

### distributed system usage

#### lock

* distributed lock (with lock timeout and acquire timeout)  
    * get lock 
    * release lock 

## Other topic

### Operation for redis

#### configuration

* changing on fly

* configuring redis as a cache

#### HA solution

##### sentinel and why sentinel works

#### cluster

## References

- [1] [Github - redis in action](https://github.com/josiahcarlson/redis-in-action)  
- [2] [redis official sites - An introduction to Redis data types and abstractions](https://redis.io/topics/data-types-intro)  
- [3] [黄健宏 - Redis 学习路线](https://blog.huangz.me/diary/2016/how-to-learn-redis.html)  
- [4] [redis official sites - Distributed locks](https://redis.io/topics/distlock)  
- [5] [redis official sites - config](https://redis.io/topics/config)  
- [6] [redis official sites - sentinel](https://redis.io/topics/sentinel)  
- [7] [redis official sites - memory optimization](https://redis.io/topics/memory-optimization)  
- [8] [redis official sites - Redis cluster tutorial](https://redis.io/topics/cluster-tutorial)  
- [9] [redis io - try redis](http://try.redis.io/)  
- [10] [Github - redis-py](https://github.com/RedisLabs/redis-py)  
