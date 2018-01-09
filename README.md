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

Input Example:
1, 101, 5.0
1, 102, 3.0
1, 103, 2.5
2, 101, 2.0
2, 102, 2.5
2, 103, 5.0
2, 104, 2.0
3, 101, 2.5
3, 104, 4.0
3, 105, 4.5
3, 107, 5.0
4, 101, 5.0
4, 103, 3.0
4, 104, 4.5
4, 106, 4.0
5, 101, 4.0
5, 102, 3.0
5, 103, 2.0
5, 104, 4.0
5, 105, 3.5
5, 106, 4.0
Output Example:
Co-occurrence:
user 1: 44 31.5 39 33.5 15.5 18 5 => recommend 104
user 2: 45.5 32.5 41.5 36 15.5 20.5 4 => recommend 106
user 3: 42.5 20 26.5 40 27 17.5 16 => recommend 103
user 4: 63 37 53.5 55 26 33 9.5 => recommend 102
user 5: 68 42.5 56.5 59 32 34.5 11.5 => recommend 107
