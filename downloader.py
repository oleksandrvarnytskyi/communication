import sys
import urllib


if sys.argv[1:]:
    url_name = sys.argv[1]
else:
    url_name = 'http://upload.wikimedia.org/wikipedia/commons/9/9c/' \
               'Image-Porkeri_001.jpg'
remote_address = url_name
file_name = url_name.split('/')[-1]
print(remote_address, file_name)
urllib.urlretrieve(remote_address, file_name)
