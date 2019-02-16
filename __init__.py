from PackageBuilder.Spec import Spec
from PackageBuilder.Package.Chroot import Chroot

import sys
import glob
import os
import time
import threading

PACKAGE_TYPES = {
    "chroot": Chroot
}



class PackageBuilder:

    def __init__(self, spec_path, package_type, output):
        # Make output folder
        if(not os.path.exists(output)):
            os.mkdir(output)

        self.packages = []

        # Queue all spec files in dir
        if(os.path.isdir(spec_path)):
            for file in glob.glob(spec_path + "/**.pbspec", recursive=True):
                spec = Spec.parse(file)
                self.packages.append(PACKAGE_TYPES[package_type](spec, output))

        else:
            spec = Spec.parse(spec_path)
            self.packages = [PACKAGE_TYPES[package_type](spec, output),]

        self.complete = False
        self.current_task = None
        self.task_count = 0
        self.tasks_completed = 0


    def build(self):
        print("Preparing tasks")
        tasks = self.prepare_tasks(self.packages)
        self.task_count = len(tasks)

        print("Running tasks")
        threading.Thread(target=self.report).start()
        self.run_tasks(tasks)



    def prepare_tasks(self, tasks):
        out = []
        for task in tasks:
            out.extend(self.prepare_tasks(task.Prepare()))
            out.append(task)

        return out


    def run_tasks(self, tasks):
        # Loop over every task
        for task in tasks:
            self.tasks_completed += 1
            self.current_task = task
            task.Run()

        self.complete = True


    def report(self):
        last_len = 0
        last_task = self.tasks_completed
        while not self.complete:
            info = ("Preparing to start build...", 0.0)
            if(self.current_task != None):
                info = self.current_task.Probe()

            if(last_task != self.tasks_completed):
                sys.stdout.write("[Task %i/%i] 100%%\n" % (last_task, self.task_count)) 
                last_task = self.tasks_completed

            text = "[Task %i/%i] %0.2d%%  %s" % (self.tasks_completed, self.task_count, info[1] * 100, info[0])
            sys.stdout.write(text + (" " * (last_len - len(text))) + "\r")
            last_len = len(text)
            time.sleep(0.01)

        print("\n\nComplete!")