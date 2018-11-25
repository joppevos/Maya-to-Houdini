import c4d
import random
from c4d import Vector


def attr_return(lamp, attr):
    return eval('lamp[attr]')


def main():
    attributes = ['c4d.REDSHIFT_LIGHT_PHYSICAL_INTENSITY', 'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_SIZEX']
    lamps = doc.GetActiveObjects(0)
    dict_variable = [{attr: attr_return(lamp, eval(attr)) for attr in attributes} for lamp in lamps]
    print(dict_variable)


if __name__ == '__main__':
    main()
