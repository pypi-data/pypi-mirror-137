import boto3
import cv2
import numpy as np
import matplotlib.image as mpimg
import os
from shapely.geometry import Polygon, box
from tqdm import trange, tqdm_notebook
from incluiasrc.utils.request_functions import *

s3_client = boto3.client('s3')


def find_closest_image(x=None, y=None,
                       album=None, verbose=True):
    """
    Finding closest image index to a given coordinate point.
    ----------
    Parameters
        x : float. Longitude of the point of interest.
        y : float. Latitude of the point of interest.
        album: geopandas dataframe. Country album.
    """

    img_index = None
    # epsilon distance to avoid numeric errors.
    epsilon = 10e-6

    x_img_min = np.abs(x - album['centroid_lon'])
    x_img_argmin = list(np.where(np.abs(x_img_min - x_img_min.min()) < epsilon)[0])

    y_img_min = np.abs(y - album['centroid_lat'])
    y_img_argmin = list(np.where(np.abs(y_img_min - y_img_min.min()) < epsilon)[0])

    # index of the image with closest centroid to the point of interest
    img_index_list = list(set(x_img_argmin) & set(y_img_argmin))
    if len(img_index_list) > 0:
        img_index = img_index_list[0]
    else:
        if verbose:
            print('Input coordinates (' + str(x) + ', ' + str(y) + ') out of imagery extraction bounds.')
        else:
            pass
    return img_index


def find_consecutive(horizontal=None,
                     album=None, x_batch_dim=None, y_batch_dim=None):
    """
    Finds a batch and cell row (col) that contains a full range of consecutive horizontal (vertical) images.
    This is an auxiliary function to calculate the pixel intersection across images and to make it a constant.
    ----------
    Parameters
        horizontal: Boolean. If True finds intersection strip. If False, finds vertical strip.
        album: geopandas dataframe. Country album.
    """

    # Find all full strips
    if horizontal:
        cell_idx = 'cell_y'
        cell_col = 'cell_x'
        batch_dim = x_batch_dim
    else:
        cell_idx = 'cell_x'
        cell_col = 'cell_y'
        batch_dim = y_batch_dim

    column_list = ['batch_label', 'cell_x', 'cell_y']
    counts_df = album[column_list].groupby(['batch_label', cell_idx], axis=0).count()
    full_strip = counts_df.loc[counts_df[cell_col] == batch_dim].copy()

    if full_strip.shape[0] == 0:
        raise Exception('There is not a single full strip, wrong shape file')

    full_strip.reset_index(['batch_label', cell_idx], inplace=True)
    full_strip.drop(cell_col, axis=1, inplace=True)

    # Two consecutive Full strips
    i = 0
    j = i + 1
    cond1 = full_strip['batch_label'].iloc[i] == full_strip['batch_label'].iloc[j]
    cond2 = full_strip[cell_idx].iloc[i] + 1 == full_strip[cell_idx].iloc[j]
    while j < full_strip.shape[0] and not (cond1 and cond2):
        i += 1
        j += 1
        cond1 = full_strip['batch_label'].iloc[i] == full_strip['batch_label'].iloc[j]
        cond2 = full_strip[cell_idx].iloc[i] + 1 == full_strip[cell_idx].iloc[j]

    batch_label, cell = full_strip.iloc[i]
    cond1 = album['batch_label'] == batch_label
    cond2 = album[cell_idx].isin([cell])

    index_list1 = album.loc[cond1 & cond2].index
    cond2 = album[cell_idx].isin([cell + 1])
    index_list2 = album.loc[cond1 & cond2].index
    return index_list1, index_list2


def find_pixel_intersection(horizontal=None, album=None,
                            bucket=None,
                            x_batch_dim=None,
                            y_batch_dim=None):
    """
    Find the number of horizontal or vertical pixels that share intersection across images.
    ----------
    Parameters
        horizontal: Boolean. If True finds horizontal intersection strip. If False, finds vertical intersection strip.
        album: geopandas dataframe. Country album.
        bucket: str. Bucket name in AWS
    """
    # Local path for storing outputs.

    local_filepath = '../data/01_raw_images/test/img_iter.png'

    max_range = 20  # the maximum width of pixels in which the image intersection can be
    index_list1, index_list2 = find_consecutive(horizontal,
                                                album=album, x_batch_dim=x_batch_dim, y_batch_dim=y_batch_dim)
    idx_range = range(max_range - 1)

    img1, img2 = None, None
    for i in range(len(index_list1)):
        s3_filepath1, s3_filepath2 = album.loc[index_list1[i]]['path'], album.loc[index_list2[i]]['path']
        s3_client.download_file(bucket, s3_filepath1, local_filepath)
        img1_iter = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
        s3_client.download_file(bucket, s3_filepath2, local_filepath)
        img2_iter = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
        if i > 0:
            if horizontal:
                img1 = cv2.hconcat([img1, img1_iter])
                img2 = cv2.hconcat([img2, img2_iter])
            else:
                img1 = cv2.vconcat([img1_iter, img1])
                img2 = cv2.vconcat([img2_iter, img2])
        else:
            img1 = img1_iter
            img2 = img2_iter

    if horizontal:
        img1 = img1[:1, :, :]
        idx_iter = list(-np.array(range(20)))
        idx_iter[0] = None
        idx_min = np.argmin([np.sum((img1 - img2[idx_iter[i + 1]:idx_iter[i], :, :]) ** 2) for i in idx_range])
        pixel_min = idx_iter[idx_min + 1]
    else:  # vertical
        img1 = img1[:, -1:, :]
        idx_iter = range(max_range)
        idx_min = np.argmin([np.sum((img1 - img2[:, idx_iter[i]:idx_iter[i + 1], :]) ** 2) for i in idx_range])
        pixel_min = idx_iter[idx_min]

    return pixel_min


def batch_generator(batch_label=None,
                    generate_batch=True,
                    verbose=False,
                    album=None,
                    bucket=None,
                    pixel_size_y=None,
                    pixel_size_x=None,
                    x_batch_dim=None,
                    y_batch_dim=None,
                    pixels_intersect_h=None,
                    pixels_intersect_v=None,
                    lat_difference=None,
                    lon_difference=None):
    """
    Generate a large mosaic of images that correspond to a batch in the album.
    ----------
    Parameters
        batch_label: str. The batch label for which the mosaic is generated.
        album: geopandas dataframe. Country album.
        bucket: str. Bucket name in AWS.
    """
    # Local path for storing outputs.
    local_filepath = '../data/01_raw_images/test/img_iter.png'

    album_batch = album[album['batch_label'] == batch_label].copy()

    if album_batch.shape[0] == 0:
        raise Exception('Invalid batch_label or batch_label with zero images')

    ###################################################################
    # Wld file for georeferencing batch. USE EPSG:4326
    album_it = album_batch.iloc[0]
    album_it_lon = float(album_it['centroid_lon'] - album_it['cell_x'] * lon_difference)
    album_it_lat = float(album_it['centroid_lat'] + ((y_batch_dim - 1) - album_it['cell_y']) * lat_difference)

    wld = np.zeros(6)
    wld[0] = pixel_size_x
    wld[3] = -pixel_size_y
    wld[4] = album_it_lon - pixel_size_x * 400 / 2
    wld[5] = album_it_lat + pixel_size_y * 400 / 2  # It is not 375! It is 200 pixels above centroid.

    if not generate_batch:
        return None, wld

    # To create a mosaic img, we will generate horizontal strips of images and we will concatentate each strip img_h .
    # The outer for is to concatenate horizontal image strips img_h into img.
    img = np.array([])  # OUTPUT: tensor that defines the image

    for cell_y in trange(y_batch_dim, desc='Iterative Progress'):
        img_h = np.array([])
        # The inner for is to concatenate vertical single images into a horizontal strip img_h
        for cell_x in range(x_batch_dim):
            # set image label for the iteration
            cell_x_label = '{:02d}'.format(cell_x)
            cell_y_label = '{:02d}'.format(cell_y)
            img_iter_path = cell_x_label + '_' + cell_y_label + '.png'
            s3_filedir = '01_raw_images/'
            s3_filepath = s3_filedir + batch_label + '/' + img_iter_path

            # check if the image is currently saved in S3
            if check_key(bucket, s3_filepath):
                # if the image exists, download it to locally to local_img_path and the read it.
                s3_client.download_file(bucket, s3_filepath, local_filepath)
                img_iter = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
            else:
                # if the image does not exist, define a blank picture in its place.
                img_iter = np.ones((375, 400, 4)).astype(np.uint8)

            # In the first iteration of the inner for, img_h is empty. Therefore Else applies and the image is copied.
            # For the following iterations an image is concatenated.
            if cell_x > 0:
                strip1 = img_h[:, -1:, 0:3].astype(int)
                strip2 = img_iter[:, pixels_intersect_v:(pixels_intersect_v + 1), 0:3].astype(int)
                union_error = np.sum(np.abs(strip1 - strip2))
                if union_error > 10000 and verbose:
                    print(s3_filepath)
                img_h = cv2.hconcat([img_h, img_iter[:, (pixels_intersect_v + 1):, :]])

            else:
                img_h = img_iter

        # Analogous routine for the joining horizontal straps.
        if cell_y > 0:
            # If there is non-empty intersection, eat a strip of pixels
            if pixels_intersect_h != 0:
                img = cv2.vconcat([img_h[:pixels_intersect_h, :, :], img])
            # Otherwise, concatenate images directly.
            else:
                img = cv2.vconcat([img_h, img])
        else:
            img = img_h

    return img, wld


def load_batch(batch_label=None, batch_dict=None, bucket=None):
    """
    Adds the batch `batch_label` into the dictionary `batch_dict` which contains the session's loaded batches.
    The batch is loaded from AWS.
    ----------
    Parameters
        batch_label : str. Batch label to load into dictionary.
        batch_dict : dict of matroids: Dictionary which contains batches and batch label as keys.
        bucket: str. Bucket name in AWS.
    """
    if batch_label not in batch_dict.keys():
        local_filepath = '../data/04_batches/' + batch_label + '.png'
        if not os.path.exists(local_filepath):
            s3_filedir = '04_batches/'
            s3_filepath = s3_filedir + batch_label + '.png'
            try:
                s3_client.download_file(bucket, s3_filepath, local_filepath)
                img = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
                batch_dict[batch_label] = img
            except:
                batch_label_zero = list(batch_dict.keys())[0]
                batch_shape = batch_dict[batch_label_zero].shape
                batch_dict[batch_label] = np.ones(batch_shape, dtype=np.uint8)
    return batch_dict


def initialize_batch(batch_list):
    """
        Initializes batch with current batches in local data folder.
        ----------
        Parameters
            batch_list: list str. All labels of batches in a list.
        """
    batch_dict = {}

    for batch_label in batch_list:
        local_filepath = '../data/04_batches/' + batch_label + '.png'
        batch_stored = os.path.exists(local_filepath)
        if batch_stored:
            img = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
            batch_dict[batch_label] = img

    return batch_dict


def mosaic_around_point(x=None, y=None, size=None, batch_dict=None,
                        album=None,
                        bucket=None,
                        lat_difference=None,
                        lon_difference=None,
                        pixel_size_y=None,
                        pixel_size_x=None,
                        y_batch_dim=None,
                        pixels_intersect_h=None,
                        pixels_intersect_v=None,
                        verbose=True
                        ):
    """
    Generates a mosaic around a point using batches. A batch is a large mosaic previously stored in S3.
    ----------
    Parameters
        x : float. Longitude of the point of interest.
        y : float. Latitude of the point of interest.
        size: int. Number of pixels of square's side output.
        batch_dict: dictionary of matrices. Initially, in the jupyter-notebook, batch_dict is initialized as
        batch_dict={}. Then on each mosaic_around_point iteration, the dictionary, which is sent back as an output,
        adds if necessary the batches that were necessary for producing the mosaic from that iteration. Since the whole
        city imagery is to memory expensive, the dictionary stores only a number of batches that the machine can store
        in RAM. Therefore, to generate mosaics fast, it is highly recommended that when using it iteratively for a list
        of coordinates, the coordinates are ordered.
        album: geopandas dataframe. Country album.
        lon_difference: float. Longitude difference between two album images centroids.
        lat_difference: float. Latitude difference between two album images centroids.
        y_batch_dim: Number of images within a batch in y-axis.
        verbose: boolean. Prints verbose
    """

    img_out = None
    wld = None
    max_batches = 10  # Maximum number of batches dict can store, each batch uses around 120Mb.

    # Starts by identifying the image id which is closest to the coordinate x,y input.
    img_index = find_closest_image(x, y, album=album, verbose=verbose)
    if img_index is None:
        return img_out, wld, batch_dict

    # Loads the image features that are necessary for this routine using its id.
    img_cols = ['batch_label', 'batch_x', 'batch_y', 'cell_x', 'cell_y', 'centroid_lon', 'centroid_lat']
    batch_label, batch_x, batch_y, cell_x, cell_y, centroid_lon, centroid_lat = album.loc[img_index][img_cols]
    # Particularly, it loads the batch where the image is and gets loaded in the variable img_batch.
    batch_dict = load_batch(batch_label, batch_dict, bucket=bucket)
    img_batch = batch_dict[batch_label]

    # We wish to calculate the pixel of the image that corresponds to the centroid x,y.
    # First, we calculate the offset of centroid of the image it falls in with respect x,y.
    image_xmove = (x - centroid_lon) / lon_difference  # -0.5 < image_xmove < 0.5
    image_ymove = (y - centroid_lat) / lat_difference  # -0.5 < image_ymove < 0.5

    # To calculate the pixel we start in the centroid of the first image (400/2) and the add the number of pixels
    # a single picture represents using cell_x *  (400 - pixels_intersect_v - 1), where cell_x is an integer.
    # Then image_xmove offsets at least -0.5 and at most 0.5. As an example 3.75 is attained as 4 - 0.25 instead of
    # 3 + 0.75. The centroid pixels are stored in image_centroid_pixel_[x,y].
    image_xmove_aux = 400 / 2 + (cell_x + image_xmove) * (400 - pixels_intersect_v - 1)
    image_centroid_pixel_x = int(round(image_xmove_aux))
    image_ymove_aux = 375 / 2 + (((y_batch_dim - 1) - cell_y) - image_ymove) * (375 + pixels_intersect_h)
    image_centroid_pixel_y = int(round(image_ymove_aux))

    # Then we simply crop the batch image according to the number of desired pixels.
    if size % 2 == 1:
        range_x_min = image_centroid_pixel_x - int((size - 1) / 2)
        range_x_max = image_centroid_pixel_x + int((size + 1) / 2)
        range_y_min = image_centroid_pixel_y - int((size - 1) / 2)
        range_y_max = image_centroid_pixel_y + int((size + 1) / 2)
    else:
        range_x_min = image_centroid_pixel_x - int(size / 2)
        range_x_max = image_centroid_pixel_x + int(size / 2)
        range_y_min = image_centroid_pixel_y - int(size / 2)
        range_y_max = image_centroid_pixel_y + int(size / 2)

    # Before cropping the batch, we need to know how much of the mosaic required is contained in this batch
    # or else, we require neighboring batches to complete the mosaic.
    ########################################################################################
    #########################################################################################
    #                      Procedure for cropping and concatenating batches.
    # Let (0,0) be the image we have cropped so far
    # but not we require to concatenate a vertical/horizontal strips and even some corners. In any case
    # we only need to consider its 8 images around the image (0,0). We begin by labeling them as follows:

    ################################
    # (-1,  1) # (0,  1) # (1,  1) #
    ################################
    # (-1,  0) # (0,  0) # (1,  0) #
    ################################
    # (-1, -1) # (0, -1) # (1, -1) #
    ################################

    # In this procedure we first crop images (0, 1) or (0, -1) and add a vertical strip above or below (0,0).
    # Then, we generate as a separate strip to the left or to the right. This strip has exactly the same height
    # of the image saved in the first step. Finally, we concatenate this image horizontally.
    # The code is done pretty much case-wise. Perhaps some code could be recycled but the independency of the cases
    # make the code quite clear.

    # batch_[x,y]_aux can take values in [-1, 1] and correspond to the batch label its working with.
    # The default values are 0,0.
    batch_x_aux = 0
    batch_y_aux = 0

    # Also the default values are the ranges previously stored, which we know they exceeded the limits of the 0,0 batch.
    range_x_min_iter, range_x_max_iter = range_x_min, range_x_max
    range_y_min_iter, range_y_max_iter = range_y_min, range_y_max

    # We begin by identifying which is the range that exceeded its dimensions so then we can load the corresponding
    # batch that contains the missing mosaic. There are four cases: left, bottom right, top, respectively.
    if range_x_min < 0:
        batch_x_aux = -1
        range_x_min_iter = 0
    if range_x_max > img_batch.shape[1]:
        batch_x_aux = 1
        range_x_max_iter = img_batch.shape[1]
    if range_y_min < 0:
        batch_y_aux = 1
        range_y_min_iter = 0
    if range_y_max > img_batch.shape[0]:
        batch_y_aux = -1
        range_y_max_iter = img_batch.shape[0]

    # We crop all the mosaic contained in the batch 0,0.
    img_out = img_batch[range_y_min_iter:range_y_max_iter, range_x_min_iter:range_x_max_iter, :]

    # From here below, only IF clauses appear which correspond to the different cases when we require other batches
    # to complete the mosaic.

    # We start by adding only top and bottom images there are two possible cases. We call the batch, and concatenate
    # its vertical strip below or above, respectively.
    if batch_y_aux in [-1, 1]:
        batch_x_iter = '{:02d}'.format(batch_x)
        batch_y_iter = '{:02d}'.format(batch_y + batch_y_aux)
        batch_iter_label = batch_x_iter + '_' + batch_y_iter
        batch_dict = load_batch(batch_iter_label, batch_dict, bucket=bucket)
        img_iter = batch_dict[batch_iter_label]
        if batch_y_aux == -1:
            range_y_min_iter = 0
            range_y_max_iter = range_y_max - img_batch.shape[0] - pixels_intersect_h + 1
            img_iter = img_iter[range_y_min_iter:range_y_max_iter, range_x_min_iter:range_x_max_iter, :]
            img_out = cv2.vconcat([img_out[:(pixels_intersect_h - 1), :, :], img_iter])
        if batch_y_aux == 1:
            range_y_min_iter = range_y_min + img_batch.shape[0] + pixels_intersect_h - 1
            range_y_max_iter = img_batch.shape[0]
            img_iter = img_iter[range_y_min_iter:range_y_max_iter, range_x_min_iter:range_x_max_iter, :]
            img_out = cv2.vconcat([img_iter[:(pixels_intersect_h - 1), :, :], img_out])

    # Then we generate left or right strips.
    img_v = np.array([])  # Initialize vertical Strip
    # We start by generating the batch labels, the x is constant and the y can be one single image or two if we
    # need to concatenate a corner. Depending on the case the different ranges get calculated.
    if batch_x_aux in [-1, 1]:
        if batch_x_aux == -1:
            range_x_min_iter = range_x_min + img_batch.shape[1] - pixels_intersect_v - 1
            range_x_max_iter = img_batch.shape[1]
        else:
            range_x_min_iter = 0
            range_x_max_iter = range_x_max - img_batch.shape[1] + pixels_intersect_v + 1
        batch_x_iter = '{:02d}'.format(batch_x + batch_x_aux)

        # First we visit image [-1,0] or [1,0], then we add vertical or horizontal strip. Just as above.
        range_y_list = [0]
        if batch_y_aux == -1:
            range_y_list.append(-1)
        if batch_y_aux == 1:
            range_y_list.append(1)

        # reset range-y values as in image (0,0)
        range_y_min_iter, range_y_max_iter = range_y_min, range_y_max
        if range_y_min < 0:
            range_y_min_iter = 0
        if range_y_max > img_batch.shape[0]:
            range_y_max_iter = img_batch.shape[0]

        for j in range_y_list:
            batch_y_iter = '{:02d}'.format(batch_y + j)
            batch_iter_label = batch_x_iter + '_' + batch_y_iter
            batch_dict = load_batch(batch_iter_label, batch_dict, bucket=bucket)
            img_iter = batch_dict[batch_iter_label]
            if j == -1:
                range_y_min_iter = 0
                range_y_max_iter = range_y_max - img_batch.shape[0] - pixels_intersect_h + 1
            if j == 1:
                range_y_min_iter = range_y_min + img_batch.shape[0] + pixels_intersect_h - 1
                range_y_max_iter = img_batch.shape[0]

            img_iter = img_iter[range_y_min_iter:range_y_max_iter, range_x_min_iter:range_x_max_iter, :]

            if j == 0:
                img_v = img_iter
            if j == -1:
                img_v = cv2.vconcat([img_v[:(pixels_intersect_h - 1), :, :], img_iter])
            if j == 1:
                img_v = cv2.vconcat([img_iter[:(pixels_intersect_h - 1), :, :], img_v])

        if batch_x_aux == -1:
            img_out = cv2.hconcat([img_v, img_out[:, (pixels_intersect_v + 1):, :]])
        else:
            img_out = cv2.hconcat([img_out, img_v[:, (pixels_intersect_v + 1):, :]])

    # Eliminates excess of stored batches in dict
    batch_keys = list(batch_dict.keys())
    batch_keys.reverse()
    batch_keys_len = len(batch_keys)
    if batch_keys_len > max_batches:
        for i in range(max_batches, batch_keys_len):
            batch_dict.pop(batch_keys[i], None)
            local_filepath = '../data/04_batches/' + batch_keys[i] + '.png'
            try:
                os.remove(local_filepath)
            except:
                pass

    # Wld file for georeferencing an image. USE EPSG:4326
    wld = np.zeros(6)

    wld[0] = pixel_size_x
    wld[3] = -pixel_size_y
    wld[4] = x - pixel_size_x * size / 2
    wld[5] = y + pixel_size_y * size / 2

    return img_out, wld, batch_dict


def mosaic_around_image(x=None, y=None, size=None,
                        album=None,
                        bucket=None,
                        x_batch_dim=None,
                        y_batch_dim=None,
                        pixels_intersect_h=None,
                        pixels_intersect_v=None,
                        ):
    """
    Displays a mosaic given a point in coordinates x (longitude) and y (latitude).
    size is used to calculate the number of images the mosaic contains.
    size=1 is a single image, size=2 is a 3x3 mosaic, size=3 is a 5x5 mosaic, etc.
    """
    # Local path for storing outputs.
    local_filedir = '../data/01_raw_images/test/'
    local_filepath = local_filedir + 'img_iter.png'

    # image index of closest point
    img_index = find_closest_image(x, y, album=album)

    # save album features from image
    batch_x, batch_y, cell_x, cell_y = album.iloc[img_index][['batch_x', 'batch_y', 'cell_x', 'cell_y']]

    # To create a mosaic img, we will generate horizontal strips of images and we will concatenate each strip img_h .
    # The outer for is to concatenate horizontal image strips img_h into img.
    img = np.array([])  # OUTPUT: tensor that defines the image

    for j in trange(1 - size, size, desc='Iterative Progress'):
        img_h = np.array([])
        # The inner for is to concatenate vertical single images into a horizontal strip img_h
        for i in range(1 - size, size):
            # set image label for the iteration
            batch_x_iter = batch_x
            batch_y_iter = batch_y
            cell_x_iter = cell_x + i
            cell_y_iter = cell_y + j

            # adjust batch and cell labels if the image is outside the current batch
            if cell_x_iter < 0:
                cell_x_iter = cell_x_iter + x_batch_dim
                batch_x_iter = batch_x - 1
            if cell_x_iter > x_batch_dim - 1:
                cell_x_iter = cell_x_iter - x_batch_dim
                batch_x_iter = batch_x + 1
            if cell_y_iter < 0:
                cell_y_iter = cell_y_iter + y_batch_dim
                batch_y_iter = batch_y - 1
            if cell_y_iter > y_batch_dim - 1:
                cell_y_iter = cell_y_iter - y_batch_dim
                batch_y_iter = batch_y + 1

            # define iteration image path
            batch_x_label = '{:02d}'.format(batch_x_iter)
            batch_y_label = '{:02d}'.format(batch_y_iter)
            batch_path_iter = batch_x_label + '_' + batch_y_label + '/'
            cell_x_label = '{:02d}'.format(cell_x_iter)
            cell_y_label = '{:02d}'.format(cell_y_iter)
            img_iter_path = cell_x_label + '_' + cell_y_label + '.png'
            s3_filedir = '01_raw_images/'
            s3_filepath = s3_filedir + batch_path_iter + img_iter_path

            # check if the image is currently saved in S3
            if check_key(bucket, s3_filepath):
                # if the image exists, download it to locally to local_img_path and the read it.
                s3_client.download_file(bucket, s3_filepath, local_filepath)
                img_iter = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
            else:
                # if the image does not exist, define a blanc picture in its place.
                img_iter = np.ones((375, 400, 4)).astype(np.uint8)

            # In the first iteration of the inner for, img_h is empty. Therefore Else applies and the image is copied.
            # For the following iterations an image is concatenated.
            if len(img_h) > 0:
                img_h = cv2.hconcat([img_h, img_iter[:, (pixels_intersect_v + 1):, :]])
            else:
                img_h = img_iter

        # Analogous routine for the joining horizontal straps.
        if j > -size + 1:
            img = cv2.vconcat([img_h[:(pixels_intersect_h - 1), :, :], img])
        else:
            img = img_h

    # img_index is useful for the other routine.
    return img
