# This is terrible never use it

import sys
import os
import tarfile
import uuid
import glob

tool_name = sys.argv[1]
package_name = sys.argv[2]
releasever = int(sys.argv[3])
output = sys.argv[4]

staging = "/tmp/PackageBuilder-DNF2Tool-%s" % uuid.uuid4().hex

if(os.path.exists("%s/system-base.tar.xz" % output)):
    tar = tarfile.open("%s/system-base.tar.xz" % output)
    tar.extractall(staging)

else:
    # Create base image
    os.system("dnf groupinstall 'Minimal Install' --installroot='%s' --releasever=%i -y" % (staging, releasever))

    # Create tar of base
    tar = tarfile.open("%s/system-base.tar.xz" % output, "w:xz")
    tar.add(staging, arcname="/")
    tar.close()

# Create snapshot
snapshot = glob.glob("%s/**" % staging, recursive=True)
snapshot.extend(glob.glob("%s/**/.*" % staging, recursive=True))
snapshot = set(snapshot)

# Install requested software
os.system("dnf install %s --installroot='%s' --releasever=%i -y" % (package_name, staging, releasever))

# Remove structure from snapshot
# Get all files, and compare to old
current = glob.glob("%s/**" % staging, recursive=True)
current.extend(glob.glob("%s/**/.*" % staging, recursive=True))

# Reverse order of list
current.reverse()

# Unlink any pre-existing files
for file in current:
    if(file in snapshot):
        if(os.path.islink(file)):
            os.unlink(file)

        elif(os.path.isdir(file)) and (len(os.listdir(file)) == 0):
            os.rmdir(file)

        elif(os.path.isfile(file)):
            os.unlink(file)


# Create image of just installed software
tar = tarfile.open("%s/%s.tar.xz" % (output, tool_name), "w:xz")
tar.add(staging, arcname="/")
tar.close()

f = open("%s/%s" % (output, tool_name), "w")
data = {
    "Overlays": [
        {
            "Archive": "./system-base.tar.xz",
            "Patches": []
        },
        {
            "Archive": "./%s.tar.xz" % tool_name,
            "Patches": []
        },
    ]
}
f.write(str(data))
f.close()