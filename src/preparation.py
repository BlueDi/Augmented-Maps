import cv2 as cv
import os
import image as img


IMAGE_FOLDER = '../resources/images'


def click_map_callback(event, x, y, flags, database):
    """
    Callback for the image
    When left click the image, print the x and y
    """
    if event == cv.EVENT_LBUTTONDOWN:
        print 'Coords:', x, y
        image_name = raw_input('Image name: ')
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        print 'Path:', image_path
        point_of_interest =	{
            image_name: {
                'path': image_path,
                'x': x,
                'y': y
            }
        }
        database.update(point_of_interest)


def click_map(database, image_base, window_name="Preparation"):
    """
    Create the callback for the image
    Display the image
    """
    map_image = img.open_image(image_base)
    cv.namedWindow(window_name)
    cv.setMouseCallback(window_name, click_map_callback, database)

    cv.imshow(window_name, map_image)

