import sys
from boto.ec2.connection import EC2Connection

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
c = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto
all = [r.instances[0] for r in c.get_all_instances( filters = {"instance-lifecycle":"spot","instance-state-name":"running"})]
import datetime
now = datetime.datetime.now()
#print "Total count: %i for %s" % ( len(all), now )

from dateutil import parser
from datetime import timedelta

# print 'All instances'

def loginst( i ):
    t = parser.parse(i.launch_time).replace(tzinfo=None)
    p = n = team = ''
    if i.tags.has_key('Name'): n = i.tags['Name']
    if i.tags.has_key('team'): team = i.tags['team']
    if i.tags.has_key('protection'): p = i.tags['protection']
    print "%s, \t%.1fh,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (n,  (now - t).total_seconds() / 3600,team, i.id, i.state, i.instance_type, i.spot_instance_request_id, i.platform, p, i.root_device_name, i.root_device_type )

# for i in all:
    # loginst( i )
        
print 'Instances for termination at night hours'

count = 0

for i in all:
    if (not i.tags.has_key('protection') or i.tags['protection'].strip() != '1' ) and ( i.instance_type not in ['t1.micro','m1.small'] or i.platform == 'windows' ) and not ( i.tags.has_key('ttl') and i.tags['ttl'].strip().isdigit() ):
        loginst( i )
        count += 1
        i.terminate() 

print "work has completed for %d instances" % count
