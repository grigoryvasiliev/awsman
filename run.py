import sys
from boto.ec2.connection import EC2Connection

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
c = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto
all = [r.instances[0] for r in c.get_all_instances()]
import datetime
now = datetime.datetime.now()
print "Total count: %i" % len(all) 

from dateutil import parser
from datetime import timedelta

for i in all:
    t = parser.parse(i.launch_time).replace(tzinfo=None)
    print "%.1fh \t %s \t\t %s\t %s\t %s\t %s\t %s\t %s" % ( (now - t).total_seconds() / 3600, i.tags['Name'], i.id, i.state, i.launch_time, i.instance_type, i.spot_instance_request_id, i.platform )
print "work has completed"
