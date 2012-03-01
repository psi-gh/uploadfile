#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created: 20.02.2012
@author: psi
'''

import sys
sys.path.insert(0, "/var/www/uploadfile/wsgi/")
import previewclass
import cgi, re, random, string, os, socket, urllib
    
def application(environ, start_response):
    print >> environ['wsgi.errors'],  "START"
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    fileAddress = form['addr'].value
    print >> environ['wsgi.errors'],  'addr is ' + fileAddress
    if 'x' in form:
        sizex = form['x'].value
    else:
        sizex = 128
    if 'y' in form: 
        sizey = form['y'].value
    else:
        sizey = 128
    print >> environ['wsgi.errors'],  fileAddress
    pr = previewclass.Preview()
    print >> environ['wsgi.errors'],  'Making preview with sizes: ' + str(sizex) + 'x' + str(sizey)
    previewPath = pr.getPreview(fileAddress, sizex, sizey)
    if (previewPath == 'Error'):
        print >> environ['wsgi.errors'],  "Error. Preview was not created!"
        status = '200 OK'
        response_headers = [('Content-type', 'html/text;')]
        start_response(status, response_headers)
        return "<html><body>Error</body></html>"
        
    print >> environ['wsgi.errors'],  previewPath
    status = '200 OK'
    response_headers = [('Content-type', 'image/jpeg;')]
    start_response(status, response_headers)
    return open(previewPath, "rb").read()

