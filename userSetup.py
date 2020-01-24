from pymel.core import *
import sys
sys.path.append('D:\\cs_tools\\scripts')


def create_tool_menu():
    if menu('cs_tools', q=1, ex=1):
        deleteUI('cs_tools')
    menu('cs_tools', l='cs_tools', p='MayaWindow')
    menuItem('render', l='render', sm=1, p='cs_tools')
    menuItem(l='Create Layers', p='render', c='import render.beauty_ao_shadow_layerManager as lm;lm.create_layers()')


scriptJob(e=['NewSceneOpened', create_tool_menu])