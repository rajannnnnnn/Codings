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
      [0,1,0,1,0,1],
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
print(land)
print(score)
print(i_,j_)
print(max_area)
