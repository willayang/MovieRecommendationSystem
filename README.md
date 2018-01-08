# MovieRecommendationSystem
Crafing different algorithm for movie recommendation
1 using co-occurence alogrithm: multiplying the symmetric square sparse cooccurrence
matrix with user preference vector to produce a vector that lead to
recommendation, choose the item user doesn’t have and with highest values in the
vector
2 User-based recommendation algorithm:
for every other user w
  compute a similarity s between u and w
   retain the top users, ranked by similarity, as a
  neighborhood n
for every item i that some user in n has a preference for,
  but that u has no preference for yet
  for every other user v in n that has a preference for i
    compute a similarity s between u and v (or use previous
    computed values)
    incorporate v’s preference for i, weighted by s, into
    a running average
return the top items, ranked by weighted average
