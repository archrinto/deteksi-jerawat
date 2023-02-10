import numpy as np
import cv2
import os, uuid

def deteksi_kemerahan(save_folder, image_processor, image):
    image_blur = cv2.GaussianBlur(image,(3,3), 1)
    
    # convert to HSV
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_BGR2HSV).astype(np.float32)
    # convert value to matlab range
    image_hsv[:,:,0] = image_hsv[:,:,0] / 180.0
    image_hsv[:,:,1] = image_hsv[:,:,1] / 255.0
    image_hsv[:,:,2] = image_hsv[:,:,2] / 255.0
    # split to H, S, V
    hue, sat, val = cv2.split(image_hsv)

    num_rows, num_cols = image_hsv.shape[0], image_hsv.shape[1]
    # penggabungan h and s
    hs = np.zeros((num_rows, num_cols, 2), np.float32)
    hs[:,:,0], hs[:,:,1] = hue, sat
    # reshape to n x 2
    hs_reshaped = np.reshape(hs, (num_cols * num_rows, 2), 'F')

    # kmeans clustering 
    num_cluster = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, (centers) = cv2.kmeans(hs_reshaped, num_cluster, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    # mengubah bentuk label ke lokasi pixel gambar
    pixel_labels = np.reshape(labels, (num_rows, num_cols), 'F')
    # menghitung jumlah pixel setiap label
    _, labels_count = np.unique(labels, return_counts=True)
    # cluster terbesar 
    biggest_cluster = np.argmax(labels_count)

    segmented = [np.zeros_like(image), np.zeros_like(image), np.zeros_like(image)]
    segmented[0][pixel_labels == 0] = image[pixel_labels == 0]
    segmented[1][pixel_labels == 1] = image[pixel_labels == 1]
    segmented[2][pixel_labels == 2] = image[pixel_labels == 2]

    # segmented gray
    image_gray = image_processor.convert_bgr_to_gray(segmented[biggest_cluster])

    # thresholding
    image_binnary = image_processor.convert_gray_to_otsu_binnary(image_gray)

    # mengisi lubang pada gambar, seperti imfill pada matlab
    image_binnary_filled = image_processor.imfill(image_binnary)

    # mengambil nilai RGB
    image_segmented = np.zeros_like(image)
    image_segmented[image_binnary_filled > 0] = image[image_binnary_filled > 0].copy()

    blue, green, red = image_segmented[:,:,0].astype(np.float32) / 255.0, image_segmented[:,:,1].astype(np.float32) / 255.0, image_segmented[:,:,2].astype(np.float32) / 255.0

    # menghitung redness   
    redness = np.zeros((num_rows, num_cols), np.float32)
    for i in range(num_rows):
        for j in range(num_cols):
            if red[i, j] > 0:
                redness[i,j] = max(0.0 ,((2.0 * red[i, j]) - (green[i, j] + blue[i, j])) / red[i, j]) ** 2.0

    # seleksi bagian wajah yang lebih dari threshold dikategorikan kemerahan
    # kalau dilihat nilainya sama persis seperti di matlab
    redness_median = np.median(redness, axis=0)

    image_redness = np.zeros_like(image)
    redness_binnary = np.zeros((num_rows, num_cols), np.uint8)
    image_redness = image_segmented.copy()
    for i in range(num_rows):
        for j in range(num_cols):
            if np.all(redness[i, j] > redness_median):
                image_redness[i, j, :] = [0, 0, 255];
                redness_binnary[i, j] = 255

    # # filter gray
    image_redness_gray = cv2.cvtColor(image_redness, cv2.COLOR_BGR2GRAY)
    image_redness_gray = cv2.GaussianBlur(image_redness_gray, ksize=(0, 0), sigmaX=0.4)
    # # image_redness_gray = cv2.GaussianBlur(image_redness_gray,(3,3), 0.5)
    redness_binnary_2 = np.zeros((num_rows, num_cols), np.uint8)
    redness_binnary_2[image_redness_gray == 76] = 255

    redness_binnary_eliminated = np.zeros_like(redness_binnary_2)
    redness_binnary_eliminated[redness < 1] = redness_binnary_2[redness < 1]

    contours, _ = cv2.findContours(redness_binnary_eliminated, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    contours_area = np.array([cv2.contourArea(cnt) for cnt in contours])

    print('--- kemerahan: jumlah contour1', len(contours))

    # eliminasi berdasarkan area
    condition_1 = contours_area >= 91

    contours_valid = []
    for i, val in enumerate(condition_1):
        if val == True:
            contours_valid.append(contours[i])

    print('--- kemerahan: valid contour1', len(contours_valid))

    # menampilkan contour pada gambar
    mask = np.zeros_like(redness_binnary)
    for cnt in contours_valid:
        cv2.drawContours(mask, [cnt], 0, 255, -1)

    image_contours = np.zeros_like(image)
    image_contours[mask == 255] = image[mask == 255]

    blue, green, red = cv2.split(image)

    image_hsv_elm = cv2.cvtColor(image_contours, cv2.COLOR_BGR2HSV)

    hue, sat, val = cv2.split(image_hsv_elm)
    hue = hue / 180.0

    # eliminasi berdasarkan warna RGB
    contours_green_mean = []
    contours_red_mean = []
    contours_blue_mean = []
    contours_hue_mean = []

    contours_valid_2 = []

    if len(contours_valid) > 0:
        for cnt in contours_valid:
            mask = np.zeros(blue.shape, np.uint8)
            cv2.drawContours(mask, [cnt], 0, 255, -1)
            contours_green_mean.append(np.mean(green[mask == 255]))
            contours_red_mean.append(np.mean(red[mask == 255]))
            contours_blue_mean.append(np.mean(blue[mask == 255]))
            contours_hue_mean.append(np.mean(hue[mask == 255]))

        cnt_green_mean = np.mean(np.array(contours_green_mean))
        cnt_red_mean = np.mean(np.array(contours_red_mean))
        cnt_blue_mean = np.mean(np.array(contours_blue_mean))
        cnt_hue_mean = np.mean(np.array(contours_hue_mean))

        cnt_green_std = np.std(contours_green_mean)
        cnt_red_std = np.std(contours_red_mean)
        cnt_blue_std = np.std(contours_blue_mean)
        cnt_hue_std = np.std(contours_hue_mean)

        color_cond_1 = np.bitwise_and(contours_red_mean >= (cnt_red_mean - cnt_red_std * 1.32),
                                    contours_red_mean <= (cnt_red_mean + cnt_red_std * 1.1))

        color_cond_2 = np.bitwise_and(contours_green_mean >= (cnt_green_mean - cnt_green_std * 1.32),
                                    contours_green_mean <= (cnt_green_mean + cnt_green_std * 1.32))

        color_cond_3 = np.bitwise_and(contours_blue_mean >= (cnt_blue_mean - cnt_blue_std * 1.32),
                                    contours_blue_mean <= (cnt_blue_mean + cnt_blue_std * 1.32))

        color_cond_4 = np.bitwise_and(contours_hue_mean >= (cnt_hue_mean - cnt_hue_std * 1.6),
                                    contours_hue_mean <= (cnt_hue_mean + cnt_hue_std * 0.005))

        color_cond_5 = np.bitwise_and(contours_hue_mean >= (cnt_hue_mean - cnt_hue_std * 0.2),
                                    contours_hue_mean <= (cnt_hue_mean + cnt_hue_std * 2.5))

        cond_12 = np.bitwise_and(color_cond_1, color_cond_2)
        cond_123 = np.bitwise_and(cond_12, color_cond_3)
        cond_1234 = np.bitwise_and(cond_123, color_cond_4)
        cond_12345 = np.bitwise_and(cond_1234, color_cond_5)

        print('--- kemerahan hue mean', contours_hue_mean)

        for i, val in enumerate(cond_1234):
            if val == True:
                contours_valid_2.append(contours_valid[i])

        print('--- kemerahan: valid contour2', len(contours_valid_2))

    normalisasi = {
        'kemerahan': []
    }

    # image size
    height, width = image.shape[0:2]

    # menampilkan contour pada gambar
    mask = np.zeros_like(redness_binnary)
    for cnt in contours_valid_2:
        cv2.drawContours(mask, [cnt], 0, 255, -1)
        # normalisasi koordinat
        x,y,w,h = cv2.boundingRect(cnt)
        points = np.reshape(cnt, (len(cnt), 2))
        points = points.astype(float)
        points[:,0] = points[:,0] / width
        points[:,1] = points[:,1] / height
        points = points.tolist()
        norm = {
            'xmin': x / width,
            'ymin': y / height,
            'ymax': (y + h) / height,
            'xmax': (x + w) / width,
            'points': points,
            'score': 100.0
        } 
        normalisasi['kemerahan'].append(norm)

    # pemberian tada pada gambar
    image_result = image.copy()
    cv2.drawContours(image_result, contours_valid_2 , -1, (255,0,0), 1)

    cv2.imwrite(os.path.join(save_folder, uuid.uuid4().hex + '.jpeg'), image_result)

    return normalisasi

if __name__ == '__main__':
    import image_processor

    image = cv2.imread('kemerahan.jpg')

    hasil = deteksi_kemerahan('./', image_processor, image)

    print(hasil)
