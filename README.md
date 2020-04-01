B551: Games and Bayes
===================================

**Part 1: IJK**

The given problem is to implement a game similar to the famous 2048. This
problem can be solved using the mini-max algorithm. The given program has to
explore the whole search tree using the depth first search (DFS) algorithm and
make a decision based on the back tracked utility values. The solution can be
implemented using two methods. In the first method, a stack is used to explore
the tree using the DFS algorithm. The second method is employed recursively. We
have followed the latter method. Below is the list of functions we have used to
solve the problem.

**Terminal(board)**

This function checks if a particular state is the terminal node of the tree or
not. It does this by checking whether there is a 'k' present on the board or
whether the board is filled with letters and there are no spaces present.
Returns a True value if the state is the terminal state and false otherwise.

**Utility(board, p1)**

As the name suggests, the function returns the utility of the terminal node. In
this case, 'Human' is min on the score. On the other hand, the weights of
letters on the board representing 'human' are subtracted from the score.

For example, the following commands are entered in the command line

python3 IJK.py ai human det

In this case player1 is the AI and player two is human. So in this particular
case, AI will be represented by capital letters and human will be represented by
lower case letters. The weights assigned to capital letters in this case will be
added to the score, on the other hand, 'ai' is MAX. Depending on the order of
the arguments entered while running the program, each letter is given a weight
depending on its position in the alphabetical series for eg A=1, B=2,C=3.... The
weights of letters on the board representing 'ai'(capital letters) are added to
the score and the weights of the letters on the board representing 'human'
(lower case letters) are subtracted from the score.

**Min/Max(move, game: Game_IJK, depth, p1, alpha, beta)**

These are two separate functions but work similarly. The move parameter takes
one of the given permitted direction letters. The d=Depth parameter calculates
the depth for the current node. It updates the depth variable and passes it on
to the next function in the recursion process. The next function takes the
current value and updates it. The process returns a utility value when it
reaches a certain depth. The p1 parameter is the parameter passed to the
functions from the next_move function. This parameter is useful in determining
the utility function for the given case. The alpha and beta values are used for
the alpha beta pruning algorithm. The loop iterates over all the directions and
passes them into a recursive function. It compares the alpha and the beta
values, and returns alpha or beta (depending on the type of function) value if
the alpha value is greater than the beta value and the type of the move
accompanied by the value. This move is then propagated upwards if it is an
efficient solution.

**Next move**

This is the function that IJK.py calls for implementing the AI logic. Here, the
tree starts with a min if the first node is 'human' and it starts with a max if
first player is AI. We write two if conditions that execute the previous
statement in the form of code. This function returns the move to be done after
expanding the tree and doing all the calculations on the present state of the
game.

In the given implementation we have not expanded the tree till the terminal node
is reached. We have then expanded it till a particular depth. This has proven to
be efficient and faster. We have tested the code for 'human vs ai' configuration
for a depth of 4. After doing human testing and making a few changes to my code,
I decided to do an AI vs AI match. AI1 will expand till a depth of 6 and AI2
will expand till a depth of 4. The AI with a better depth worked quite nicely,
but the match didn’t have an undisputed winner. The player with that has more
depth should have won, but this was not happening. So I made a change to my
utility function. We added the number of empty tiles present in the state. This
did make a significant difference. And thus in the following tests, the AI with
more depth won with a huge margin as expected.

![alt text](https://github.iu.edu/cs-b551-fa2019/svbhakth-mabartak-sbhujbal-a2/blob/master/part1/IJK.png)

**Output for AI vs AI. AI representing capital letter has more depth.**

**Part 2: Horizon Finding**

**Approach:** The problem states that given an input image, we need to
distinctly identify the horizon. We use Bayes Net to solve this problem. The
code produces an edge strength map that measures how strong the image gradient
(local contrast) is at each point. The stronger the image gradient, higher will
be the chance that pixel lies along the ridgeline. For this we created a 2D
numpy array which measures the strength of each pixel in original image. Now, we
select the that pixel who’s edge strength is maximum and the corresponding row
co-ordinate. To generalize, this gradient data is our observed variables.

**Part 1: Simple Bayes Net**

In this approach, we use simple Bayes Net. We calculate the edge strength for
all the pixels in the input image. For each column, we find the maximum value of
the gradient and the corresponding row co-ordinate for the gradient. Plotting
the corresponding row of this pixel will result in the horizon line. In other
words, we want to estimate the most probable row for each column in the edge
strength matrix.

Output Image 1

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_simple/output_simple1.jpg)

Output Image 2

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_simple/output_simple4.jpg)

Output Image 3

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_simple/output_simple5.jpg)

Output Image 4

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_simple/output_simple8.jpg)

Output Image 5

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_simple/output_simple7.jpg)

In Simple Bayes Net implementation, the output image 2 is resulting into a
distorted line because the image has gradient maximum at those points. The
results can be made accurate ie. making the horizon line smoother by applying
Viterbi Algorithm.

**Part 2 : HMM with Viterbi Algorithm**

In this approach, we use Viterbi Algorithm to find the emission probabilities of
all the states. Initially we carry out all the steps as in Part 1: Simple Bayes
Net. Then, we calculate the emission probabilities of each state. This is done
by normalizing the edge strength along a column. The next step is to calculate
transition probabilities from each pixel from a column to each pixel in the next
column using a decreasing function and then normalizing these values. For this,
we have calculated the distance *d* from each pixel in one state to the next
state (difference in row indices) and using the function 1/2d+1 to assign
probabilities. The pixels further away will have lower probabilities.

Finally, we calculate maximum a posterior estimate using Viterbi algorithm using
a negative log of probabilities to prevent floating point underflow. The results
improved significantly compared to the simple Bayes network. But for some cases
we still fail to detect the ridge line. The results are given below.

Output Image 1

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_map/output_map.jpg)

Output Image 2

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_map/output_map4.jpg)

Output Image 3

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_map/output_map5.jpg)

Output Image 4

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_map/output_map7.jpg)

Output Image 5

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_map/output_map8.jpg)


**Part 3: HMM with human feedback**

HMM with human feedback is improvisation to the above algorithm. Human gives a
single (row coordinate, column coordinate) coordinate which lies on the ridge
line. For the given column index, we recalculate the emission probabilities such
that the row index given has the maximum emission probability. This is again
achieved using the function 1/2d+1, where *d* difference between the given row
index and any row in the given column. The pixels further away will have lower
probabilities and the pixel on the ridge line will have the maximum emission
probability. Later steps are aligned with the same steps as in Part 2: HMM with
Viterbi Algorithm. We have incorporated one more significant change in the code
which is to backtrack from the last column of the image and use a boundary to
check for the ridge element. We extract the row index of the ridge element with
the highest probability in the last column of the Viterbi matrix. Then we move
to the preceding column and check only in the pixels ‘in the neighborhood’ of
the row index extracted from the last column. We have defined this neighborhood
to be 8 pixels wide since one can assume the ridge element to be found in this
width (the ridge transitions smoothly, it does not jump around; so it is safe to
assume that the ridge element would be found in this 8-pixel wide window). We
iterate through the entire Viterbi matrix backwards and pick the highest
probabilities within our ‘pixel window’ and create the ridge line. The result of
output image is smoother and has significantly improved in some cases.

For eg: In the picture of Mount Rushmore, (mountain7.jpg), the algorithm is able
to sketch the ridge line almost perfectly. This is a vast improvement from the
results obtained in the previous algorithms.

Output Image 1

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_human/output_human1.jpg)

Output Image 2

![alt text](https://github.com/madhura42/Games-and-Bayes/blob/master/part2/output_human/output_human7.jpg)
