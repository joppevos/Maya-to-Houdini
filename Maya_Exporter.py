import maya.cmds as cmds
import json, os
""" Export the attributes of each light in Maya """

# list the selected lamps in the scene
lamps = cmds.ls(selection=True)

# attribute keys to place in dict
attributes = ['scale', 'rotate', 'translate', 'intensity', 'exposure', 'color', 'affectsDiffuse', 'affectsSpecular',
              'areaVisibleInRender', 'areaBidirectional', 'volumeRayContributionScale']


# list of dict with attr keys and lamp in lamps
def attribute_maker(attributes,lamps):
    lamp_dict = [{attr: cmds.getAttr('{}.{}'.format(lamp, attr)) for attr in attributes} for lamp in lamps]

    # get the filepath name
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    # add the name of the lamps to lamp_dict
    for dicts, name in zip(lamp_dict, lamps):
        dicts['name'] = name
        dicts['filename'] = raw_name
    return lamp_dict


# TODO: WRAP IN FUNCTION
json = json.dumps(attribute_maker(attributes,lamps))
file = open('C:\\Users\\render\\Desktop\\redshiftscript\\rs_mayaLampAttr\\lamp_dict.json', 'w')
file.write(json)
file.close()

# TODO: WRAP IN TRY IF NO LIGHTS ARE SELECTED ERROR,
# AND FINALLY GIVE MESSAGE TO USER 'LIGHT DATA HAS BEEN EXPORTED!"

attribute_maker(attributes, lamps)

