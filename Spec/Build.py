from PackageBuilder.Spec.Dependancy import Dependancy
from PackageBuilder.Spec.Source import Source

import os
import ast

class Build:
    def __init__(self, data: dict, file: str):
        self.PreBuild = []
        self.Build = data["Build"]
        self.PostBuild = []
        self.WorkingDirectiory = data["WorkingDirectiory"]
        self.Deps = []
        self.Tools = []
        self.Sources = [Source(x, os.path.dirname(file)) for x in data["Sources"]]
        self.SystemImports = []

        if("PreBuild" in data):
            self.PreBuild = data["PreBuild"]

        if("PostBuild" in data):
            self.PostBuild = data["PostBuild"]

        if("SystemImports" in data):
            self.SystemImports = data["SystemImports"]

        if("Deps" in data):
            self.Deps = [Dependancy(x) for x in data["Deps"]]

        if("Tools" in data):
            self.Tools = [Tool(x) for x in data["Tools"]]


class Tool:
    def __init__(self, name: str):
        specs = "/etc/PackageBuilder/tools"

        if("PBTOOLS" in os.environ):
            specs = os.environ["PBTOOLS"]

        file = open("%s/%s" % (specs, name))
        data = ast.literal_eval(file.read())
        file.close()

        self.Overlays = []
        self.Builds = []
        self.SystemImports = []
        self.Tools = []

        if("SystemImports" in data):
            self.SystemImports = data["SystemImports"]

        if("Builds" in data):
            self.Builds = [Build(x, "%s/%s" % (specs, name)) for x in data["Builds"]]

        if("Overlays" in data):
            self.Overlays = [Source(x, specs) for x in data["Overlays"]]

        if("Tools" in data):
            self.Tools = [Tool(x) for x in data["Tools"]]