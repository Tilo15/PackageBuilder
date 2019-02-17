from PackageBuilder.Spec.Package import Package

import ast

class Spec:

    @staticmethod
    def parse(path: str) -> Package:
        f = open(path)
        data = ast.literal_eval(f.read())
        f.close()

        return Package(data, path)