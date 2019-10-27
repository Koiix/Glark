

def change(data):
    data = data[0:2]
    return data

b = 'hello'

ba = bytes(b, 'UTF-8')

print(ba)

x = change(ba)

newdata = ba[len(x):len(ba)]
print(newdata)
