from os.path import join as pjoin
import os


class Config:

    def __init__(self):
        # setting CNN (graphic elements) model
        self.image_shape = (64, 64, 3)

        self.project_root = os.path.dirname(os.path.abspath(__file__))[:os.path.dirname(os.path.abspath(__file__)).find("smart_ui_tf20")+13]

        self.CNN_PATH = pjoin(self.project_root, "models", "cnn-wireframes-only.h5")

        self.element_class = ['checkbox', 'dash', 'div_rect', 'div_round', 'down_arrow', 'left_arrow',
                              'leftd_arrow', 'radio', 'right_arrow', 'rightd_arrow', 'scroll', 'text',
                              'triangle_down', 'triangle_up']
        self.class_number = len(self.element_class)

        # # setting EAST (ocr) model
        # self.EAST_PATH = 'C:\\Users\\tezan\\Downloadseast_icdar2015_resnet_v1_50_rbox'

        self.COLOR = {'checkbox': (0, 255, 0), 'dash': (0, 0, 255), 'div_rect': (255, 166, 166),
                      'div_round': (255, 166, 0),
                      'down_arrow': (77, 77, 255), 'left_arrow': (255, 0, 166), 'leftd_arrow': (166, 0, 255),
                      'radio': (166, 166, 166),
                      'right_arrow': (0, 166, 255), 'rightd_arrow': (0, 166, 10), 'scroll': (50, 21, 255),
                      'text': (80, 166, 66), 'triangle_down': (0, 66, 80), 'triangle_up': (88, 66, 0),
                      'Compo':(0, 0, 255), 'Text':(169, 255, 0), 'Block':(80, 166, 66)}
