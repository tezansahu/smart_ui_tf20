# Text & Attribute Extractor 
For each of the components detected by the UI Element Detector, text and other attributes are extracted based on its class assigned by the chosen deep learning model. These attributes contain font and color related properties.

## Text Recognition using OCR 
OCR techniques are applied on the text and image classified components. Text recognition is performed using [`tesserocr`](https://pypi.org/project/tesserocr/) and [`keras-ocr`](https://keras-ocr.readthedocs.io/en/latest/). 

`tesserocr` works best when there is a (very) clean segmentation of the foreground text from the background. For other cases, `keras-ocr` is used in conjunction with `tesserocr` to improve text recognition.

---

## Attribute Extraction
For every class predicted by the deep learning model, following attributes are extracted:
- div-rectangular
    - background-color
- div-rounded
    - background-color
    - border-radius
- text
    - color
    - font-size
    - font-family
    - font-weight
    - font-style
    - text-decoration
- icons
    - color
- scroll bar
    - background-color
- image
    - background-color

### Colors
Color pallette is extracted using the `getcolors()` method in the `Pillow` library. The color with the most pixels is cited as the background-color attribute and the color with the second most pixels is cited as the color attribute.

### Font-Related Properties
`PyTessBaseAPI` exposes several tesseract API methods which are used to extract the font-related properties of the `tesserocr`-recognised text. Following is a description of the font properties that are extracted - 

- `font-size`: states the font-size of the text
- `font-family`: states the font of the text
- `font-weight`: states if the text is bold.
- `font-style`: states if the text is italic.
- `text-decoration`: states if the text is underlined.

---