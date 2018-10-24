import hou
import json


def create_light(name):
    """ create lights in the scene"""

    # Get scene root node
    sceneroot = hou.node('/obj/')
    # Create light
    light = sceneroot.createNode('hlight::2.0', '{}'.format(name))
    light.setParms({'light_type': 'grid'})
    return light


def read_json():
    """ let user select the attribute filepath to read  """

    filepath = hou.ui.selectFile()
    newpath = filepath.replace('/', '\\')
    read_file = open('{}'.format(newpath), 'r')
    lampattr = json.load(read_file)
    return lampattr


def translate_light():
    """ position the light with correct scale,rotation and translation """

    lampattr = read_json()
    for lamp in lampattr:
        name = lamp.get('name')
        light = create_light(name)
        translates = lamp.get('translate')
        comment = lamp.get('filename')
        rotations = lamp.get('rotate')
        scales = lamp.get('scale')
        for translate in translates:
            light.setParms({'tx': translate[0], 'ty': translate[1], 'rz': translate[2]})
        for rotation in rotations:
            light.setParms({'rx': rotation[0], 'ry': rotation[1], 'rz': rotation[2]})
        for scale in scales:
            light.setParms({'areasize1': scale[0], 'areasize2': scale[1]})

        # create comment-description for each light
        light.setGenericFlag(hou.nodeFlag.DisplayComment, True)
        light.setComment(comment)


def attributes_light():
    """ add all the attributes to the light"""

# TODO: ADD ATTRIBUTES TO RSLIGHT
# intensity = 'multiplier' x
# exposure =  x
# color = 'tintcolor' x
# affect Diffuse x
# Affect Specular x
# Bi-directional
# visibile
# aovLightGroup
# volumeRayContributionScale


    # Display creation message
    # hou.ui.displayMessage('Lights have been generated!')


# call function
translate_light()

