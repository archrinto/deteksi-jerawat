import numpy as np
import cv2
import image_processor

def deteksi_keriput(image):
    # convert to HSV
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    # convert value to matlab range
    image_hsv[:,:,0] = image_hsv[:,:,0] / 180.0
    image_hsv[:,:,1] = image_hsv[:,:,1] / 255.0
    image_hsv[:,:,2] = image_hsv[:,:,2] / 255.0
    # split to H, S, V
    hue, sat, val = cv2.split(image_hsv)

    num_rows, num_cols = image_hsv.shape[0], image_hsv.shape[1]
    # penggabungkan h and s
    hs = np.zeros((num_rows, num_cols, 2), np.float32)
    hs[:,:,0], hs[:,:,1] = hue, sat
    # reshape to n x 2
    hs_reshaped = np.reshape(hs, (num_cols * num_rows, 2), 'F')

    # kmeans clustering 
    num_cluster = 2
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

    gray_segmented = np.zeros_like(image)
    gray_segmented[image_binnary_filled > 0] = image[image_binnary_filled > 0]
    gray_segmented = cv2.cvtColor(gray_segmented, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(gray_segmented, cv2.CV_32F)
    # abs
    laplacian = cv2.convertScaleAbs(laplacian)

    gray_segmented_elim = (gray_segmented)-(laplacian)

    # mengambil area keriput
    num_row, num_col = image_gray.shape[:2]

    areas = [
        # dahi
        [
            [round(num_row * 20/100), round(num_row * 30/100)],
            [round(num_col * 25/100), round(num_col * 80/100)]
        ],
        # tengah mata
        [
            [round(num_row * 34/100), round(num_row * 43/100)],
            [round(num_col * 44/100), round(num_col * 55/100)]
        ],
        # mata kiri
        [
            [round(num_row * 38/100), round(num_row * 44/100)],
            [round(num_col * 15/100), round(num_col * 25/100)]
        ],
        # mata kanan
        [
            [round(num_row * 38/100), round(num_row * 44/100)],
            [round(num_col * 75/100), round(num_col * 85/100)]
        ],
        # kantung mata kiri
        [
            [round(num_row * 44.5/100), round(num_row * 55/100)],
            [round(num_col * 20/100), round(num_col * 43/100)],
        ],
        # kantung mata kanan
        [
            [round(num_row * 44.5/100), round(num_row * 55/100)],
            [round(num_col * 55/100), round(num_col * 80/100)]
        ],
    ]

    # menampilkan area deteksi keriput
    image_area_deteksi = [np.zeros_like(image_gray) for i in areas];
    for i, area in enumerate(areas):
        r1, r2 = area[0]
        c1, c2 = area[1]

    image_area_deteksi[i][r1:r2, c1:c2] = gray_segmented[r1:r2, c1:c2]

    # deteksi canny edge
    image_gray_edge = cv2.Canny(cv2.GaussianBlur(gray_segmented,(5,5),0), 55, 18)
    # sobelx = cv2.Sobel(src=gray_segmented, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=cv2.GaussianBlur(gray_segmented,(3,3),1), ddepth=-1, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    # sobelxy = cv2.Sobel(src=gray_segmented, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

    sobely[sobely < 150] = 0

    contours, hierarchy = cv2.findContours(sobely.copy(), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    contours_area = np.array([cv2.contourArea(cnt) for cnt in contours])

    contours_valid = []
    for i, val in enumerate(np.bitwise_and(contours_area > 30, contours_area < 400)):
        if val == True:
            contours_valid.append(contours[i])

    sobelyarea = np.zeros_like(image_gray)
    for cnt in contours_valid:
        cv2.drawContours(sobelyarea, [cnt], 0, 255, -1)

    # seleksi contour di dalam area
    mask = np.zeros_like(image_gray_edge)
    for i, area in enumerate(areas):
        r1, r2 = area[0]
        c1, c2 = area[1]

        mask[r1:r2, c1:c2] = sobelyarea[r1:r2, c1:c2]

    image_hasil = image.copy()
    normalisasi = {
        'keriput': []
    }
    contours_hasil, _ = cv2.findContours(mask.copy(), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    height, width = image.shape[0:2]

    for cnt in contours_hasil:
        cv2.drawContours(image_hasil, [cnt], 0, 100, -1)
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

        normalisasi['keriput'].append(norm)

    cv2.imwrite('hasil_keriput.jpg', image_hasil)
    # cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid4().hex + '.jpeg'), image_hasil)

    return normalisasi


if __name__ == '__main__': 
    image = cv2.imread('keriput.png')
    hasil = deteksi_keriput(image)
    print(hasil)