import boto
import re
import sys

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]

ec2Connection = boto.connect_ec2(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

imgs = ec2Connection.get_all_images(owners=['self'])

print len(imgs)
print str(imgs[0].description) + imgs[0].id


# Get the list of registered AMIs.
imageIds, imageNames = zip(*[(image.id, image.name + ", " + str(image.description)) for image in ec2Connection.get_all_images(owners=['self'])])
imageNames = dict(zip(imageIds, imageNames))

# Get list of snapshots and AMIs
reAmi = re.compile('ami-[^ ]+')
snapshots = []
snapshotsToDelete = []
snapshotsUnknown = []
imageSnapshots = {}

for snapshot in ec2Connection.get_all_snapshots(owner='self'):
    # Get id and image ID via regex.
    snapshotId = snapshot.id
    snapshotImageId = reAmi.findall(snapshot.description)
    if len(snapshotImageId) != 1:
        snapshotsUnknown.append(snapshotId)
    else:
        snapshotImageId = snapshotImageId[0]
        
    # Update lists
    snapshots.append(snapshotId)
    if snapshotImageId not in imageIds:
        snapshotsToDelete.append(snapshotId)
    else:
        if snapshotImageId in imageSnapshots:
            imageSnapshots[snapshotImageId].append(snapshotId)
        else:
            imageSnapshots[snapshotImageId] = [snapshotId]

print "Mapped snapshots:"
for image in sorted(imageSnapshots.keys()):
    print image + ": " + imageNames[image]
    for snapshot in imageSnapshots[image]:
        print "\t- " + snapshot

print
print "Orphans: " + ','.join(sorted(snapshotsToDelete))
print
print "Unknown: " + ','.join(sorted(snapshotsUnknown))
# Close connection to EC2.
ec2Connection.close()
