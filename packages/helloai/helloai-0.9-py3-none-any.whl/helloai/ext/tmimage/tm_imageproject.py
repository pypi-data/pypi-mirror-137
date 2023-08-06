import os
import cv2
import tensorflow.keras as keras
import numpy as np

import zipfile
from collections import OrderedDict
import traceback

from helloai.core.image import Image

np.set_printoptions(suppress=True)

__all__ = ['TMImageProject']


class TMImageProject:
    def __init__(self):
        self.__model = None
        self.__labels = []
        self.__label = None
        self.__confidence = None

    def load_model(self, file_path):
        if not os.path.exists(file_path):
            print('폴더가 존재하지 않습니다')
            return

        
        
        model_file = os.path.join(file_path, 'keras_model.h5')
        label_file = os.path.join(file_path, 'labels.txt')
        if not os.path.exists(model_file) or not os.path.exists(label_file):
            print('모델 파일 또는 라벨 파일이 존재하지 않습니다')
            print(model_file)
            print(label_file)
            return

        self.__load_model(model_file)
        self.__load_labels(label_file)

    def __load_labels(self, path):
        print(f'<TMImageModel> load label path={path}')
        f = open(path, 'r', encoding='UTF8')
        lines = f.readlines()
        labels = []

        # for line in lines:
        #     items = line.split(' ')
        #     labels[items[0].strip('\n')] = items[1].strip('\n')

        for line in lines:
            labels.append(line.split(' ')[1].strip('\n'))

        self.__labels = labels
        return True

    def __load_model(self, path):
        print(f'<TMImageModel> load model path={path}')

        self.__model = keras.models.load_model(path)
        return True

    def process(self, img):
        """입력된 이미지를 분류한다.
        입력 이미지를 정사각형으로 만들고, 티쳐블머신에서 학습할 때 사용하던 영상처럼 Flip을 하는 것이 결과가 좋을 수 있다

        Args:
            img (Image): 입력 이미지. (정사각형이고 플립된 이미지가 결과가 좋을 수 있다.)

        Returns:
            str : 분류된 클래스(라벨)
        """
        if not isinstance(img, Image) or img.image is None:
            return []

        # TODO 이미지 사이즈를 224x224로 변경해야 한다. 입력이미지가 정사각형인지 아닌지 상관없이 넓이x높이 224x224로 리사이즈
        # same as the cropping process in TM2
        frame = img.resize(width=224, height=224).frame
        
        # bgr -> rgb, 변경하지 않으면 결과가 좋지않다.
        frame = frame[:,:,::-1]

        # flips the image
        # frame = cv2.flip(frame, 1) # 데이터를 입력할때 플립시켜서 넣어야 된다.
        # cv2.imshow('224', frame)
        # normalize the image and load it into an array that is the right format for keras
        normalized_img = (frame.astype(np.float32) / 127.0) - 1
        
        # 텐서플로우 데이터로 입력하기 위해서, 축 추가 
        # np를 이용한 축추가 : np_final = np.expand_dims(np_image_data,axis=0)
        data_for_model = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data_for_model[0] = normalized_img

        prediction = self.__model.predict(data_for_model)

        alist = prediction[0].tolist()
        index = alist.index(max(alist))
        self.__label = self.__labels[index]
        self.__confidence = round(alist[index], 3)    # round(n,2)
        return self.__labels[index]

    # This function proportionally resizes the image from your webcam to 224 pixels high
    def __image_resize(self, img, height, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = img.shape[:2]
        r = height / float(h)
        dim = (int(w * r), height)
        resized = cv2.resize(img, dim, interpolation=inter)
        return resized

    # this function crops to the center of the resize image
    def __cropTo(self, img):
        # size = 224
        height, width = img.shape[:2]

        sideCrop = (width - 224) // 2
        return img[:, sideCrop:(width - sideCrop)]

    # https://srbrnote.work/archives/1297#:~:text=Python%20%E3%81%A7%20zip%20%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92,%E3%81%93%E3%82%8C%E3%82%89%E3%82%92%E4%BD%BF%E3%81%84%E3%81%BE%E3%81%99%E3%80%82
    def __load_zip(self, path):
        # temp 폴더를 찾아야 하는데..
        file_datas = OrderedDict()

        try:
            with zipfile.ZipFile(path, 'r') as zip_data:
                infos = zip_data.infolist()

                for info in infos:
                    file_data = zip_data.read(info.filename)
                    file_datas[info.filename] = file_data
        except zipfile.BadZipFile:
            print(traceback.format_exc())

        return file_datas

    # # https://provia.tistory.com/53
    # def __download_unzip(self, url):
    #     # temp 폴더를 찾아야 하는데..
    #     if not os.path.exists('./ml-1m'):
    #         url = 'http://files.grouplens.org/datasets/movielens/ml-1m.zip'
    #         response = requests.get(url, stream=True)
    #         total_length = response.headers.get('content-length')
    #         bar = tqdm.tqdm_notebook(total=int(total_length))
    #         with open('./ml-1m.zip', 'wb') as f:
    #             for data in response.iter_content(chunk_size=4096):
    #                 f.write(data)
    #                 bar.update(4096)
    #         zip_ref = zipfile.ZipFile('./ml-1m.zip', 'r')
    #         zip_ref.extractall('.')
    #         zip_ref.close()
    
    @property
    def labels(self):
        return self.__labels

    @property
    def confidence(self):
        return self.__confidence

    def summary(self):
        if self.__model:
            self.__model.summary()
            print('labels :', self.labels)
        else:
            print('모델이 로딩되지 않았습니다')

    def __repr__(self):
        return f"<hello.core.TMImageModel at memory location: ({hex(id(self))})>"
