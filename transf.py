import os, io, sys
import shutil
import PIL.Image as PILimage
from datetime import datetime
import pprint

from hachoir import metadata
from hachoir import parser

PICT_EXT_LIST = {".jpg", ".jpeg", ".jfif", ".bmp", ".gif", ".png", ".tif", ".tiff", ".webp"}
PICT_EXT_LIST = {}
RAW_PICT_EXT_LIST = {".arw", ".cr2", ".cr3", ".crw", ".dcr", ".dcs", ".dng", ".drf", ".gpr", \
                     ".k25", ".kdc", ".mrw", ".nef", ".nrw", ".orf", ".pef", ".ptx", ".raf", \
                     ".raw", ".rw2", ".sr2", ".srf", ".srw", ".x3f"}
RAW_PICT_EXT_LIST = {}                   
VIDEO_EXT_LIST = {".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".m4p", ".m4v", ".avi", ".wmv", ".avchd", ".mov", ".3gp"}


# -------------------------------------------
def main():
# -------------------------------------------    

    basepath    = "I:\\"
    target      = "D:\\VIDEOS_BASE"

    path_non_trie = target + os.sep + "non_trie" + os.sep
    if not(os.path.exists(path_non_trie)):
        os.makedirs(path_non_trie)

    os.chdir(basepath)

    for root, _, files in os.walk(".", topdown=True):

        for f_name in files:

            # File infos
            
            img_path = os.path.join(root, f_name)
            file_ext = os.path.splitext(img_path)[1].lower()
            fs = os.stat(img_path)

            try:

                copy = False
                tri = False
                dt = None

                if (file_ext in PICT_EXT_LIST):

                    # exif-like file

                    copy = True                

                    try:

                        img = PILimage.open(img_path)
                        img_exif = img._getexif()
                        dt = img_exif.get(36867)
                        if (dt):
                            tri = True

                    except Exception as e:

                        tri = False
                        print("Non trié : " + img_path)

                    img.close()

                elif (file_ext in RAW_PICT_EXT_LIST):
                    
                    # raw file

                    copy = True
                    tri = True
                    d  = datetime.fromtimestamp(fs.st_mtime)
                    dt = "{:04d}:{:02d}:{:02d}".format(d.year, d.month, d.day)


                elif (file_ext in VIDEO_EXT_LIST):
                    
                    # video file

                    copy = True
                    tri = True
                    d  = datetime.fromtimestamp(fs.st_mtime)
                    dt = "{:04d}:{:02d}:{:02d}".format(d.year, d.month, d.day)

                    p = parser.createParser(img_path)
                    m = metadata.extractMetadata(p)
                    print(m.get("creation_date"))

                # Copying file

                if (copy) and (tri):

                    # Destination folder (based on date)
                    
                    yr = dt[0:4]
                    dest_dt = "{:04d}-{:02d}-{:02d}".format(int(yr), int(dt[5:7]), int(dt[8:10]))

                    yr_path = target + os.sep + yr
                    pic_path = yr_path + os.sep + dest_dt + os.sep
                                    
                    if not(os.path.exists(yr_path)):
                        #print(yr_path, "n'existe pas")
                        os.makedirs(yr_path)
                        
                    if not(os.path.exists(pic_path)):
                        #print(pic_path, "n'existe pas")
                        os.makedirs(pic_path)

                else:

                    pic_path = target + os.sep + "non_trie" + os.sep

                if (copy):
                    
                    if not(os.path.exists(pic_path + f_name)):
                        #print("{} --> {}".format(img_path, pic_path + f_name))
                        #shutil.copy2(img_path, pic_path + f_name)
                        shutil.copy2(img_path, pic_path + f_name)
                        print("copie " + img_path + " -> " + pic_path + f_name)
                    else:
                        print("copie déjà présente" + img_path + " -> " + pic_path + f_name)


                else:

                    #print("NON TRAITE : " + img_path)
                    pass
                
            except Exception as e:

                print("Erreur sur " + img_path)
                print(copy, tri)
                pprint.pprint(img_exif)
                raise(e)

                    
                
# -------------------------------------------
#  main call
# -------------------------------------------

if __name__ == '__main__':
    main()
