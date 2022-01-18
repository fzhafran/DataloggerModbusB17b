import os, sys, shutil, glob

dir = open("tempdir.txt", "r")
tempdir = dir.read()
files = glob.glob(os.path.join(tempdir + "\*"))
for file in files :
    try :
        try :
            os.remove(file)
        except :
            shutil.rmtree(file, ignore_errors= True)
    except Exception as exc :
        print(exc)