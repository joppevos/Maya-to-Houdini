import hou
import json
import os

# TODO:
# ## set current working directory
# #os.chdir(r'C:\Users\render\Desktop\\')
# #os.getcwd()
# ## import exported fbx
# #hou.hipFile.importFBX('lamp.fbx')
#
# ## TODO: Assign created RSlamp as child to fbx
#
# hou.hipFile.importFBX('lamp.fbx')
# parent = hou.node('/obj/lamp_fbx1/rsPhysicalLight1')
# print(parent)


def create_light(name):
    """ create lights in the scene"""

    # Get scene root node
    sceneroot = hou.node('/obj/scene_fbx/')
    # Create light
    light = sceneroot.createNode('rslight', '{}'.format(name + '_H'))
    light.setParms({'light_type': 3})
    return light


def filepath():
    """ ask for file path"""
    filepath = hou.ui.selectFile()
    return filepath


def read_json():
    """ let user select the attribute filepath to read  """
    # TODO: FIX GIVEN FILEPATH $HIP/Desktop/test.json.
    path = filepath()
    if path.lower().endswith('.json'):
        read_file = open('{}'.format(path), 'r')
        lampattr = json.load(read_file)
        return lampattr, path
    else:
        hou.ui.displayMessage('Please select a .json file ')


def import_fbx(path):
    """ imports the fbx from each lamp """
    newpath = os.path.dirname(path) + '/'
    os.chdir(newpath)
    hou.hipFile.importFBX('scene.fbx')
    # houpath = hou.node('/obj/{}/'.format(filename))
    # null = hou.node('/obj/{}/{}/'.format(filename, filename))
    # light.setInput(0, null, 0)


def translate_light():
    """ position the light with correct scale,rotation and translation """

    lampattr, path = read_json()
    # import fbx
    import_fbx(path)
    for lamp in lampattr:
        name = lamp.get('name')
        # TODO: IF ANIMATION YES. IMPORT FBX
        light = create_light(name)
        # Connect lights to Null objects
        houpath = hou.node('/obj/scene_fbx/')
        null = hou.node('/obj/scene_fbx/{}/'.format(name))
        light.setInput(0, null, 0)
        translates = lamp.get('translate')
        rotations = lamp.get('rotate')
        scales = lamp.get('scale')
        colors = lamp.get('color')
        # for translate in translates:
        #     light.setParms({'tx': translate[0], 'ty': translate[1], 'tz': translate[2]})
        # for rotation in rotations:
        #     light.setParms({'rx': rotation[0], 'ry': rotation[1], 'rz': rotation[2]})
        for scale in scales:
            light.setParms({'areasize1': scale[0]*2, 'areasize2': scale[1]*2})
        for color in colors:
            light.setParms({'light_colorr': color[0], 'light_colorg': color[1], 'light_colorb': color[2]})
        set_attributes(light, lamp)
    # Display creation message
    #hou.node(“ / obj”).layoutChildren()


def set_attributes(light, lamp):
    """ set the attributes for the light """
    comment = lamp.get('filename')
    light.setParms({'RSL_intensityMultiplier': lamp.get('intensity')})
    light.setParms({'Light1_exposure': lamp.get('exposure')})
    light.setParms({'RSL_affectDiffuse': lamp.get('affectsDiffuse')})
    light.setParms({'RSL_affectSpecular': lamp.get('affectsSpecular')})
    light.setParms({'RSL_bidirectional': lamp.get('areaBidirectional')})
    light.setParms({'RSL_visible': lamp.get('areaVisibleInRender')})
    light.setParms({'RSL_volumeScale': lamp.get('volumeRayContributionScale')})
    # create comment-description for each light
    light.setGenericFlag(hou.nodeFlag.DisplayComment, True)
    light.setComment(comment)




# call function
translate_light()
# Display creation message
hou.ui.displayMessage('Lights have been generated!')

