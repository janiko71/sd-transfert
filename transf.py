import os, io, sys
import shutil
import PIL.Image as PILimage
from datetime import datetime

PICT_EXT_LIST = {".jpg", ".jpeg", ".jfif", ".bmp", ".gif", ".png", ".tif", ".tiff", ".webp"}
RAW_PICT_EXT_LIST = {".arw", ".cr2", ".cr3", ".crw", ".dcr", ".dcs", ".dng", ".drf", ".gpr", \
                     ".k25", ".kdc", ".mrw", ".nef", ".nrw", ".orf", ".pef", ".ptx", ".raf", \
                     ".raw", ".rw2", ".sr2", ".srf", ".srw", ".x3f"}
VIDEO_EXT_LIST = {".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".mov", ".ogv", ".mp4", ".m4p", ".m4v", ".avi", ".ts", ".webm", ".wm", ".wmv", ".avchd"}


# -------------------------------------------
def main():
# -------------------------------------------    

    basepath    = "E:\\"
    target      = "I:\\test\\"

    os.chdir(basepath)

    for root, _, files in os.walk(".", topdown=True):

        for f_name in files:

            # File infos
            
            img_path = os.path.join(root, f_name)
            file_ext = os.path.splitext(img_path)[1].lower()
            fs = os.stat(img_path)

            try:

                copy = False
                
                if (file_ext in PICT_EXT_LIST):

                    # exif-like file

                    copy = True
                    
                    img = PILimage.open(img_path)
                    img_exif = img._getexif()
                    dt = img_exif.get(36867)

                elif ((file_ext in RAW_PICT_EXT_LIST) or (file_ext in VIDEO_EXT_LIST)):
                    
                    # video or raw file

                    copy = True
                    
                    d  = datetime.fromtimestamp(fs.st_ctime)
                    dt = "{:04d}:{:02d}:{:02d}".format(d.year, d.month, d.day)

                # Destination folder (based on date)
                
                yr = dt[0:4]
                dest_dt = "{:04d}-{:02d}-{:02d}".format(int(yr), int(dt[5:7]), int(dt[8:10]))

                yr_path = target + os.sep + yr
                pic_path = yr_path + os.sep + dest_dt + os.sep

                # Copying file

                if (copy):
                
                    if not(os.path.exists(yr_path)):
                        print(yr_path, "n'existe pas")
                        os.makedirs(yr_path)
                        
                    if not(os.path.exists(pic_path)):
                        print(pic_path, "n'existe pas")
                        os.makedirs(pic_path)
                    
                    if not(os.path.exists(pic_path + f_name)):
                        print("{} --> {}".format(img_path, pic_path + f_name))
                        shutil.copy2(img_path, pic_path + f_name)
                
            except Exception as e:

                print("Erreur " + str(e) + " sur " + img_path)
                print(d, dt)
                    
                
# -------------------------------------------
#  main call
# -------------------------------------------

if __name__ == '__main__':
    main()
