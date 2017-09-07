import numpy


class Data:
    def __init__(self, path):

        data_file = open(path, 'r')

        self.data_list = data_file.readlines()

        data_file.close()

        self.curr_line = 0

        pass

    def next_batch(self, size, conv=False):

        next_line = self.curr_line + size

        array = self.data_list[self.curr_line:next_line]

        self.curr_line += size

        if self.curr_line > 60000:
            self.curr_line = 0

        batch_matrix = numpy.array([], dtype=numpy.float64).reshape(0, 784)
        batch_targets = numpy.array([], dtype=numpy.float64).reshape(0, 10)

        for record in array:
            all_values = record.split(',')
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            targets = numpy.zeros(10) + 0.01
            targets[int(all_values[0])] = 0.99
            batch_matrix = numpy.vstack([batch_matrix, inputs])
            batch_targets = numpy.vstack([batch_targets, targets])

        if conv:
            batch_matrix = batch_matrix.reshape([-1, 28, 28, 1])

        vals = {
            'x': batch_matrix,
            'y': batch_targets
        }

        return vals

        pass
    pass
