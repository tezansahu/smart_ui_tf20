import streamlit as st
import time
import json
import base64
import requests
import uuid
import re
import cv2
from PIL import Image
import random
import string
import os

CNN_MODELS = {
	"CNN (Wireframes & ReDraw)": "cnn-generalized",
	"CNN (RICO Dataset)": "cnn-rico", 
	"CNN (Wireframes only)": "cnn-wireframes-only"
}

def get_button_css(button_id):
	custom_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """
	
	return custom_css

def download_button(json_data):
	data_str = json.dumps(json_data, indent=4)
	b64 = base64.b64encode(data_str.encode('utf-8')).decode()

	button_uuid = str(uuid.uuid4()).replace('-', '')
	button_id = re.sub('\d+', '', button_uuid)

	dl_link = get_button_css(button_id) + f'<a download="wireframe.json" id="{button_id}" href="data:file/txt;base64,{b64}">Download JSON File</a><br></br>'

	return dl_link


def render_output_button(html_page_url):
	button_uuid = str(uuid.uuid4()).replace('-', '')
	button_id = re.sub('\d+', '', button_uuid)

	link = get_button_css(button_id) + f'<a id="{button_id}" href="{html_page_url}" target="_blank">Render HTML Output</a><br></br>'
	return link


def imgshow(uploaded_file):
  if uploaded_file is not None:
	  image = uploaded_file.read()
	  st.image(image, caption='Wireframe Image', use_column_width=True)


def save_image_temp(uploaded_file):
	if uploaded_file is not None:
	  img = Image.open(uploaded_file)
	  filename = "temp_" + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]) + ".png"
	  img.save(filename)
	  return filename


def delete_file(filename):
	if os.path.exists(filename):
		os.remove(filename)


def delete_temp_files(img_filename):
	delete_file(img_filename)
	delete_file("ip/" + img_filename.replace("png", "json"))
	delete_file("compo.json")
	delete_file("result.jpg")
	delete_file("ip/result.jpg")
	os.rmdir("ip")


def display_result(json_data, html_page_url):

	download_btn_str = download_button(json_data)
	render_btn_str = render_output_button(html_page_url)

	buttons_str = f"{render_btn_str}{download_btn_str}"
	st.markdown(buttons_str, unsafe_allow_html=True)

	st.json(json_data)


def submit_clicked(value, uploaded_img_file, options):
	if(value):
		with st.spinner(text='Submitted successfully. Processing image...'):
			img_filename = save_image_temp(uploaded_img_file)

			# UI Component Detection
			comp_det_statement = "python ./uiComponentDetector/run_single.py --img {img} --op_dir ./ --clf --min_grad {min_grad} --ffl_block {ffl_block} --min_ele_area {min_ele_area} --max_word_inline_gap {max_word_inline_gap} --max_line_gap {max_line_gap} -cnn {cnn}".format(
				img=img_filename,
				min_grad=options["min_grad"],
				ffl_block=options["ffl_block"],
				min_ele_area=options["min_ele_area"],
				max_word_inline_gap=options["max_word_inline_gap"],
				max_line_gap=options["max_line_gap"],
				cnn=options["cnn_model"]
			)
			if options["merge_contained_ele"]:
				comp_det_statement += " --merge_contained_ele"
			os.system(comp_det_statement)

			st.success('Completed Processing!')

			with open("compo.json", "r") as fin:
				json_data = json.load(fin)

			# Dummy HTML rendering of the wireframe image
			html_page_url = "demo.html"

			img = Image.open("ip/result.jpg")
			st.image(img, caption='Identified Components', use_column_width=True)

			display_result(json_data, html_page_url)

			delete_temp_files(img_filename)


def main():
	st.title('Smart UI')
	st.subheader('Techfest 2020-21')

	uploaded_file = st.file_uploader("Choose a wireframe image file", type=["png", "jpg", "JPG", "jpeg"])
	imgshow(uploaded_file)

	st.sidebar.title("Advanced Options")
	options = {}
	
	st.sidebar.subheader("For UI Elements:")
	options["cnn_model"] = CNN_MODELS[st.sidebar.selectbox(
		"Model for UI Component Classification:", 
		options=["CNN (Wireframes & ReDraw)", "CNN (Wireframes only)", "CNN (RICO Dataset)"]
	)]
	
	options["min_grad"] = st.sidebar.slider("Gradient Threshold to produce Binary Map", min_value=1, max_value=10, value=3, step=1)
	options["ffl_block"] = st.sidebar.slider("Fill-flood threshold", min_value=1, max_value=10, value=5, step=1)
	options["min_ele_area"] = st.sidebar.slider("Minimum Area for Components", min_value=10, max_value=200, value=25, step=1)
	options["merge_contained_ele"] = st.sidebar.checkbox("Merge Elements Contained in Others")

	st.sidebar.subheader("For Text:")
	options["max_word_inline_gap"] = st.sidebar.slider("Max Text Word Gap to be Same Line", min_value=1, max_value=15, value=4, step=1)
	options["max_line_gap"] = st.sidebar.slider("Max Text Line Gap to be Same Paragraph", min_value=1, max_value=20, value=4, step=1)

	submitted = st.button("Submit")
	submit_clicked(submitted, uploaded_file, options)


	st.write('_Developed with ❤️ by [Rishabh](https://rishabharya.site/), [Shreya](https://laddhashreya2000.github.io) & [Tezan](https://tezansahu.github.io/)_')

if __name__ == "__main__":
	main()