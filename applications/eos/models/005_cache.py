# from gluon.contrib.redis_utils import RConn
# from gluon.contrib.redis_cache import RedisCache
# rconn = RConn('localhost', 6379)
# cache.redis = RedisCache(redis_conn=rconn, debug=True)

# # We can now use cache.redis in place of (or along with) cache.ram and cache.disk.
# # We can also obtain Redis statistics by calling:
# # cache.redis.stats()

# # Use redis for session
# sessiondb = RedisSession(redis_conn=rconn, session_expiry=False)
# sessiondb = RedisSession(redis_conn=rconn, session_expiry=3600)
# session.connect(request, response, db2)

#------------------------------------------------------------------------------
# Caching duration
#------------------------------------------------------------------------------
if not session.cache:
    session.cache = myconf.get('app.cache')
    session.cache_1d = myconf.get('app.cache_1d')
    session.cache_1w = myconf.get('app.cache_1w')
    session.cache_1m = myconf.get('app.cache_1m')