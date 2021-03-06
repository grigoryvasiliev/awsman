import sys
from boto.ec2.connection import EC2Connection

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
c = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto

import datetime
now = datetime.datetime.now()
print "Total count: %i for %s" % ( len(all), now )

from dateutil import parser
from datetime import timedelta

print 'All instances'

def loginst( i ):
    t = parser.parse(i.launch_time).replace(tzinfo=None)
    p = n = ''
    if i.tags.has_key('Name'): n = i.tags['Name']
    if i.tags.has_key('protection'): p = 'protected'
    print "%.1fh \t %s \t %s\t %s\t %s\t %s\t %s \t %s" % ( (now - t).total_seconds() / 3600, n, i.id, i.state,  
    i.instance_type, i.spot_instance_request_id, i.platform, p )

for i in all:
    loginst( i )
        
print 'Instances for termination'
        
for i in all:
    if not i.tags.has_key('protection') and i.state == 'running' and ( i.instance_type not in ['t1.micro','m1.small'] or i.platform == 'windows' ):
        loginst( i )
        i.terminate()
print "work has completed"
