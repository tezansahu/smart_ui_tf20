import json
from yattag import Doc,indent


def jsontoHtml(pathtojson):
    jsonfile = open(pathtojson)
    jsontolist = json.load(jsonfile)
    n=len(jsontolist)
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            for i in range(0,n):
                with tag(jsontolist[i]["element"], style= 'height:'+ str(jsontolist[i]["height"])+'px' + ';'+ 'width:'+ str(jsontolist[i]["width"])+'px' + ';'+ 'top:'+ str(jsontolist[i]["y"]) +'px'+ ';' + 'left:'+ str(jsontolist[i]["x"])+'px' + ';'+ 'position:fixed;' ):
                        text('hi')
    out_html= open('output.html','w')
    print(indent(doc.getvalue()), file=out_html)
    out_html.close()                               


def main():
    jsontoHtml('output.json') 
     
if __name__ == "__main__":
	main()

