# from bs4 import BeautifulSoup
# from imutils import paths
import os
# import pandas as pd
import cv2
import json
from PIL import Image
import tesserocr
from tesserocr import PyTessBaseAPI, OEM
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--img", type=str, help="path/to/img")
parser.add_argument("--json", type=str, help="path/to/json")


def extractAttributes(image, jsonfile):
    # grab all image paths then construct the training and testing split
    # imagePaths = list(paths.list_files(images_path))

    im = cv2.imread(image)

    f = open(jsonfile, "r+") 
    output = []
    # returns JSON object as  
    # a dictionary 
    data = json.load(f) 
    # Iterating through the json 
    # list 
    for i in data['compos']: 
        # print(i) 
        # extract the image dimensions
        w = int(i["width"])
        h = int(i["height"])

        # loop over all object elements
        # extract the label and bounding box coordinates
        label = i["class"]
        xmin = int(i['column_min'])
        xmax = int(i['column_max'])
        ymin = int(i['row_min'])
        ymax = int(i['row_max'])
        extracted = im[ymin:ymax, xmin:xmax]
        
        # d = label+str(i['id'])
        
        extracted = cv2.cvtColor(extracted, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(extracted)
        item = {}
        if(label=="text"):
            item = {'element':label, 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            colors = sorted(im_pil.getcolors())
            element = {}
            element['text'] = str(tesserocr.image_to_text(im_pil)).rstrip()
            # element['font-color'] = colors[-2]
            element['font-color'] = '#%02x%02x%02x' % colors[-2][1]
            # print(element['text'])
            if(element['text'] ):
                with PyTessBaseAPI(oem=OEM.TESSERACT_ONLY, path="./tessdata") as api:
                    api.SetImage(im_pil)
                    api.Recognize() 
                    iterator = api.GetIterator()
                    font = iterator.WordFontAttributes()
                    # print(iterator.WordFontAttributes())
                    element['font-size'] = font['pointsize']
                    element['font-family'] = font['font_name']
                    if(font['bold']):
                        element['font-weight'] = 'bold'
                    if(font['italic']):
                        element['font-style'] = 'italic'
                    if(font['underlined']):
                        element['text-decoration'] = 'underline'
            item['properties'] = element
            print(item)
        elif(label=="div_rect"):
            colors = sorted(im_pil.getcolors())
            item = {'element': "div", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            element['background-color'] = '#%02x%02x%02x' % colors[-1][1]
            item['properties'] = element
            print(item)
            
        elif(label=="image"):
            element = {}
            element['text'] = str(tesserocr.image_to_text(im_pil)).rstrip()           
            # print(element['text'])
            if(element['text'] ):
                item = {'element':"text", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
                colors = sorted(im_pil.getcolors())
                element['font-color'] = '#%02x%02x%02x' % colors[-2][1]
                with PyTessBaseAPI(oem=OEM.TESSERACT_ONLY, path="./tessdata") as api:
                    api.SetImage(im_pil)
                    api.Recognize() 
                    iterator = api.GetIterator()
                    font = iterator.WordFontAttributes()
                    # print(iterator.WordFontAttributes())
                    element['font-size'] = font['pointsize']
                    element['font-family'] = font['font_name']
                    if(font['bold']):
                        element['font-weight'] = 'bold'
                    if(font['italic']):
                        element['font-style'] = 'italic'
                    if(font['underlined']):
                        element['text-decoration'] = 'underline'
                item['properties'] = element
                print(item)
            else:
                colors = sorted(im_pil.getcolors())
                element = {}
                item = {'element':label, 'x': xmin, 'y': ymin, 'width': w, 'height': h}
                element['background-color'] = '#%02x%02x%02x' % colors[-1][1]
                item['properties'] = element
                print(item)
            

        elif(label=="div_round"):
            colors = sorted(im_pil.getcolors())
            item = {'element': "div", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            element['background-color'] = '#%02x%02x%02x' % colors[-1][1]
            element['border_radius'] = int(min(w, h)/2)
            item['properties'] = element
            print(item)
            
            # print(border_radius)
        elif(label=="dash"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'horizontal-rule'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)

        elif(label=="checkbox"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            element['image'] = 'checkbox'
            item['properties'] = element
            print(item)
        elif(label=="down_arrow"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'arrow_drop_down'
            element['color'] = '#%02x%02x%02x' % colors[-2][1] # if not white then keep
            item['properties'] = element
            print(item)
        elif(label=="left_arrow"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'chevron-left'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        elif(label=="radio"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            element['image'] = 'radio-button'
            item['properties'] = element
            print(item)
        elif(label=="right_arrow"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'chevron-right'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        elif(label=="scroll"):
            item = {'element': "scrollbar", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['color'] = '#%02x%02x%02x' % colors[-1][1]
            item['properties'] = element
            print(item)
        elif(label=="toggle_switch"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'toggle_on'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        elif(label=="up_arrow"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'arrow_drop_up'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        elif(label=="triangle-down"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'arrow_drop_down'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        elif(label=="triangle-up"):
            item = {'element': "icon", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['image'] = 'arrow_drop_up'
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        elif(label=="Background"):
            item = {'element': "background", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            element = {}
            colors = sorted(im_pil.getcolors())
            element['color'] = '#%02x%02x%02x' % colors[-2][1]
            item['properties'] = element
            print(item)
        else:
            item = {'element': "unknown", 'x': xmin, 'y': ymin, 'width': w, 'height': h}
            print(item)
        output.append(item)

    # Closing file 
    f.close()
    with open(jsonfile, "w") as f:
        json.dump(output, f, indent=4)
     
        

# icon, div, text, image, background  --- if image has text then make it text. ---class should be name.

def main():
    args = parser.parse_args()
    extractAttributes(args.img, args.json)

if __name__ == "__main__":
    main()