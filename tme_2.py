s = 7
t = 10
house = []
answer_apples = []
answer_oranges = []
num = 0

apples_fallen = 0
oranges_fallen = 0
house.append(t)

a = 4
b = 12

m = 3
n = 3

apples = [2,3,-4]
oranges = [3,-2,-4]

""" for i in range(s,t+1):
    for j in apples:
        if i  == j+a:
            apples_fallen+=1
    for k in oranges:
        if i == k+b:
            oranges_fallen+=1 """

apples_fallen = [apples_fallen +1 for i in range(s,t+1) for j in apples if i == j+a]
oranges_fallen = [oranges_fallen+1 for i in range(s,t+1) for k in oranges if i == k+b]

print(len(apples_fallen))
print(len(oranges_fallen))


