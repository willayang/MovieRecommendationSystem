import sys
import numpy as np

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
  return True 

def construct_rating_matrix():
  users = []
  movies = []
  ratings = []
  user_to_idx = {}
  movie_to_idx = {}
  # create user list and movie list
  # store all input data for later use 
  for line in sys.stdin:
    fields = line.split(',')
    if check_input(fields) == False:
      return
    for i in range(3):
      fields[i] = fields[i].strip();# delete the withespace
    users.append(fields[0])
    movies.append(fields[1])
    ratings.append(float(fields[2])) 
    if fields[0] not in user_to_idx:
      user_to_idx[fields[0]] = len(user_to_idx)
    if fields[1] not in movie_to_idx:
      movie_to_idx[fields[1]] = len(movie_to_idx)
  # create mapping between index and users/movies
  idx_to_user = np.zeros(len(user_to_idx), dtype='int')
  idx_to_movie = np.zeros(len(movie_to_idx), dtype='int')
  for u in user_to_idx:
    idx_to_user[user_to_idx[u]] = u
  for m in movie_to_idx:
    idx_to_movie[movie_to_idx[m]] = m
  # create the (sparse) rating matrix, each row is one movie
  # each colunm is one user
  all_ratings = np.zeros((len(movie_to_idx), len(user_to_idx)))
  for i in range(len(users)):
     user = users[i]
     movie = movies[i]
     rating = ratings[i]
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
   
def construct_co_occurence(all_ratings):
  num_movies = np.shape(all_ratings)[0]#get the length of all_rating[0]
  co_occurence = np.zeros((num_movies, num_movies))
  for i in range(num_movies):
    movie_rates_i = all_ratings[i]#?
    co_occurence[i,i] = np.shape(np.nonzero(movie_rates_i))[1]#?
    for j in range(i+1, num_movies):
      movie_rates_j = all_ratings[j]
      rates = movie_rates_i * movie_rates_j
      co_occurence[i,j] = np.shape(np.nonzero(rates))[1]
      co_occurence[j,i] = np.shape(np.nonzero(rates))[1]
  '''
  print 'Co-occurence:'
  print co_occurence 
  '''
  return co_occurence

def make_recommendation(all_ratings, co_occurence, idx_to_movie):
  mask  = all_ratings / all_ratings
  mask[np.isnan(mask)] = 0
  mask = 1 - mask
  new_ratings = np.dot(co_occurence, all_ratings)
  new_ratings = new_ratings * mask
  max_rate_idx = np.argmax(new_ratings, axis = 0)
  recom = idx_to_movie[max_rate_idx]
  '''
  print 'mask:'
  print mask
  print 'new_ratings:'
  print new_ratings
  print 'Recom:'
  print recom
  '''
  return recom 

if __name__ == '__main__':
  all_ratings, idx_to_movie, idx_to_user = construct_rating_matrix()
  co_occurence = construct_co_occurence(all_ratings)
  recom = make_recommendation(all_ratings, co_occurence, idx_to_movie)
  for i in range(len(recom)):
    print 'User ' + str(idx_to_user[i]) + ': recommend ' + str(recom[i])
