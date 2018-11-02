# TODO: Batch export selected lights as fbx.
# TODO: World bake the lights FBXExportBakeComplexAnimation -v [true|false];


import maya.cmds as cmds
import maya.mel as mel
import os


list = cmds.ls(sl=1)
print(list)

filepath = 'C:/Users/render/Desktop/lampen/' + 'scene' + '.fbx'
print(filepath)
mel.eval('FBXExportBakeComplexAnimation -q; ')
mel.eval('FBXExport -f "{}" -s'.format(filepath)) # remove -s to export all