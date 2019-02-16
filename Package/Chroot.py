from PackageBuilder.Package import Package
import os

class Chroot(Package):

    def Run(self):
        if(not os.path.exists(self.output)):
            os.mkdir(self.output)

        os.system("cp -r %s/* %s" % (self.root, self.output))
        self.progress = 0.5

        self._cleanup()
        self.progress = 1.0