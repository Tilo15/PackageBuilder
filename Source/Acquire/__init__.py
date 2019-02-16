from PackageBuilder.Task import Task

class Acquirer(Task):
    def __init__(self, address: str, dest: str):
        self.address = address
        self.dest = dest
        self.progress = 0.0
        self.label = "Acquiring"

    def Prepare(self):
        return []

    def Run(self):
        raise NotImplementedError

    def Probe(self):
        return (self.label, self.progress)

    @staticmethod
    def Understands(address: str):
        raise NotImplementedError


