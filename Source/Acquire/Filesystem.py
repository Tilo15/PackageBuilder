from PackageBuilder.Source.Acquire import Acquirer
import shutil
import os

class Filesystem(Acquirer):

    def Run(self):
        if(self.address.startswith("./")):
            self.address = self.relative_path + self.address[1:]

        if(os.path.isdir(self.address)):
            shutil.copytree(self.address, self.dest)
        else:
            shutil.copy(self.address, self.dest)
            
        self.progress = 1.0

    @staticmethod
    def Understands(address: str):
        return address.startswith("/") or address.startswith("./")