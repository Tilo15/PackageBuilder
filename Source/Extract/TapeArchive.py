from PackageBuilder.Source.Extract import Extractor
from tarfile import TarFile
import os

class TapeArchive(Extractor):

    def Run(self):
        self.label = "Untarring"
        tar = TarFile.open(self.path)
        tar.extractall(path=self.dest, numeric_owner=True)
        self.progress = 1.0

    @staticmethod
    def Understands(path: str):
        return os.path.isfile(path)