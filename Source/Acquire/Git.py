from PackageBuilder.Source.Acquire import Acquirer
import os

class Git(Acquirer):

    def Run(self):
        self.label = "Cloning %s" % self.address

        os.system("cd '%s'; git clone '%s'" % (self.dest, self.address))

        self.progress = 1.0
        

    @staticmethod
    def Understands(address: str):
        return address.startswith("git://")