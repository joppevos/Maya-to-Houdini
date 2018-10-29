import maya.cmds as cmds
import json
import os

""" Export the attributes of each light in Maya """




# TODO: WORLD-BAKE EACH LAMP

# TODO: EXPORT EACH LAMP AS FBX FILE
""" 
    
"""
# list the selected lamps in the
def list_lamps():
    lamps = cmds.ls(selection=True)
    if lamps == []:
        cmds.confirmDialog(title='Confirm', message='Please select any Lights')
        error = ValueError('No lights selected')
        raise error
    else:
        return lamps


# TODO: ADD NORMALIZE ATTRIBUTE
# attribute keys to place in dict
attributes = ['scale', 'rotate', 'translate', 'intensity', 'color', 'affectsDiffuse', 'affectsSpecular',
              'areaVisibleInRender', 'areaBidirectional', 'volumeRayContributionScale', 'exposure']


# list of dict with attr keys and lamp in lamps
def attribute_maker(attributes, lamps):
    lamp_dict = [{attr: cmds.getAttr('{}.{}'.format(lamp, attr)) for attr in attributes} for lamp in lamps]
    # get the scene name of maya
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    # add the name of the lamps to lamp_dict and the filename of scene to dict
    for dicts, name in zip(lamp_dict, lamps):
        dicts['name'] = name
        dicts['filename'] = raw_name
    return lamp_dict



def filepath():
    """ ask user for local file path to save and returns the give path"""
    basicFilter = "*.json"
    filepath = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2)
    return filepath


def write_attributes(attrdict):
    """ Write out the attributes in json"""
    filename = ''.join(filepath())
    file = open('{}'.format(filename), 'w')
    file.write(attrdict)
    file.close()
    cmds.confirmDialog(title='LightExporter', message='Lights have been exported')


json = json.dumps(attribute_maker(attributes, list_lamps()))

write_attributes(json)



