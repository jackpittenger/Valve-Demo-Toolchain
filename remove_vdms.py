# Created by https://github.com/realSaddy
import os
import argparse

parser = argparse.ArgumentParser(description="Remove all .vdm files from a directory, by https://github.com/realSaddy")

parser.add_argument("folder", type=str, help="The directory in which to remove the .vdms")

args = parser.parse_args()

if os.path.exists(args.folder):
    results = [x for x in os.listdir(args.folder) if x.endswith('.vdm')]
    sc = 0
    ec = 0
    for result in results:
        try:
            os.remove(args.folder+"/"+result)
            sc += 1
        except Exception as e:
            print("ERROR removing "+result+" | "+e)
            ec += 1
    print("Removed "+str(sc)+" .vdm files with "+str(ec)+" errors!")
else:
    print("ERROR: Folder doesn't exist!")

