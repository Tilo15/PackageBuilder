from PackageBuilder.Task import Task
from PackageBuilder.Spec.Build import Build as BuildSpec
from PackageBuilder.Spec.Build import Tool as ToolSpec
from PackageBuilder.Spec import Spec
from PackageBuilder.Source import Source
from PackageBuilder.LDD import ldd
from PackageBuilder.Build.StandardImports import STANDARD_IMPORTS
from PackageBuilder.Build.StandardSkel import STANDARD_SKEL

import os
import glob
import shutil

class Build(Task):
    def __init__(self, spec: BuildSpec, root_path: str, cleanup=True):
        self.spec: BuildSpec = spec
        self.step = "Preparing Build Enviornment"
        self.progress = 0.0
        self.root_path = root_path
        self.cleanup = cleanup
        self.working_dir = "src/%s" % spec.WorkingDirectiory

    def Prepare(self):
        tasks = []

        # Get Source
        tasks.extend([Source(x, "%s/src" % self.root_path) for x in self.spec.Sources])

        # Build all build dependancies
        for dep in self.spec.Deps:
            # TODO handle optionality

            if(dep.SpecFile == ""):
                raise Exception("Build dependancy must have a spec file")

            # Get the spec
            dep_spec = Spec.parse(dep.SpecFile)

            # Build
            tasks.append(Build(dep_spec.Build, self.root_path, False))

        # Connect build tools
        for tool in self.spec.Tools:
            tasks.append(Tool(tool, self.root_path))

        return tasks


    def Run(self):
        # Progress reporting step size
        step_size = 1.0/(len(self.spec.PreBuild) + len(self.spec.PostBuild) + len(self.spec.Tools) + 4)

        # Create skeliton folder structure
        for folder in STANDARD_SKEL:
            os.makedirs("%s/%s" % (self.root_path, folder), exist_ok=True)

        imports = self.spec.SystemImports
        imports.extend(STANDARD_IMPORTS)

        # Copy requested executables
        for sys_import in self.spec.SystemImports:
            self._import(sys_import)
            libs = ldd(sys_import)
            for lib in libs:
                self._import(lib)

        self._mount_system()

        # If the working dir does not exist, create it
        if(not os.path.exists("%s/%s" % (self.root_path, self.working_dir))):
            os.mkdir("%s/%s" % (self.root_path, self.working_dir))

        # Update progress
        self.progress = step_size

        # Run commands
        self.step = "Running Pre-Build Commands"

        for command in self.spec.PreBuild:
            self._chroot(command)
            self.progress += step_size

        # Take snapshot of system
        self.step = "Creating Snapshot"
        self._umount_system()
        snapshot = glob.glob("%s/**" % self.root_path, recursive=True)
        snapshot.extend(glob.glob("%s/**/.*" % self.root_path, recursive=True))
        snapshot = set(snapshot)

        self._mount_system()
        self.progress += step_size


        # Build
        self.step = "Building"
        self._chroot(self.spec.Build)
        self.progress += step_size

        # Run commands
        self.step = "Running Post-Build Commands"

        for command in self.spec.PostBuild:
            self._chroot(command)
            self.progress += step_size


        # Cleanup
        self._umount_system()

        if(self.cleanup):
            self.step = "Cleaning Up"

            self._chroot("rm -fr /src")
            
            # Get all files, and compare to old
            current = glob.glob("%s/**" % self.root_path, recursive=True)
            current.extend(glob.glob("%s/**/.*" % self.root_path, recursive=True))

            # Reverse order of list
            current.reverse()

            # Progress reporting
            minor_step = step_size / len(current)


            # Unlink any pre-existing files
            for file in current:
                if(file in snapshot):
                    if(os.path.islink(file)):
                        os.unlink(file)

                    elif(os.path.isdir(file)) and (len(os.listdir(file)) == 0):
                        os.rmdir(file)

                    elif(os.path.isfile(file)):
                        os.unlink(file)
                
                self.progress += minor_step

        self.progress = 1.0


    def Probe(self):
        return (self.step, self.progress)

    def _chroot(self, command):
        os.system("chroot %s /bin/bash -c \"cd '%s'; %s\"" % (self.root_path, self.working_dir, command.replace('\"', '\\\"')))

    def _import(self, file):
        parent = os.path.dirname(file)
        os.makedirs("%s/%s" % (self.root_path, parent), exist_ok=True)
        shutil.copy(file, "%s/%s" % (self.root_path, file))

    def _mount_system(self):
        os.system("mount -o bind /proc '%s/proc'" % self.root_path)
        os.system("mount -o bind /dev '%s/dev'" % self.root_path)
        os.system("mount -o bind /run '%s/run'" % self.root_path)

    def _umount_system(self):
        os.system("umount '%s/proc'" % self.root_path)
        os.system("umount '%s/dev'" % self.root_path)
        os.system("umount '%s/run'" % self.root_path)



class Tool(Task):
    def __init__(self, spec: ToolSpec, root_path: str):
        self.spec = spec
        self.root_path = root_path
        self.progress = 0.0

    def Prepare(self):
        tasks = [Tool(x, self.root_path) for x in self.spec.Tools]
        tasks.extend([Build(x, self.root_path) for x in self.spec.Builds])
        tasks.extend([Source(x, self.root_path) for x in self.spec.Overlays])
        return tasks

    def Run(self):
        for sys_import in self.spec.SystemImports:
            libs = ldd(sys_import)
            for lib in libs:
                self._import(lib)
                
            self._import(sys_import)

        self.progress = 1.0

    def Probe(self):
        return ("Importing tool into build environment", self.progress)


    def _import(self, file):
        parent = os.path.dirname(file)
        os.makedirs("%s/%s" % (self.root_path, parent), exist_ok=True)
        shutil.copy(file, "%s/%s" % (self.root_path, file))