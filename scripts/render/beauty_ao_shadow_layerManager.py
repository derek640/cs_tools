import os, sys
import pymel.core as pm

import maya.app.renderSetup.model.renderSetup as rs
from maya.app.renderSetup.model.typeIDs import *

import mtoa.core as ar
import mtoa.aovs as aovs

def create_layers():
    if not pm.objExists('objs'):
        pm.confirmDialog(t='confirm', m='No objs grp, please put all object under it!', b=['ok'])
        sys.exit('')

    rs_ins = rs.instance()
    rs_ins.getDefaultRenderLayer().setRenderable(0)
    ar.createOptions()

    aovs.AOVInterface().addAOV('ao', aovType='float')
    ao = pm.createNode('aiAmbientOcclusion')
    ao.outColor >> pm.PyNode('aiAOV_ao').defaultValue

    asm = pm.createNode('aiShadowMatte')

    # rs layer
    for obj in pm.PyNode('objs').getChildren():

        # beauty with out shadow
        print obj.name(), obj.type()

        obj.getShape().aiSubdivType.set(1)
        obj.getShape().aiSubdivIterations.set(2)

        rsl = rs_ins.createRenderLayer('rsl_beauty_'+obj.name())
        col = rsl.createCollection('ca1_beauty_'+obj.name())
        col.getSelector().setPattern('objs')
        cola = col.createCollection('ca2_beauty_'+obj.name())
        cola.getSelector().setFilterType(2)
        cola.getSelector().setPattern('* -'+obj.getShape().name())
        ov_matte = cola.createOverride('override_beauty_m_'+obj.name(), absOverride)
        ov_matte.finalize('aiMatte')
        ov_matte.setAttrValue(1)
        ov_shadow = cola.createOverride('override_beauty_s_'+obj.name(), absOverride)
        ov_shadow.finalize('castsShadows')
        ov_shadow.setAttrValue(0)

        # shadow
        rsl = rs_ins.createRenderLayer('rsl_shadow_'+obj.name())
        col = rsl.createCollection('ca1_shadow_'+obj.name())
        col.getSelector().setPattern('objs')
        cola = col.createCollection('ca2_shadow_'+obj.name())
        cola.getSelector().setFilterType(2)
        cola.getSelector().setPattern('* -'+obj.getShape().name())
        ov_matte = cola.createOverride('override_shadow_m_'+obj.name(), absOverride)
        ov_matte.finalize('aiMatte')
        ov_matte.setAttrValue(1)
        ov_shadow = cola.createOverride('override_shadow_s_'+obj.name(), absOverride)
        ov_shadow.finalize('primaryVisibility')
        ov_shadow.setAttrValue(0)

        cola = col.createCollection('ca3_shadow_'+obj.name())
        cola.getSelector().setFilterType(2)
        cola.getSelector().setPattern(obj.getShape().name())
        colb = cola.createCollection('ca4_shadow_'+obj.name())
        colb.getSelector().setFilterType(5)
        colb.getSelector().setPattern('*')
        ov_shader = cola.createOverride('override2_beauty_s_'+obj.name(), shaderOverride)
        ov_shader.setShader('aiShadowMatte1')