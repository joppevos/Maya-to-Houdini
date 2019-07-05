import hou
import json
import os


def create_light(name):
    """ create lights in the scene"""
    sceneroot = hou.node('/obj/scene_fbx/')
    light = sceneroot.createNode('rslight', '{}'.format(name + '_H'))
    light.setParms({'light_type': 3})
    return light, sceneroot


def filepath():
    """ ask for file path"""
    filepath = hou.ui.selectFile()
    return filepath


def read_json():
    """ let user select the attribute filepath to read  """
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


def translate_light():
    """ position the light with correct scale,rotation and translation """
    lampattr, path = read_json()
    # import fbx
    import_fbx(path)
    sceneroot = hou.node('/obj/scene_fbx/')
    globalnull = sceneroot.createNode('null', 'size_locator')
    globalnull.setParms({'scale': 1})
    for lamp in lampattr:
        name = lamp.get('name')
        light, sceneroot = create_light(name)
        # Connect lights to Null objects
        null = hou.node('/obj/scene_fbx/{}/'.format(name))
        light.setInput(0, null, 0)
        null.setInput(0, globalnull, 0)
        scales = lamp.get('scale')
        colors = lamp.get('color')
        
        for scale in scales:
            light.setParms({'areasize1': (scale[0]*2), 'areasize2': (scale[1]*2), 'areasize3': (scale[2]*2)})
        for color in colors:
            light.setParms({'light_colorr': color[0], 'light_colorg': color[1], 'light_colorb': color[2]})
        set_attributes(light, lamp)
    sceneroot.layoutChildren()


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
    light.setParms({'RSL_areaShape': lamp.get('areaShape')})
    # create comment-description for each light
    light.setGenericFlag(hou.nodeFlag.DisplayComment, True)
    light.setComment(comment)

if __name__ == '__main__':
    translate_light()
    hou.ui.displayMessage('Lights have been generated!')
