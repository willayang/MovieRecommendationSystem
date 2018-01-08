import sys
import numpy as np
#from sklearn.metrics.pairwise import cosine_similarity

# percentage of top similar users. e.g., 1.0 is 100%, 0.5 is 50%
def cosine_similarity (a, b)
    c = a * b
    
TOP_K = 1.0 

def error_input(cause, data):
  if cause == 1:
    print 'Wrong input len at line \n' + data 
  elif cause == 2:
    print 'Same user rate movie ' + data + ' more than once'

def check_ratings(users, movies, ratins):
  # check same user doesn't rate same movie more than once
  pass

def check_input(fields):
  if len(fields) != 3:
    error_input(1, line)
    return False
  for i in range(3):
    fields[i] = fields[i].strip()
    if len(fields[i]) == 0:
      error_input(1, line)
      return False

'''
Create all_ratings matrix, with num_of_movie as rows, and num_of_user as cols
         user_1  user_2 user_3 ... user_n
movie_1  1.5     0.0    2.0    ... 0.0
movie_2  0.0     0.0    1.0    ... 3.5
movie_3  0.0     2.5    0.0    ... 0.0
...
movie_n  1.0     0.0    0.0    ... 2.5

The reason to create this matrix:
  Both of the co-occurence matrix and similarity matrix, need to multiply
  with the user ratings, which are one vector for each user. So to multiply
  with all the user ratings, it is essentially the same as multiplying with
  the matrix above -- all together for all users at one time, rather than
  writing a loop, and do matrix-vector multiplications one at a time.
'''

'''
  idx_to_user = [user_1, user_2, ... user_n]
  user_to_idx = {user_1:0, user_2:1, ... user_n:n-1}
'''
def construct_rating_matrix():
  users = []
  movies = []
  ratings = []
  user_to_idx = {}
  movie_to_idx = {}
  # create user list and movie list
  # store all input data for later use 
  #for line in sys.stdin:
  with open('input', 'r') as f:
    for line in f:
      fields = line.split(',') # this should split each input line to 3 words: [user, movie, rate]
      if check_input(fields) == False:
        return
      for i in range(3):
        fields[i] = fields[i].strip(); # strip out all space at the beginning and end of string
      users.append(fields[0])
      movies.append(fields[1])
      ratings.append(float(fields[2])) 
      if fields[0] not in user_to_idx:
        user_to_idx[fields[0]] = len(user_to_idx) # add new key:value pair, e.g., user_2:1
      if fields[1] not in movie_to_idx:
        movie_to_idx[fields[1]] = len(movie_to_idx)
  # create mapping between index and users/movies
  idx_to_user = np.zeros(len(user_to_idx), dtype='int') # len(user_to_idx) is number of users
  idx_to_movie = np.zeros(len(movie_to_idx), dtype='int')
  for u in user_to_idx:
    idx_to_user[user_to_idx[u]] = u
  for m in movie_to_idx:
    idx_to_movie[movie_to_idx[m]] = m
  # create the (sparse) rating matrix, each row is one movie
  # each colunm is one user
  all_ratings = np.zeros((len(movie_to_idx), len(user_to_idx))) # number of movie X number of users
  for i in range(len(users)):
     user = users[i]
     movie = movies[i]
     rating = ratings[i]
     # insert non zero rates into all_rating matrix, indexed by movie index as row index, and
     # user index as column index.
     all_ratings[movie_to_idx[movie], user_to_idx[user]] = rating
  '''
  print 'all_ratings:'
  print all_ratings
  print 'idx_to_movie:'
  print idx_to_movie
  print 'idx_to_user:'
  print idx_to_user
  print 'movie_to_idx:'
  print movie_to_idx
  print 'user_to_idx:'
  print user_to_idx
  '''
  return all_ratings, idx_to_movie, idx_to_user

def compute_similarity(all_ratings):
  num_users  = np.shape(all_ratings)[1] # get the dimension of columns, which is the number of columns (user)
  similarity_matrix = np.zeros((num_users, num_users))
  # .T is matrix transpose. Remember all_ratings is movie as row, user as column. To compute the
  # similarity between user, need to transpose to user as row, movie as column. Since the cosine_similarity
  # function below only compute similarity between rows.
  all_ratings_T = all_ratings.T
  for i in range(num_users):
    # This function computes the cosine similarity between row_i with all other rows (including
    # itself. Each time the function returns a vector, each entry is a similarity score of row_i
    # with another row_j. This vector is the i-th row in the similarity matrix.
    non_zero_idx = np.nonzero(all_ratings_T[i,:])
    similarity_matrix[i:,] = cosine_similarity(all_ratings_T[i,non_zero_idx], all_ratings_T[:,non_zero_idx[0]])
  print similarity_matrix
  return similarity_matrix   
  
def make_recommendation_user_based(all_ratings, similarity, idx_to_movie):
  '''
  The following 3 lines tranform the all_rating matrix into only 1 and 0. 
  Those non zero ratings become 0, 0 ratings become 1. This matrix is call 'movie_mask'
  since we only want to recommend unrated movies, those already rated will be masked off.
  By multiplying with this 'movie_mask', already rated movies will becomes 0, hence not 
  able to be recommended again.
  '''
  movie_mask  = all_ratings / all_ratings  # divide by itself, so non zero ratings becomes 1, BUT 0 divide by itself becomes NA 
  movie_mask[np.isnan(movie_mask)] = 0     # np.isnan checks if a number is NA. This line makes all the NA to be 0
  movie_mask = 1 - movie_mask              # 1 subtract the matrix, 1 becomes 0, 0 becomes 1
  num_users  = np.shape(all_ratings)[1]
  # if TOP_K = 1.0, pick all other users as neighbor
  # if TOP_K < 1.0, pick a subset of most similar ones as neighbor. For example,
  # when TOP_K = 0.5, pick the top 50% of most similar other users as neighbors. 
  top_users = int((num_users - 1) * TOP_K) # compute how many top similar users to use. If pick 100%, then there are num_users - 1 neighbors
  # argsort sorts an array, but returns the index rather than the value. For example, to sort [2,3,1], it returns [2,0,1] which are the index
  # of '1','2','3'.
  # after getting the index of the sorted array, only pick the top similar ones by [:,num_users-top_users-1:num_users-1]. remember similarity
  # is sorted from small to big, so the big ones are more similar, hence pick the last 'top_users' ones as the top most similar neighbors.
  top_similar = np.argsort(similarity, axis = 1)[:,num_users-top_users-1:num_users-1]
  '''
  This is another mask, only top similary users are 1, other unselected users are 0. Similar
  to the 'movie_mask' above, by multiplying with the mask matrix, unwanted entries will be 0.
  '''
  similarity_mask = np.zeros((num_users, num_users))
  for i in range(num_users):
    similarity_mask[i, top_similar[i]] = 1 # initialize to be all 0 matrix above, set to 1 only for those top similar neighbors
  similarity = similarity * similarity_mask # multiplying the similarity matrix by the mask, only top similar neighbors's similarity scores remain non zero
  rating_mask = 1 - movie_mask
  rating_mask = np.dot(rating_mask, similarity_mask)
  new_ratings = np.dot(all_ratings, similarity) # compute the rating for unrated movie, np.dot is matrix multiply
  new_ratings = new_ratings / rating_mask
  new_ratings[np.isnan(new_ratings)] = 0
  new_ratings = new_ratings * movie_mask # then the new rating multiply with the movie_maks above, so only unrated movies remain non zero
  max_rate_idx = np.argmax(new_ratings, axis = 0) # arxmax pick the maximum rating, return its index
  recom = idx_to_movie[max_rate_idx] # get the movie name using the movie index
  return recom 

# This is a 'main' function in python way
if __name__ == '__main__':
  all_ratings, idx_to_movie, idx_to_user = construct_rating_matrix()
  ''' co-occurence matrix method
  co_occurence = construct_co_occurence(all_ratings)
  recom = make_recommendation_co_occurence(all_ratings, co_occurence, idx_to_movie)
  for i in range(len(recom)):
    print 'User ' + str(idx_to_user[i]) + ': recommend ' + str(recom[i])
  '''
  ''' user based method '''
  similarity = compute_similarity(all_ratings)
  recom = make_recommendation_user_based(all_ratings, similarity, idx_to_movie)
  for i in range(len(recom)):
    print 'User ' + str(idx_to_user[i]) + ': recommend ' + str(recom[i])
  
  
