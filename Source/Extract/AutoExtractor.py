from PackageBuilder.Source.Extract import Extractor
from PackageBuilder.Source.Extract.Directiory import Directiory
from PackageBuilder.Source.Extract.TapeArchive import TapeArchive


EXTRACTORS = [Directiory, TapeArchive]


class AutoExtractor(Extractor):
    def __init__(self, path: str, dest: str):
        super().__init__(path, dest)
        self.extractor = None


    def Prepare(self):
        return []

    def Run(self):
        for extractor in EXTRACTORS:
            if(extractor.Understands(self.path)):
                self.extractor = extractor(self.path, self.dest)

        if(self.extractor == None):
            raise Exception("Could not find extractor for file '%s'" % path)

        return self.extractor.Run()

    def Probe(self):
        if(self.extractor != None):
            return self.extractor.Probe()
        return ("Determining what extractor to use", 0.0)


