from __future__ import print_function

def lambda_handler(event, context):
    
    import sys
    
    import boto3
    
    ec2 = boto3.resource('ec2')
    
    instances = ec2.instances.filter( 
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}, {'Name': 'instance-lifecycle', 'Values': ['spot']}] )
        
    all = [i for i in instances]
    
    import datetime
    
    print( "Total count: %i for %s" % ( len(all), datetime.datetime.now() ) )
    
    from dateutil import parser
    
    from datetime import timedelta
    
    def loginst( i ):
        
        t = i.launch_time
        
        tz_info = t.tzinfo
        
        import datetime
    
        now = datetime.datetime.now( tz_info )
        
        p = n = team = ''
        
        for tag in i.tags:
            if tag['Key'] == 'Name':
                n = tag['Value']

        for tag in i.tags:
            if tag['Key'] == 'team':
                team = tag['Value']

        for tag in i.tags:
            if tag['Key'] == 'protection':
                p = tag['Value']
        
        print( "%.1fh,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % 
                ( (now - t).total_seconds() / 3600,(now - t).total_seconds(), n, team, i.id, i.state, i.instance_type, i.spot_instance_request_id, i.platform, p, i.root_device_name, i.root_device_type ) )

    def any_tags( all ):
        
        print( 'Try to find instance with any tags...' )
        
        for i in all:
            
            if (  i.tags is not None and len( i.tags ) ):
                
                print( 'Found this one:' )
                
                print( i.tags )
                
                loginst( i )
                
                return True
                
            loginst( i )
            
        print( 'No tags found' )
        
        return False
    
    if any_tags( all ):
        
        print( 'Instances for termination at weekend night hours' )

        count = 0
    
        for i in all:
            
            tag_ttl = ''
            
            if i.tags:
            
                for tag in i.tags:
                    
                    if tag['Key'] == 'ttl':
                        
                        tag_ttl = tag['Value'] 
            
            if not ( tag_ttl and tag_ttl.strip().isdigit() ):
                
                loginst( i )
                
                count += 1
                
                i.terminate() 
    
        print( "work has completed for %d instances" % count )
        
    else:
        
        print( 'INTERRUPT: No tags found' )