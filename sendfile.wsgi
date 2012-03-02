#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created: 08.02.2012
@author: psi
'''

import cgi, re, random, string, os, socket, urllib
import base64
from PIL import Image
import glob
import sys
sys.path.insert(0, "/var/www/uploadfile/wsgi/")
import previewclass
import imghdr

def getFolderName(length = 8, charset = string.ascii_letters + string.digits):
    return ''.join(random.choice(charset) for x in range(length))


def writeToFile(data, filename, environ):
    fn = getFolderName()
    print >> environ['wsgi.errors'],  fn
    
    filePath = os.path.dirname(os.path.abspath( __file__ )) + '/Storage/' + fn
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    print >> environ['wsgi.errors'], filename

    if len(filename.split('.')) < 2:
        ext = imghdr.what("this parameter is ignored", data)
        if ext != None:
            filename += '.' + ext
            print >> environ['wsgi.errors'], 'fullFilePath after correct ' + filename

    fullFilePath = filePath + '/' + filename
    print >> environ['wsgi.errors'], fullFilePath

            
    f = open(fullFilePath, 'wb')
    f.write(data)
    f.close()

    fileLink = environ['wsgi.url_scheme'] + '://' + environ['HTTP_HOST'] + '/uploadfile/wsgi/Storage/' + fn + '/' + urllib.quote(filename)
    return fileLink
    #uploadfile - папка в .../www, строка тут и настройки в sites-available

    
def application(environ, start_response):
    print >> environ['wsgi.errors'], "Calling sendfile module "
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
#    print >> environ['wsgi.errors'], repr(form)
    print >> environ['wsgi.errors'], 'Filename is ' + form['file1'].filename
    print >> environ['wsgi.errors'], 'to = ' + str(form['to'].value)
    fileLink = writeToFile(form.getvalue('file1'), form['file1'].filename, environ)  
    status = '200 OK'
    print >> environ['wsgi.errors'], fileLink
    output = "top.Ext.dispatch({controller:'Chat', action: 'upload_result', args : ['" + str(fileLink) + "', '" + str(form['to'].value) + "']});"
    if form.has_key('device'):
        print >> environ['wsgi.errors'], 'device = ' + str(form['device'].value)        
        if form['device'].value == 'pc':
            output = "<script type='text/javascript'>" + output + "</script>"

    print >> environ['wsgi.errors'], output
    response_headers = [('Content-type', 'text/html;'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    print >> environ['wsgi.errors'], "Success"
    return [output]

