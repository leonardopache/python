l = list(range(20, 30))

for __ in l:
    print('Just iterate')
else:
    print('loop finished')

for i, val in enumerate(l):
    print(i, val)

#set comprehensions
s = {i for i in l if not i % 2}
print(s)

# 3 x 3 matrix
zero_matrix = [[0 for _ in range(3)] for _ in range(3)]
for row in zero_matrix:
    print(row)

#recursion
def string_p(s):
    if s:
        print(s[-1], s[0])
        string_p(s[:-1])

string_p('Leonardo')
