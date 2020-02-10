import os, sys
import pymel.core as pm

import maya.app.renderSetup.model.renderSetup as rs
from maya.app.renderSetup.model.typeIDs import *

import mtoa.core as ar
import mtoa.aovs as aovs


def create_layers():
    if not pm.objExists('objs'):
        pm.confirmDialog(t='confirm', m='No objs grp, please put all objects under it!', b=['ok'])
        sys.exit('')

    # save origin
    current_file = pm.sceneName()
    if 'original' in current_file.basename():
        pm.saveFile()
    else:
        origin_file = current_file.dirname() + '/' + current_file.basename().stripext() + '_original' + current_file.ext
        pm.saveAs(origin_file)

    rs_ins = rs.instance()
    rs_ins.getDefaultRenderLayer().setRenderable(0)
    ar.createOptions()
    pm.setAttr('defaultArnoldDriver.mergeAOVs', 1)
    pm.setAttr('defaultRenderGlobals.imageFilePrefix', '<Scene>/<RenderLayer>')

    aovs.AOVInterface().addAOV('ao', aovType='rgba')
    ao = pm.createNode('aiAmbientOcclusion')
    ao.outColor >> pm.PyNode('aiAOV_ao').defaultValue

    asm = pm.createNode('aiShadowMatte')

    # rs layer
    for obj in pm.PyNode('objs').getChildren():
        # if has a rayswitch child
        flag = 1 if obj.getChildren(typ='transform') else 0

        # beauty with out shadow
        print obj.name(), obj.type()

        obj.getShape().aiSubdivType.set(1)
        obj.getShape().aiSubdivIterations.set(2)

        rsl = rs_ins.createRenderLayer(obj.name()+'_beauty')

        co1 = rsl.createCollection('co1_'+obj.name())
        co1.getSelector().setPattern('*')

        co2 = co1.createCollection('co2_'+obj.name())
        co2.getSelector().setPattern('objs')

        co3 = co2.createCollection('co3_'+obj.name())
        co3.getSelector().setFilterType(2)
        other_shapes = [i for i in pm.PyNode('objs').getChildren() if i != obj]
        other_shapes_name = ', '.join([i.getShape().name() for i in other_shapes])
        co3.getSelector().setPattern(other_shapes_name)
        ov1 = co3.createOverride('ov1_'+obj.name(), absOverride)
        ov1.finalize('primaryVisibility')
        ov1.setAttrValue(0)
        ov2 = co3.createOverride('ov2_'+obj.name(), absOverride)
        ov2.finalize('castsShadows')
        ov2.setAttrValue(0)

        co4 = co2.createCollection('co4_'+obj.name())
        co4.getSelector().setFilterType(2)
        co4.getSelector().setPattern(obj.getShape().name())
        ov3 = co4.createOverride('ov3_'+obj.name(), absOverride)
        ov3.finalize('aiSelfShadows')
        ov3.setAttrValue(1)

        # shadow
        rsl = rs_ins.createRenderLayer(obj.name()+'_shadow')
        co5 = rsl.createCollection('co5_'+obj.name())
        co5.getSelector().setPattern('*')
        co6 = co5.createCollection('co6_'+obj.name())
        co6.getSelector().setPattern('objs')
        co7 = co6.createCollection('co7_'+obj.name())
        co7.getSelector().setFilterType(2)
        co7.getSelector().setPattern(other_shapes_name)
        ov4 = co7.createOverride('ov4_'+obj.name(), absOverride)
        ov4.finalize('primaryVisibility')
        ov4.setAttrValue(0)

        co8 = co6.createCollection('co8_'+obj.name())
        co8.getSelector().setFilterType(2)
        co8.getSelector().setPattern(obj.getShape().name())
        # co9 = co8.createCollection('co9_'+obj.name())
        # co9.getSelector().setFilterType(5)
        # co9.getSelector().setPattern('*')
        ov6 = co8.createOverride('ov6_'+obj.name(), shaderOverride)
        ov6.setShader(asm.name())

        if flag:
            for ii in obj.getChildren(typ='transform'):
                ii.getShape().aiSubdivType.set(1)
                ii.getShape().aiSubdivIterations.set(2)

            coa = co2.createCollection('coa_'+obj.name())
            coa.getSelector().setFilterType(2)
            rayswitch_names = ', '.join([i.getShape().name() for i in obj.getChildren(typ='transform')])
            coa.getSelector().setPattern(rayswitch_names)
            ova = coa.createOverride('ova_'+obj.name(), absOverride)
            ova.finalize('primaryVisibility')
            ova.setAttrValue(1)

            cob = co6.createCollection('cob_'+obj.name())
            cob.getSelector().setFilterType(2)
            cob.getSelector().setPattern(rayswitch_names)
            ovb = cob.createOverride('ovb_'+obj.name(), absOverride)
            ovb.finalize('primaryVisibility')
            ovb.setAttrValue(1)

    rsl = rs_ins.createRenderLayer('all_objs')
    co = rsl.createCollection('co_all')
    co.getSelector().setPattern('*')

    # save after script
    modify_file = current_file.dirname() + '/' + current_file.basename().stripext() + '_modify' + current_file.ext
    pm.saveAs(modify_file)