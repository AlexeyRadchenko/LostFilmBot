import urllib3
from os.path import abspath
from io import BytesIO


def get_img_file_in_memory(url=None, path=None):
    """close bytes_obj.close()"""
    if not path:
        path = abspath('.')+'/'
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    bytes_obj = BytesIO(r.read(1024))
    bytes_obj.name = "image.jpg"
    r.release_conn()
    return bytes_obj

print(get_img_file_in_memory(url='http://static.lostfilm.tv/Images/366/Posters/image.jpg'))