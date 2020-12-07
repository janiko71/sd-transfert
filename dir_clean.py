import os

basepath = "D:\\PHOTOS_TRIEES\\jean_smartphone_reference"

cont = True

while cont:

    for root, dir, files in os.walk(basepath, topdown=True):

        cont = False;

        try:
            os.rmdir(root)
            print("delete ", root)
            cont = True
        except OSError as ose:
            print("keep ", root, str(ose))
            pass