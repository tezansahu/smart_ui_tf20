from os.path import join as pjoin
import cv2
import os
from argparse import ArgumentParser

import detect_compo.ip_region_proposal as ip

parser = ArgumentParser()
parser.add_argument("--img", type=str, help="path/to/img")
parser.add_argument("--op_dir", type=str, help="path/to/output/directory")
parser.add_argument("--min_grad", type=int, default=3, help="Gradient Threshold to produce Binary Map")
parser.add_argument("--ffl_block", type=int, default=5, help="Fill-flood threshold")
parser.add_argument("--min_ele_area", type=int, default=25, help="Minimum Area for Components")
parser.add_argument("--max_word_inline_gap", type=int, default=4, help="Max Text Word Gap to be Same Line")
parser.add_argument("--max_line_gap", type=int, default=4, help="Max Text Line Gap to be Same Paragraph")
parser.add_argument("--cnn", type=str, default="cnn-wireframes-only", help="Model for UI Component Classification")
parser.add_argument("--clf", action='store_true')
parser.add_argument("--merge_contained_ele", action='store_true', help="Merge Elements Contained in Others")


# def resize_height_by_longest_edge(img_path, resize_length=800):
#     org = cv2.imread(img_path)
#     height, width = org.shape[:2]
#     if height > width:
#         return resize_length
#     else:
#         return int(resize_length * (height / width))


if __name__ == '__main__':

    '''
        ele:min-grad: gradient threshold to produce binary map         
        ele:ffl-block: fill-flood threshold
        ele:min-ele-area: minimum area for selected elements 
        ele:merge-contained-ele: if True, merge elements contained in others
        text:max-word-inline-gap: words with smaller distance than the gap are counted as a line
        text:max-line-gap: lines with smaller distance than the gap are counted as a paragraph

        Tips:
        1. Larger *min-grad* produces fine-grained binary-map while prone to over-segment element to small pieces
        2. Smaller *min-ele-area* leaves tiny elements while prone to produce noises
        3. If not *merge-contained-ele*, the elements inside others will be recognized, while prone to produce noises
        4. The *max-word-inline-gap* and *max-line-gap* should be dependent on the input image size and resolution

        mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
        web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
    '''
    args = parser.parse_args()

    key_params = {
        'min-grad': args.min_grad, 
        'ffl-block': args.ffl_block, 
        'min-ele-area': args.min_ele_area, 
        'merge-contained-ele': args.merge_contained_ele,
        'max-word-inline-gap': args.max_word_inline_gap, 
        'max-line-gap': args.max_line_gap,
        'cnn': args.cnn
    }

    # set input image path
    input_path_img = args.img
    output_root = args.op_dir

    # resized_height = resize_height_by_longest_edge(input_path_img)
    img = cv2.imread(input_path_img)
    height, _ = img.shape[:2]

    is_clf = args.clf

    os.makedirs(pjoin(output_root, 'ip'), exist_ok=True)
    
    # switch of the classification func
    classifier = None
    if is_clf:
        classifier = {}
        from cnn.CompDetCNN import CompDetCNN
        classifier['Elements'] = CompDetCNN(cnn_type=args.cnn)
    ip.compo_detection(input_path_img, output_root, key_params,
                        classifier=classifier, resize_by_height=height, show=False)
