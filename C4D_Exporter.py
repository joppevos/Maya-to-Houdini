
import c4d
import random
from c4d import Vector

def main():
    select = doc.GetActiveObjects(0)
    dict_variable = [{attr: lamp[c4d.REDSHIFT_LIGHT_PHYSICAL_EXPOSURE] for attr in attributes} for lamp in lamps]
    print(dict_variable)
    c4d.EventAdd()

main()