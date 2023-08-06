def get_video_info(filename):
    """
    returns information about video file in a dictionary format


    Parameters
    ----------
    filename :: (string)
        full filename including root

    Returns
    -------
    video_info :: (dictionary)

    Examples
    --------
    >>> video_info = get_video_info(filename)
    """
    import cv2
    dic = {}
    vidcap = cv2.VideoCapture(filename)
    dic['filename'] = filename
    dic['width'] = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    dic['height'] = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dic['gain'] = vidcap.get(cv2.CAP_PROP_GAIN)
    dic['iso'] = vidcap.get(cv2.CAP_PROP_ISO_SPEED)
    dic['frame_count'] = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    dic['format'] = vidcap.get(cv2.CAP_PROP_FORMAT)
    dic['fps'] = round(vidcap.get(cv2.CAP_PROP_FPS),0)
    return dic

def parse_video_into_frames(filename, verbose = False):
    import cv2
    from os.path import exists,split
    from os import mkdir
    import sys
    root = split(filename)[0]
    prefix = split(filename)[1].split('.')[0]
    print('Checking if the file exist ...')
    print('File does exist:',exists(filename))
    images_root = root +'/'+prefix+'_images/'
    if not exists(images_root):
        mkdir(images_root)
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()
    count = 0
    success = True
    while success:
      success,image = vidcap.read()
      if success:
          if verbose:
              print(f'extractinf frame # {count} and saving to {images_root}')
          #cv2.imwrite(images_root+"frame%d.tiff" % count, image)     # save frame as JPEG file
          from PIL import Image
          im = Image.fromarray(image)
          im.save(images_root+f"frame{count}.tiff" , dpi = (600,600))
          if cv2.waitKey(10) == 27:                     # exit if Escape is hit
              break
          count += 1
      else:
          count += 1
