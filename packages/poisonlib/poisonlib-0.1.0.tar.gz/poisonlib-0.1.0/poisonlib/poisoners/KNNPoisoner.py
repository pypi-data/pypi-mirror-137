from scipy import stats
from sklearn.neighbors import KDTree
import numpy as np


class KNNPoisoner:

    def __init__(self, perc_poison=0.1, k=2):
        self.perc_poison = perc_poison
        self.k = k
        self.n_poison = None
        self.X = None
        self.labels = None
        self.tree = None
        self.poisoned_X = None
        self.poisoned_labels = None
        self.neighbors = {}

    def find_neighbors(self):
        """
        (internal) Pre-compute neighbors for all input points
        :return: -
        """
        self.tree = KDTree(np.c_[self.X[:, 0].ravel(), self.X[:, 1].ravel()])
        _, indices = self.tree.query(self.X, self.k + 1)
        indices = [index[1:] for index in indices]
        self.neighbors = {i: indices[i] for i in range(len(self.X))}

    def get_corruption(self, y_poisoned):
        """
        (internal) get corruption for a  given set of flipped labels
        :param y_poisoned:  poisoned labels
        :return:            number of corrupted labels
        """
        pred_y = np.array([stats.mode(self.labels[self.neighbors[i]]).mode for i in range(len(self.X))])
        pred_y_poisoned = np.array([stats.mode(y_poisoned[self.neighbors[i]]).mode for i in range(len(self.X))])

        return np.sum(pred_y != pred_y_poisoned)

    def poison(self, X, labels):
        """
        Get the best poisoning for the given input data
        :param X:       Input points
        :param labels:  Labels of the input points
        :return:
        a numpy array of flipped labels for the input points in the same order
        """

        self.X = X
        self.labels = labels
        self.n_poison = int(self.perc_poison * len(self.X))

        self.find_neighbors()

        print(f'Identifying {self.n_poison} poison points..')
        unique_labels = np.unique(labels)

        poison_results = {}

        for i, x in enumerate(self.X):
            labels_to_check = list(set(unique_labels) - set([self.labels[i]]))
            #         print(f'For point {x}, label - {y[i]}, checking - {labels_to_check}')
            for label in labels_to_check:
                y_poisoned = np.array(self.labels)
                y_poisoned[i] = label

            poison_results[str(i) + ':' + str(label)] = self.get_corruption(y_poisoned)

        top_m = sorted(poison_results.items(), key=lambda item: item[1], reverse=True)[0:self.n_poison]
        y_poisoned = np.array(self.labels)
        for row in top_m:
            index, label = [int(val) for val in row[0].split(':')]
            y_poisoned[int(index)] = int(label)

        print(y_poisoned, self.get_corruption(y_poisoned))

        self.poisoned_labels = y_poisoned
