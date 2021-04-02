import os
import urllib
from os import path


def download_dataset(file_name: str, bucket_name: str = "ow-blog-datasets", no_cache: bool = False,
                     cache_dir: str = "c:\\temp"):
    url_format = 'https://{0}.s3.amazonaws.com/{1}'
    url = url_format.format(bucket_name, file_name)

    if not path.exists(cache_dir):
        os.mkdir(cache_dir)

    filename = urllib.parse.quote(url, '')

    filepath = path.join(cache_dir, filename)

    if path.exists(filepath):
        return filepath

    urllib.request.urlretrieve(url, filepath)

    return filepath
