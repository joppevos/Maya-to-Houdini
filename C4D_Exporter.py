
import c4d
import random
from c4d import Vector

def main():
    select = doc.GetActiveObjects(0)
    dict_variable = [{attr: lamp[c4d.REDSHIFT_LIGHT_PHYSICAL_EXPOSURE] for attr in attributes} for lamp in lamps]
    print(dict_variable)
    c4d.EventAdd()

main()


import c4d
#Welcome to the world of Python

def rand():
    import random
    x = random.randrange(1,1000,1)
    return x

def update():
    obj = doc.GetObjects()
    v = c4d.Vector(rand(),rand(), rand())
    obj[0].SetRelPos(v)

def main():
    if frame%10:
        update()