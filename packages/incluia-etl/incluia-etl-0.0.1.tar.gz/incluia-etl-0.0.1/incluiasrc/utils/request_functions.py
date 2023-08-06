import boto3
import botocore
from botocore.exceptions import ClientError
import datetime
import geopandas as gpd
import io
import json
import matplotlib.image as mpimg
import numpy as np
import os
import pandas as pd
from PIL import Image
import random

s3_client = boto3.client('s3')


def corners_coordinates(lat=None, lon=None):
    """
    Returns a 4 coordinate points--latitude and longitude--where the corners of a satellite image are.
    ------------------------------------------------
    parameters:
        lat: float. Centroid of image latitude
        lon: float. Centroid of image longitude
        out: lat1, lat2, lon1, lon2: floats. Coordinates of corners.
    """
    # Earth Modelled as a Sphere
    lat_r = lat / 180 * np.pi
    # lon_r = lon / 180 * np.pi

    r1 = 6378137.0  # radius at equator
    r2 = 6356752.3  # radius at pole

    # https://rechneronline.de/earth-radius/
    numerator = (r1 ** 2 * np.cos(lat_r)) ** 2 + (r2 ** 2 * np.sin(lat_r)) ** 2
    denominator = (r1 * np.cos(lat_r)) ** 2 + (r2 * np.sin(lat_r)) ** 2
    earth_radius = np.sqrt(numerator / denominator)
    # https://groups.google.com/g/google-maps-js-api-v3/c/hDRO4oHVSeM?pli=1
    metersperpx = earth_radius / (128 / np.pi) * np.cos(lat_r) / 2 ** 20
    mts = metersperpx * np.array([400, 400])  # each pixel how many meters they represent

    # Wikipedia formulas on pages latitude and longitude
    # Earth Modelled as an Ellipsoid

    e2 = 1 - r2 ** 2 / r1 ** 2  # squared excentricity
    # Obtaining latitude and longitude of corners of an image given centroid

    ################################################
    lat_grad_mts = np.pi * r1 * (1 - e2) / (180 * (1 - e2 * np.sin(lat_r) ** 2) ** 1.5)
    lat_dif = mts[0] / lat_grad_mts  # album cte

    lat1 = lat - lat_dif / 2  # image corners
    lat2 = lat + lat_dif / 2  # image corners
    lon_grad_mts = np.pi * r1 * np.cos(lat_r) / (180 * (1 - e2 * np.sin(lat_r) ** 2) ** 0.5)
    lon_dif = mts[1] / lon_grad_mts  # album cte

    lon1 = lon - lon_dif / 2  # image corners
    lon2 = lon + lon_dif / 2  # image corners

    return lat1, lat2, lon1, lon2


def get_vector_map(bucket=None, local_filepath=None, crs=4326, force_s3=False):
    """
        Reads almost any vector-based spatial data format including ESRI shapefile (.shp), GeoJSON files and more.
        Then, transforms the geopandas to the Coordinate Reference System (CRS) given by crs.
        Returns a GeoDataFrame object.

        Parameters
        ----------
        bucket: str.  S3 bucket name to upload to.
        local_filepath : str. Path of a vector file stored in geopandas.
        crs : int. The Coordinate Reference System (CRS) to transform the geopandas. Default = 4326.
        force_s3: boolean. Forces download from s3 even if local file exists.
        """

    # Read file extension
    extension = os.path.splitext(local_filepath)[1]

    try:
        if not force_s3:
            print('Reading localfile: ' + local_filepath)
            vector_map = gpd.read_file(local_filepath)
        else:
            # Generates an exception so it jumps to the except chunk and reads from s3
            pd.read_csv('')
    except:
        if extension == '.shp':
            for fileformat in ['.cpg', '.dbf', '.prj', '.shp', '.shx']:
                filename, _, local_filedir, s3_filedir = filepath_breaker(local_filepath)
                s3_filepath = s3_filedir + filename + fileformat
                local_filepath = local_filedir + filename + fileformat
                print('Downloading ' + s3_filepath + ' from S3: ', end='')
                get_object(bucket=bucket, s3_filepath=s3_filepath, local_filepath=local_filepath)
                print('done')

            local_filepath = local_filedir + filename + extension
        elif extension == '.geojson':
            filename, _, local_filedir, s3_filedir = filepath_breaker(local_filepath)
            s3_filepath = s3_filedir + filename + extension
            local_filepath = local_filedir + filename + extension
            print('Downloading ' + s3_filepath + ' from S3: ', end='')
            get_object(bucket=bucket, s3_filepath=s3_filepath, local_filepath=local_filepath)
            print('done')
        else:
            print('File extension invalid. Must be geojson or shp')
        vector_map = gpd.read_file(local_filepath)
    # CRS maps Python to places on the Earth.
    # For example, one of the most commonly used CRS is the WGS84 latitude-longitude projection.
    # This can be referred to using the authority code "EPSG:4326" or epsg=4326.
    vector_map = vector_map.to_crs(epsg=crs)
    return vector_map


def get_object(bucket=None, s3_filepath=None, local_filepath=None, profile_name=None):
    """
        Get a file from an S3 bucket to local

        Parameters
        ----------
        bucket: str. S3 bucket name to upload to.
        s3_filepath: str. S3 object path.
        local_filepath: str. Local path for storing file.
        profile_name: str. Profile AWS name.
    """
    s3 = boto3.resource('s3')

    try:
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)
        s3.Bucket(bucket).download_file(s3_filepath, local_filepath)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('The object does not exist.')
        else:
            raise

    return None


def upload_object(bucket=None, local_filepath=None, s3_filepath=None, profile_name=None):
    """
        Upload a file from local to an S3 bucket

        Parameters
        ----------
        local_filepath: str. Local path of file to upload
        bucket: str. S3 bucket name to upload to.
        s3_filepath: str. S3 object name to save to. If not specified then local_filepath is used
        profile_name: str. Profile AWS name.
        """
    # Store in same location in S3 and Locally.
    if s3_filepath is None:
        s3_filepath = local_filepath.replace('../data/', '')

    # Upload the file
    out = True
    try:
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)
        print('Saving file in S3 as: ' + s3_filepath + ' ... ', end='')
        s3_client.upload_file(Filename=local_filepath, Bucket=bucket, Key=s3_filepath)
        print('done')
    except ClientError as e:
        logging.error(e)
        out = False
    return out


def get_gpd(bucket=None, key=None, profile_name=None, colnames_to_lower=False):
    """
        Load a gpd dataframe of an S3 bucket to RAM.

        Parameters
        ----------
        bucket: str. Bucket name to load from.
        key: str. S3 object name path.
        profile_name : str. AWS profile name.
        colnames_to_lower : bool. Specifies if column names need to be converted to lower.
    """
    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    s3 = boto3.resource('s3')
    # Load the file
    try:
        s3.Object(bucket, key).load()
        bytes_obj = s3.Object(bucket, key).get()['Body'].read().decode('utf-8')
        out_dict = json.loads(bytes_obj)
        out_df = gpd.GeoDataFrame.from_features(out_dict["features"], crs='EPSG:4326')
    except botocore.exceptions.ClientError:
        out_df = None

    if colnames_to_lower:
        out_df.columns = out_df.columns.str.lower()

    return out_df


def get_csv(bucket=None, local_filepath=None,
            profile_name=None, colnames_to_lower=False, header='infer', encoding=None, force_s3=False):
    """
        Load a csv file of an S3 bucket to RAM.

        Parameters
        ----------
        bucket: str. Bucket name to load from.
        local_filepath: Local path where csv is stored
        profile_name : str. AWS profile name.
        colnames_to_lower : bool. Specifies if column names need to be converted to lower.
        header: str. Refer to pd.read_csv function.
        encoding: read csv encoding. Read pd_read_csv encoding option.
        force_s3: force to download file from s3 and overwrites localfile if exits.
    """

    try:
        if not force_s3:
            out_df = pd.read_csv(local_filepath, sep=',', header=header, encoding=encoding)
            print('Reading localfile: ' + local_filepath + ' ', end='')
        else:
            # Generates an exception so it jumps to the except chunk
            pd.read_csv('')
    except:
        print('Downloading ' + local_filepath.replace('../data/', '') + ' from S3: ', end='')
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)

        s3 = boto3.resource('s3')
        # Load the file
        try:
            filename, _, _, s3_filedir = filepath_breaker(local_filepath)
            s3_filepath = s3_filedir + filename + '.csv'
            s3.Object(bucket, s3_filepath).load()
            if encoding == None:
                bytes_obj = s3.Object(bucket, s3_filepath).get()['Body'].read().decode('utf-8-sig')
            else:
                bytes_obj = s3.Object(bucket, s3_filepath).get()['Body'].read().decode(encoding)
            out_df = pd.read_csv(io.StringIO(bytes_obj), header=header, encoding=encoding)

        except botocore.exceptions.ClientError:
            out_df = None

    if colnames_to_lower:
        out_df.columns = out_df.columns.str.lower()

    print('done')
    return out_df


def get_feather(bucket=None, key=None, profile_name=None, colnames_to_lower=False):
    """
        Load a feather file of an S3 bucket to RAM.

        Parameters
        ----------
        bucket: str. Bucket name to load from.
        key: str. S3 object name path.
        profile_name : str. AWS profile name.
        colnames_to_lower : bool. Specifies if column names need to be converted to lower.
    """
    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket, key).load()
        bytes_obj = s3.Object(bucket, key).get()['Body'].read()
        feather = pd.read_feather(io.BytesIO(bytes_obj))

    except botocore.exceptions.ClientError:
        feather = None

    if colnames_to_lower:
        feather.columns = feather.columns.str.lower()

    return feather


def get_img(bucket=None, s3_filepath=None, local_filepath=None, rm=True, wld=True):
    """
        Load a gpd dataframe of an S3 bucket to RAM.

        Parameters
        ----------
        bucket: str. Bucket name to load from.
        s3_filepath: str. S3 object name path.
        local_filepath: str. Local path to save S3 Object.
        rm: boolean. If True removes local file after reading in RAM.
        wld: boolean. If True, downloads wld file associated to local.
    """
    try:
        s3_client.download_file(bucket, s3_filepath, local_filepath)
        img = (mpimg.imread(local_filepath) * 255).astype(np.uint8)
        img = img[:, :, :-1]
        img = Image.fromarray(img)  # Assumes range [1,255]
        if rm and os.path.exists(local_filepath):
            os.remove(local_filepath)

        if wld:
            local_filepath = local_filepath.replace('png', 'wld')
            s3_filepath = s3_filepath.replace('png', 'wld')
            s3_client.download_file(bucket, s3_filepath, local_filepath)
    except:
        raise Exception('Image not available')
    return img


def check_key(bucket=None, key=None, profile_name=None):
    """
    Checks if a file exists in an S3 bucket. Return True if exists and False if it does not.

    ----------
    Parameters
        bucket: str. Bucket name to load from.
        key: str. S3 object name path.
        profile_name : str. AWS profile name.
    """
    if profile_name is not None:
        boto3.setup_default_session(profile_name=profile_name)

    s3 = boto3.resource('s3')
    exists = True
    try:
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False  # The object does not exist.
        else:
            raise  # Something else has gone wrong.

    return exists


def hour_to_day_period(h=None):
    """
    Simple function that returns the following mapping:
    0 if current hor between [0, 5]
    1 if current hor between [6, 11]
    2 if current hor between [12, 17]
    3 if current hor between [18, 23]
    The output is an index of an array of floats, that represent parameters of a distribution (mean and var)
    that can modify the request frequency.
    """
    hour_periods = np.array([6, 12, 18, 24])
    hour_periods_condition = hour_periods - 1
    if h <= hour_periods_condition[0]:
        index = 0
    elif h <= hour_periods_condition[1]:
        index = 1
    elif h <= hour_periods_condition[2]:
        index = 2
    else:
        index = 3
    return index


def smooth_request_transition(current_hour=None, vector_schedule=None):
    """
    To make the transition frequency smooth we redefine the var and mean statistics when they are close
    to the change of period. This transition occurs within the previous hour before the change.
    """

    hour_periods = np.array([6, 12, 18, 24])
    hour_periods_condition = hour_periods - 1  # hours before a transition of frequency

    current_minute = datetime.datetime.now().minute

    i = hour_to_day_period(current_hour)  # compute current index i
    statistic = vector_schedule[i]
    if current_hour in hour_periods_condition:
        # from the vector schedule, keep the current statistic and the next.
        i_next = (i + 1) % 4
        current_stat = vector_schedule[i]
        next_stat = vector_schedule[i_next]

        # define a random variable that as minutes goes by, it approaches to 1.
        time_ratio = random.uniform(current_minute, 60) / 60
        # define a statistic that approaches to statistic_max as time goes by
        # and such that its domain is between current_stat and next_stat
        statistic = (1 - time_ratio) * current_stat + time_ratio * next_stat

    return statistic


def freq_param(time_freq_init=None, time_freq_final=None, n_days=None, start_date=None):
    """
    Changes the frequency parameter smoothly.
    time_freq_init: float. The initial frequency of requests.
    time_freq_final: float. The final frequency of requests.
    n_days: integer. Days transcurred to reach from time_freq_init to time_freq_final
    start_date : str. Starting date written as Y-m-d, example 2021-01-15
    """
    start_date_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    days_transcurred = (datetime.datetime.now() - start_date_datetime).days
    slope = (time_freq_final - time_freq_init) / n_days
    time_freq = slope * days_transcurred + time_freq_init
    time_freq = max([time_freq, time_freq_final])
    return time_freq


def autolabel(rects=None, ax=None):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height) + ' %',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')


def filepath_breaker(local_filepath):
    """
        Breaks string of a local_filepath into different useful strings to save file in s3 or change fileformat.
        local_filepath: string. Relative path of where a local file is stored.
    """
    s3_filepath = local_filepath.replace('../data/', '')
    filename_fileformat = local_filepath.split('/', local_filepath.count('/'))[-1]
    filename = filename_fileformat.split('.', filename_fileformat.count('.'))[0]
    fileformat = '.' + filename_fileformat.split('.', filename_fileformat.count('.'))[-1]
    local_filedir = local_filepath.replace(filename_fileformat, '')
    s3_filedir = s3_filepath.replace(filename_fileformat, '')
    return filename, fileformat, local_filedir, s3_filedir
