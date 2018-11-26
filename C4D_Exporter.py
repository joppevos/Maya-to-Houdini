import c4d
import json
from c4d import Vector
import pprint


def attr_return(lamp, attr):
    return eval('lamp[attr]')


class Exporter:

    def __init__(self):
        self.lamps = doc.GetActiveObjects(0)
        self.attributes = ['c4d.REDSHIFT_LIGHT_PHYSICAL_INTENSITY',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_SIZEX',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_SIZEY',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_EXPOSURE',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_COLOR',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_VISIBLE_IN_RENDER',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_BIDIRECTIONAL',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_BIDIRECTIONAL',
                           'c4d.REDSHIFT_LIGHT_PHYSICAL_AREA_GEOMETRY',
                           'c4d.REDSHIFT_LIGHT_AFFECTS_DIFFUSE',
                           'c4d.REDSHIFT_LIGHT_AFFECTS_SPECULAR',
                           'c4d.ID_BASELIST_NAME',
                           ]

    def attr_maker(self):
        """
        Returns all required attributes of each lamp in a dict
        """
        attr_list = [{attr: attr_return(lamp, eval(attr)) for attr in self.attributes} for lamp in self.lamps]
        for dic, lamp in zip(attr_list, self.lamps):
            # get scale
            vec = lamp.GetAbsScale()
            scale = (vec[0], vec[1], vec[2])
            dic['scale'] = scale
        return attr_list

    def write_file(self):
        dump = json.dumps(self.attr_maker())
        print(dump)
        file = open('C:/Users/render/Desktop/', 'w')
        file.write(attrdict)
        file.close()


instance = Exporter()

if __name__ == '__main__':
    pprint.pprint(instance.write_file())