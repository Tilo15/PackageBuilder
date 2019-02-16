from PackageBuilder.Package import Package
import os
from distutils.dir_util import copy_tree

class Chroot(Package):

    def Run(self):
        if(not os.path.exists(self.output)):
            os.mkdir(self.output)

        copy_tree(self.root, self.output)
        self.progress = 0.5

        self._cleanup()
        self.progress = 1.0