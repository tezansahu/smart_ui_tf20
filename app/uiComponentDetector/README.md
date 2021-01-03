# GUI Component Classifier

## UI Component Detection & Classification
_UI Component Detection has been adapted from [UIED](https://github.com/MulongXie/UIED)_. For classification of the detected GUI components, one can use the following:

- CNN trained on [RICO Dataset](http://interactionmining.org/rico) _([cnn-rico-1.h5](https://drive.google.com/file/d/1Gzpi-V_Sj7SSFQMNzy6bcgkEwaZBhGWS/view?usp=sharing))_
- CNN trained using transfer learning on the wireframes dataset provided by organizers _([cnn-wireframes-only.h5](https://drive.google.com/file/d/1eUqku9yAZ8MfxCS5FxlsagZmcP1PN-JU/view?usp=sharing))_
- CNN trained using transfer learning on a more generalized dataset obtained from wireframes & the [ReDraw Dataset](https://zenodo.org/record/2530277) _([cnn-generalized.h5](https://drive.google.com/file/d/1XPw_hhm_ZwhD-_TppMXgCbOe3XTr641u/view?usp=sharing))_

These models can be downloaded using the links mentioned & stored in `smart_ui_tf20/models/` folder. Corresponding changes are automatically recognized by the configs in the `smart_ui_tf20/app/uiComponentDetector/config/CONFIG.py` file.

## OCR for Text in Detected Components [TODO]