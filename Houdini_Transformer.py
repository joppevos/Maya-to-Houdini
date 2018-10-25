import hou
import json


def create_light(name):
    """ create lights in the scene"""

    # Get scene root node
    sceneroot = hou.node('/obj/')
    # Create light
    light = sceneroot.createNode('rslight', '{}'.format(name))
    light.setParms({'light_type': 3})
    return light


def read_json():
    """ let user select the attribute filepath to read  """
    filepath = hou.ui.selectFile()
    if filepath.lower().endswith('.json'):
        read_file = open('{}'.format(filepath), 'r')
        lampattr = json.load(read_file)
        return lampattr
    else:
        hou.ui.displayMessage('Please select a .json file ')


def translate_light():
    """ position the light with correct scale,rotation and translation """

    lampattr = read_json()
    for lamp in lampattr:
        name = lamp.get('name')
        light = create_light(name)
        translates = lamp.get('translate')
        rotations = lamp.get('rotate')
        scales = lamp.get('scale')
        colors = lamp.get('color')
        for translate in translates:
            light.setParms({'tx': translate[0], 'ty': translate[1], 'tz': translate[2]})
        for rotation in rotations:
            light.setParms({'rx': rotation[0], 'ry': rotation[1], 'rz': rotation[2]})
        for scale in scales:
            light.setParms({'areasize1': scale[0]+1, 'areasize2': scale[1]+1})
        for color in colors:
            light.setParms({'light_colorr': color[0], 'light_colorg': color[1], 'light_colorb': color[2]})
        set_attributes(light, lamp)


def set_attributes(light, lamp):
    """ set the attributes for the light """
    comment = lamp.get('filename')
    light.setParms({'light_intensity': lamp.get('intensity')})
    light.setParms({'RSL_affectDiffuse': lamp.get('affectsDiffuse')})
    light.setParms({'RSL_affectSpecular': lamp.get('affectsSpecular')})
    light.setParms({'RSL_bidirectional': lamp.get('areaBidirectional')})
    light.setParms({'RSL_visible': lamp.get('areaVisibleInRender')})
    light.setParms({'RSL_volumeScale': lamp.get('volumeRayContributionScale')})
    # create comment-description for each light
    light.setGenericFlag(hou.nodeFlag.DisplayComment, True)
    light.setComment(comment)


    # Display creation message
    hou.ui.displayMessage('Lights have been generated!')


# call function
translate_light()

