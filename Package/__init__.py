from PackageBuilder.Task import Task
from PackageBuilder.Spec.Package import Package as PackageSpec
from PackageBuilder.Build import Build

import os
import shutil
import glob
import uuid

class Package(Task):
    def __init__(self, spec: PackageSpec, output: str, staging="/tmp"):
        self.spec = spec
        self.output = output

        self.progress = 0.0
        self.stage = "Packaging"

        self.staging = "%s/PackageBuilder-Package-%s" % (staging, uuid.uuid4().hex)
        self.root = "%s/BuildRoot" % self.staging
        os.mkdir(self.staging)
        os.mkdir(self.root)


    def Prepare(self):
        return [Build(self.spec.Build, self.root),]


    def Run(self):
        raise NotImplementedError


    def Probe(self):
        return (self.stage, self.progress)


    def _cleanup(self):
        shutil.rmtree(self.staging)
        pass