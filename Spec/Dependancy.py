
class Dependancy:
    def __init__(self, data: dict):
        self.SpecFile = ""
        self.Package = ""
        self.Optional = False

        if("SpecFile" in data):
            self.SpecFile = data["SpecFile"]

        if("Package" in data):
            self.Package = data["Package"]

        if("Optional" in data):
            self.Optional = data["Optional"]