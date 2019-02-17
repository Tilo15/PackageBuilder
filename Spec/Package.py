from PackageBuilder.Spec.Dependancy import Dependancy
from PackageBuilder.Spec.Build import Build

class Package:

    def __init__(self, data: dict, file: str):
        self.Name = data["Name"]
        self.Summary = data["Summary"]
        self.Version = data["Version"]
        self.Arch = data["Arch"]
        self.Licence = data["Licence"]
        self.Deps = [Dependancy(x) for x in data["Deps"]]
        self.Build = Build(data["Build"], file)

        self.Icon = ""
        self.Website = ""
        self.LicenceURL = ""
        self.Screenshots = []
        self.Description = ""
        self.Category = ""
        
        # Optional data
        if("Icon" in data):
            self.Icon = data["Icon"]

        if("Website" in data):
            self.Website = data["Website"]

        if("LicenceURL" in data):
            self.LicenceURL = data["LicenceURL"]

        if("Screenshots" in data):
            self.Screenshots = data["Screenshots"]

        if("Description" in data):
            self.Description = data["Description"]

        if("Category" in data):
            self.Category = data["Category"]