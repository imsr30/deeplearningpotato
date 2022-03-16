import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np

classes={0:"Bacterial Spot",1:"Early Blight",2:"Healthy",3:"Late Blight"}
model=load_model("C:/Users/Sriram.Sundaresan/Desktop/temp/model_dump/resnet_model.hdf5")

app=Flask(__name__)
upload_dir="C:/Users/Sriram.Sundaresan/Desktop/temp/static/uploads/"
app.config["UPLOAD_FOLDER"]=upload_dir
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_label(img_path):
	img=image.load_img(img_path,target_size=(244,244))
	img=np.array(img).reshape(1,244,244,3)
	predict=model.predict(img)
	predict=np.argmax(predict)
	return classes[predict]
	
@app.route('/')
def upload_form():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'image' not in request.files:
		flash('No file part')
		return redirect(request.url)
	image = request.files['image']
	if image.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if image and allowed_file(image.filename):
		filename = secure_filename(image.filename)
		image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		img_path=f"static/uploads/{filename}"
		prediction=predict_label(img_path)
		return render_template('home.html', filename=filename,prediction=prediction)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>/<prediction>')
def display_image(filename,prediction):
	return redirect(url_for('static', filename='uploads/' + filename, prediction=prediction), code=301)

if __name__ == "__main__":
    app.run()