from skimage.filter import threshold_otsu,gaussian
from skimage.segmentation import clear_border
from skimage.measure import label,regionprops

def get_detection(img,blur_size=2):
    # Apply otsu filtering to the image:
    img = gaussian(img,blur_size)
    flt = threshold_otsu(img)
    otsu = img >= flt
    if not otsu[otsu.shape[0]//2,otsu.shape[1]//2]: return None
    #
    # Label regions:
    label_image,nlabel = label(otsu,return_num=True)
    #
    # Find the label at the center, clear regions with other labels.
    center_label = label_image[label_image.shape[0]//2,label_image.shape[1]//2]
    label_image[label_image!=center_label] = -1
    label_image[label_image==center_label] = 1
    return label_image


def detect_object(img,blur_size=2):
    """
    Extracts information of the object detected at the center of the image.

    Objects are detected applying a threshold, the one at the center is picked, approximating it as a (possibily rotated) ellipse.

    Args:
        img : numpy.ndarray
            Astronomical data cube.
        blur_size: int
            Size of the gaussian filter applied to the image to detect the objects.

    Returns:
        properties : tuple or None
            Tuple with properties of the object found at the center of the image (*centroid_x*,*centroid_y*,*angle*,*major_ratio*,*minor_ratio*).
            None when no object was found at the center.
        detection_mask:
            Image labeled with the detected objects, may be used for debug.
    """
    label_image = get_detection(img,blur_size)
    if label_image is None: return (None,label_image)
    #
    # Find the properties of the center region:
    props = regionprops(label_image)
    cent_x = props[0].centroid[1]
    cent_y = props[0].centroid[0]
    angle = props[0].orientation
    ma_axis = props[0].major_axis_length
    mi_axis = props[0].minor_axis_length

    return ((cent_x,cent_y,angle,ma_axis,mi_axis),label_image)
