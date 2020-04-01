#!/usr/local/bin/python3

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

def edge_strength_map(input_image):
    # calculate "Edge strength map" of an image
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels

def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

#main program
input_filename = sys.argv[1]
row_coord = int(sys.argv[2])
col_coord = int(sys.argv[3])

# load in image
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength_map(input_image) + 1

# edge strength map
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# =============================================================================
# 1. Simple Bayes Net
# =============================================================================

input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength_map(input_image) + 1

# compute the ridge y-coordinates with maximum 
ridge = edge_strength.argmax(axis=0)

imageio.imwrite('output_simple.jpg', draw_edge(input_image, ridge, (0, 0, 255), 5))
print("Checkpoint 1")

# =============================================================================
# 2. HMM with Viterbi
# =============================================================================

input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength_map(input_image) + 1

# compute emission probabilities
emission_prob = -log(edge_strength/sum(edge_strength, axis = 0))

#create viterbi matrix
viterbi_matrix = ones(emission_prob.shape)
viterbi_matrix[:,0] = emission_prob[:,0]

for col in range(1, edge_strength.shape[1]):
    for row_j in range(edge_strength.shape[0]):
        
        row_i = 0
        trans_array = array([])
        
        while row_i < edge_strength.shape[0]:
            
            #calculate transition probabilities
            p_ij = 1/(2**(abs(row_j - row_i)+1))
            trans_array = append(trans_array, p_ij)

            row_i += 1
        
        #normalizing transition probabilities
        trans_array_norm = -log(trans_array/sum(trans_array))
        
        viterbi_matrix[row_j, col] = min(trans_array_norm + viterbi_matrix[:, col-1]) + emission_prob[row_j, col]

ridge = viterbi_matrix.argmin(axis=0)

imageio.imwrite('output_map.jpg', draw_edge(input_image, ridge, (255, 0, 0), 5))

print("Checkpoint 2")

# =============================================================================
# 3. HMM with human input
# =============================================================================

input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength_map(input_image) + 1

#row_coord = 44
#col_coord = 159

# compute emission probabilities
emission_prob = edge_strength/sum(edge_strength, axis = 0)

#tweaking emission probablities for human input
em_array = array([])
for row_i in range( emission_prob.shape[0] ):
    em = 1/(2**(abs(row_coord - row_i)+1))
    em_array = append(em_array, em)

#normalizing emission probabilities and appending back to emission probability array
em_array_norm = em_array/sum(em_array)
emission_prob[:, col_coord] = em_array_norm

#taking -log of emission probabilities
emission_prob = -log(emission_prob)

#create viterbi matrix
viterbi_matrix = ones(emission_prob.shape)
viterbi_matrix[:,0] = emission_prob[:,0]

for col in range(1, edge_strength.shape[1]):
    for row_j in range(edge_strength.shape[0]):
        
        row_i = 0
        trans_array = array([])
        
        while row_i < edge_strength.shape[0]:

            #calculate transition probabilities and append to array
            p_ij = 1/(2**(abs(row_j - row_i)+1))
            trans_array = append(trans_array, p_ij)

            row_i += 1
        
        #normalizing transition probabilities
        trans_array_norm = -log(trans_array/sum(trans_array))
                
        viterbi_matrix[row_j, col] = min(trans_array_norm + viterbi_matrix[:, col-1]) + emission_prob[row_j, col]

ridge = array([])
ridge = append( ridge, argmin(viterbi_matrix[:,-1]) )

for col in range(viterbi_matrix.shape[1]-2, -1, -1):
    int_max = +2147483647
    
    bound = int(ridge[-1])
    
    #Setting boundary conditions 7 pixel wide
    viterbi_matrix[:bound-3, col] = int_max
    viterbi_matrix[bound+4:, col] = int_max
    
    ridge_element = argmin(viterbi_matrix[:,col])
    ridge = append( ridge, ridge_element )

ridge = flip(ridge)

imageio.imwrite('output_human3.jpg', draw_edge(input_image, ridge, (0, 255, 0), 5))

print("Checkpoint 3")
print("Code has finished running")