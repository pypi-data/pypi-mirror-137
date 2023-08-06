import tensorflow as tf


def gridify_tensor(tensor, grid_size=128):
    zero_pad_height = tensor.shape[1] % grid_size
    zero_pad_width = tensor.shape[2] % grid_size

    paddings = tf.constant([[0, 0], [0, grid_size - zero_pad_height], [0, grid_size - zero_pad_width], [0, 0]])
    tensor = tf.pad(tensor, paddings, "CONSTANT")
    tensor_grid = []
    tensor_height = tensor.shape[1] // grid_size
    tensor_width = tensor.shape[2] // grid_size
    for i in range(tensor_height):
        for j in range(tensor_width):
            tensor_slice = tensor[:, (i*grid_size):(i*grid_size)+grid_size, (j*grid_size):(j*grid_size)+grid_size, :]
            tensor_grid.append(tensor_slice)

    return tensor_grid, (tensor_height, tensor_width)


def tensorfy_grid(grid, grid_structure, original_tensor_shape):
    tensor_rows = []
    for i in range(grid_structure[0]):
        tensor_row = tf.zeros(grid[0].shape)
        for j in range(grid_structure[1]):
            current_tensor = grid[i*grid_structure[1]+j]
            if j == 0:  # Inefficient
                tensor_row = current_tensor
            else:
                tensor_row = tf.concat([tensor_row, current_tensor], 2)
        tensor_rows.append(tensor_row)
    tensor = tf.concat(tensor_rows, 1)

    return tensor[:, 0:original_tensor_shape[1], 0:original_tensor_shape[2], :]
