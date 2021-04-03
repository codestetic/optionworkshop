import os
import xml.etree.ElementTree as ET
from os import path
from urllib import request, parse

__url_format__ = 'https://{0}.s3.amazonaws.com/{1}'


def list_datasets(bucket_name: str = "ow-blog-datasets", cache_dir: str = "c:\\temp"):
    __ensure_cache_dir__(cache_dir)
    url = __url_format__.format(bucket_name, '')

    filename = parse.quote(url, '')
    filepath = path.join(cache_dir, filename)
    request.urlretrieve(url, filepath)
    xml = ET.parse(filepath)

    result = []
    ns = {'default': 'http://s3.amazonaws.com/doc/2006-03-01/'}
    for key in xml.findall(".//default:Key", ns):
        result.append(key.text)

    return result


def download_dataset(file_name: str, bucket_name: str = "ow-blog-datasets", no_cache: bool = False,
                     cache_dir: str = "c:\\temp"):
    __ensure_cache_dir__(cache_dir)
    url = __url_format__.format(bucket_name, file_name)

    filename = parse.quote(url, '')
    filepath = path.join(cache_dir, filename)

    if path.exists(filepath):
        return filepath

    request.urlretrieve(url, filepath)

    return filepath


def __ensure_cache_dir__(cache_dir: str):
    if not path.exists(cache_dir):
        os.mkdir(cache_dir)
