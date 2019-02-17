
from PackageBuilder.Package import Package
from PackageBuilder.Spec import Spec
import os
import tarfile

class BuildTool(Package):

    def Run(self):
        if(not os.path.exists(self.output)):
            os.mkdir(self.output)

        self.progress = 0.25
        tar = tarfile.open("%s/%s.tar.xz" % (self.output, self.spec.Name), "w:xz")
        tar.add(self.root, arcname="/")
        tar.close()

        self.progress = 0.5

        # Get list of dependancies (Optionality ignored)
        deps = []
        for dep in self.spec.Deps:
            # Using a spec file
            if(dep.SpecFile != ""):
                spec = Spec.parse(dep.SpecFile)
                deps.append(spec.Name)

            # Using a package name
            elif(dep.Package != ""):
                deps.append(dep.Package)


        tool = open("%s/%s" % (self.output, self.spec.Name), "w")
        data = {
            "Overlays": [
                {
                    "Archive": "./%s.tar.xz" % self.spec.Name,
                    "Patches": []
                },
            ],
            "Tools": deps
        }
        tool.write(str(data))
        tool.close()

        
        self.progress = 0.75

        self._cleanup()
        self.progress = 1.0