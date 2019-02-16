from PackageBuilder.Source.Extract import Extractor
import shutil
import os

class Directiory(Extractor):

    def Run(self):
        shutil.copytree(self.path, self.dest)
        self.progress = 1.0

    @staticmethod
    def Understands(path: str):
        return os.path.isdir(path)