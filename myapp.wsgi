#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created: 08.02.2012
@author: psi
'''

import cgi, re, random, string, os, socket, urllib

def getFolderName(length = 8, charset = string.ascii_letters + string.digits):
    return ''.join(random.choice(charset) for x in range(length))

def writeToFile(data, filename, environ):
    fn = getFolderName()
    print >> environ['wsgi.errors'],  fn
    
    filePath = os.path.dirname(os.path.abspath( __file__ )) + '/' + fn
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    print >> environ['wsgi.errors'], filename
    f = open(filePath + '/' + filename, 'wb')
    f.write(data)
    f.close()
    
    return environ['wsgi.url_scheme'] + '://' + environ['HTTP_HOST'] + '/uploadfile/wsgi/' + fn + '/' + urllib.quote(filename)
    #return environ['HTTP_ORIGIN'] + '/uploadfile/wsgi/' + fn + '/' + urllib.quote(filename)
    #uploadfile - папка в .../www, строка тут и настройки в sites-available
    
def application(environ, start_response):
    print >> environ['wsgi.errors'], "Start " + repr(environ)
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    #print >> environ['wsgi.errors'], repr(form)
    output=writeToFile(form.getvalue('file1'), form['file1'].filename, environ)  
    status = '200 OK'
    #output = "<script type='text/javascript'>top.Ext.dispatch({controller:'Chat', action: 'upload_result', args : ['" + str(output) + "']});</script>"
    print >> environ['wsgi.errors'], output
    output = "top.Ext.dispatch({controller:'Chat', action: 'upload_result', args : ['" + str(output) + "']});"

    print >> environ['wsgi.errors'], output
    response_headers = [('Content-type', 'text/html;'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    print >> environ['wsgi.errors'], "Success"
    return [output]

