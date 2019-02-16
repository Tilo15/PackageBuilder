from PackageBuilder.Task import Task

class Extractor(Task):
    def __init__(self, path: str, dest: str):
        self.path = path
        self.dest = dest
        self.progress = 0.0
        self.label = "Extracting"

    def Prepare(self):
        return []

    def Run(self):
        raise NotImplementedError

    def Probe(self):
        return (self.label, self.progress)

    @staticmethod
    def Understands(path: str):
        raise NotImplementedError

