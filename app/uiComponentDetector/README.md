# UI Component Detector & Classifier

## Component Detection

UI Component Detection has been adapted from [UI Element Detection](https://github.com/MulongXie/UIED). The algorithm for detection is mentioned below:

- Region detection method first detects the layout blocks of a GUI using the _flood-filling algorithm_ over the greyscale map
- _Suzuki's Contour tracing algorithm_ is used to compute the boundary of the block and produce a block map
- A binary map of the input GUI, and for each detected block are generated, followed by it segmenting the corresponding region of the binary map (the binarization method based on the _gradient map_ of the GUI image)
- _Connected component labeling_ is used to identify GUI element regions in each binary block segment (as GUI elements can be any shape, it identifies a smallest rectangle box that covers the detected regions as the bounding boxes)

---

## Element Classification

For classification of the detected GUI components, one can use the following:

- CNN trained on [RICO Dataset](http://interactionmining.org/rico) _([cnn-rico-1.h5](https://drive.google.com/file/d/1Gzpi-V_Sj7SSFQMNzy6bcgkEwaZBhGWS/view?usp=sharing))_
- CNN trained using transfer learning on the wireframes dataset provided by organizers _([cnn-wireframes-only.h5](https://drive.google.com/file/d/1eUqku9yAZ8MfxCS5FxlsagZmcP1PN-JU/view?usp=sharing))_
- CNN trained using transfer learning on a more generalized dataset obtained from wireframes & the [ReDraw Dataset](https://zenodo.org/record/2530277) _([cnn-generalized.h5](https://drive.google.com/file/d/1XPw_hhm_ZwhD-_TppMXgCbOe3XTr641u/view?usp=sharing))_

These models can be downloaded using the links mentioned & stored in `smart_ui_tf20/models/` folder. Corresponding changes are automatically recognized by the configs in the `smart_ui_tf20/app/uiComponentDetector/config/CONFIG.py` file.

---