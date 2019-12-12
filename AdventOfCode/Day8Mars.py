import numpy as np
import matplotlib.pyplot as plt

def reshape_input(num_string, width, height):
    # Takes input number and reshapes it as appropriate
    n_elements = len(str(num_string))
    n_layers = n_elements // (width*height)

    # convert string to list
    input_list = [int(x) for x in str(num_string)]
    # reshape as array, don't ask how this works
    return np.reshape(input_list, [n_layers,height,width])


def min_zeros(input_array):
    # finds layer of array with minimal zeros
    num_zeros = np.sum(np.sum(input_array==0, axis=1), axis=1)

    layer_idx = num_zeros.argmin()
    return layer_idx, input_array[layer_idx, :, :]


def produce_output(num_string, width, height):
    # produces the arbitrary required output for this task
    input_array = reshape_input(num_string, width, height)
    idx, layer = min_zeros(input_array)

    return np.sum(layer == 1)*np.sum(layer == 2)


def make_picture(num_string, width, height):
    input_array = reshape_input(num_string, width, height)

    output_image = -np.ones([height, width])

    layer_idx = 0
    while (output_image == -1).any():
        mask1 = (input_array[layer_idx, :, :] == 1) & (output_image == -1)
        mask0 = (input_array[layer_idx, :, :] == 0) & (output_image == -1)
        output_image[mask1] = 1
        output_image[mask0] = 0
        layer_idx += 1

    plt.imshow(output_image)

    return output_image