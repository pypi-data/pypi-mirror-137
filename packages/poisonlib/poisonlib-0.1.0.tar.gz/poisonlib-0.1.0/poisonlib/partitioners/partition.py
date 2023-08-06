import numpy as np
import math



class Partition:
    """
        This class partitions a space into grid cell of with alpha.
        use client method buckets to get the dictionary with points partitioned into buckets.
        p = Partition(X, 1)
        buckets = p.get_buckets()
    """
    def __init__(self, arr, alpha):
        self.arr = arr
        self.alpha = alpha
        self.buckets = {}
        self._partition_data()

    


    def _find_cell(self, grid_arr, x):
        """ function to find a coordinate grid cell.
            arr: numpy array, alpha: grid width i.e. power of 2, x: coordinate.
        """

        # lsh type formula to find the correct grid cell
        probe = int(math.floor((x-grid_arr[0])/self.alpha))
        
        if grid_arr.shape[0] == 1:
            return [grid_arr[0], grid_arr[0] + self.alpha]

        if probe == len(grid_arr)-1:
            return [grid_arr[probe], grid_arr[probe]+self.alpha]
        if probe == 0:
            return [grid_arr[probe], grid_arr[probe+1]]

        if (grid_arr[probe] <= x and grid_arr[probe+1] >= x):
            return [grid_arr[probe], grid_arr[probe + 1]]

        return []
        

    def _partition_data(self):
        """
            partition takes an array of points and partitions
            the space in a grid with each grid cell of width alpha
        """
        # create multiple partitions for the data. return array of partitions
        xmin, xmax = np.floor(np.amin(self.arr[:, 0])), np.ceil(np.amax(self.arr[:, 0]))
        ymin, ymax = np.floor(np.amin(self.arr[:, 1])), np.ceil(np.amax(self.arr[:, 1]))

        # create verticle and horizontal lines
        v_lines = np.arange(xmin, xmax, self.alpha)
        h_lines = np.arange(ymin, ymax, self.alpha)

        for x in self.arr:
            v_bound = self._find_cell(v_lines, x[0])
            h_bound = self._find_cell(h_lines, x[1])
            b = ' '.join([str(elem) for elem in v_bound + h_bound])
            if b not in self.buckets:
                self.buckets[b] = []
            self.buckets[b].append(x)

    def get_buckets(self):
        """
         return a dictionary with key as the coord. and value as points inside the gridof the buckets
         {'x_1 x_2 y_1, y_2': [[7.3, 2.9], [7.7, 2.6], [7.7, 2.8], [7.4, 2.8]] }

        """
        return self.buckets