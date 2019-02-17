

class Source:

    def __init__(self, data: dict, relative_path: str):
        self.RelativePath = relative_path
        self.Archive = data["Archive"]
        self.Patches = data["Patches"]
