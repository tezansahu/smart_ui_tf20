# GUI Component Classifier

## UI Component Detection & Classification
_UI Component Detection has been adapted from [UIED](https://github.com/MulongXie/UIED)_. For classification of the detected GUI components, one can use the following:

- CNN trained on [RICO Dataset](http://interactionmining.org/rico) _([cnn-rico-1.h5]())_
- CNN trained using transfer learning on our custom dataset _([cnn-custom.h5]())_

These models can be downloaded using the links mentioned & stored in `smart_ui_tf20/models/` folder & corresponding changes should be made in the `smart_ui_tf20/app/uiComponentDetector/CONFIG.py` file.

## OCR for Text in Detected Components [TODO]