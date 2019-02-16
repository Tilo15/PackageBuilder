from PackageBuilder.Task import Task
from PackageBuilder.Spec.Source import Source as SourceSpec
from PackageBuilder.Source.Acquire.AutoAcquirer import AutoAcquirer
from PackageBuilder.Source.Extract.AutoExtractor import AutoExtractor

import uuid
import os


class Source(Task):
    def __init__(self, spec: SourceSpec, dest: str, staging="/tmp"):
        self.spec = spec
        self.staging = "%s/PackageBuilder-Source-%s" % (staging, uuid.uuid4().hex)
        self.dest = dest
        self.patches = []
        os.mkdir(self.staging)

        self.patch_progress = 0.0


    def Prepare(self):
        # Create array for tasks
        tasks = []

        # Get source
        tasks.append(AutoAcquirer(self.spec.Archive, "%s/source" % self.staging))

        # Extract source
        tasks.append(AutoExtractor("%s/source" % self.staging, self.dest))

        # Acquire patches
        for patch in self.spec.Patches:
            path = "%s/%s.patch" % (self.dest, uuid.uuid4().hex)
            tasks.append(AutoAcquirer(patch, path))
            self.patches.append(path)

        return tasks


    def Run(self):
        # Apply patches
        for patch in self.patches:
            if(os.system("patch < '%s'" % patch) != 0):
                raise Exception("Failed to apply patch '%s'" % patch)
            else:
                self.patch_progress += 1.0/len(self.patches)
        

        self.patch_progress = 1.0


    def Probe(self):
        return ("Patching", self.patch_progress)
