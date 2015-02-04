import sys
from boto.ec2.connection import EC2Connection

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
c = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
import boto
all = [r.instances[0] for r in c.get_all_instances( filters = {"instance-lifecycle":"spot","instance-state-name":"running"})]
import datetime
now = datetime.datetime.now()
print "Total count: %i for %s" % ( len(all), now )

from dateutil import parser
from datetime import timedelta

def loginst( i ):
    t = parser.parse(i.launch_time).replace(tzinfo=None)
    p = n = team = ''
    if i.tags.has_key('Name'): n = i.tags['Name']
    if i.tags.has_key('team'): team = i.tags['team']
    if i.tags.has_key('protection'): p = i.tags['protection']
    print "%.1fh,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % ( (now - t).total_seconds() / 3600,(now - t).total_seconds(), n, team, i.id, i.state, i.instance_type, i.spot_instance_request_id, i.platform, p, i.root_device_name, i.root_device_type )

print 'Instances for termination with no team tag'
print "Lifetime(h),Lifetime(sec),Name,team,id,state,instance_type,spot_request_id,platform,protection"
for i in all:
    t = (now - parser.parse(i.launch_time).replace(tzinfo=None)).total_seconds()
    if ( not i.tags.has_key('team') or i.tags['team'] not in ['dmp','mmex','rmad','rmex', 'sasp', 'ecolabs', 'rmsp','unicorn','logman'] ) and t > 1800:
        loginst( i )
        i.terminate()

print "work has completed"
