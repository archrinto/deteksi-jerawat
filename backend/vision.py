import os
import numpy as np
import cv2
import dlib
import requests


BASEDIR = os.path.dirname(os.path.realpath(__file__))
TF_ACNE_SERVING_URL = 'http://acne-model.herokuapp.com/v1/models/model:predict'
FACIAL_LANDMARK_MODEL = os.path.join(BASEDIR, 'ai_model', 'shape_predictor_81_face_landmarks.dat')
LABEL_MAP = {
    1: 'jerawat'
}


detector_landmark = dlib.shape_predictor(FACIAL_LANDMARK_MODEL)
detector_face = dlib.get_frontal_face_detector()


def shape2np(shape, dtype="int"): 
    coords = np.zeros((81, 2), dtype=dtype)

    for i in range(0, 81):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    return coords


def rect2bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    return (x, y, w, h)



def face_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector_face(gray, 1)

    if len(rects) == 0:
        return None

    face_area = []
    for (i, rect) in enumerate(rects):
        face_area.append( (rect.right() - rect.left()) * (rect.bottom() - rect.top()))
    
    max_index = np.argmax(face_area)
    face_rect = rects[max_index]

    return face_rect


def detect_landmark(image_gray, face):
    shape = detector_landmark(image_gray, face)
    shape = shape2np(shape)

    return shape


def face_segmentation(image, face):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    landmark = detect_landmark(gray, face)

    mask = np.zeros((image.shape[0], image.shape[1])) 
    pts = np.concatenate((landmark[0:16], landmark[69:81]))
    # membuat garis tepian wajah
    hull = cv2.convexHull(pts)

    cv2.drawContours(mask, [hull], -1, 1, -1)

    imgcp = image.copy()
    # segmentasi wajah
    imgcp[mask == 0] = (40, 40, 40)

    # seleksi titik diatas koordinat 0 
    pts = pts[pts[:,0] >= 0]
    pts = pts[pts[:,1] >= 0]

    # mengambil nilai min dan max 
    minx = np.min(pts[:,0])
    maxx = np.max(pts[:,0])
    miny = np.min(pts[:,1])
    maxy = np.max(pts[:,1])
    h = maxy - miny
    w = maxx - minx

    box = (minx, miny, h, w)

    return imgcp, box, landmark


def save_image(filename, image):
    cv2.imwrite(filename, image)


def image_fromblob(imagestr):
    try:
        image = cv2.imdecode(np.fromstring(imagestr, np.uint8), cv2.IMREAD_COLOR)
        return image
    except Exception as error:
        print(error)
        return None
    

def read_image(filename):
    return cv2.imread(filename)


def deteksi_objek(image):
    max_boxes_to_draw = 300 # perlu penyesuaian
    min_score_thresh = 0.09 # perlu penyesuaian

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(image, axis=0)
    payload = {"instances": img.tolist()}

    try:
        res = requests.post(TF_ACNE_SERVING_URL, json=payload)    
    except Exception as e:
        print(e)
        return []

    output_dict = res.json()["predictions"][0]


    classes = np.array(output_dict['detection_classes'], dtype="uint8")
    boxes = np.array(output_dict['detection_boxes'])
    scores = output_dict['detection_scores']

    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    
    detection_result = {}

    for key in LABEL_MAP.keys():
        detection_result[LABEL_MAP[key]] = []

    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
            if classes[i] in LABEL_MAP.keys():
                box = tuple(boxes[i].tolist())
                detection_result[LABEL_MAP[classes[i]]].append({
                    'box': box,
                    'score': scores[i]
                })

    return detection_result