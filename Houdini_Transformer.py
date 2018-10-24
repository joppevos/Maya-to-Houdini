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
    # TODO: FIX FILE PATH SELECTOR
    #filepath = hou.ui.selectFile()
    #print(filepath)
    #newpath = filepath.replace('/', '\\')
    read_file = open('C:\Users\Joppe\Desktop\\rs.json', 'r')
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
        colors = lamp.get('color')
        for translate in translates:
            light.setParms({'tx': translate[0], 'ty': translate[1], 'rz': translate[2]})
        for rotation in rotations:
            light.setParms({'rx': rotation[0], 'ry': rotation[1], 'rz': rotation[2]})
        for scale in scales:
            light.setParms({'areasize1': scale[0], 'areasize2': scale[1]})
        for color in colors:
            light.setParms({'light_colorr': color[0], 'light_colorg': color[1], 'light_colorb': color[2]})
        light.setParms({'light_intensity': lamp.get('intensity')})
        # TODO: CLEAN UP IN FORLOOP WITH LIST
        light.setParms({'RSL_affectDiffuse': lamp.get('affectsDiffuse')})
        light.setParms({'RSL_affectSpecular': lamp.get('affectsSpecular')})
        light.setParms({'RSL_bidirectional': lamp.get('areaBidirectional')})
        light.setParms({'RSL_visible': lamp.get('areaVisibleInRender')})
        light.setParms({'RSL_volumeScale': lamp.get('volumeRayContributionScale')})

        # create comment-description for each light
        light.setGenericFlag(hou.nodeFlag.DisplayComment, True)
        light.setComment(comment)





# TODO: ADD ATTRIBUTES TO A FUNCTION RSLIGHT


# TODO: WANRING FOR 'AFFECT DIFFUSE/SPECULAR FROM MAYA. NOT AVAILABLE IN HOUDINI' double check it?
    # Display creation message
    # hou.ui.displayMessage('Lights have been generated!')


# call function
translate_light()

