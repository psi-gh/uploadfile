'''
Created: 09.02.2012
@author: psi
'''

import os, time, shutil, datetime
import random, string, time

def getsubs(dir):
    files = []
    fullsubdirs = []
    subdirs = os.walk(dir).next()[1]
    #print 'fierst subdirs ' + repr (subdirs)
    for sd in subdirs:
        sd = os.path.join(dir, sd)
        fullsubdirs.append(sd)
        for dirname, dirnames, filenames in os.walk(sd):
            for filename in filenames:
                files.append(os.path.join(dir, filename))
    
    return fullsubdirs, files

def main():

    dirs, f = getsubs("/var/www/uploadfile/wsgi")
    for x in dirs:
        if (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(x))) > datetime.timedelta (days=1):
            print('removing ' + x + ' time is ' + time.asctime( time.localtime(os.path.getmtime(x))))
            shutil.rmtree(x)
    f=open('/home/pavel/123.txt', 'a')    
    f.write(time.asctime() + '\n')
    f.close()
            
        
if __name__ == "__main__":
    main()
    
