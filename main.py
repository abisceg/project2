from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
from google.cloud import storage
# for vision
from google.cloud import vision
from PIL import Image, ImageDraw
import io
import types

# import google.cloud
# from google.cloud import storage
# vars
# noinspection PyPackageRequirements,PyPackageRequirements
#UPLOAD_FOLDER = '/home/abisceg/Desktop/gcp_python/project2/uploads'
UPLOAD_FOLDER = '/var/www/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])

#instantiate flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.run(debug=True)

@app.route('/golfform')
def form():
    return render_template('form.html')




'''
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
'''

#upload to google function
def upload_blob(file_stream,  destination_blob_name, content_type):

    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    # storage_client = storage.Client.from_service_account_json('/home/abisceg/.config/gcloud/legacy_credentials/abisceg@gmail.com/adc.json')
    #shouldnt be hardcoded but for now..
    bucket_name='bucket-67'
    # watch
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    # cant upload from filename (local) need to upload from string
    # blob.upload_from_filename(source_file_name)
    blob.upload_from_string(file_stream, content_type=content_type)

def cloud_vision():
    #cloud vision newly uploaded file


'''
#from google doc: https://cloud.google.com/python/getting-started/using-cloud-storage
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
'''

@app.route('/list')
def list_blobs_go():
    list_blobs()
    return "Hello gcp World"


def list_blobs():
    bucket_name = 'bucket-67'
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    # storage_client = storage.Client.from_service_account_json('/home/abisceg/.config/gcloud/legacy_credentials/abisceg@gmail.com/adc.json')
    #storage_client = storage.Client.from_service_account_json('/home/abisceg/PycharmProjects/project2-new/venv/uml-advcc-project2-207700-c829dbac9a9e.json')

    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)



@app.route('/golfcard', methods=['GET', 'POST'])
def submitted_form_golf():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    # filename = secure_filename(file.filename)
    if request.method == 'POST':
        # f = request.files['file']
        f = request.files.get('file')
        fname = secure_filename(f.filename)
        # needed for upload
        bucket_name = 'bucket-67'
        source_file_name = f
        destination_blob_name = fname
        # f.save(fname)
        # this doesnt work when running devapperserver, because gapps doesnt want you storing locally!
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
        # return redirect(url_for('submitted_form_golf', fname=fname))
        # all google stuff
        upload_blob(f.read(), fname, f.content_type)

    return render_template(
        'submitted_form_golf.html',
        name=name,
        email=email,
        site=site,
        file=f,
        filename=fname,
        comments=comments)






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/testform', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template('testuploadform.html')



    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''






'''
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method =='POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.png')
'''

@app.route('/dropform')
def dropform():
    return render_template('dropform.html')

@app.route('/dropform/hello')
def hello():

    return 'Hello, World 2!'


@app.route('/hello')
def hello2():
    return 'Hello, World'


'''
app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)
    return "successful_upload"

'''


'''
app.route('/sendfile', methods = ['POST'])
def send_file():
    fileob = request.files["fileuploading"]
    filename = secure_filename(fileob.filename)
    save_path =

#upload blob to gs from local
def upload_blob(bucket_name, source_file_name, destination_blob_name):

    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name)

'''