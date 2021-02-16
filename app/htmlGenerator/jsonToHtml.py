import json
import os
from yattag import Doc,indent
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("--json", type=str, help="path/to/json/input")
parser.add_argument("--html", type=str, help="path/to/html/output")

COMPONENT_TO_TAG = {
    "text": "span",
    "icon": "i",
    "div": "div",
    "background":"body",
    "image": "img",
    "checkbox": "input",
    "radio": "input"
}

repo_root = os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).find("smart_ui_tf20")+13]

def jsonComponentsToHtmlString(components):
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            # We use google material icons
            doc.asis('<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">')
            doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        with tag('body', style=f"background-color: {components[0]['properties']['background-color']}"):    #first element in components is background
            for i, component in enumerate(components[1:]):
                is_button = False

                # Add generic styling elements
                component_style = f"""
                    position: fixed;
                    top: {str(component["y"])}px;
                    left: {str(component["x"])}px;
                    height: {str(component["height"])}px;
                    width: {str(component["width"])}px;
                """.replace("\n", "")

                # Add more styling elements using component.properties
                if "properties" in component.keys():
                    for prop in component["properties"].keys():
                        if prop != "text":
                            # Set the border-radius (of a div) based on the smallest side (assuming true size isn't mentioned in the JSON)
                            if prop == "border-radius":
                                component_style += f"{prop}: {component['properties']['border-radius']}px"

                                # Using a heuristic that a rounded div generally corresponds to a clickable button
                                is_button = True
                                component_style += "; cursor: pointer"
                            else:
                                component_style += f"{prop}: {component['properties'][prop]}"
                        if prop.endswith("size"):
                            component_style += "px"
                        component_style += "; "

                # Create HTML tags with attributes based on each component
                if component["element"] == "icon":
                    with tag(COMPONENT_TO_TAG[component["element"]], style=component_style, klass="material-icons"):
                        txt = component["properties"]["image"]
                        text(txt)

                elif component["element"] == "image":
                    # f"padding:2px; background-color:{ component['properties']['background-color']}"
                    dummy_img_path = os.path.join(repo_root, "app", "htmlRender", "assets", "dummy.png")
                    doc.stag(COMPONENT_TO_TAG[component["element"]], src=dummy_img_path, height=f"{str(component['height'])}px", width=f"{str(component['width'])}px", style=component_style) 

                elif component["element"] == "checkbox" or component["element"] == "radio":
                    doc.input(type=component["element"], style=component_style, name=f"input_{i}")

                elif component["element"] == "text":
                    with tag(COMPONENT_TO_TAG[component["element"]], style=component_style + "z-index: 2;"):                      
                        if "properties" in component.keys():
                            text(component["properties"]["text"])              

                elif component["element"] == "div":
                    if is_button:
                        # If the div is a button, add an 'onClick' attribute 
                        with doc.tag(COMPONENT_TO_TAG[component["element"]], style=component_style + "z-index: -1;", onclick="location.href='#';"):
                            text("")
                    else:
                        with doc.tag(COMPONENT_TO_TAG[component["element"]], style=component_style + "z-index: -1;"):
                            text("")

                else:
                    pass    
                        
    return indent(doc.getvalue())


def jsonToHtml(pathToJson, outputHtmlFile="output.html"):
    with open(pathToJson, "r") as jsonfile:
        components = json.load(jsonfile)
    htmlString = jsonComponentsToHtmlString(components)
    with open(outputHtmlFile, "w") as out_html:
        out_html.write(htmlString)

def main():
    args = parser.parse_args()
    jsonToHtml(args.json, args.html)

if __name__ == "__main__":
    main()