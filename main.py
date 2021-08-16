from flask import Flask, flash, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.request
import os
from werkzeug.utils import secure_filename

main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devislab.db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(main)

UPLOAD_FOLDER = 'static/uploads/'

main.secret_key = "secret key"
main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
main.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    male = db.Column(db.Boolean)
    female = db.Column(db.Boolean)
    photo = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Registration %r>' % self.id


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/registration', methods=['POST', 'GET'])
def reg():

    if request.method == 'POST':
        file = request.files['File']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.filename = 'picture.png'
            file.save(os.path.join(main.config['UPLOAD_FOLDER'], file.filename))
            # # print('upload_image filename: ' + filename)
            # flash('Image successfully uploaded and displayed below')
            # return render_template('index.html', filename=filename)
        photo = ('static/uploads/' + file.filename)
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']
        if request.form['Male'] == 'Male':
            male = True
            female = False
        elif request.form['Male'] == 'Female':
            male = False
            female = True
        else:
            male = False
            female = False

        reg = Registration(username=username, email=email, password=password,
                           male=male, female=female, photo=photo)
        try:
            db.session.add(reg)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'

    else:
        return render_template('registration.html')


# @main.route('/completeRegistration')
# def completeRegistration():
#     completeRegistration = Registration.query.order_by(Registration.date.desc()).all()
#     return render_template("completeRegistration.html", completeRegistration=completeRegistration)
#
#
# @main.route('/completeOrder/<int:id>/del')
# def orderDelete(id):
#     completeRegistration = Registration.query.get_or_404(id)
#
#     try:
#         db.session.delete(completeRegistration)
#         db.session.commit()
#         return redirect('/completeRegistration')
#     except:
#         return 'Error'


if __name__ == '__main__':
    main.run(debug=True)
