import numpy as np
import cv2


def scale_to_max_size(image, max_size):
  h, w, c = image.shape

  scale = max_size / h if h > w else max_size / w

  height = int(h * scale)
  width = int(w * scale)
  
  return cv2.resize(image, (height, width))


def convert_bgr_to_rgb_color(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def convert_bgr_to_gray(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def get_image_size(image):
  height = image.shape[0]
  width = image.shape[1]

  return height, width


def convert_gray_to_otsu_binnary(image):
  # ref: https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html

  thresh = cv2.threshold(image.copy(), 0, 255, cv2.THRESH_OTSU)[1]
  
  return thresh


def fill_hole_binnary(image):
  # ref: https://learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/

  image_cp = image.copy()
  h, w = image.shape[:2]
  mask = np.zeros((h+2, w+2), np.uint8)
  # Floodfill from point (0, 0)
  cv2.floodFill(image_cp, mask, (0,0), 255);
  # Invert floodfilled image
  image_flood_fill_inv = cv2.bitwise_not(image_cp)

  return image | image_flood_fill_inv


def connected_component_labeling(image):
  # ref https://pyimagesearch.com/2021/02/22/opencv-connected-component-labeling-and-analysis/
  
  connectivity = 4
  output = cv2.connectedComponentsWithStats(image, connectivity, cv2.CV_32S)
  numLabels, labels, stats, centroids = output
  
  return numLabels, labels, stats, centroids


def extract_bgr_color(image):
  blue = image[:,:,0]
  green = image[:,:,1]
  red = image[:,:,2]

  return blue, green, red

def create_kernel(radius):
  return np.ones((radius, radius),np.uint8)


def morphology_closing(image, kernel):
  return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


def read_image(path):
  return cv2.imread(path)


def show_image(title, image):
  cv2.imshow(title, image)
  cv2.waitKey(0)









