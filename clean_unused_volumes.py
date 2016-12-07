import boto3

def lambda_handler(event, context):
    
    price = { 'gp2': 0.1, 'io1': 0.125, 'st1' : 0.045, 'sc1': 0.025, 'standard' : 0.045 }

    ec2 = boto3.resource("ec2")  
    
    vol = ec2.volumes.filter( Filters=[{'Name': 'status', 'Values': ['available']}] )

    num = 0
    size = 0
    cost = 0
    
    to_delete = []
    
    for v in vol:
        
        num += 1
        
        print("Volume %s Size %s Type: %s Created: %s" % (v, v.size, v.volume_type, v.create_time))
        
        size += int( v.size )
        
        is_protected = False
        
        name = ''
        team = ''

        if v.tags is None:
            print("No tags volume: %s" % v.id)
        else:
            for t in v.tags:
                
                print(" %s %s" % (v.id, t) )

                if t['Key'] == 'team':
                    team = t['Value']
                
                if t['Key'] == 'Name':
                    name = t['Value']
                
                if t['Key'] == 'protection':
                    print("Protected volume: %s" % v.id)
                    is_protected = True
        
        if not is_protected:
            to_delete.append({'vol':v, 'name':name, 'team':team})

    for vol in to_delete:
        v = vol['vol']
        cost += v.size * price.get( v.volume_type, 100 )
        print("Kill volume %s %s %d GB created: %s team: %s" % (v.id, vol['name'], v.size, v.create_time, vol['team']) )
        v.delete()
    
    print("Total num of volumes: %d, killed: %d, protected: %d, size %d GBs, Saved cost: %f" % (num, len(to_delete), num-len(to_delete), size, cost) )
    
    return 'Done'