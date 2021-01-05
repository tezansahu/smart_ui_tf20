import os
import cv2
import json
from PIL import Image
import tesserocr
from tesserocr import PyTessBaseAPI, OEM
import keras_ocr
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--img", type=str, help="path/to/img")
parser.add_argument("--json", type=str, help="path/to/json")

repo_root = os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).find("smart_ui_tf20")+13]
tess_data_dir = os.path.join(repo_root, "app", "tessdata")

pipeline = keras_ocr.pipeline.Pipeline()

ELEMENT_NAME = {
    "text": "text",
    "div_rect": "div",
    "image": "image",
    "div_round": "div",
    "dash": "icon",
    "triangle_down": "icon",
    "triangle_up": "icon",
    "right_arrow": "icon",
    "left_arrow": "icon",
    "up_arrow": "icon",
    "down_arrow": "icon",
    "scroll": "scrollbar",
    "toggle_switch": "icon",
    "checkbox": "checkbox",
    "radio": "radio",
    "Background": "background"
}

IMAGE_NAME = {
    "triangle_down": "arrow_drop_down",
    "triangle_up": "arrow_drop_up",
    "right_arrow": "chevron-right",
    "left_arrow": "chevron-left",
    "up_arrow": "arrow_drop_up",
    "down_arrow": "arrow_drop_down",
    "dash": "horizontal-rule",
    "toggle_switch": "toggle_on"
}

def extract_text(properties, im_pil):
    
    with PyTessBaseAPI(oem=OEM.TESSERACT_ONLY, path=tess_data_dir) as api:
        api.SetImage(im_pil)
        api.Recognize() 
        iterator = api.GetIterator()
        font = iterator.WordFontAttributes()
        properties['font-size'] = font['pointsize']
        properties['font-family'] = font['font_name']
        if(font['bold']):
            properties['font-weight'] = 'bold'
        if(font['italic']):
            properties['font-style'] = 'italic'
        if(font['underlined']):
            properties['text-decoration'] = 'underline'
    return properties
            
def extractAttributes(image, jsonfile):

    im = cv2.imread(image)
    f = open(jsonfile, "r+") 
    data = json.load(f) 
    output = []
    x, y, _ = im.shape
    # loop over all items in json
    for i in data['compos']: 
        # extract the image dimensions
        w = int(i["width"])
        h = int(i["height"])

        # extract the label and bounding box coordinates
        label = i["class"]
        xmin = int(i['column_min'])
        xmax = int(i['column_max'])
        ymin = int(i['row_min'])
        ymax = int(i['row_max'])
        
        if(label=="text" or label=="image"):
            xmin = max(0, xmin-5)
            ymin = max(0, ymin-5)
            xmax = min(xmax+5, y)
            ymax = min(ymax+5, x)
        # extract the cropped out image according to the bounding box
        extracted = im[ymin:ymax, xmin:xmax]

        # convert the colors (for converting to PIL)
        extracted = cv2.cvtColor(extracted, cv2.COLOR_BGR2RGB)

        # convert image array to a PIL image
        im_pil = Image.fromarray(extracted)

        item = {'element': ELEMENT_NAME[label], 'x': xmin, 'y': ymin, 'width': w, 'height': h}
        properties = {}

        
        # extracting colors from image
        try:
            colors = sorted(im_pil.getcolors())
            bgcolor = '#%02x%02x%02x' % colors[-1][1]
            forecolor = '#%02x%02x%02x' % colors[-2][1]
        except Exception:
            # default colors
            bgcolor = "#fff"
            forecolor = "#000"
        
        # for property extraction based on labels
        if(label=="text"):
            text = str(tesserocr.image_to_text(im_pil)).rstrip()
            # print(text)
            if(text):
                properties['text'] = text
                properties['color'] = forecolor
                properties = extract_text(properties, im_pil)
                
            
        elif(label=="div_rect"):
            properties['background-color'] = bgcolor
            
        elif(label=="image"):
            text_tesserocr = str(tesserocr.image_to_text(im_pil)).rstrip()
            text_kerasocr = None
            ext = pipeline.recognize([extracted])[0]
            if len(ext) > 0:
                text_kerasocr = ext[0][0]
            
            if text_kerasocr:
                item["element"] = "text"
                properties['text'] = text_kerasocr
                properties['color'] = forecolor
                if text_tesserocr:
                    properties = extract_text(properties, im_pil)

            else:
                properties['background-color'] = bgcolor

        elif(label=="div_round"):
            properties['background-color'] = bgcolor
            properties['border-radius'] = int(min(w, h)/2)
            
        elif(item['element']=="icon"):
            properties['image'] = IMAGE_NAME[label]
            properties['color'] = forecolor
            
        elif(label=="radio" or label=="checkbox"):
            pass

        elif(label=="scroll"):
            properties['background-color'] = bgcolor
            
        elif(label=="Background"):
            properties['background-color'] = bgcolor
            
        if(properties):
            item['properties'] = properties  
        # print(item)
        output.append(item)

    # Closing file 
    f.close()
    with open(jsonfile, "w") as f:
        json.dump(output, f, indent=4)
     

if __name__ == "__main__":
    args = parser.parse_args()
    extractAttributes(args.img, args.json)