from PackageBuilder import PackageBuilder, PACKAGE_TYPES
import sys
import os

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Usage:")
        print("\tPackageBuilder specfile package_type [output]\n")
        print("Supported Package Types:")
        for ptype in PACKAGE_TYPES.keys():
            print("\t%s" % ptype)
        
        print()
        exit(1)


    # Get args
    spec = sys.argv[1]
    package_type = sys.argv[2]
    output = os.getcwd() + "/Build"

    if(len(sys.argv) > 3):
        output = sys.argv[3]
        if(not output.startswith("/")):
            output = "%s/%s" % (os.getcwd(), output)

    builder = PackageBuilder(spec, package_type, output)
    builder.build()

    

