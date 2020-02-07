import os, sys
import maya.app.renderSetup as renderSetup
import mtoa.aovs as aovs
from pymel.core import *


def create_layers():
    if not objExists('objs'):
        confirmDialog(t='confirm', m='No objs grp, please put all object under it!', b=['ok'])
        print 'haha'
        sys.exit('')

    rs = renderSetup.model.renderSetup.instance()
    rs.getDefaultRenderLayer().setRenderable(0)

    aovs.AOVInterface().addAOV('ao', aovType='float')
    ao = createNode('aiAmbientOcclusion')
    ao.outColor >> PyNode('aiAOV_ao').defaultValue

    asm = createNode('aiShadowMatte')

    # rs layer
    for obj in PyNode('objs').getChildren():

        # beauty with out shadow
        print obj.name(), obj.type()

        obj.getShape().aiSubdivType.set(1)
        obj.getShape().aiSubdivIterations.set(2)

        rsl = rs.createRenderLayer('rsl_beauty_'+obj.name())
        col = rsl.createCollection('ca1_beauty_'+obj.name())
        col.getSelector().setPattern('objs')
        cola = col.createCollection('ca2_beauty_'+obj.name())
        cola.getSelector().setFilterType(2)
        cola.getSelector().setPattern('* -'+obj.getShape().name())
        ov_matte = cola.createOverride('override_beauty_m_'+obj.name(), renderSetup.model.typeIDs.absOverride)
        ov_matte.finalize('aiMatte')
        ov_matte.setAttrValue(1)
        ov_shadow = cola.createOverride('override_beauty_s_'+obj.name(), renderSetup.model.typeIDs.absOverride)
        ov_shadow.finalize('castsShadows')
        ov_shadow.setAttrValue(0)

        # shadow
        rsl = rs.createRenderLayer('rsl_shadow_'+obj.name())
        col = rsl.createCollection('ca1_shadow_'+obj.name())
        col.getSelector().setPattern('objs')
        cola = col.createCollection('ca2_shadow_'+obj.name())
        cola.getSelector().setFilterType(2)
        cola.getSelector().setPattern('* -'+obj.getShape().name())
        ov_matte = cola.createOverride('override_shadow_m_'+obj.name(), renderSetup.model.typeIDs.absOverride)
        ov_matte.finalize('aiMatte')
        ov_matte.setAttrValue(1)
        ov_shadow = cola.createOverride('override_shadow_s_'+obj.name(), renderSetup.model.typeIDs.absOverride)
        ov_shadow.finalize('primaryVisibility')
        ov_shadow.setAttrValue(0)

        cola = col.createCollection('ca3_shadow_'+obj.name())
        cola.getSelector().setFilterType(2)
        cola.getSelector().setPattern(obj.getShape().name())
        colb = cola.createCollection('ca4_shadow_'+obj.name())
        colb.getSelector().setFilterType(5)
        colb.getSelector().setPattern('*')
        ov_shader = cola.createOverride('override2_beauty_s_'+obj.name(), renderSetup.model.typeIDs.shaderOverride)
        ov_shader.setShader('aiShadowMatte1')