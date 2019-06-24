from flask import Flask, render_template, flash, request
from flask import url_for,redirect, session, abort
from werkzeug import secure_filename
from backend import dbOperations
import os

app = Flask(__name__)
app.secret_key = "super secret key"
UPLOAD_FOLDER = 'static/docs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods=['GET', 'POST'])
def mainPage():
	if request.method =='POST':
		try:
			if 'uploadDoc' in request.form:
				docDBName = request.form['docDBName']
				doc = request.files['document']
				docName = secure_filename(doc.filename)
				docPath = os.path.join(app.config['UPLOAD_FOLDER'],docName)
				doc.save(app.config['UPLOAD_FOLDER']+docName)
				with open(docPath) as f:
					docContent = f.read()
				f.close()
				backend = dbOperations()
				backend.insertIntoDoc(docDBName,docPath)
				getPresentDocs = backend.listDocTable()
				flash('File Read Successfully','success')

				return render_template('index.html',
				docContent = docContent,docInfo = getPresentDocs[1])
			else:
				prevDocPath = request.form['prevDocPath']
				with open(prevDocPath) as f:
					docContent = f.read()
				f.close()
				backend = dbOperations()
				getPresentDocs = backend.listDocTable()
				flash('File Read Successfully','success')

				return render_template('index.html',
				docContent = docContent,docInfo = getPresentDocs[1])

		except Exception as e:
			flash('Error While Uploading File: '+str(e),'danger')
			return render_template('index.html',docInfo = getPresentDocs[1])
	else:
		backend = dbOperations()
		getPresentDocs = backend.listDocTable()
		return render_template('index.html',docInfo = getPresentDocs[1])




if __name__ == '__main__':
	app.debug = True
	app.run()
