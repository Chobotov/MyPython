cortej = ('1','2','3','4','5','6','7','8','9','10')
dictionary = {}


def add(i):
    dictionary[i] = i ** 2


for i in range(1, 50):
    if i % 2 == 0:
        add(i)

print(cortej)
print(dictionary)
