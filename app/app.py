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
import uiComponentDetector as det
import os

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

	  img = Image.open(uploaded_file)
	  filename = "temp_" + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]) + ".png"
	  img.save(filename)
	  return filename
		

def display_result(json_data, html_page_url):

	download_btn_str = download_button(json_data)
	render_btn_str = render_output_button(html_page_url)

	buttons_str = f"{render_btn_str}{download_btn_str}"
	st.markdown(buttons_str, unsafe_allow_html=True)

	st.json(json_data)


def submit_clicked(value, img_filename):
	if(value):
		# st.success('')
		with st.spinner(text='Submitted successfully. Processing image...'):
			# time.sleep(5)		# Dummy waiting to indicate processing (to be replaced by actual ui component detecton pipeline)
			
			os.system("python ./uiComponentDetector/run_single.py --img {} --op_dir ./".format(img_filename))

			st.success('Completed Processing!')

			with open("compo.json", "r") as fin:
				json_data = json.load(fin)

			# Dummy HTML rendering of the wireframe image
			html_page_url = "demo.html"

			img = Image.open("ip/result.jpg")
			st.image(img, caption='Identified Components', use_column_width=True)

			display_result(json_data, html_page_url)


def main():
	st.title('Smart UI')
	st.subheader('Techfest 2020-21')

	uploaded_file = st.file_uploader("Choose a wireframe image file", type=["png", "jpg", "JPG", "jpeg"])
	filename = imgshow(uploaded_file)

	submitted = st.button("Submit")
	submit_clicked(submitted, filename)


	st.write('_Developed with ❤️ by [Rishabh](https://rishabharya.site/), [Shreya](https://laddhashreya2000.github.io) & [Tezan](https://tezansahu.github.io/)_')

if __name__ == "__main__":
	main()