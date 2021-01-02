import json
from yattag import Doc,indent

COMPONENT_TO_TAG = {
    "text": "p",
    "icon": "i",
    "div": "div"
}

ICON_NAME = {
    "traingle-down": "arrow_drop_down",
    "traingle-up": "arrow_drop_up",
    "right-arrow": "chevron-right",
    "left-arrow": "chevron-left",
    "dash": "horizontal-rule"
}

def jsonComponentsToHtmlString(components):
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            # We use google material icons
            doc.asis('<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">')
        with tag('body'):
            for component in components:
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
                            radius = int(min(component["height"], component["width"])/2)
                            component_style += f"{prop}: {radius}px"
                        else:
                            component_style += f"{prop}: {component['properties'][prop]}"
                    if prop.endswith("size"):
                        component_style += "px"
                    component_style += "; "

                # Icon components are dealt with differently because they need a separate class
                if component["element"] == "icon":
                    with tag(COMPONENT_TO_TAG[component["element"]], style=component_style, klass="material-icons"):
                        txt = ICON_NAME[component["properties"]["image"]]
                        text(txt)
                else:
                    with tag(COMPONENT_TO_TAG[component["element"]], style=component_style):
                        txt = ""
                        if "text" in component["properties"].keys():
                            txt = component["properties"]["text"]
                        text(txt)
    return indent(doc.getvalue())


def jsonToHtml(pathToJson, outputHtmlFile="output.html"):
    with open(pathToJson, "r") as jsonfile:
        components = json.load(jsonfile)
    htmlString = jsonComponentsToHtmlString(components)
    with open(outputHtmlFile, "w") as out_html:
        out_html.write(htmlString)
