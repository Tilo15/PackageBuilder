from PackageBuilder.Task import Task
from PackageBuilder.Spec.Build import Build as BuildSpec
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
        tasks.append(Source(self.spec.Source, "%s/src" % self.root_path))

        # Build all build dependancies
        for dep in self.spec.Deps:
            if(dep.SpecFile == ""):
                raise Exception("Build dependancy must have a spec file")

            # Get the spec
            dep_spec = Spec.parse(dep.SpecFile)

            # Build
            tasks.append(Build(dep_spec.Build, self.root_path, False))

        return tasks


    def Run(self):
        # Progress reporting step size
        step_size = 1.0/(len(self.spec.PreBuild) + len(self.spec.PostBuild) + 4)

        # Create skeliton folder structure
        for folder in STANDARD_SKEL:
            os.mkdir("%s/%s" % (self.root_path, folder))

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
        snapshot = set(glob.glob("%s/**" % self.root_path, recursive=True))
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
            
            # Get all files, and compare to old
            current = glob.glob("%s/**" % self.root_path, recursive=True)

            # Reverse order of list
            current.reverse()

            # Progress reporting
            minor_step = step_size / len(current)


            # Unlink any pre-existing files
            for file in current:
                if(file in snapshot):
                    if(os.path.isdir(file)) and (len(os.listdir(file)) == 0):
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


