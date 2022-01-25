import numpy as np
import cv2
import uuid
import os
import vision

from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, abort, make_response

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
def deteksi_jerawat():
    # menerima upload files
    images = upload()

    results = []

    for index, image in enumerate(images):
        if image is None or len(image) == 0:
            result = None
            results.append(result)
            continue

        # face detection and segmentation
        face_box = vision.face_detection(image)
        height = int(image.shape[0])
        width = int(image.shape[1])

        face_seg, face_seg_box, face_land = (image, (0, 0, height, width), None)
        if face_box is not None:
            face_seg, face_seg_box, face_land = vision.face_segmentation(image, face_box)
            face_land = face_land.astype(int).tolist()

        # crop image
        if face_seg_box is not None:
            x, y, h, w = face_seg_box
            face_seg_box = np.array(face_seg_box, int).tolist()
            face_seg = image[y:y+h, x:x+w].copy()
            # cv2.imwrite( os.path.join(UPLOAD_FOLDER, uuid.uuid4().hex + '.jpeg'), face_seg)
        
        # deteksi jerawat
        deteksi_objek = vision.deteksi_objek(face_seg)
        normalisasi = {}

        if len(deteksi_objek) > 0:
            for obj in list(deteksi_objek.keys()):
                normalisasi[obj] = []
                for item in deteksi_objek[obj]:
                    # ymin, xmin, ymax, xmax
                    norm = {
                        'xmin': (item['box'][1] * face_seg_box[3] + face_seg_box[0]) / width,
                        'ymin': (item['box'][0] * face_seg_box[2] + face_seg_box[1]) / height,
                        'ymax': (item['box'][2] * face_seg_box[2] + face_seg_box[1]) / height,
                        'xmax': (item['box'][3] * face_seg_box[3] + face_seg_box[0]) / width,
                        'score': item['score']
                    } 
                    normalisasi[obj].append(norm)
                    image[int(norm['ymin']*height):int((norm['ymax']*height)), int(norm['xmin'] * width):int((norm['xmax'] * width))] = (0, 0, 0)

            cv2.imwrite(os.path.join(UPLOAD_FOLDER, uuid.uuid4().hex + '.jpeg'), image)


        result = {
            'face_box': face_seg_box,
            'face_landmark': face_land,
            'deteksi_objek': normalisasi
        }
        results.append(result)

    # print(results)

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)