import cv2
import os
import uuid
import numpy as np

def deteksi_jerawat(app, vision, image):
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

        cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid4().hex + '.jpeg'), image)
    
    return face_seg_box, face_land, normalisasi

    