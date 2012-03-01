'''
Created: 24.02.2012
@author: psi
'''

import httplib2
import logging
import hashlib
import os
from PIL import Image
import glob

log_path = '/var/log/preview.log'
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
log_level = 'DEBUG'
logging.basicConfig(filename = log_path, filemode = 'a', level = vars(logging)[log_level], format = log_format)
logger = logging.getLogger('test')

class Preview:
    
    def generatePreview(self,filename, sizex, sizey):
        size = int(sizex), int(sizey)
        logger.info('Sizes: ' + str(repr(size)))
        for infile in glob.glob(filename):
            file, ext = os.path.splitext(infile)
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            newname = file + ext
            im.save(newname)
            logger.info(newname)
        trash, result = os.path.split(newname)
        return result
    
    def getPreview(self,fileAddress, sizex=128, sizey=128 ):
        logger.info('Start')
        logger.info('fileaddress is ' + fileAddress)
        # if file exist already?
        ext = fileAddress.split('.')[-1]
        filename = hashlib.md5(fileAddress + str(sizex) + str(sizey)).hexdigest() + '.' + ext
        fullFilePath = os.path.dirname(os.path.abspath( __file__ )) + '/Previews/' + filename
        logger.info(fullFilePath)
        if os.path.exists(fullFilePath):
            logger.info('Preview ' + fullFilePath + ' already exist')            
            return fullFilePath
        # get type and length
        h = httplib2.Http()
        resp = h.request(fileAddress, 'HEAD')
        if ((resp[0]['status'] != '200' and resp[0]['status'] != '304') or 'image' not in resp[0]['content-type']):
            logger.info('Error')
            return 'Error'
        logger.info('check')
        # download image
        h = httplib2.Http()
        resp = h.request(fileAddress, 'GET')
        r = resp[1]
        # writing image
        e = open(fullFilePath, 'wb')
        e.write(r)
        e.close()
        self.generatePreview(fullFilePath, sizex, sizey)
        logger.info('Done')
        return fullFilePath
