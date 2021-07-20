from flask import Flask, render_template, request , send_from_directory, url_for, session,redirect
from uuid import uuid4
from flask_pymongo import Pymongo
import bcrypt
import os

app = Flask(__name__)

app.config['MONGO_DBNAME']='minor'
app.config['MONGO_URI']='mongodb+srv://minor:Komal16%40@test.qpcxw.mongodb.net/test?authSource=admin&replicaSet=atlas-5vwoyr-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

classes = ['COVID19','NORMAL','PNEUMONIA']

mongo = Pymongo(app)
@app.route('/', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
         users= mongo.db.users
         existing_user  = users.find_one({'name':request.form['name']})
         if existing_user is None:
           hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8')),bcrypt.gensalt()
           users.insert({'name':request.form['name'], 'password':hashpass})
           session['name']= request.form['name']
           return redirect(url_for('sample'))
    if 'name' in session:
        return 'you are logged in as the following users:' + session['name']
    return   render_template('sample.html')



@app.route('/login.html',  methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['name']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'),login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['name'] = request.form['name']
            return redirect(url_for('sample'))
    return 'invalid username or password combination'

@app.route('/upload.html')
def uploading():
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        #import tensorflow as tf
        import numpy as np
        from keras.preprocessing import image
        from keras.applications.resnet50 import preprocess_input
        from keras.models import load_model
        new_model = load_model('model.h5')
        new_model.summary()
        test_image = image.load_img('images/'+filename,target_size=(224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        test_image = preprocess_input(test_image)
        result = new_model.predict(test_image)
#        result=list(training_set.class_indices)[np.argmax(predictions[0])]
        result1 = result[0]
        for i in range(6):
    
            if result1[i] == 1.:
                break;
        prediction = classes[i]

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("report.html",image_name=filename, text=prediction)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)
    

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')
if __name__=="__main__":
     app.secret_key='secretivekeyagain'
     app.run(debug=True)        
