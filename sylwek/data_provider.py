import time
import numpy as np
from matplotlib import pyplot as plt
from sylwek.similarity_measure import SimilarityMeasure
from utils import mnist_reader

class DataProvider:
    images = {}
    labels = {}
    similarity_measure = None

    next_id = -1  #TODO 2. Prosimy nadać każdemu obrazkowi unikalny identyfikator `image_id` (np. indeks z tablicy)

    def __init__(self):
        print("Init: Data Provider.")
        self.similarity_measure = SimilarityMeasure(self.images)
        # load data
        X_train, y_train = mnist_reader.load_mnist('../data/fashion', kind='train')
        X_test, y_test = mnist_reader.load_mnist('../data/fashion', kind='t10k')

        # Add images and labels
        self.add_image(X_train,y_train)
        self.add_image(X_test,y_test)


    def get_image(self,image_id):
        if image_id in self.images:
            return self.images[image_id]
        else:
            return None

    def add_image(self, images,labels):
        if not len(images) == len(labels):
            print("Images and labels must be the same size")
            print(" System Exit -1")
            exit(-1)
        for index,image in enumerate(images):
            id = self._next_id()
            self.images[id] = image
            self.add_label(id, labels[index])

    def add_label(self,id,label):
        if label in self.labels:
           self.labels[label].append(id)
        else:
            self.labels[label] = []
            self.labels[label].append(id)

    def _next_id(self):
        """
        2. Prosimy nadać każdemu obrazkowi unikalny identyfikator `image_id` (np. indeks z tablicy)
        :return: next id
        """
        self.next_id += 1
        return self.next_id

    def show_image(self,image_id):
        """
        3. Prosimy potraktować obrazki jako 784 (28x28) elementowy wektor
        :param image_id: id of image
        """
        data = self.images[image_id]
        data = np.resize(data, (28, 28))
        plt.imshow(data)
        plt.show()


if __name__ == "__main__":

    dp = DataProvider()
    exetime = int(round(time.time() * 1000))
    id = 50
    mi = dp.similarity_measure.most_similar(id, top_limit = 10)
    exetime = int(round(time.time() * 1000)) - exetime
    print("total time {}[ms]".format( exetime))

    # Show
    dp.show_image(id)
    for id in mi:
        dp.show_image(id)



