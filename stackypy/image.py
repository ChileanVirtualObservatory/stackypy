import numpy as np

from .detect import *

from skimage.transform import rotate,resize

def center_and_extend(img,cent_x=None,cent_y=None,mask=True):
    cent_x = int(round(cent_x)) if cent_x != None else img.shape[1]//2
    cent_y = int(round(cent_y)) if cent_y != None else img.shape[0]//2
    m_left = cent_x
    m_right = img.shape[1]-cent_x-1
    m_up = cent_y
    m_down = img.shape[0]-cent_y-1
    max_margin = max(m_left,m_right,m_up,m_down)
    side = max_margin*3
    if side%2==0: side+=1
    # Create new images.
    nimg = np.zeros((side,side))
    if mask:
        nmask = np.zeros((side,side))
    # Put old image on the new one, also create the mask.
    new_x = side//2-cent_x
    new_y = side//2-cent_y
    nimg[new_y:new_y+img.shape[0],new_x:new_x+img.shape[1]] = img
    #
    if mask:
        nmask[new_y:new_y+img.shape[0],new_x:new_x+img.shape[1]] = 1
        return nimg,nmask
    else:
        return nimg

def rotate_and_scale(img,siz_x,siz_y,angle,interp_order=1):
    img = rotate(img,np.rad2deg(angle),cval=0,order=interp_order)
    img = resize(img,(siz_y,siz_x),order=interp_order,mode='constant')
    return img

def transform_to_meet(img,ma_axis,mi_axis,angle=0,interp_order=1,blur_size=2):
    (detection,_) = detect_object(img,blur_size=blur_size)
    if detection==None: return None
    (c_x,c_y,ang,ma_ax,mi_ax) = detection
    img,mask = center_and_extend(img,c_x,c_y)
    new_x = int(round(ma_axis*img.shape[1]/ma_ax))
    new_y = int(round(mi_axis*img.shape[0]/mi_ax))
    img = rotate_and_scale(img,new_x,new_y,-ang,interp_order)
    mask = rotate_and_scale(mask,new_x,new_y,-ang,interp_order)
    if angle!=0:
        img = center_and_extend(img,mask=False)
        mask = center_and_extend(mask,mask=False)
        img = rotate(img,np.rad2deg(angle),cval=0,order=interp_order)
        mask = rotate(mask,np.rad2deg(angle),cval=0,order=interp_order)
    return img,mask

def blit_add(target,source,loc_x=0,loc_y=0):
    # Find the common ranges of both the target and source.
    str_y = max(0,loc_y)
    str_x = max(0,loc_x)
    end_y = min(target.shape[0],loc_y+source.shape[0])
    end_x = min(target.shape[1],loc_x+source.shape[1])
    str_y_2 = max(0,-loc_y)
    str_x_2 = max(0,-loc_x)
    end_y_2 = str_y_2+end_y-str_y
    end_x_2 = str_x_2+end_x-str_x
    # Create final source image of the same size than the target and has it on the right position but also the neutral element value outside.
    final_source = np.zeros(target.shape)
    final_source[str_y:end_y,str_x:end_x] = \
        source[str_y_2:end_y_2,str_x_2:end_x_2]
    # Apply the operation
    target = target+final_source
    return target

def stack_to_template(images,interp_order=1,blur_size=2):
    """
    Detects the central objects on a series of images, then scales and rotates these images so that all the central objects detected overlap on the same position as the one in images[0]. Images are then averaged together to create a final one.

    Objects are detected with the detect_object function.

    Args:
        images : list of numpy.ndarray's
            List of astronomical data cubes
        interp_order : int
            Order of interpolation used when rotating and scaling the images.
        blur_size: int
            Magnitude of the gaussian blur passed to the detect_object function.

    Returns:
        properties : tuple or None
            Tuple with properties of the object found at the center of the image (*centroid_x*,*centroid_y*,*angle*,*major_ratio*,*minor_ratio*).
            None when no object was found at the center.
        detection_mask: numpy.ndarray
            Image labeled with the detected objects, may be used for debug.
    """
    template = images[0].copy()
    (detection,_) = detect_object(images[0],blur_size=blur_size)
    if detection==None:
        raise ValueError("Object could not be detected at the center of template!")
    #
    (c_x,c_y,ang,ma_ax,mi_ax) = detection
    ponderation = np.ones(template.shape)
    used_images = [0]
    for i in range(1,len(images)):
        result = transform_to_meet(images[i],ma_ax,mi_ax,ang,interp_order,blur_size)
        if result==None:
            warnings.warn("Failed to detect central object on image, ignoring.")
            continue
        used_images.append(i)
        # Get the image and the mask and blit_add it to the template
        img,mask = result
        blit_x = int(round(c_x-img.shape[1]/2))
        blit_y = int(round(c_y-img.shape[0]/2))
        template = blit_add(template,img,blit_x,blit_y)
        ponderation = blit_add(ponderation,mask,blit_x,blit_y)
    # Divide the template by the ponderation to calculate the means
    template = (template+ponderation//2)//ponderation
    return template,used_images
