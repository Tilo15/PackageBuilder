from PackageBuilder.Spec.Dependancy import Dependancy
from PackageBuilder.Spec.Source import Source

class Build:
    def __init__(self, data: dict):
        self.PreBuild = data["PreBuild"]
        self.Build = data["Build"]
        self.PostBuild = data["PostBuild"]
        self.WorkingDirectiory = data["WorkingDirectiory"]
        self.Deps = [Dependancy(x) for x in data["Deps"]]
        self.Source = Source(data["Source"])
        self.SystemImports = []

        if("SystemImports" in data):
            self.SystemImports = data["SystemImports"]