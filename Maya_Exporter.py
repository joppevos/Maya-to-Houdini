import maya.cmds as cmds
import json
import os
import maya.mel as mel


def list_all_lamps():
    lamps = cmds.ls(selection=True)
    if not lamps:
        cmds.confirmDialog(title='Confirm', message='Please select any Light')
    else:
        return lamps


def attribute_generator(attributes, lamps):
    lamp_dict = [{attr: cmds.getAttr('{}.{}'.format(lamp, attr)) for attr in attributes} for lamp in lamps]
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)
    for dicts, name in zip(lamp_dict, lamps):
        dicts['name'] = name
        dicts['filename'] = raw_name
    return lamp_dict


def ask_filepath_location():
    basicFilter = "*.json"
    filepath = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2)
    return filepath


def write_attributes(*args):
    """ Write out the attributes in json and fbx"""
    attrdict = write_json()
    filename = ''.join(ask_filepath_location())
    file = open('{}'.format(filename), 'w')
    file.write(attrdict)
    file.close()
    write_fbx(filename)
    cmds.confirmDialog(title='LightExporter', message='Lights have been exported')


def write_fbx(filename):
    path = os.path.dirname(filename)
    fbxpath = '{}/'.format(path) + 'scene' + '.fbx'
    mel.eval('FBXExportBakeComplexAnimation -q; ')  # bake animation
    mel.eval('FBXExport -f "{}" -s'.format(fbxpath))  # remove -s to export all


def world_duplicater(*arg):
    """ bake lamps to world space and remove from parent"""
    lamps = cmds.ls(selection=True)
    bakelist = []
    for lamp in lamps:
        par = cmds.listRelatives(lamp, parent=True)
        if not par:
            continue
        else:
            duplicated_lamps = cmds.duplicate(lamp, name=lamp + '_bakedToWorld', rc=True, rr=True)
            children = cmds.listRelatives(duplicated_lamps, c=True, pa=True)[1:]
            for child in children:
                cmds.delete(child)
            tobake = cmds.parent(duplicated_lamps, w=True)
            bakelist.append(tobake)
            cmds.parentConstraint(lamp, tobake, mo=False)
            cmds.scaleConstraint(lamp, tobake, mo=False)

        # get Start and End Frame of Time Slider
    startframe = cmds.playbackOptions(q=True, minTime=True)
    endframe = cmds.playbackOptions(q=True, maxTime=True)
    for i in bakelist:
        cmds.bakeResults(i, t=(startframe, endframe))
        cmds.delete(i[0] + '*Constraint*')
    cmds.confirmDialog(title='Duplicater', message='Baked and duplicated child lights to worldscale')


def write_json():
    attributes = ['scale', 'rotate', 'translate', 'intensity', 'color', 'affectsDiffuse', 'affectsSpecular',
                  'areaVisibleInRender', 'areaBidirectional', 'volumeRayContributionScale', 'exposure', 'areaShape']
    attr = json.dumps(attribute_generator(attributes, list_all_lamps()))
    return attr


def launch_interface():
    """ menu to start function with buttons"""
    cmds.window(width=250, title='Light Exporter')
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Step1. Bake and duplicate selected lights', command=world_duplicater)
    cmds.button(label='Step2. Export selected lights', command=write_attributes)
    cmds.showWindow()


if __name__ == '__main__':
    launch_interface()
