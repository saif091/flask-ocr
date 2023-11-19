from flask import Flask, render_template, request
import os, pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image

project_dir = os.path.dirname(os.path.abspath(__file__))

app=Flask(__name__,
        static_url_path = '',
        template_folder = 'templates')

photos = UploadSet('photos',IMAGES)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'images'

class GetText(object):
    def __init__(self,file):
        self.file = pytesseract.image_to_string(Image.open(project_dir+'/images/' + file))



@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return 'there is no photo in form'
        name = request.form['img-name']+'.jpg'
        photo = request.files['photo']
        path = os.path.join(app.config['UPLOAD_FOLDER'],name)
        photo.save(path)

        textObject = GetText(name)
        

        return render_template('result.html',output=textObject.file) 
    return render_template('home.html')



if __name__ == '__main__':
    app.run()
