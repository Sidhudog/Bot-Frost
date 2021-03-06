import math
import cv2
import numpy
from PIL import Image
from numpy import random
import os
import random as RAN
import time

face_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_eye.xml'))


# Pass an image to fry, pretty self explanatory
async def fry(image, emote_amount, noise, contrast):
    print('Generating gray image...')
    gray = numpy.array(image.convert('L'))

    print('Adding emotes...')
    await add_emotes(image, emote_amount)

    print('Finding eyes and characters...')
    eye_coods = await find_eyes(gray)
    char_coords = await find_chars(gray)

    print('Adding lens flare...')
    await add_flares(image, eye_coods)
    print('Adding chars...')
    await add_chars(image, char_coords)

    [w, h] = [image.width - 1, image.height - 1]
    w *= numpy.random.random(1)
    h *= numpy.random.random(1)
    r = int(((image.width + image.height) / 15) * (numpy.random.random(1)[0] + 1))

    bulge_bool = RAN.choice([True, False])
    if bulge_bool:
        print('Bulging the image...')
        image = await bulge(image, numpy.array([int(w), int(h)]), r, 3, 5, 1.8)

    print('Increasing the noise...')
    image = await add_noise(image, random.random() * noise)
    print('Changing contrast...')
    image = await change_contrast(image, random.random() * contrast)

    print('Done!')
    return image


async def find_chars(gray):
    ret, mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(gray, gray, mask=mask)
    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(new_img, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    coords = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        if w > 70 and h > 70:
            continue
        coords.append((x, y, w, h))
    return coords


async def find_eyes(gray):
    coords = []

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            coords.append((x + ex + ew / 2, y + ey + eh / 2))
    if len(coords) == 0:
        print("\tNo eyes found.")
        pass
    return coords


async def add_flares(image, coords):
    flare = Image.open(random_file('utils/images/flares/')).convert('RGBA')
    for coord in coords:
        image.paste(flare, (int(coord[0] - flare.size[0] / 2), int(coord[1] - flare.size[1] / 2)), flare)
    return image


async def add_chars(image, coords):
    char = Image.open(random_file('utils/images/chars/')).convert('RGBA')
    for coord in coords:
        if numpy.random.random(1)[0] > 0.1:
            continue
        resized = char.copy()
        resized.thumbnail((coord[2], coord[3]), Image.ANTIALIAS)
        image.paste(resized, (int(coord[0]), int(coord[1])), resized)
    return image


async def add_emotes(image, max):
    for i in range(max):
        emote = Image.open(random_file('utils/images/emotes/')).convert('RGBA')

        coord = numpy.random.random(2) * numpy.array([image.width, image.height])

        size = int((image.width / 10) * (numpy.random.random(1)[0] + 1))
        emote.thumbnail((size, size), Image.ANTIALIAS)
        image.paste(emote, (int(coord[0]), int(coord[1])), emote)


async def change_contrast(image, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        return 128 + factor * (c - 128)

    return image.point(contrast)


async def add_noise(image, factor):
    def noise(c):
        return c * (1 + numpy.random.random(1)[0] * factor - factor / 2)

    return image.point(noise)


# creates a bulge like distortion to the image
# parameters:
#   img = PIL image
#   f   = numpy.array([x, y]) coordinates of the centre of the bulge
#   r   = radius of the bulge
#   a   = flatness of the bulge, 1 = spherical, > 1 increases flatness
#   h   = height of the bulge
#   ior = index of refraction of the bulge material
async def bulge(img, f, r, a, h, ior):
    # print("Creating a bulge at ({0}, {1}) with radius {2}... ".format(f[0], f[1], r))

    # load image to numpy array
    width = img.width
    height = img.height
    img_data = numpy.array(img)

    # ignore too large images
    if width * height > 3000 * 3000:
        return img

    # determine range of pixels to be checked (square enclosing bulge), max exclusive
    x_min = int(f[0] - r)
    if x_min < 0:
        x_min = 0
    x_max = int(f[0] + r)
    if x_max > width:
        x_max = width
    y_min = int(f[1] - r)
    if y_min < 0:
        y_min = 0
    y_max = int(f[1] + r)
    if y_max > height:
        y_max = height

    # make sure that bounds are int and not numpy array
    if isinstance(x_min, type(numpy.array([]))):
        x_min = x_min[0]
    if isinstance(x_max, type(numpy.array([]))):
        x_max = x_max[0]
    if isinstance(y_min, type(numpy.array([]))):
        y_min = y_min[0]
    if isinstance(y_max, type(numpy.array([]))):
        y_max = y_max[0]

    # # array for holding bulged image
    # bulged = numpy.copy(img_data)
    # time_start = time.time()
    # for y in range(y_min, y_max):
        # for x in range(x_min, x_max):
            # ray = numpy.array([x, y])

            # # find the magnitude of displacement in the xy plane between the ray and focus
            # s = length(ray - f)

            # # if the ray is in the centre of the bulge or beyond the radius it doesn't need to be modified
            # if 0 < s < r:
                # # slope of the bulge relative to xy plane at (x, y) of the ray
                # m = -s / (a * math.sqrt(r ** 2 - s ** 2))

                # # find the angle between the ray and the normal of the bulge
                # theta = numpy.pi / 2 + numpy.arctan(1 / m)

                # # find the magnitude of the angle between xy plane and refracted ray using snell's law
                # # s >= 0 -> m <= 0 -> arctan(-1/m) > 0, but ray is below xy plane so we want a negative angle
                # # arctan(-1/m) is therefore negated
                # phi = numpy.abs(numpy.arctan(1 / m) - numpy.arcsin(numpy.sin(theta) / ior))

                # # find length the ray travels in xy plane before hitting z=0
                # k = (h + (math.sqrt(r ** 2 - s ** 2) / a)) / numpy.sin(phi)

                # # find intersection point
                # intersect = ray + (normalise(f - ray)) * k

                # # assign pixel with ray's coordinates the colour of pixel at intersection
                # if 0 < intersect[0] < width - 1 and 0 < intersect[1] < height - 1:
                    # bulged[y][x] = img_data[int(intersect[1])][int(intersect[0])]
                # else:
                    # bulged[y][x] = [0, 0, 0, 0]
            # else:
                # bulged[y][x] = img_data[y][x]
    # time_end = time.time()
    # print(f"First algorithm: {time_end - time_start}")

   
    f_new = f
    bulge_square = numpy.copy(img_data)#img_data[x_min:x_max, y_min:y_max]
    
    #following is equivalent to s = length(ray - f)
    bulge_y, bulge_x = numpy.mgrid[0:bulge_square.shape[0], 0:bulge_square.shape[1]]
    bulge_x = bulge_x - f_new[0]
    bulge_y = bulge_y - f_new[1]
    bulge_s = numpy.hypot(bulge_x, bulge_y)
    circle = ((0<bulge_s) & (bulge_s<r))
    
    #following is equivalent to m = -s / (a * math.sqrt(r ** 2 - s ** 2))
    bulge_m = numpy.copy(bulge_s)
    bulge_m[circle] = (-1 * bulge_m[circle]) / (a * numpy.sqrt(r**2 - bulge_m[circle]**2))
    
    #following is equivalent to theta = numpy.pi / 2 + numpy.arctan(1 / m)
    bulge_theta = numpy.copy(bulge_s)
    bulge_theta[circle] = (numpy.pi / 2) + numpy.arctan(1 / bulge_m[circle])
    
    #following is equivalent to phi = numpy.abs(numpy.arctan(1 / m) - numpy.arcsin(numpy.sin(theta) / ior))
    bulge_phi = numpy.copy(bulge_s)
    bulge_phi[circle] = numpy.abs(numpy.arctan(1 / bulge_m[circle]) - numpy.arcsin(numpy.sin(bulge_theta[circle]) / ior))
                                                
    #following is equivalent to k = (h + (math.sqrt(r ** 2 - s ** 2) / a)) / numpy.sin(phi)
    bulge_k = numpy.copy(bulge_s)
    bulge_k[circle] = (h + (numpy.sqrt(r**2 - bulge_s[circle]**2) / a)) / numpy.sin(bulge_phi[circle])
    
    bulge_norm_y, bulge_norm_x = numpy.mgrid[0:bulge_square.shape[0], 0:bulge_square.shape[1]].astype(numpy.float32)
    bulge_norm_x =  f_new[1] - bulge_norm_x
    bulge_norm_y =  f_new[0] - bulge_norm_y
    bulge_norm_x[circle] = (bulge_norm_x[circle] / bulge_s[circle])
    bulge_norm_y[circle] = (bulge_norm_y[circle] / bulge_s[circle])
    
    #following is equivalent to intersect = ray + (normalise(f - ray)) * k
    bulge_intersect_y, bulge_intersect_x =   numpy.mgrid[0:bulge_square.shape[0], 0:bulge_square.shape[1]].astype(numpy.float32)
    bulge_intersect_x[circle] = bulge_intersect_x[circle] + (bulge_norm_x[circle]) * bulge_k[circle]
    bulge_intersect_y[circle] = bulge_intersect_y[circle] + (bulge_norm_y[circle]) * bulge_k[circle]
    
    # if 0 < intersect[0] < width - 1 and 0 < intersect[1] < height - 1:
        # bulged[y][x] = img_data[int(intersect[1])][int(intersect[0])]
    # else:
        # bulged[y][x] = [0, 0, 0, 0]
    orig_image_square = numpy.copy(img_data)
    intersect_area = ((0 < bulge_intersect_x) & (bulge_intersect_x < orig_image_square.shape[1])) & ((0 < bulge_intersect_y) & (bulge_intersect_y < orig_image_square.shape[0]))
    bulge_square[(numpy.logical_not(intersect_area)&circle)] = [0,0,0,0]
    bulge_square = replace_values(numpy.copy(orig_image_square), numpy.copy(bulge_square), circle, intersect_area, bulge_intersect_x, bulge_intersect_y)
    bulge_square[numpy.logical_not(circle)] = orig_image_square[numpy.logical_not(circle)]
    
    bulged = numpy.copy(img_data)
    bulged = bulge_square
    
    img = Image.fromarray(bulged)
    return img

def replace_values(orig_image_square, bulge_square, circle, intersect_area, bulge_intersect_x, bulge_intersect_y):
    indices = (numpy.transpose(numpy.nonzero(intersect_area&circle)))
    
    
    img_ix = (bulge_intersect_y[[*indices.T]].astype(int), bulge_intersect_x[[*indices.T]].astype(int))
    orig_img_ix = numpy.transpose(img_ix)
    
    bulge_square[[*indices.T]] = orig_image_square[[*orig_img_ix.T]]
            
    return bulge_square

# return the length of vector v
def length(v):
    return numpy.sqrt(numpy.sum(numpy.square(v)))


# returns the unit vector in the direction of v
def normalise(v):
    return v / (length(v))


def random_file(path):
    return path + numpy.random.choice(os.listdir(path))
