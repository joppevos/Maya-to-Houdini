import maya.cmds as cmds


def world_duplicater():
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
