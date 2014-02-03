import sys
from boto.ec2.connection import EC2Connection

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
c = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto
all = [r.instances[0] for r in c.get_all_instances()]
import datetime
now = datetime.datetime.now()
for i in all:
    #time = datetime.datetime(*time.strptime(i.launch_time, "%Y-%m-%dT%H:%M:%S")[:6])
    print " %s %s %s %s %s" % (i.id, i.state, i.launch_time, i.instance_type, i.spot_instance_request_id)
print "work has completed"
