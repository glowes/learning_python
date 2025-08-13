def add(a):
    """
    add a to 1
    """

    b = a + 1
    print(a," if you add one, you get: ",b)
    return b


def Mult(a,b):
    c = a * b
    return(c)
    print("This is not printed")



def countWords(s):
    words_list = s.split(" ")
    print(f"frase passada: {s}")
    return len(words_list)


res = add(5)
print(res)
res = Mult(5,6)
print(res)
res = countWords("Love you Sofia")
#print(res) 
#help(add)
print(f"palavras na frase: {res}")