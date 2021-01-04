import json
from yattag import Doc,indent

COMPONENT_TO_TAG = {
    "text": "p",
    "icon": "i",
    "div": "div",
    "background":"body",
    "image": "img",
    "checkbox": "input",
    "radio": "input"
}

# ICON_NAME = {
#     "triangle-down": "arrow_drop_down",
#     "triangle-up": "arrow_drop_up",
#     "right-arrow": "chevron-right",
#     "left-arrow": "chevron-left",
#     "up-arrow": "arrow_drop_up",
#     "down-arrow": "arrow_drop_down",
#     "dash": "horizontal-rule"
# }

def jsonComponentsToHtmlString(components):
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            # We use google material icons
            doc.asis('<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">')
        with tag('body', style=f"{components[0]["properties"]["color"]}"):    #first element in components is background
            for component in components[1:]:
                # Add generic styling elements
                component_style = f"""
                    position: fixed;
                    top: {str(component["y"])}px;
                    left: {str(component["x"])}px;
                    height: {str(component["height"])}px;
                    width: {str(component["width"])}px;
                """.replace("\n", "")

                # Add more styling elements using component.properties
                for prop in component["properties"].keys():
                    if prop != "text":
                        # Set the border-radius (of a div) based on the smallest side (assuming true size isn't mentioned in the JSON)
                        if prop == "border-radius":
                            # radius = int(min(component["height"], component["width"])/2)
                            component_style += f"{prop}: {component["properties"]["border-radius"]}px"
                        else:
                            component_style += f"{prop}: {component['properties'][prop]}"
                    if prop.endswith("size"):
                        component_style += "px"
                    else:
                        component_style += f"{prop}: {component['properties'][prop]}"
                    component_style += "; "

                # Icon components are dealt with differently because they need a separate class
                if component["element"] == "icon":
                    with tag(COMPONENT_TO_TAG[component["element"]], style=component_style, klass="material-icons"):
                        txt = ICON_NAME[component["properties"]["image"]]
                        text(txt)

                elif component["element"] == "image":
                    doc.stag(COMPONENT_TO_TAG[component["element"]], src="assets/dummy.jpg", height=f"{str(component["height"])}px", width=f"{str(component["width"])}px", style=f"padding:2px;background-color:{ component["properties"]["background-color"]}") 

                elif component["element"] == "checkbox" or component["element"] == "radio":
                    doc.tag(COMPONENT_TO_TAG[component["element"]] , type=component["element"])    

                elif component["element"] == "text":
                    with tag(COMPONENT_TO_TAG[component["element"]], style=component_style):                      
                        text(component["properties"]["text"])              

                elif component["element"] == "div":
                    doc.tag(COMPONENT_TO_TAG[component["element"]], style=component_style)

                else:
                    pass    
                        
    return indent(doc.getvalue())


def jsonToHtml(pathToJson, outputHtmlFile="output.html"):
    with open(pathToJson, "r") as jsonfile:
        components = json.load(jsonfile)
    htmlString = jsonComponentsToHtmlString(components)
    with open(outputHtmlFile, "w") as out_html:
        out_html.write(htmlString)
