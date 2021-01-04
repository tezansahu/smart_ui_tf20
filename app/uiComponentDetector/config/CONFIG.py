from os.path import join as pjoin
import os


class Config:

    def __init__(self, cnn_type="cnn-wireframes-only"):
        # setting CNN (graphic elements) model
        self.image_shape = (64, 64, 3)

        self.project_root = os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).find("smart_ui_tf20")+13]

        # For CNN trained on Wireframes only
        if cnn_type == "cnn-wireframes-only":
            self.CNN_PATH = pjoin(self.project_root, "models", "cnn-wireframes-only.h5")

            self.element_class = ['checkbox', 'dash', 'div_rect', 'div_round', 'down_arrow', 'left_arrow',
                              'leftd_arrow', 'radio', 'right_arrow', 'rightd_arrow', 'scroll', 'text',
                              'triangle_down', 'triangle_up']
            self.class_number = len(self.element_class)

            self.COLOR = {'checkbox': (0, 255, 0), 'dash': (0, 0, 255), 'div_rect': (255, 166, 166),
                        'div_round': (255, 166, 0),
                        'down_arrow': (77, 77, 255), 'left_arrow': (255, 0, 166), 'leftd_arrow': (166, 0, 255),
                        'radio': (166, 166, 166),
                        'right_arrow': (0, 166, 255), 'rightd_arrow': (0, 166, 10), 'scroll': (50, 21, 255),
                        'text': (80, 166, 66), 'triangle_down': (0, 66, 80), 'triangle_up': (88, 66, 0),
                        'Compo':(0, 0, 255), 'Text':(169, 255, 0), 'Block':(80, 166, 66)}
        
        # For CNN trained on Generalized Dataset (Wireframes & subset of ReDraw Dataset)
        elif cnn_type == "cnn-generalized":
            self.CNN_PATH = pjoin(self.project_root, "models", "cnn-generalized.h5")

            self.element_class = ['checkbox', 'dash', 'div_rect', 'div_round', 'down_arrow', 'image', 'left_arrow',
                                'radio', 'right_arrow', 'scroll', 'text', 'toggle_switch', 'up_arrow']
            self.class_number = len(self.element_class)

            self.COLOR = {'checkbox': (0, 255, 0), 'dash': (0, 0, 255), 'div_rect': (255, 166, 166),
                        'div_round': (255, 166, 0),
                        'down_arrow': (77, 77, 255), 'image': (166, 0, 255), 'left_arrow': (255, 0, 166),
                        'radio': (166, 166, 166),
                        'right_arrow': (0, 166, 255), 'scroll': (50, 21, 255),
                        'text': (80, 166, 66), 'toggle_switch': (0, 66, 80), 'up_arrow': (88, 66, 0),
                        'Compo':(0, 0, 255), 'Text':(169, 255, 0), 'Block':(80, 166, 66)}
        
        # For CNN trained on RICO Dataset
        elif cnn_type == "cnn-rico":
            self.CNN_PATH = pjoin(self.project_root, "models", "cnn-rico-1.h5")

            self.element_class = ['Button', 'CheckBox', 'Chronometer', 'EditText', 'ImageButton', 'ImageView',
                              'ProgressBar', 'RadioButton', 'RatingBar', 'SeekBar', 'Spinner', 'Switch',
                              'ToggleButton', 'VideoView', 'TextView']
            self.class_number = len(self.element_class)

            self.COLOR = {'Button': (0, 255, 0), 'CheckBox': (0, 0, 255), 'Chronometer': (255, 166, 166),
                      'EditText': (255, 166, 0),
                      'ImageButton': (77, 77, 255), 'ImageView': (255, 0, 166), 'ProgressBar': (166, 0, 255),
                      'RadioButton': (166, 166, 166),
                      'RatingBar': (0, 166, 255), 'SeekBar': (0, 166, 10), 'Spinner': (50, 21, 255),
                      'Switch': (80, 166, 66), 'ToggleButton': (0, 66, 80), 'VideoView': (88, 66, 0),
                      'TextView': (169, 255, 0), 'NonText': (0,0,255),
                      'Compo':(0, 0, 255), 'Text':(169, 255, 0), 'Block':(80, 166, 66)}

            
