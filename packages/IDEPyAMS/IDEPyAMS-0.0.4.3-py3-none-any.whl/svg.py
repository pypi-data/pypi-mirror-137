#-------------------------------------------------------------------------------
# Name:        SVG
# Author:      D.fathi
# Created:     16/12/2021
# Copyright:   (c) D.fathi 2021
# Licence:     free
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# class svgElement: object of SVG Elements
#-------------------------------------------------------------------------------


class svgElement(object):
    def __init__(self,ref):
        self.ref=ref;
        self.namePart='';
        self.svgout=0;
        self.id='0';
    def __name__(self):
         return 'SVGElement'

    def val(self,description,value):
        v="document.getElementById('"+self.id+"')."+description+'='+value;
        self.page.runJavaScript(v);

    def textContent(self,value):
        v="document.getElementById('"+self.id+"').textContent='"+value+"'";
        self.page.runJavaScript(v);

