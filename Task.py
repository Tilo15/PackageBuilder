
class Task:
    def Prepare(self):
        raise NotImplementedError

    def Run(self):
        raise NotImplementedError

    def Probe(self):
        raise NotImplementedError
