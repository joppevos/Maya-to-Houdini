import maya.cmds as cmds
import json
import os

""" Export the attributes of each light in Maya """

# TODO: WORLD-BAKE EACH LAMP

# TODO: EXPORT EACH LAMP AS FBX FILE
""" 

"""


# list selected lamps in scene
def list_lamps():
    lamps = cmds.ls(selection=True)
    if lamps == []:
        cmds.confirmDialog(title='Confirm', message='Please select any Lights')
        error = ValueError('No lights selected')
        raise error
    else:
        return lamps


def key_checker():
    """ checks lamps for keyframes """
    lamps = cmds.ls(selection=True)
    for i in lamps:
        # check lamps for keyframes
        connection = ''.join(cmds.listConnections('{}'.format(i)))
        if connection == 'defaultLightSet':
            return False    # no keyframes
        else:
            return True     # keyframes


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


def write_attributes(*args):
    """ Write out the attributes in json and fbx"""
    attrdict = json_maker()
    filename = ''.join(filepath())
    file = open('{}'.format(filename), 'w')
    file.write(attrdict)
    file.close()
    write_fbx(filename)
    cmds.confirmDialog(title='LightExporter', message='Lights have been exported')


def write_fbx(filename):
    path = os.path.dirname(filename)
    print(path)
    fbxpath = '{}/'.format(path) + 'scene' + '.fbx'
    print(fbxpath)
    mel.eval('FBXExportBakeComplexAnimation -q; ')  # bake animation
    mel.eval('FBXExport -f "{}" -s'.format(fbxpath))  # remove -s to export all


def world_duplicater(*arg):
    """ bake lamps to world space and remove from parent"""
    lamps = cmds.ls(selection=True)
    bakelist = []
    for lamp in lamps:
        par = cmds.listRelatives(lamp, parent=True)
        if par == None:
            pass  # RUN SCRIPT WITHOUT DUPLICATING AND BAKING
        else:
            # duplicate lights
            duplights = cmds.duplicate(lamp, name=lamp + '_bakedToWorld', rc=True, rr=True)
            # delete duplicated children
            childtrentd = cmds.listRelatives(duplights, c=True, pa=True)[1:]
            for c in childtrentd:
                cmds.delete(c)
            # unparent object,add constraints and append it to bake List
            tobake = cmds.parent(duplights, w=True)
            bakelist.append(tobake)
            cmds.parentConstraint(lamp, tobake, mo=False)
            cmds.scaleConstraint(lamp, tobake, mo=False)


        # get Start and End Frame of Time Slider
    startframe = cmds.playbackOptions(q=True, minTime=True)
    endframe = cmds.playbackOptions(q=True, maxTime=True)
    # bake Animation and delete Constraints
    for i in bakelist:
        cmds.bakeResults(i, t=(startframe, endframe))
        cmds.delete(i[0] + '*Constraint*')
    cmds.confirmDialog(title='Duplicater', message='Baked and duplicated child lights to worldscale')

def json_maker():
    """ collect attributes in attr returns """
    attr = json.dumps(attribute_maker(attributes, list_lamps()))
    return attr

def menu():
    """ menu to start function with buttons"""
    cmds.window(width=250)
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Step1. Select lights to export', command=world_duplicater)
    cmds.button(label='Step2. Select baked and non-baked lights', command=write_attributes)
    cmds.showWindow()


menu()



