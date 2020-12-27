import streamlit as st


def imgshow(uploaded_file):
  if uploaded_file is not None:
	  image= uploaded_file.read()
	  img = st.image(image, caption='Train image', use_column_width=False)


def success(value):
	if(value):
		st.success('Succesfully Submitted')	  

st.title('Smart UI')
st.write('Developed by Tezan, Shreya and Rishabh')
uploaded_file = st.file_uploader("Choose a image file")
imgshow(uploaded_file)
value = st.button("Submit")	 # return a boolean value 
success(value)


# if(value):
# 	st.success('hello')  










# image=CV2.imread("1.png")
