lista=[]
lista2=[]
num=0

for i in range (1,121):
    lista.append(i)


num=int(input("Ingrese un número entre 1 y 120: "))

while num>120:
    num=int(input("Ingrese un número entre 1 y 120: "))


while num!=-1:
    for j in range(len(lista)):
        if num == lista[j-1]:
            lista2 = lista.pop(lista[j-1])
    break


print(lista)
print(lista2)