# import database library
from sshtunnel import SSHTunnelForwarder
import pymongo
import urllib
import pprint

import configure as conf

param = conf

# define ssh tunnel
server = SSHTunnelForwarder(
    param.BASTION_HOST,
    ssh_username=param.BASTION_USER,
    ssh_password=param.BASTION_PASS,
    remote_bind_address=(param.DB_HOST, param.DB_PORT),
    local_bind_address=(param.LOCAL_BIND_HOST, param.LOCAL_BIND_PORT)
)

# tunnel and bind port
server.start()

# connect to database
connection = pymongo.MongoClient(
    host=server.local_bind_host,
    port=server.local_bind_port,
    username=param.DB_USER,
    password=param.DB_PASS,
    authSource=param.DB_AUTH_SOURCE,
    authMechanism=param.DB_AUTH_MECH
)
