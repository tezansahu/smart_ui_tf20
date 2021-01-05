# Smart UI (Team ID: SU-208042)


## Problem Statement

Generate a JSON file (`output.json`) from the screenshot of the wireframe. The file should contain the details of various elements used in the webpage.

[Link to Detailed Problem Statement](assets/pdf/SmartUI.pdf)

---

## Our Solution

![App Demo](assets/images/demo.gif)


### Usage:

Clone the Repository:

```console
> git clone https://github.com/tezansahu/smart_ui_tf20.git
> cd smart_ui_tf20/
```

> _**Note:** The installation of dependenices & running of app works best in Anaconda with Python 3.7_

Install the dependencies:

```console
> conda install -c conda-forge --file requirements.txt
> pip install keras-ocr
```

> _**Note:** Since `keras-ocr` is not found in any of the Anaconda channels, it has to be installed separately as mentioned above._

Download necessary models & repositories for running the app:

```console
> python models/download_models.py   # Download the models to be used by the app
> git clone https://github.com/tesseract-ocr/tessdata.git ./app/tessdata/   # Clone the tessdata/ for legacy OCR being used in the app
```

Start the app:

```condole
> cd app/
> streamlit run app.py
```

This should start the app on `localhost` & fire up a tab in the browser

---

## Overview:

<!-- [Include a short writeup of the pipeline - adding a block diagram would be nice (block names to be same as the titles of the respecive Readme files)]

[Mention the names of the different blocks in a list & link them to the corresponding sections in this readme (see below)] -->
We use a three stage pipeline to generate a JSON file containing the attributes of all the components in the input wireframe image. We then render the JSON output into an HTML file. 

<p align="center">
  <img src='assets/images/pipeline.png' />
</p>

The pipeline, as shown in the figure, comprises of the following stages - 

- [UI Component Detection & Classification](#UI-Component-Detection-&-Classification)
- [Text & Attribute Extraction for Identified Components](#Text-&-Attribute-Extraction-for-Identified-Components)
- [HTML Generation from JSON](#HTML-Generation-from-JSON-_(Bonus)_)


### UI Component Detection & Classification

Taking inspiration from the paper ["_Object Detection for Graphical User Interface: Old Fashioned or Deep Learning or a Combination?_"](https://arxiv.org/pdf/2008.05132.pdf), we apply a hybrid approach _(Traditional Image-Processing + Deep Learning)_ to identify the various UI Components from a Wireframe Image. The two stages of this process are described below.

#### Image-Processing Based UI Element Detection:

Given a wireframe image as input, we first segment out the regions containing probable UI components using Image Processing techniques including contour detection, etc. Details about the implementation can be found [here](./app/uiComponentDetector/README.md).

> _**Note:** This portion of the code is an adapted version of the code found in [UI Element Detection (UIED)](https://github.com/MulongXie/UIED)._

#### Deep Learning Models (for Classification):

The following DL Models (CNNs) have been developed to categorize the detected UI elements into specific classes:

1. __CNN Trained on RICO Dataset__ _(Pretrained & used in UIED)_
2. __CNN Trained on Wireframes Dataset (provided by organizers)__ _(Transfer Learning using Model 1 as Base Model)_
3. __CNN Trained on Generalized Dataset (Wireframes + ReDraw Dataset)__ _(Transfer Learning using Model 2 as Base Model)_

Details about the models, inculding their training, performance & downloadable weights can be found [here](./models/README.md).

### Text & Attribute Extraction for Identified Components

For each of the identified components in the previous stage of the pipeline, its necessary attributes & styles are extracted, along with the text that the element may contain. These attributes include font & color related attributes. Details about the text recognition & attribute extracton process can be found [here](./app/attributeExtractor/README.md). The output is a JSON file containing the identified UI Elements along with their attributes (`properties`).

### HTML Generation from JSON _(Bonus)_

The JSON file generated above is passed through the HTML generation pipeline to obtain a HTML file that renders the components identified from the wireframe image into a webpage. Details of this process can be found [here](./app/htmlGenerator/README.md).

> _**Note:** The HTML code generated may not be of the best quality, but can render the JSON with sufficient accuracy to relate it to the original image input._

---

<p align="center">Created with ❤️ by <a href="https://rishabharya.site/" target="_blank">Rishabh Arya</a>, <a href="https://laddhashreya2000.github.io" target="_blank">Shreya Laddha</a> & <a href="https://tezansahu.github.io/" target="_blank">Tezan Sahu</a></p>