import numpy as np
import cv2
import os, uuid

def deteksi_bintik_hitam(app, image_processor, image):
    # extract color channel
    blue, green, red = [image[:,:,0],image[:,:,1],image[:,:,2]]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:,:,0];

    # convert hue to 0-1 range from 1-180 range
    hue = hue / 180.0

    # extract to gray
    image_gray = image_processor.convert_bgr_to_gray(image)

    # image size
    height, width = image.shape[0:2]

    # morphological closing
    kernel = image_processor.create_kernel(10)
    image_closing = image_processor.morphology_closing(image_gray, kernel)

    # hasus convert ke tipe data integer dahulu untuk menghindari 
    # reverse negative number tipe data uint8
    image_closing = image_closing.astype(np.int16)
    image_gray_closing = image_closing - image_gray
    image_gray_closing[image_gray_closing < 0] = 0
    image_gray_closing = image_gray_closing.astype(np.uint8)

    # gray thresholding
    image_binnary = image_processor.convert_gray_to_otsu_binnary(image_gray_closing)

    # menghitung area setiap contour ~ regionprops.Area
    contours, hierarchy = cv2.findContours(image_binnary.copy(), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    contours_area = np.array([cv2.contourArea(cnt) for cnt in contours])

    # mencari rata2 dan std dari area contour
    contours_area_mean = np.mean(contours_area)
    contours_area_std = np.std(contours_area)

    # filter nilai contours area
    condition_1 = contours_area <= (contours_area_mean + contours_area_std)
    condition_2 = contours_area >= (image.shape[0] * image.shape[1] * 0.00005)

    contours_valid = []
    for i, val in enumerate(np.bitwise_and(condition_1, condition_2)):
        if val == True:
            contours_valid.append(contours[i])

    mask = np.zeros_like(blue)
    for cnt in contours_valid:
        cv2.drawContours(mask, [cnt], 0, 255, -1)

    # mencari nilai mean intencity, max intecity, min intencity
    contours_green_mean = []
    contours_red_mean = []
    contours_blue_mean = []
    contours_hue_mean = []

    for cnt in contours_valid:
        mask = np.zeros(blue.shape, np.uint8)
        cv2.drawContours(mask, [cnt], 0, 255, -1)
        contours_green_mean.append(np.mean(green[mask == 255]))
        contours_red_mean.append(np.mean(red[mask == 255]))
        contours_blue_mean.append(np.mean(blue[mask == 255]))
        contours_hue_mean.append(np.mean(hue[mask == 255]))


    cnt_green_mean = np.mean(np.array(contours_green_mean))
    # cnt_red_mean = np.mean(np.array(contours_red_mean))
    # cnt_blue_mean = np.mean(np.array(contours_blue_mean))
    cnt_hue_mean = np.mean(np.array(contours_hue_mean))

    cnt_green_std = np.std(contours_green_mean)
    # cnt_red_std = np.std(contours_red_mean)
    # cnt_hue_std = np.std(contours_hue_mean)

    # filter contour berdasarkan nilai intensitas warna
    color_condition_1 = np.array(contours_green_mean) > (cnt_green_mean - cnt_green_std)
    color_condition_2 = np.array(contours_hue_mean) < cnt_hue_mean

    contours_valid_2 = []
    normalisasi = {
        'bintik_hitam': []
    }
    index = 0;
    for i, val in enumerate(np.bitwise_and(color_condition_1, color_condition_2)):
        if val == True:
            contours_valid_2.append(contours_valid[i])
            x,y,w,h = cv2.boundingRect(contours_valid[i])
            norm = {
                'xmin': x / width,
                'ymin': y / height,
                'ymax': (y + h) / height,
                'xmax': (x + w) / width,
                'score': 100.0
            } 
            normalisasi['bintik_hitam'].append(norm)
            index += 1

    # pemberian tada pada gambar
    image_result = image.copy()
    cv2.drawContours(image_result, contours_valid_2 , -1, (255,0,0), 1)

    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid4().hex + '.jpeg'), image_result)

    return normalisasi


    