

import os
import uuid
from urllib.request import urlopen
import tempfile
from tempfile import NamedTemporaryFile
from shutil import unpack_archive
from urllib.parse import urlparse
from random_word import RandomWords
import zipfile
from zipfile import ZipFile
import gzip
import tarfile
import requests


__all__ = ['fetch', 'unzip', 'fetch_and_unzip']


def fetch(url, folder=None, file_name=None):
    
    if not folder:
        # Temp folder
        folder = tempfile.gettempdir()
        # print('folder: ', folder)

    # 폴더가 없으면 만들고, 있으면 안 만든다.
    os.makedirs(folder, exist_ok=True)

    # 파싱
    parts = urlparse(url)
    # print(parts)

    if not file_name:
        # 확장자 찾기 
        file_ext = os.path.splitext(parts.path)[1]   
        # print('extension : ', file_ext, type(file_ext), len(file_ext))

        file_name = os.path.basename(parts.path)  #eds_report.csv
        # print('file_name : ', file_name, type(file_name), len(file_name))
        
        if not file_name:
            # 임시 파일을 만든다.
            file_name = str(uuid.uuid4()).split('-')[0] + '.tmp'
            # print('temp filename : ', type(file_name), file_name)
        
        # 확장자가 있다는 것은 파일명이 있다는 것으로 간주 
        # if file_ext in ('.gz', '.zip', 'gzip', 'bzip2', 'lzma'):
        #     names = parts.path.split('/')
        #     file_name = names[-1]
        #     print('filename : ', file_name)
        # else:
        #     # 임시 파일을 만든다.
        #     # file_name = uuid.uuid4().split('-')[0]
        #     file_name = str(uuid.uuid4()).split('-')[0] + '.tmp'
        #     print('temp word filename : ', type(file_name), file_name)

    # print('download at ', os.path.join(folder, file_name))
    
    with open(os.path.join(folder, file_name), 'wb') as my_file:
        data = requests.get(url)
        my_file.write(data.content)
        return os.path.join(folder, file_name)
        
    return None


def unzip(path):
    path_to_zip_file = path
    directory_to_extract_to = os.path.dirname(path_to_zip_file)

    # print('unzip file:', path_to_zip_file)
    # print('unzip folder:', directory_to_extract_to)
    
    # 확장자 찾기 
    file_ext = os.path.splitext(path_to_zip_file)[1]
    # print('extension : ', file_ext, type(file_ext), len(file_ext))
    
    
    
    if file_ext in ('.gz', '.gzip', '.bzip2', '.lzma'):
        tar = tarfile.open(path_to_zip_file, mode='r:*')
        dir_name = tar.getmembers()[0].name.split('/')[0]
        # print('dir name: ', dir_name)

        tar.extractall(path=directory_to_extract_to)
        tar.close()
        return os.path.join(directory_to_extract_to, dir_name)
    elif file_ext in ('.zip',):
        with ZipFile(path_to_zip_file, 'r') as zipObj:
            dir_name = zipObj.namelist()[0].split('/')[0]
            # print('dir name: ', dir_name)
            zipObj.extractall(path=directory_to_extract_to)
            return os.path.join(directory_to_extract_to, dir_name)
    return None

def fetch_and_unzip(url, folder=None, file_name=None):
    return unzip(fetch(url, folder, file_name))

