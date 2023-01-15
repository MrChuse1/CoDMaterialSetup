import maya.cmds as cmds
def addToShaderList(node):
    connections = cmds.listConnections('defaultShaderList1.s')
    cmds.connectAttr(str(node) + '.msg', 'defaultShaderList1.s[' + str(len(connections) + 101)+ ']')

def removeFromShaderList(node):
    cmds.disconnectAttr(str(node) + '.msg', 'defaultShaderList1.s', nextAvailable=True)

def setupSkin():
    Mats = cmds.ls(selection=True)
    # print(Mats)
    for mat in Mats:
        if cmds.nodeType(mat) == 'RedshiftMaterial':
            if cmds.nodeType(cmds.listConnections(str(mat) + '.diffuse_color')[0]) == 'RedshiftColorLayer':
                colorNode = cmds.listConnections(str(cmds.listConnections(str(mat) + '.diffuse_color')[0]) + '.layer1_color')[0]
                print(colorNode)
            if cmds.nodeType(cmds.listConnections(str(mat) + '.diffuse_color')[0]) == 'file':
                colorNode = cmds.listConnections(str(mat) + '.diffuse_color')[0]
            shadingNode:str = cmds.listConnections(str(mat) + '.outColor')[0]
            bumpNode:str = cmds.listConnections(str(mat) + '.bump_input')[0]
            glossNode:str = cmds.listConnections(str(mat) + '.refl_roughness')[0]
            cmds.rename(mat,str(mat) + '_RM')
            skinNode = cmds.createNode('RedshiftSkin', name= mat)
            addToShaderList(skinNode)
            print("Material Created: " + skinNode)

            deepCNode = cmds.createNode('RedshiftColorCorrection', name= str(mat) + '_deepCC')
            addToShaderList(deepCNode)
            cmds.connectAttr(str(colorNode) + '.outColor', str(mat) + '_deepCC' + '.input')
            cmds.setAttr(str(mat) + '_deepCC' + '.hue', 355)
            cmds.setAttr(str(mat) + '_deepCC' + '.saturation', 1.2)

            shallowCNode = cmds.createNode('RedshiftColorCorrection', name= str(mat) + '_shallowCC')
            addToShaderList(shallowCNode)
            cmds.connectAttr(str(colorNode) + '.outColor', str(mat) + '_shallowCC' + '.input')
            cmds.setAttr(str(mat) + '_shallowCC' + '.hue', 5)
            cmds.setAttr(str(mat) + '_shallowCC' + '.saturation', 0.8)

            cmds.connectAttr(str(mat) + '_deepCC' + '.outColor', str(mat) + '.deep_color')
            cmds.connectAttr(str(colorNode) + '.outColor', str(mat) + '.mid_color')
            cmds.connectAttr(str(mat) + '_shallowCC' + '.outColor', str(mat) + '.shallow_color')
        
            cmds.connectAttr(str(bumpNode) + '.out', str(mat) + '.bump_input')
            cmds.connectAttr(str(glossNode) + '.outColorR', str(mat) + '.refl_gloss0')
            cmds.connectAttr(str(mat) + '.outColor', str(shadingNode) + '.surfaceShader', force=True)

            cmds.setAttr(str(mat) + '.refl_weight0', 0.6)

            # mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
            # cmds.delete(str(mat) + '_RM')

setupSkin()