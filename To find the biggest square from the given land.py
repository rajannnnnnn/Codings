"""
A farmer wants to farm their land with the maximum area where good land is present.
The "land" is represented as a matrix with 1s and Os, where 1s mean good land and Os
mean bad land. The farmer only want to farm in a square of good land with the maximum
area. Please help the farmer to find the maximum area of the land they can farm in
good land.


"""
def function(i,j,dim):
    if len(land)>i+dim and len(land[0])>j+dim:
        for _ in range(dim):
            if not (land[i+_][j+dim]==1 and land[i+dim][j+_]==1):
                return dim
        if land[i+dim][j+dim]==1:
            return function(i,j,dim+1)
        else:
            return dim
    else:
        return dim

land=[[0,1,1,1,0,1],
      [0,1,1,1,0,1],
      [0,1,1,1,1,1],
      [0,1,1,1,0,1]]

score=[]
max_area=False
for i in range(len(land)):
    score.append([])
    for j in range(len(land[i])):
        if land[i][j]==1:
            area = function(i,j,1)
            score[-1].append(area)
            if area>max_area:
                max_area = area
                i_=i
                j_=j
        else:
            score[-1].append(0)
for i in range(len(land)):
    for j in range(len(land[i])):
        print(land[i][j],end=" ")
    print()
print()
for i in range(len(score)):
    for j in range(len(score[i])):
        print(score[i][j],end=" ")
    print()
print()
print(f"The biggest good square place is of length {max_area} square starts from {i_},{j_} to {i_+max_area-1},{j_+max_area-1}")
