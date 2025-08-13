#Type your code here

def safe_divide():

    nm  = int(input("insert the numerador: "))
    dnm = int(input("insert the denominator: "))
    res = 0
    try:
       res =  nm/dnm
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return
    except:
        print("Some error has occur")
    finally:
        print("Process finish")
        return res


print(safe_divide())