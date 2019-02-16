from PackageBuilder.Source.Acquire import Acquirer
from PackageBuilder.Source.Acquire.Filesystem import Filesystem
from PackageBuilder.Source.Acquire.HTTP import HTTP

ACQUIRERS = [Filesystem, HTTP]


class AutoAcquirer(Acquirer):
    def __init__(self, address: str, dest: str):
        super().__init__(address, dest)

        self.acquirer = None
        for acquirer in ACQUIRERS:
            if(acquirer.Understands(address)):
                self.acquirer = acquirer(address, dest)

        if(self.acquirer == None):
            raise Exception("Could not find acquirer for address '%s'" % address)

    def Prepare(self):
        return self.acquirer.Prepare()

    def Run(self):
        return self.acquirer.Run()

    def Probe(self):
        return self.acquirer.Probe()


