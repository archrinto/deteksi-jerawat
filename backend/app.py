import os
import vision
import image_processor

from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, abort, make_response

from deteksi_jerawat import deteksi_jerawat
from deteksi_bintik_hitam import deteksi_bintik_hitam

### CONFIG ###
BASEDIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = 'data_images'
ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}


### UTIL ###
# Mengecek apakah file gambar atau bukan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def numpy2list(arr):
    return arr.tolist() if len(arr) > 0 and arr is not None else []

# upload image
def upload():
    files = request.files.getlist("file[]")
    
    # menerima multiple image upload
    images = []
    for file_ in files:
        # membaca file dari blob
        image = vision.image_fromblob(file_.read())
        # print(image)
        images.append(image)

        # filename = os.path.join(UPLOAD_FOLDER, uuid.uuid4().hex + '.jpeg')
        # cv2.imwrite(filename, image)
        
    return images


### MAIN APP ###
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/deteksi_jerawat', methods=['POST'])
def deteksi_jerawat_handler():
    # menerima upload files
    images = upload()

    results = []

    for index, image in enumerate(images):
        if image is None or len(image) == 0:
            result = None
            results.append(result)
            continue
        
        face_seg_box, face_land, normalisasi = deteksi_jerawat(app, vision, image)

        result = {
            'face_box': face_seg_box,
            'face_landmark': face_land,
            'deteksi_objek': normalisasi
        }
        results.append(result)

    # print(results)

    return jsonify(results)

@app.route('/deteksi_bintik_hitam', methods=['POST'])
def deteksi_bintik_hitam_handler():
    # menerima upload files
    images = upload()

    results = []

    for index, image in enumerate(images):
        if image is None or len(image) == 0:
            result = None
            results.append(result)
            continue
        
        normalisasi = deteksi_bintik_hitam(app, image_processor, image)

        result = {
            'deteksi_objek': normalisasi
        }
        results.append(result)

    # print(results)

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)