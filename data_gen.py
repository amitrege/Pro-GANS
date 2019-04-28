import numpy as np

def get_sample(mean, stdev):
    return np.random.multivariate_normal(mean, (stdev**2)*np.identity(2))

def gen_mixture(no_of_dist, dataset_size, scaling_factor = (100, 10)):
    # Generate means and stdev of the mixture
    mean = np.random.rand(no_of_dist, 2)* scaling_factor[0]
    stdev = np.random.rand(no_of_dist)* scaling_factor[1]

    # Generate dataset
    idx = np.random.randint(0, high = no_of_dist, size = dataset_size)
    mean_arr = mean[idx]
    stdev_arr = stdev[idx]

    data = np.zeros((dataset_size, 2))
    for i in range(dataset_size):
        data[i] = get_sample(mean_arr[i], stdev_arr[i])
    
    return idx, data, mean, stdev

# Fixed size of images : 64 x 64 x 1
# For simplicity keep size of squares to be exponents of 2 i.e. 2, 4, 8 ...
def draw_square(im, square_size, top_left = None):
    if top_left is None:
        top_left = np.random.randint(0, high = 8 - square_size, size = 2)
    #top_right = top_left + np.array([0, square_size])
    #bottom_left = top_left + np.array([square_size, 0])
    #bottom_right = top_left + np.array([square_size, square_size])

    # Set colour 
    im[top_left[0] : top_left[0] + square_size, top_left[1] : top_left[1] + square_size] = 1

    return im, top_left

def non_overlapping_square(im, no_of_squares, square_size):
    bad_corners = True
    while bad_corners:
        top_left = np.random.randint(0, high = 8 - square_size - 1, size = (no_of_squares, 2))
        new_im = np.copy(im)
        found_combination = False
        for i in range(0, no_of_squares):
            relevant_square = new_im[top_left[i][0]: top_left[i][0] + square_size, top_left[i][1] : top_left[i][1] + square_size] 
            neighbors = relevant_square[relevant_square == 1]
            if neighbors.shape[0] == 0:
                draw_square(new_im, square_size, top_left[i])
                if i == no_of_squares - 1:
                    found_combination = True
            else:
                bad_corners = True
                break

        if bad_corners and not found_combination:
            continue
        bad_corners = False
    return new_im



def gen_square_dataset(no_of_squares, square_size, overlap):
    im = np.zeros((8,8))

    idx = []
    if overlap:
        for i in range(no_of_squares):
            im, ind = draw_square(im, square_size)
            idx.append(ind)
    else:
        im = non_overlapping_square(im, no_of_squares, square_size)

    return im

i = gen_square_dataset(4, 2, False)
print(i)
