# This is terrible never use it

import sys
import os
import tarfile
import uuid

tool_name = sys.argv[1]
package_name = sys.argv[2]
releasever = int(sys.argv[3])
output = sys.argv[4]

staging = "/tmp/PackageBuilder-DNF2Tool-%s" % uuid.uuid4().hex
os.system("dnf install %s --installroot='%s' --releasever=%i -y" % (package_name, staging, releasever))

# TODO look into how we might be able to trim out unneeded stuff here
tar = tarfile.open("%s/%s.tar.xz" % (output, tool_name), "w:xz")
tar.add(staging, arcname="/")
tar.close()

f = open("%s/%s" % (output, tool_name), "w")
data = {
    "Overlays": [
        {
            "Archive": "%s/%s.tar.xz" % (output, tool_name),
            "Patches": []
        },
    ]
}
f.write(str(data))
f.close()