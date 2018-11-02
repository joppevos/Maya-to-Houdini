import hou
import os

""" Houdini FBX parent-er"""
lampen = ['lampje1','lampje2']


os.chdir(r'C:\Users\render\Desktop\\')
os.getcwd()

hou.hipFile.importFBX('lamp.fbx')
path = hou.node('/obj/lamp_fbx/')
null = hou.node('/obj/lamp_fbx/rsPhysicalLight1/')

light2 = path.createNode('rslight', 'rslight2')
light2.setInput(0, null, 0)
