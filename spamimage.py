import os
import numpy as np 
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,request,render_template
from werkzeug.utils import secure_filename

app=Flask(__name__)
model_path=r'C:\Users\ATHUL AKSHAY\Desktop\Spam Image\Spam Image Filter.h5'
model=load_model(model_path)

@app.route('/')
def index1():
    return render_template('Home-Page.html')

def preprocess_image(image_path):
    img=image.load_img(image_path,target_size=(224,224))
    img_array=image.img_to_array(img)
    img_array=np.expand_dims(img_array,axis=0)
    return img_array

def model_predict(file_path,model):
    processed_img=preprocess_image(file_path)
    preds=model.predict(processed_img)

    spamthreshold=0.8

    if preds>=spamthreshold:
        return 'The Image is SPAM'
    else:
        return 'The image is NOT SPAM'

@app.route('/nextpage',methods=['GET','POST'])

def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No File Part'
        

        file=request.files['file']
        if file.filename == '':
            return 'No File Choosen'

        if file:
            filename=secure_filename(file.filename)
            file_path=os.path.join('uploads',filename)
            file.save(file_path)
            result=model_predict(file_path,model)
            return result
    return render_template('SPAM-IMAGE-NEW.html')

if __name__=='__main__':
    app.run(debug=True,port=5004)
    














































# from flask import Flask,request,render_template
# import os
# app=Flask(__name__)
# app.config['Upload_image']='static/images'
# @app.route('/')
# def data():
#     return render_template('Spam image.html')
# @app.route('/submit',method=['POST'])
# def spamimage():
#     file=request.files['file']
#     file.save(os.path.join(app.config['Upload_image'],file.filename))
#     return 'Successfully'
# if __name__=='__main__':
#     app.run(debug=True)
