from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages
from django.views.decorators.csrf import csrf_exempt
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib.request import urlopen

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + ".<br/>"
                # To avoid Unicode trouble
                htmlFile.write (line)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                htmlFile.write (" Link: " + "<a href=" + self.theContent)
                htmlFile.write (">" + self.theContent + "</a><br/><br/>")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def mainPage(request):
    group = Pages.objects.all()
    list = ''
    for item in group:
        list = list + item.name + '<br>'
    return HttpResponse("La lista de recursos disponibles es la siguiente:<br><br>" +
    list + '<br>'
    "Un ejemplo de cómo pedir un recurso es: "
    "http://localhost:8000/pepito<br><br>"
    "Si pides un recurso que no existe, la página te lo indicará")

@csrf_exempt
def getPage(request, text):
    if request.method == "GET":
        try:
            global htmlFile
            object = Pages.objects.get(name = text)
            theParser = make_parser()
            theHandler = myContentHandler()
            theParser.setContentHandler(theHandler)
            url = "http://barrapunto.com/index.rss"
            url = urlopen(url)
            rss = url.read().decode("utf-8")
            url.close()
            xmlFile = open('barrapunto.rss', 'w')
            xmlFile.write(rss)
            xmlFile.close()
            htmlFile = open('barrapunto.html', 'w')
            htmlFile.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>")
            htmlFile.write("<h1>Titulares y links de barrapunto.com</h1>")
            xmlFile = open('barrapunto.rss', "r")
            theParser.parse(xmlFile)
            htmlFile.close()
            htmlFile = open('barrapunto.html', 'r')
            barrapunto = htmlFile.read()
            return HttpResponse(barrapunto + object.page)
        except Pages.DoesNotExist:
            return HttpResponse("No hay una página para " + text)
    else:
        page = Pages(name = text, page = request.body.decode("utf-8"))
        page.save()
        return HttpResponse("New page created")
