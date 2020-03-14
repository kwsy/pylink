lst = [1]


a = 10
def test():
    a = 110
    lst = lst.append(2)

test()

print(lst)