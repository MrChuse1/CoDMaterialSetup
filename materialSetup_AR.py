
## Redshift Material Converter for Maya by MrChuse
## https://twitter.com/MrChuse
## Version 1.0.7


import maya.cmds as cmds
import random
import maya.mel as mel
import os as os
import csv
from pathlib import Path
import glob
from PIL import Image

textPath = ""
MatName = ""
MatDirectory = ""
MatList = []
FileType = ""
MatProgress = 0
Game = ''
REngine = ''
NoNormals = []

MatDiffuse={
    "Redshift":".diffuse_color",
    "Arnold":".baseColor",
}

MatSpec={
    "Redshift":".refl_weight",
    "Arnold":".specular",
}

MatSpecColor={
    "Redshift":".refl_reflectivity",
    "Arnold":".specularColor",
}

MatMetallic={
    "Redshift":".refl_metalness",
    "Arnold":".metalness",
}

MatRough={
    "Redshift":".refl_roughness",
    "Arnold":".specularRoughness",
}

MatSheen={
    "Redshift":".sheen_weight",
    "Arnold":".sheen",
}

MatSheenRough={
    "Redshift":".sheen_roughness",
    "Arnold":".sheenRoughness",
}

MatBump={
    "Redshift":".bump_input",
    "Arnold":".normalCamera",
}

MatBumpY={
    "Redshift":".flipY",
    "Arnold":".invertY",
}

MatBumpOut={
    "Redshift":".out",
    "Arnold":".outValue",
}

BumpL1={
    "Redshift":".base_color",
    "Arnold":".input1",
}
BumpL2={
    "Redshift":".layer1_color",
    "Arnold":".input2",
}
BumpL3={
    "Redshift":".layer2_color",
    "Arnold":".input3",
}
BumpL4={
    "Redshift":".layer3_color",
    "Arnold":".input4",
}

BumpMixL1={
    "Redshift":".layer1_mask",
    "Arnold":".mix2",
}
BumpMixL2={
    "Redshift":".layer2_mask",
    "Arnold":".mix3",
}
BumpMixL3={
    "Redshift":".layer3_mask",
    "Arnold":".mix4",
}

BumpE1={
    "Redshift":".layer1_enable",
    "Arnold":".enable2",
}

BumpE2={
    "Redshift":".layer2_enable",
    "Arnold":".enable3",
}
BumpE3={
    "Redshift":".layer3_enable",
    "Arnold":".enable4",
}
MatOpacity={
    "Redshift":".opacity_color",
    "Arnold":".opacity",
}

MatEmmision={
    "Redshift":".emission_color",
    "Arnold":".emissionColor",
}

OSLNodeText={
    "Redshift":".sourceText",
    "Arnold":".code",
}
def Main():
    global modelsPath
    global modelsFolders
    global MatList
    global Game
    global MatName
    global MatDirectory
    global MatProgress
    global FileType
    global REngine
    modelsPath = cmds.textField("models_path", q=True, tx=True)
    # modelsPath = "I:\\Scripts\\Test\\xmodels"
    modelsFolders = os.listdir(str(modelsPath))
    # print(modelsFolders)
    FileType = "." + cmds.optionMenu('image_type', q=True, v=True).lower()
    REngine = cmds.optionMenu('render', q=True, v=True)
    # print("FileType: " + FileType)
    # cmds.progressWindow(title="Material Converter",status="Importing...",progress=0,ii=False)
    models = []
    for folder in modelsFolders:
        if not folder.__contains__('.'):
            models.append(folder)
    print(models)
    # for folder in models:
        # print(models)
    for model in models:
        print("Model: ", model)
        if not model.__contains__('.'):
            modelFiles = os.listdir(str(modelsPath + '/' + model))
            for file in modelFiles:
                if file.endswith("_images.txt"):
                    MatList.append(str(file[:-len("_images.txt")]))
            cmds.progressWindow(edit=True,status="Model: " + folder)
            # print('Materials: ', MatList)


    # for mat in MatList:
    #     print('Material: ', mat)
        for MatName in MatList:
            # print('==================', MatName, '=====================')
            MatDirectory = modelsPath + '/' + model
            # print("Material: ", MatName)
            if  cmds.objExists(MatName) and MatName != "lambert1":
                # print("Node Type: " + str(cmds.nodeType(MatName)))
                
                if cmds.nodeType(MatName) != "aiStandardSurface" and cmds.nodeType(MatName) != "RedshiftMaterial" and cmds.nodeType(MatName) != "transform" and cmds.nodeType(MatName) != 'shadingEngine' and cmds.nodeType(MatName) != 'RedshiftSkin':
                    if REngine == 'Redshift':
                        # materialNode = mel.eval('''rsCreateShadingNode "rendernode/redshift/shader/surface" "-asShader" "" RedshiftMaterial;''')
                        materialNode = cmds.shadingNode('RedshiftMaterial', asShader=True)
                        modelSG = cmds.listConnections(MatName + '.outColor', destination=True)[0]
                        # print(modelSG)
                        # cmds.connectAttr(str(materialNode + '.outColor'), str(modelSG + '.surfaceShader'), force=True)
                        # cmds.delete(MatName)
                        # cmds.rename(materialNode, MatName)
                        # print("Material Created: " + MatName)

                    if REngine == 'Arnold':
                        materialNode = cmds.shadingNode('aiStandardSurface', asShader=True)
                        modelSG = cmds.listConnections(MatName + '.outColor', destination=True)[0]
                        # print(modelSG)
                    cmds.connectAttr(str(materialNode + '.outColor'), str(modelSG + '.surfaceShader'), force=True)
                    cmds.delete(MatName)
                    cmds.rename(materialNode, MatName)
                    print("Material Created: " + MatName)
                    
                    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
                    Game = cmds.optionMenu('game', q=True, v=True)
                    # print("Game: " + Game)
                    if Game == "Black Ops Cold War" or Game == "Black Ops 4":
                        SetupMaterialTreyarch()
                    if Game == "Vangaurd" or Game == 'Modern Warfare II':
                        SetupMaterial_S4_IW9()
                    if Game == "Modern Warfare Remastered":
                        SetupMaterialH1()
                    cmds.progressWindow(edit=True,progress=int(MatProgress/len(modelsFolders)))
                    MatProgress = MatProgress + 1
            else:
                print(MatName, " does not exist.")

        MatList.clear()

    print("Thse Materials have no Normal Maps: \n", NoNormals)
        



def ConvertGlossToRough():
    global MatName
    if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True and REngine == 'Redshift':
        cmds.setAttr(MatName + ".refl_isGlossiness", 1)
        

def CreateImageNode(Node2d="Node2dTemp",Place2dNode="Place2dNodeTemp"):
    imageNode = mel.eval('shadingNode -asTexture -isColorManaged file;')
    cmds.rename(imageNode, str(Node2d))
    image2dNode = mel.eval('shadingNode -asUtility place2dTexture;')
    cmds.rename(image2dNode, str(Place2dNode))
    # print(Place2dNode, Node2d)
    cmds.connectAttr( str(Place2dNode)+'.coverage', str(Node2d)+'.coverage', force=True)
    cmds.connectAttr( str(Place2dNode)+'.translateFrame', str(Node2d)+'.translateFrame', force=True)
    cmds.connectAttr( str(Place2dNode)+'.rotateFrame', str(Node2d)+'.rotateFrame', force=True)
    cmds.connectAttr( str(Place2dNode)+'.mirrorU', str(Node2d)+'.mirrorU', force=True)
    cmds.connectAttr( str(Place2dNode)+'.mirrorV', str(Node2d)+'.mirrorV', force=True)
    cmds.connectAttr( str(Place2dNode)+'.stagger', str(Node2d)+'.stagger', force=True)
    cmds.connectAttr( str(Place2dNode)+'.wrapU', str(Node2d)+'.wrapU', force=True)
    cmds.connectAttr( str(Place2dNode)+'.wrapV', str(Node2d)+'.wrapV', force=True)
    cmds.connectAttr( str(Place2dNode)+'.repeatUV', str(Node2d)+'.repeatUV', force=True)
    cmds.connectAttr( str(Place2dNode)+'.offset', str(Node2d)+'.offset', force=True)
    cmds.connectAttr( str(Place2dNode)+'.rotateUV', str(Node2d)+'.rotateUV', force=True)
    cmds.connectAttr( str(Place2dNode)+'.noiseUV', str(Node2d)+'.noiseUV', force=True)
    cmds.connectAttr( str(Place2dNode)+'.vertexUvOne', str(Node2d)+'.vertexUvOne', force=True)
    cmds.connectAttr( str(Place2dNode)+'.vertexUvTwo', str(Node2d)+'.vertexUvTwo', force=True)
    cmds.connectAttr( str(Place2dNode)+'.vertexUvThree', str(Node2d)+'.vertexUvThree', force=True)
    cmds.connectAttr( str(Place2dNode)+'.vertexCameraOne', str(Node2d)+'.vertexCameraOne', force=True)
    cmds.connectAttr( str(Place2dNode)+'.outUV', str(Node2d)+'.uv', force=True)
    cmds.connectAttr( str(Place2dNode)+'.outUvFilterSize', str(Node2d)+'.uvFilterSize', force=True)

def CreateFileNode(name):
    filenode = mel.eval('createRenderNodeCB -as2DTexture "" file ("")')
    cmds.rename(filenode,name)

def Filter(map):
    return map.replace("~","").replace("-","_").replace("$","").replace("&","")

def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def SetupMaterialTreyarch():
    cMap = ""
    aoMap = ""
    nMap = ""
    gMap = ""
    sMap = ""
    eMap = ""
    dnMap = ""
    dnMask = ""
    dnMap1 = ""
    dnMap2 = ""
    dnMap3 = ""
    dnMap4 = ""
    cFile = MatDirectory + "/" + MatName + "_images.txt"
    # print("Material: " + MatName)
    textOpen = open(cFile, "r")
    fList = textOpen.readlines()
    sList = []
    i=0
    for lines in fList:
        semantic_temp = fList[i].split(",")
        semantic_replace = semantic_temp[1]
        semantic_temp[1] = semantic_replace[:-1]
        sList.append(semantic_temp)
        # print(semantic_temp)
        i = i + 1
    sList[0].remove("semantic")
    # print(sList)
    i=0
    for elements in sList:
        if sList[i][0] == "colorMap":
            cMap = sList[i][1]
        elif sList[i][0] == "normalMap":
            nMap = sList[i][1]
        elif sList[i][0] == "aoMap":
            aoMap = sList[i][1]
        elif sList[i][0] == "glossMap":
            gMap = sList[i][1]
        elif sList[i][0] == "specColorMap":
            sMap = sList[i][1]
        elif sList[i][0] == "emissiveMap":
            eMap = sList[i][1]
        elif sList[i][0] == "detailMap":
            dnMap = sList[i][1]
        elif sList[i][0] == "detailNormalMask":
            dnMask = sList[i][1]
        elif sList[i][0] == "detailNormal1":
            dnMap = sList[i][1]
        elif sList[i][0] == "detailNormal2":
            dnMap2 = sList[i][1]
        elif sList[i][0] == "detailNormal3":
            dnMap3 = sList[i][1]
        elif sList[i][0] == "detailNormal4":
            dnMap4 = sList[i][1]
        i = i + 1
    # print("Colour Map: " + cMap + "\n" + "Normal Map: " + nMap + "\n" + "Occlusion Map: " + aoMap + "\n" + "Gloss Map: " + gMap, "\n" + "Specular Map: " + sMap)
    textOpen.close()
    
    if cmds.checkBox("image_folder", q=True, v=True) == True:
        cMapFP = MatDirectory + "/_images/" + MatName + "/"
    elif cmds.checkBox("image_folder", q=True, v=True) == False:
        cMapFP = MatDirectory + "/_images/"
    
    ## Color Map
    if os.path.exists(str(cMapFP + cMap + FileType)) and cMap != "$black_color" and cMap != "$white_diffuse" and cMap != "$blacktransparent_color":
        if not cmds.objExists(cMap):
            CreateImageNode(str(cMap),"Place2"+str(cMap))
        cmds.connectAttr(str(cMap) + ".outColor", MatName + str(MatDiffuse[REngine]))
        if cmds.checkBox("enable_alpha", q=True, v=True) == True:
            cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'R'))
            cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'G'))
            cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'B'))
        cmds.setAttr(str(cMap) + ".fileTextureName", cMapFP + cMap + FileType, type="string")
    elif cMap == "$white_diffuse":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 1, 1, 1)
    elif cMap == "$black_diffuse" or cMap == "$black" or cMap == "$black_color":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 0, 0, 0)

    # Specular Map
    if os.path.exists(cMapFP + sMap + FileType) and sMap != "$specular" and sMap != "$white_specular":
        if not cmds.objExists(sMap):
            CreateImageNode(str(sMap),"Place2"+str(sMap))
            cmds.setAttr(str(sMap) + ".fileTextureName", cMapFP + sMap + FileType, type="string")
            
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 1 - Colour Edge & Tint
            cmds.setAttr(str(MatName) + ".refl_edge_tintR", 1, clamp=True)
            cmds.setAttr(str(MatName) + ".refl_edge_tintG", 1, clamp=True)
            cmds.setAttr(str(MatName) + ".refl_edge_tintB", 1, clamp=True)
        
        cmds.connectAttr(str(sMap) + ".outColor", MatName + str(MatSpecColor[REngine]))

    elif sMap == "$specular":
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 0.23, 0.23, 0.23)
    elif sMap == "$white_specular":
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 1, 1, 1)
    elif not os.path.exists(cMapFP + sMap + FileType):
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 3) # 3 - IOR

    # AO Map
    if os.path.exists(cMapFP + aoMap + FileType) and aoMap != "$white_ao" and aoMap != "$occlusion_black" and aoMap != "$occlusion_50" and aoMap != "$occlusion":
        try:
            if not cmds.objExists(aoMap):
                CreateImageNode(str(aoMap),"Place2"+str(aoMap))
                cmds.setAttr(str(aoMap) + ".fileTextureName", cMapFP + aoMap + FileType, type="string")
            if REngine == 'Redshift':
                cmds.connectAttr(str(aoMap) + ".outColor", MatName + ".overall_color")   
        except:
            print("Gloss map not found")
    elif aoMap == "$black" or aoMap == "$occlusion_black":
        cmds.setAttr(str(MatName) + ".overall_color", 0, 0, 0)

    # Gloss Map
    if os.path.exists(cMapFP + gMap + FileType) and gMap != "$gloss" and gMap != "$white_gloss" and gMap != "$black" and gMap != "$black_gloss":
        # try:
            if not cmds.objExists(gMap):
                CreateImageNode(str(gMap),"Place2"+str(gMap))
                cmds.setAttr(str(gMap) + ".fileTextureName", cMapFP + gMap + FileType, type="string")
                glossNode = mel.eval('shadingNode -asTexture ramp;')
                cmds.rename(glossNode, str(gMap) + "_ramp")
                cmds.setAttr(str(gMap) + "_ramp.colorEntryList[1].position", 1)
                cmds.setAttr(str(gMap) + "_ramp.colorEntryList[1].color", 1, 1, 1)
                cmds.setAttr(str(gMap) + "_ramp.colorEntryList[2].position", 0)
                cmds.setAttr(str(gMap) + "_ramp.colorEntryList[2].color", 0, 0, 0)
                if REngine =='Arnold' and bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                    reverseNode = mel.eval('shadingNode -asTexture reverse;')
                    cmds.rename(reverseNode, str(gMap) + '_reverse')
                    cmds.connectAttr(str(gMap) + ".outColorR", str(gMap) + '_reverse.inputX')
                    cmds.connectAttr(str(gMap) + '_reverse.outputX', str(gMap) + "_ramp" + ".vCoord")
                if REngine == 'Redshift':
                    cmds.connectAttr(str(gMap) + ".outColorR", str(gMap) + "_ramp" + ".vCoord")
            cmds.connectAttr(str(gMap) + "_ramp" + ".outColorR", MatName + str(MatRough[REngine]))
            cmds.setAttr(str(gMap) + ".colorSpace", "Raw", type="string")
        # except:
        #     print("Gloss map not found")
    elif gMap == "$gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.23)
        if REngine == 'Arnold':
            cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.77)
    elif gMap == "$white_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 1)
        if REngine == 'Arnold':
            cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0)
    elif gMap == "$black" or gMap == "$black_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0)
        if REngine == 'Arnold':
            cmds.setAttr(str(MatName) + str(MatRough[REngine]), 1)
    
    if os.path.exists(cMapFP + nMap + FileType) and nMap != "$identitynormalmap" and nMap != "$normal":
        # try:
            if not cmds.objExists(nMap):
                CreateImageNode(str(nMap),"Place2"+str(nMap))
                cmds.setAttr(str(nMap) + ".fileTextureName", cMapFP + nMap + FileType, type="string")
                cmds.setAttr(str(nMap) + ".colorSpace", "Raw", type="string")
            if REngine == 'Redshift':
                bumpNode = mel.eval('shadingNode -asTexture RedshiftBumpMap;')
                cmds.setAttr(bumpNode + ".scale", 1)
                cmds.setAttr(bumpNode + ".inputType", 1)
            elif REngine == 'Arnold':
                bumpNode = mel.eval('shadingNode -asTexture aiNormalMap')
            
            cmds.rename(bumpNode, str(MatName) + "_bump")
            
            cmds.setAttr(str(MatName) + '_bump' + str(MatBumpY[REngine]), 1)
            cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
            cmds.connectAttr(str(MatName) + "_bump" + str(MatBumpOut[REngine]), MatName + str(MatBump[REngine]))
            print('Attempting to create detail map')

    # print((cMapFP + dnMap + FileType).replace('\\','\\\\'))
    # if os.path.exists((cMapFP + dnMap + FileType).replace('\\','\\\\')):
    #     print('Detail Map detected')
    if not cmds.objExists(str(MatName) + "_bumpLayer") and os.path.exists((cMapFP + dnMask + FileType).replace('\\','\\\\')) or os.path.exists((cMapFP + dnMap + FileType).replace('\\','\\\\')):
        print('Function starting..')
        if not cmds.objExists(str(MatName) + "_bumpLayer"):
                if REngine == 'Redshift':
                    detailNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
                    cmds.setAttr(detailNode + ".layer1_blend_mode", 1)
                if REngine == 'Arnold':
                    detailNode = mel.eval('shadingNode -asTexture aiLayerRgba')
                    cmds.setAttr(str(detailNode) + '.enable2', 1)
                cmds.rename(detailNode, str(MatName) + "_bumpLayer")
                cmds.disconnectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
                cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
                cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + ".input")

        if os.path.exists(cMapFP + dnMap + FileType) and dnMap != "$identitynormalmap" and dnMap != "$normal" and dnMap != '':
            if not cmds.objExists(dnMap):
                CreateImageNode(str(dnMap),"Place2"+str(dnMap))
                cmds.setAttr(str(dnMap) + ".fileTextureName", cMapFP + dnMap + FileType, type="string")
                cmds.setAttr(str(dnMap) + ".colorSpace", "Raw", type="string")
                print('Detail Map Created')
            
            cmds.connectAttr(str(dnMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL2[REngine]))
            cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE1[REngine]), 1)
            
        if os.path.exists(cMapFP + dnMap2 + FileType) and dnMap2 != "$identitynormalmap" and dnMap2 != "$normal" and dnMap2 != '':
            if not cmds.objExists(dnMap2):
                CreateImageNode(str(dnMap2),"Place2"+str(dnMap2))
                cmds.setAttr(str(dnMap2) + ".fileTextureName", cMapFP + dnMap2 + FileType, type="string")
                cmds.setAttr(str(dnMap2) + ".colorSpace", "Raw", type="string")
                print('Detail Map Created')

            cmds.connectAttr(str(dnMap2) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL3[REngine]))
            cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE2[REngine]), 1)

        if os.path.exists(cMapFP + dnMap3 + FileType) and dnMap3 != "$identitynormalmap" and dnMap3 != "$normal" and dnMap3 != '':
            if not cmds.objExists(dnMap3):
                CreateImageNode(str(dnMap3),"Place2"+str(dnMap3))
                cmds.setAttr(str(dnMap3) + ".fileTextureName", cMapFP + dnMap3 + FileType, type="string")
                cmds.setAttr(str(dnMap3) + ".colorSpace", "Raw", type="string")
                print('Detail Map Created')

            cmds.connectAttr(str(dnMap3) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL3[REngine]))
            cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE3[REngine]), 1)

        if os.path.exists(cMapFP + dnMask + FileType) and dnMask != "$mask" and dnMask != "$black_multimask":
            
            if not cmds.objExists(dnMask) and dnMask != '$mask':
                CreateImageNode(str(dnMask),"Place2"+str(dnMask))
                cmds.setAttr(str(dnMask) + ".fileTextureName", cMapFP + dnMask + FileType, type="string")
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL1[REngine]))
                cmds.connectAttr(str(dnMask) + ".outColorG", str(MatName) + "_bumpLayer" + str(BumpMixL2[REngine]))
                cmds.connectAttr(str(dnMask) + ".outColorB", str(MatName) + "_bumpLayer" + str(BumpMixL3[REngine]))        
            # if not cmds.objExists(dnMap2) and dnMap2 != "$identitynormalmap" and dnMap2 != "$normal":
            #     CreateImageNode(str(dnMap2),"Place2"+str(dnMap2))
            #     cmds.setAttr(str(dnMap2) + ".fileTextureName", cMapFP + dnMap2 + FileType, type="string")
            #     cmds.setAttr(str(dnMap2) + ".colorSpace", "Raw", type="string")
            # if not cmds.objExists(dnMap3) and dnMap3 != "$identitynormalmap" and dnMap3 != "$normal":
            #     CreateImageNode(str(dnMap3),"Place2"+str(dnMap3))
            #     cmds.setAttr(str(dnMap3) + ".fileTextureName", cMapFP + dnMap3 + FileType, type="string")
            #     cmds.setAttr(str(dnMap3) + ".colorSpace", "Raw", type="string")
            # if not cmds.objExists(dnMap4) and dnMap4 != "$identitynormalmap" and dnMap4 != "$normal":
            #     CreateImageNode(str(dnMap4),"Place2"+str(dnMap4))
            #     cmds.setAttr(str(dnMap4) + ".fileTextureName", cMapFP + dnMap4 + FileType, type="string")
            #     cmds.setAttr(str(dnMap4) + ".colorSpace", "Raw", type="string")
            
            # cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_enable", 0)
            # if dnMap1 != "$identitynormalmap" and dnMap1 != "$normal":
            #     # try:
            #         cmds.connectAttr(str(dnMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
            #         cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL1[REngine]))
            #         cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE1[REngine]), 1)
            #         if REngine == 'Redshift':
            #             cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_blend_mode", 1)
                # except:
                #     print("Detail Map 1 skipped")
            # if dnMap2 != "$identitynormalmap" and dnMap2 != "$normal":
            #     try:
            #         cmds.connectAttr(str(dnMap2) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL2[REngine]))
                    
            #         cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE2[REngine]), 1)
            #         if REngine == 'Redshift':
            #             cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer2_blend_mode", 1)
            #     except:
            #         print("Detail Map 2 skipped")
            # if dnMap3 != "$identitynormalmap" and dnMap3 != "$normal":
            #     try:
            #         cmds.connectAttr(str(dnMap3) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL3[REngine]))

            #         cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE3[REngine]), 1)
            #         if REngine == 'Redshift':
            #             cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer3_blend_mode", 1)
            #     except:
            #         print("Detail Map 3 skipped")

            if os.path.exists(cMapFP + eMap + FileType) and cMap != "$black_color":
                if not cmds.objExists(eMap):
                    CreateImageNode(str(eMap),"Place2"+str(eMap))
                cmds.connectAttr(str(eMap) + ".outColor", MatName + MatEmmision[REngine])
                cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMap + FileType, type="string")
                cmds.setAttr(str(MatName) + ".emission_weight", 1)
            # except:
            #     print("Image not found")

OSLText = '''
        color Transformer(float R, float G){


        float NR = (R + G) * 0.5;
        float NG = (R - G) * 0.5;
        float NB = 1.0 - abs(NR) - abs(NG);


        return color(NR * 0.5 + 0.5,NG * -1 * 0.5 + 0.5,NB * 0.5 + 0.5);
    }
    shader specialthing(

        color inColor = color(0,0,0),

        output color outColor = 0

    )

    {
        outColor = Transformer(inColor[0]*2-1, inColor[1]*2-1);
    }'''

def SetupMaterial_S4_IW9():
    global NoNormals
    csMap = ""
    nMap = ""
    gMap = ""
    eMap = ""
    oMap = ""
    sssMap = ""
    dnMask = ""
    dnMap1 = ""
    dnMap2 = ""
    dnMap3 = ""
    ngoMapUF = ""
    eMapUF = ""
    oMapUF = ""
    dnMaskUF = ""
    dnMap1UF = ""
    dnMap2UF = ""
    dnMap3UF = ""
    sssMapUF = ""
    isSkinMaterial = False


    colorSemantic = {
    'Vangaurd': 'unk_semantic_0x0',
    'Modern Warfare II': 'unk_semantic_0x0'}

    ngoSemantic = {
        'Vangaurd': 'unk_semantic_0x8',
        'Modern Warfare II': 'unk_semantic_0x4'}

    opacitySemantic = {
        'Vangaurd': 'unk_semantic_0x18',
        'Modern Warfare II': 'unk_semantic_0xC'}

    emmisiveSemantic = {
        'Vangaurd': 'unk_semantic_0x10',
        'Modern Warfare II': 'INSERT_EMMISIVE_HERE'}

    subsurfaceSemantic = {
        'Vangaurd': 'unk_semantic_0x6F',
        'Modern Warfare II': 'unk_semantic_0x26'}

    detailMaskSemantic = {
        'Vangaurd': 'unk_semantic_0x9F',
        'Modern Warfare II': 'INSERT_MASK_HERE'}

    detail1Semantic = {
        'Vangaurd': 'unk_semantic_0x9',
        'Modern Warfare II': ''}
    detail2Semantic = {
        'Vangaurd': 'unk_semantic_0xA',
        'Modern Warfare II': ''}
    detail3Semantic = {
        'Vangaurd': 'unk_semantic_0xB',
        'Modern Warfare II': ''}
    
    cFile = MatDirectory + "/" + MatName + "_images.txt"
    # print("Material: " + MatName)
    textOpen = open(cFile, "r")
    fList = textOpen.readlines()
    sList = []
    i=0
    for lines in fList:
        semantic_temp = fList[i].split(",")
        semantic_replace = semantic_temp[1]
        semantic_temp[1] = semantic_replace[:-1]
        sList.append(semantic_temp)
        # print(semantic_temp)
        i = i + 1
    sList[0].remove("semantic")
    # print(sList)
    i=0
    for elements in sList:
        if sList[i][0] == colorSemantic[Game]:
            csMap = sList[i][1].partition("&")[0]
            csMapUF = sList[i][1]
        elif sList[i][0] == ngoSemantic[Game]:
            ngoMap = sList[i][1].replace('~','').partition("&")[0]
            ngoMapUF = sList[i][1]
            nMap = sList[i][1].replace('~','').partition("&")[0] + '_n'
        elif sList[i][0] == emmisiveSemantic[Game]:
            eMap = sList[i][1].partition("~")[0]
            eMapUF = sList[i][1]
        elif sList[i][0] == opacitySemantic[Game]:
            oMap = sList[i][1].partition("~")[0]
            oMapUF = sList[i][1]
        elif sList[i][0] == subsurfaceSemantic[Game]:
            sssMap = sList[i][1].partition("~")[0].partition("&")[0]
            sssMapUF = sList[i][1].partition("~")[0]
        elif sList[i][0] == detailMaskSemantic[Game]:
            dnMask = sList[i][1].partition("~")[0].partition("&")[0]
            dnMaskUF = sList[i][1]
        elif sList[i][0] == detail1Semantic[Game]:
            dnMap1 = sList[i][1].partition("&")[0]
            dnMap1UF = sList[i][1]
        elif sList[i][0] == detail2Semantic[Game]:
            dnMap2 = sList[i][1].partition("&")[0]
            dnMap2UF = sList[i][1]
        elif sList[i][0] == detail3Semantic[Game]:
            dnMap3 = sList[i][1].partition("&")[0]
            dnMap3UF = sList[i][1]
        i = i + 1
    # print("Colour and Specular Map: " + csMap + "\n" + "Normal, Gloss and Occlusion Map: " + ngoMapUF + "\n" + "Normal Mask: " + dnMask)
    textOpen.close()

    if cmds.checkBox("image_folder", q=True, v=True) == True:
        cMapFP = MatDirectory + "/_images/" + MatName + "/"
    elif cmds.checkBox("image_folder", q=True, v=True) == False:
        cMapFP = MatDirectory + "/_images/"

    # if sssMap != 'ximage_3c29eeff15212c37' and sssMap != '':
    #     isSkinMaterial = True

    # if isSkinMaterial == True and cmds.nodeType(MatName) != 'RedshiftSkin':
    #     cmds.rename(MatName,str(MatName) + '_temp')
    #     skinNode = cmds.createNode('RedshiftSkin')
    #     cmds.rename(skinNode, MatName)
    #     cmds.connectAttr(MatName + '.outColor', cmds.listConnections(str(MatName) + '_temp.outColor', destination=True)[0] + '.surfaceShader', force=True)
    #     cmds.delete(str(MatName) + '_temp')

    ## Color Map
    if os.path.exists(cMapFP + csMapUF + FileType) and csMap != "$black" and isSkinMaterial == False:
        if not cmds.objExists(csMap):
            CreateImageNode(str(csMap),"Place2"+str(csMap))
            # colorNode = mel.eval('shadingNode -asUtility reverse;')
            # cmds.rename(colorNode, str(csMap) + "_alpha_reverse")
            cmds.setAttr(str(csMap) + ".fileTextureName", cMapFP + csMapUF + FileType, type="string")
        if REngine == 'Redhsift':
            cmds.setAttr(MatName + '.refl_fresnel_mode', 2)
            cmds.setAttr(MatName + MatSheen[REngine], 0.4)
        if REngine == 'Arnold':
            cmds.setAttr(MatName + MatSheen[REngine], 0.1)
        cmds.connectAttr(str(csMap) + ".outColor", MatName + str(MatDiffuse[REngine]))
        if has_transparency(Image.open(cMapFP + csMapUF + FileType)):
            cmds.connectAttr(str(csMap) + ".outAlpha", MatName + MatMetallic[REngine])
        cmds.setAttr(MatName + MatSpec[REngine], 0)

        
        # print("Color Layer connected")
    elif csMap == "$black":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 0, 0, 0)

    ## Specular Map
    # if os.path.exists(cMapFP + csMapUF + FileType) and csMap != "$black" and isSkinMaterial == False:
    #     print("Specular Map exists")
    #     if not cmds.objExists(csMap):
    #         CreateImageNode(str(csMap),"Place2"+str(csMap))
    #         # print("Specular Map Node created")
    #         cmds.setAttr(str(csMap) + ".fileTextureName", cMapFP + csMapUF + FileType, type="string")
    #     if not cmds.objExists(str(csMap) + '_specularLayer'):
    #         # Creates color layer
    #         print("Specular Layer Created")
    #         if REngine == 'Redshift':
    #             specularLayerNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
    #         if REngine == 'Arnold':
    #             specularLayerNode = mel.eval('shadingNode -asTexture aiLayerRgba;')
    #             cmds.setAttr(specularLayerNode + BumpE1[REngine], 1)
    #         cmds.rename(specularLayerNode, str(csMap) + "_specularLayer")
    #         cmds.setAttr(str(csMap) + "_specularLayer" + str(BumpL1[REngine]), 0.22, 0.22, 0.22)
    #         # Connects Color Map to Color Layer
    #         cmds.connectAttr(str(csMap) + ".outColor", str(csMap) + "_specularLayer" + str(BumpL2[REngine]))
    #         cmds.connectAttr(str(csMap) + ".outAlpha", str(csMap) + "_specularLayer" + str(BumpMixL1[REngine]))
    #     # Connects color layer to material
    #     cmds.connectAttr(str(csMap) + "_specularLayer" + ".outColor", MatName + str(MatSpecColor[REngine]))
    #     if REngine == 'Redshift':
    #         cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 1 - Colour Edge & Tint
    #         cmds.setAttr(str(MatName) + ".refl_edge_tintR", 1, clamp=True)
    #         cmds.setAttr(str(MatName) + ".refl_edge_tintG", 1, clamp=True)
    #         cmds.setAttr(str(MatName) + ".refl_edge_tintB", 1, clamp=True)
        

    # if isSkinMaterial == True and os.path.exists(cMapFP + csMapUF + FileType):
    #     if not cmds.objExists(csMap):
    #         CreateImageNode(str(csMap),"Place2"+str(csMap))
    #     if not cmds.objExists(sssMap):
    #         CreateImageNode(str(sssMap),"Place2"+str(sssMap))
    #     if not cmds.objExists(str(csMap) + '_ShallowCC'):
    #         shallowNode = cmds.createNode('RedshiftColorCorrection')
    #         cmds.rename(shallowNode, str(csMap) + '_ShallowCC')
    #         cmds.connectAttr(str(csMap) + '.outColor', str(csMap) + '_ShallowCC' + '.input')
    #         cmds.setAttr(str(csMap) + '_ShallowCC' + '.hue', 5)
    #         cmds.setAttr(str(csMap) + '_ShallowCC' + '.saturation', .8)
    #     cmds.connectAttr(str(sssMap) + '.outColor', str(MatName) + '.deep_color')
    #     cmds.connectAttr(str(csMap) + '.outColor', str(MatName) + '.mid_color')
    #     cmds.connectAttr(str(csMap) + '_ShallowCC' + '.outColor', str(MatName) + '.shallow_color')

    ## Gloss Map
    if os.path.exists(cMapFP + ngoMapUF + FileType) and gMap != "$black":
        if not cmds.objExists(ngoMap):
            CreateImageNode(str(ngoMap),"Place2"+str(ngoMap))
            cmds.setAttr(str(ngoMap) + ".fileTextureName", cMapFP + ngoMapUF + FileType, type="string")
            cmds.setAttr(str(ngoMap) + ".colorSpace", "Raw", type="string")
        if not cmds.objExists(str(ngoMap) + '_ramp'):
            rampNode = mel.eval('shadingNode -asTexture ramp;')
            cmds.rename(rampNode, str(ngoMap) + "_ramp")
            cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[1].position", 1)
            cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[1].color", 1, 1, 1)
            cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[2].position", 0)
            cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[2].color", 0, 0, 0)
            if REngine == 'Redshift':
                cmds.connectAttr(str(ngoMap) + ".outColorR", str(ngoMap) + "_ramp" + ".vCoord")
        if REngine =='Arnold' and bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                if not cmds.objExists(str(ngoMap) + '_reverse'):
                    reverseNode = mel.eval('shadingNode -asTexture reverse;')
                    cmds.rename(reverseNode, str(ngoMap) + '_reverse')
                    cmds.connectAttr(str(ngoMap) + ".outColorR", str(ngoMap) + '_reverse.inputX')
                    cmds.connectAttr(str(ngoMap) + '_reverse.outputX', str(ngoMap) + "_ramp" + ".vCoord")
        
        if isSkinMaterial == True:
            cmds.connectAttr(str(ngoMap) + "_ramp" + ".outColorR", MatName + ".refl_gloss0")
        else:
            cmds.connectAttr(str(ngoMap) + "_ramp" + ".outColorR", MatName + str(MatRough[REngine]))
            cmds.connectAttr(str(ngoMap) + "_ramp" + ".outColorR", MatName + str(MatSheenRough[REngine]))
        
        ConvertGlossToRough()

    ## Normal Map
    if os.path.exists(cMapFP + ngoMapUF + '_n' + FileType) and ngoMap != "$normal":
        if not cmds.objExists(str(ngoMap) + '_bump'):
            if REngine == 'Redshift':
                bumpNode = mel.eval('shadingNode -asTexture RedshiftBumpMap;')
                cmds.setAttr(bumpNode + ".inputType", 1)
                cmds.setAttr(bumpNode + ".scale", 1)
            if REngine == 'Arnold':
                bumpNode = mel.eval('shadingNode -asTexture aiNormalMap;')
            cmds.rename(bumpNode, str(MatName) + "_bump")
        if REngine == 'Redshift':
            if not cmds.objExists(ngoMap):
                CreateImageNode(str(ngoMap),"Place2"+str(ngoMap))
                cmds.setAttr(str(ngoMap) + ".fileTextureName", cMapFP + ngoMapUF + FileType, type="string")
                cmds.setAttr(str(ngoMap) + ".colorSpace", "Raw", type="string")
            if not cmds.objExists(str(ngoMap) + "_OSLConverter"):
                OSLShader = mel.eval('shadingNode -asShader RedshiftOSLShader;')
                cmds.rename(OSLShader, str(ngoMap) + "_OSLConverter")
                removeFromShaderList(str(ngoMap) + "_OSLConverter")
                cmds.setAttr(str(ngoMap) + "_OSLConverter" + str(OSLNodeText[REngine]), OSLText, type="string")
                cmds.connectAttr(str(ngoMap) + ".outColorG", str(ngoMap) + "_OSLConverter" + ".inColorR")
                cmds.connectAttr(str(ngoMap) + ".outAlpha", str(ngoMap) + "_OSLConverter" + ".inColorG")
            cmds.connectAttr(str(ngoMap) + "_OSLConverter" + ".outColor", str(MatName) + "_bump" + ".input")
        if REngine == 'Arnold':
            if not cmds.objExists(nMap):
                CreateImageNode(str(nMap),"Place2"+str(nMap))
                cmds.setAttr(str(nMap) + ".fileTextureName", cMapFP + nMap + FileType, type="string")
                cmds.setAttr(str(nMap) + ".colorSpace", "Raw", type="string")
            cmds.connectAttr(str(nMap) + '.outColor', str(MatName) + "_bump" + '.input')

        cmds.connectAttr(str(MatName) + "_bump" + str(MatBumpOut[REngine]), MatName + str(MatBump[REngine]))
        
        if os.path.exists(cMapFP + dnMap1UF + FileType) and dnMap1 != "$black":
                    if not cmds.objExists(dnMap1):
                        CreateImageNode(str(dnMap1),"Place2"+str(dnMap1))
                        cmds.setAttr(str(dnMap1) + ".fileTextureName", cMapFP + dnMap1UF + FileType, type="string")
                        oslNode = mel.eval('shadingNode -asShader RedshiftOSLShader;')   
                        cmds.rename(oslNode, str(dnMap1) + "_OSLConverter")
                        cmds.setAttr(str(dnMap1) + "_OSLConverter" + ".sourceText", OSLText, type="string")
                        oslNode = mel.eval('shadingNode -asTexture RedshiftColorCorrection;')
                        cmds.rename(oslNode, str(dnMap1) + "_OSLConverterCC")
                        cmds.connectAttr(str(dnMap1) + ".outColorG", str(dnMap1) + "_OSLConverter" + ".inColorR")
                        cmds.connectAttr(str(dnMap1) + ".outAlpha", str(dnMap1) + "_OSLConverter" + ".inColorG")
                        cmds.connectAttr(str(dnMap1) + "_OSLConverter" + ".outColor", str(dnMap1) + "_OSLConverterCC" + ".input")
                        print("Detail Map created and connected to colour correct node")
                        cmds.setAttr(str(dnMap1) + "_OSLConverterCC" + ".contrast", 0.75)
                        cmds.setAttr(str(dnMap1) + ".colorSpace", "Raw", type="string")
                    cmds.disconnectAttr(str(ngoMap) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bump" + ".input")
                    detailLayerNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
                    cmds.rename(detailLayerNode, str(MatName) + "_bumpLayer")
                    cmds.connectAttr(str(ngoMap) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
                    cmds.connectAttr(str(dnMap1) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL2[REngine]))
                    cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + ".input")
                    cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_blend_mode", 1)
        if os.path.exists(cMapFP + dnMap2UF + FileType) and dnMap2 != "$black":
                        if not cmds.objExists(dnMap2):
                            CreateImageNode(str(dnMap2),"Place2"+str(dnMap2))
                            cmds.setAttr(str(dnMap2) + ".fileTextureName", cMapFP + dnMap2UF + FileType, type="string")
                            detail2Node = mel.eval('shadingNode -asShader RedshiftOSLShader;')   
                            cmds.rename(detail2Node, str(dnMap2) + "_OSLConverter")
                            cmds.setAttr(str(dnMap2) + "_OSLConverter" + ".sourceText", OSLText, type="string")
                            detail2CCNode = mel.eval('shadingNode -asTexture RedshiftColorCorrection;')
                            cmds.rename(detail2CCNode, str(dnMap2) + "_OSLConverterCC")
                            cmds.connectAttr(str(dnMap2) + ".outColorG", str(dnMap2) + "_OSLConverter" + ".inColorR")
                            cmds.connectAttr(str(dnMap2) + ".outAlpha", str(dnMap2) + "_OSLConverter" + ".inColorG")
                            cmds.connectAttr(str(dnMap2) + "_OSLConverter" + ".outColor", str(dnMap2) + "_OSLConverterCC" + ".input")
                            print("Detail Map 2 created and connected to colour correct node")
                            cmds.setAttr(str(dnMap2) + "_OSLConverterCC" + ".contrast", 0.75)
                            cmds.setAttr(str(dnMap2) + ".colorSpace", "Raw", type="string")
                        cmds.connectAttr(str(dnMap2) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL3[REngine]))
                        cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE2[REngine]), 1)
                        cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer2_blend_mode", 1)
        if os.path.exists(cMapFP + dnMap3UF + FileType) and dnMap3 != "$black":
                        if not cmds.objExists(dnMap3):
                            CreateImageNode(str(dnMap3),"Place2"+str(dnMap3))
                            cmds.setAttr(str(dnMap3) + ".fileTextureName", cMapFP + dnMap3UF + FileType, type="string")
                            detail3Node = mel.eval('shadingNode -asShader RedshiftOSLShader;')   
                            cmds.rename(detail3Node, str(dnMap3) + "_OSLConverter")
                            cmds.setAttr(str(dnMap3) + "_OSLConverter" + ".sourceText", OSLText, type="string")
                            detail3CCNode = mel.eval('shadingNode -asTexture RedshiftColorCorrection;')
                            cmds.rename(detail3CCNode, str(dnMap3) + "_OSLConverterCC")
                            cmds.connectAttr(str(dnMap3) + ".outColorG", str(dnMap3) + "_OSLConverter" + ".inColorR")
                            cmds.connectAttr(str(dnMap3) + ".outAlpha", str(dnMap3) + "_OSLConverter" + ".inColorG")
                            cmds.connectAttr(str(dnMap3) + "_OSLConverter" + ".outColor", str(dnMap3) + "_OSLConverterCC" + ".input")
                            print("Detail Map 2 created and connected to colour correct node")
                            cmds.setAttr(str(dnMap3) + "_OSLConverterCC" + ".contrast", 0.75)
                            cmds.setAttr(str(dnMap3) + ".colorSpace", "Raw", type="string")
                        cmds.connectAttr(str(dnMap3) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL4[REngine]))
                        cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE3[REngine]), 1)
                        cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer3_blend_mode", 1)
        if os.path.exists(cMapFP + dnMaskUF + FileType) and dnMask != "$black":
            CreateImageNode(str(dnMask),"Place2"+str(dnMask))
            cmds.setAttr(str(dnMask) + ".fileTextureName", cMapFP + dnMaskUF + FileType, type="string")
            if dnMap1 != "$black":
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL1[REngine]))
            if dnMap2 != "$black":
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL2[REngine]))
            if dnMap3 != "$black":
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL3[REngine]))

        ## Emmisive Map
        if os.path.exists(cMapFP + eMapUF + FileType) and eMap != "$black":
                if not cmds.objExists(eMap):
                    CreateImageNode(str(eMap),"Place2"+str(eMap))
                cmds.connectAttr(str(eMap) + ".outColor", MatName + str(MatEmmision[REngine]))
                cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMapUF + FileType, type="string")
                cmds.setAttr(str(MatName) + ".emission_weight", 1)

        # ## Opacity Map
        if os.path.exists(cMapFP + oMapUF + FileType) and oMap != "$black" and oMap != 'ximage_3c29eeff15212c37' and isSkinMaterial == False:
                if not cmds.objExists(oMap):
                    CreateImageNode(str(oMap),"Place2"+str(oMap))
                cmds.connectAttr(str(oMap) + ".outColor", str(MatName) + str(MatOpacity[REngine]))
                cmds.setAttr(str(oMap) + ".fileTextureName", cMapFP + oMapUF + FileType, type="string")
    else:
        NoNormals.append(MatName)

def SetupMaterialH1():
    global MatName
    global FileType
    global OSLText

    FileType = "." + cmds.optionMenu('image_type', q=True, v=True).lower()
    cMap = ""
    aoMap = ""
    nMap = ""
    gMap = ""
    sMap = ""
    eMap = ""
    dnMap = ""
    cFile = MatDirectory + "/" + MatName + "_images.txt"
    # print("Material: " + MatName)
    textOpen = open(cFile, "r")
    fList = textOpen.readlines()
    sList = []
    i=0
    for lines in fList:
        semantic_temp = fList[i].split(",")
        semantic_replace = semantic_temp[1]
        semantic_temp[1] = semantic_replace[:-1]
        sList.append(semantic_temp)
        # print(semantic_temp)
        i = i + 1
    sList[0].remove("semantic")
    # print(sList)
    i=0
    for elements in sList:
        if sList[i][0] == "colorMap":
            cMap = sList[i][1]
        elif sList[i][0] == "normalMap":
            nMap = sList[i][1]
        elif sList[i][0] == "occlusionMap":
            aoMap = sList[i][1]
        elif sList[i][0] == "specularMap":
            gMap = sList[i][1]
            sMap = sList[i][1]
        elif sList[i][0] == "emissiveMap":
            eMap = sList[i][1]
        elif sList[i][0] == "detailMap":
            dnMap = sList[i][1]
        i = i + 1
    # print("Textures: " + "\n" + "Colour Map: " + cMap + "\n" + "Normal Map: " + nMap + "\n" + "Occlusion Map: " + aoMap + "\n" + "Gloss Map: " + gMap, "\n" + "Specular Map: " + sMap)
    textOpen.close()
    
    if cmds.checkBox("image_folder", q=True, v=True) == True:
        cMapFP = MatDirectory + "/_images/" + MatName + "/"
    elif cmds.checkBox("image_folder", q=True, v=True) == False:
        cMapFP = MatDirectory + "/_images/"
    
    # Color Map
    if os.path.exists(cMapFP + cMap + FileType) and cMap != "$black_color" and cMap != "$white_diffuse" and cMap != "$blacktransparent_color":
        try:
            if not cmds.objExists(cMap):
                CreateFileNode(str(cMap))
                cmds.connectAttr(str(cMap) + ".outColor", MatName + str(MatDiffuse[REngine]), force=True)
            if cmds.checkBox("enable_alpha", q=True, v=True) == True:
                cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'R'), force=True)
                cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'G'), force=True)
                cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'B'), force=True)
            cmds.setAttr(str(cMap) + ".fileTextureName", cMapFP + cMap + FileType, type="string")
        except:
            print("Specular Map failed")
    elif cMap == "$white_diffuse":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 1, 1, 1)
    elif cMap == "$black_diffuse" or cMap == "$black" or cMap == "$black_color":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 0, 0, 0)
    
    # Specular Map
    if os.path.exists(cMapFP + sMap + FileType) and not sMap.__contains__("$white"):
        try:
            if not cmds.objExists(Filter(sMap)):
                CreateFileNode(str(Filter(sMap)))
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 1 - Colour Edge & Tint
            cmds.connectAttr(str(Filter(sMap)) + ".outColor", MatName + str(MatSpecColor[REngine]))
            cmds.setAttr(str(Filter(sMap)) + ".fileTextureName", cMapFP + sMap + FileType, type="string")
            cmds.setAttr(str(MatName) + ".refl_edge_tintR", 1, clamp=True)
            cmds.setAttr(str(MatName) + ".refl_edge_tintG", 1, clamp=True)
            cmds.setAttr(str(MatName) + ".refl_edge_tintB", 1, clamp=True)
        except:
            print("Specular Map failed")
    elif sMap == "$specular":
        cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 0.23, 0.23, 0.23)
    elif sMap.find("&white") == -1:
        cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 1, 1, 1)
    elif not os.path.exists(cMapFP + sMap + FileType):
        cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 3) # 3 - IOR

    # Occlusion Map
    if os.path.exists(cMapFP + aoMap + FileType) and aoMap != "$white_ao" and aoMap != "$occlusion_black" and aoMap != "$occlusion_50" and aoMap != "$occlusion":
        try:
            CreateFileNode(str(Filter(aoMap)))
            cmds.connectAttr(str(Filter(aoMap)) + ".outColor", MatName + ".overall_color", force=True)
            cmds.setAttr(str(Filter(aoMap)) + ".fileTextureName", cMapFP + aoMap + FileType, type="string")
        except:
            print("Occlusion Map failed")
    elif aoMap == "$black" or aoMap == "$occlusion_black":
        cmds.setAttr(str(MatName) + ".overall_color", 0, 0, 0)

    # Gloss Map
    if os.path.exists(cMapFP + gMap + FileType) and gMap != "$gloss" and gMap != "$white_gloss" and gMap != "$black" and gMap != "$black_gloss":
            try:
                if not cmds.objExists(Filter(gMap)):
                    CreateFileNode(str(Filter(gMap)))
                    cmds.setAttr(str(Filter(gMap)) + ".fileTextureName", cMapFP + gMap + FileType, type="string")
                    cmds.setAttr(str(Filter(gMap)) + ".colorSpace", "Raw", type="string")
                if not cmds.objExists(Filter(gMap) + "_Ramp"):
                    rampNode = mel.eval('shadingNode -asTexture ramp;')
                    cmds.rename(rampNode, str(Filter(gMap)) + "_Ramp")
                    rampNode = str(Filter(gMap)) + "_Ramp"
                    cmds.setAttr(rampNode + ".colorEntryList[1].position", 1)
                    cmds.setAttr(rampNode + ".colorEntryList[1].color", 1, 1, 1)
                    cmds.setAttr(rampNode + ".colorEntryList[2].position", 0)
                    cmds.setAttr(rampNode + ".colorEntryList[2].color", 0, 0, 0)
                    cmds.connectAttr(str(Filter(gMap)) + ".outAlpha", rampNode + ".vCoord")
                cmds.connectAttr(str(Filter(gMap)) + "_Ramp" + ".outColorR", MatName + str(MatRough[REngine]))
            except:
                print("Gloss Map failed")
    elif gMap == "$gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.23)
    elif gMap == "$white_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 1)
    elif gMap == "$black" or gMap == "$black_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0)

    # Normal Map
    if os.path.exists(cMapFP + nMap + FileType) and nMap != "$identitynormalmap" and nMap != "$normal":
        try:
            if not cmds.objExists(nMap):
                CreateFileNode(str(nMap))
                cmds.setAttr(str(nMap) + ".fileTextureName", cMapFP + nMap + FileType, type="string")
            normalNode = mel.eval('shadingNode -asTexture RedshiftBumpMap;')
            cmds.rename(normalNode, str(MatName) + "_bump")
            cmds.setAttr(str(MatName) + "_bump.inputType", 1)
            cmds.setAttr(str(MatName) + '_bump' + str(MatBumpY[REngine]), 1)
            cmds.setAttr(str(MatName) + "_bump.scale", 1)
            cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
            cmds.connectAttr(str(MatName) + "_bump" + str(MatBumpY[REngine]), MatName + str(MatBump[REngine]))
            cmds.setAttr(str(nMap) + ".colorSpace", "Raw", type="string")
            if os.path.exists(cMapFP + dnMap + FileType) and dnMap != "$identitynormalmap" and dnMap != "$normal":
                if not cmds.objExists(dnMap):
                    CreateFileNode(str(dnMap))
                    cmds.setAttr(str(dnMap) + ".fileTextureName", cMapFP + dnMap + FileType, type="string")
                    detailNode = mel.eval('shadingNode -asShader RedshiftOSLShader;')
                    cmds.setAttr(detailNode + ".sourceText", OSLText, type="string")
                    cmds.connectAttr(str(dnMap) + ".outColor", detailNode + ".inColor")
                    cmds.rename(detailNode, str(dnMap) + "_OSLConverter")
                cmds.disconnectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
                normalLayerNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
                cmds.rename(normalLayerNode, str(MatName) + "_bumpLayer")
                cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
                cmds.connectAttr(str(dnMap) + ".outColorR", str(MatName) + "_bumpLayer" + ".layer1_colorR")
                cmds.connectAttr(str(dnMap) + ".outColorG", str(MatName) + "_bumpLayer" + ".layer1_colorG")
                cmds.connectAttr(str(dnMap) + "_OSLConverter" + ".outColorB", str(MatName) + "_bumpLayer" + ".layer1_colorB")
                cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + ".input")
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_blend_mode", 1)
                cmds.setAttr(str(dnMap) + ".colorSpace", "Raw", type="string")
        except:
            print("Normal Map failed")

    # Emissive Map
    if os.path.exists(cMapFP + eMap + FileType) and cMap != "$black_color":
        try:
            if not cmds.objExists(eMap):
                CreateImageNode(str(eMap),"Place2"+str(eMap))
            cmds.connectAttr(str(eMap) + ".outColor", MatName + str(MatEmmision[REngine]))
            cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMap + FileType, type="string")
            cmds.setAttr(str(MatName) + ".emission_weight", 1)
        except:
            print("Emmision Map failed")
        

####################################################
###### Extra Options ######
####################################################

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

WINDOW_TITLE = "Call of Duty Material Tool"
WINDOW_WIDTH = 400

ROW_SPACING = 2
PADDING = 5

def addColumnLayout():
    cmds.columnLayout(adjustableColumn=True, columnAttach=('both', PADDING))
    
def addFrameColumnLayout(label, collapsable):
    cmds.frameLayout(collapsable=collapsable, label=label)
    addColumnLayout()

def addInnerRowLayout(numberOfColumns):
    cmds.rowLayout(
        numberOfColumns=numberOfColumns,
        bgc=[0,0,0]
    )

def addDoubleRowLayout():
    cmds.rowLayout(
        numberOfColumns=2, 
        adjustableColumn2=2, 
        columnWidth2=[150, 20],
        columnAlign2=['right', 'left'], 
        columnAttach2=['right', 'left']
    )

def parentToLayout():
    cmds.setParent('..')

def addSpacer():
    cmds.columnLayout(adjustableColumn=True)
    cmds.separator(height=PADDING, style="none")
    parentToLayout()
    
def addHeader(windowTitle):
    addColumnLayout()
    cmds.text(label='<span style=\"color:#ccc;text-decoration:none;font-size:20px;font-family:courier new;font-weight:bold;\">' + windowTitle + '</span>', height=50)
    parentToLayout()
    
def addText(label):
    return cmds.text(label='<span style=\"color:#ccc;text-decoration:none;font-size:px;font-family:courier new;font-weight:bold;\">' + label + '</span>')
    
def addButton(label, command):
    cmds.separator(height=ROW_SPACING, style="none")
    controlButton = cmds.button(label=label, command=(command))
    cmds.separator(height=ROW_SPACING, style="none")
    return controlButton
    
def addButtonNoCommand(label):
    cmds.separator(height=ROW_SPACING, style="none")
    controlButton = cmds.button(label=label)
    cmds.separator(height=ROW_SPACING, style="none")
    return controlButton
        
def addIntField():
    return cmds.intFieldGrp()
        
def addIntSlider():
    return cmds.intFieldGrp()
        
# Int Slider
def addIntSliderGroup(min, max, value):
    return cmds.intSliderGrp(field=True, minValue=min, maxValue=max, fieldMinValue=min, fieldMaxValue=max, value=value)
        
# Float Slider
def addFloatSliderGroup(min, max, value):
    return cmds.floatSliderGrp(field=True, minValue=min, maxValue=max, fieldMinValue=min, fieldMaxValue=max, value=value)
    
# Checkbox
def addCheckboxOld(label):
    return cmds.checkBox(label=label)

def addCheckbox(identifier, label,cc = None, value=False):
    cmds.checkBox(identifier,label=str(label),cc=str(cc),v=bool(value))

# Radio Button
def startRadioButtonCollection():
    return cmds.radioCollection()
    
def addRadioButton(label):
    return cmds.radioButton(label=label)
    
# Object Selection List
def addToObjectSelectionList(listIdentifier):
    currentList = cmds.textScrollList(listIdentifier, query=True, allItems=True)
    selection = cmds.ls(selection=True)
    for obj in selection:
        if not isinstance(currentList, list) or obj not in currentList:
            cmds.textScrollList(listIdentifier, edit=True, append=obj)
        
def removeFromObjectSelectionList(listIdentifier):
    listSelection = cmds.textScrollList(listIdentifier, query=True, selectItem=True)
    
    if listSelection != None:
        for listObject in listSelection:
            cmds.textScrollList(listIdentifier, edit=True, removeItem=listObject)
    
def addObjectSelectionList(listIdentifier, label):
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(columnAttach3=['left', 'left', 'right'], numberOfColumns=3, adjustableColumn=3, columnWidth3=[10, 30, 100])
    cmds.iconTextButton(listIdentifier, style='iconOnly', image1='addClip.png', width=22, height=22, command='addToObjectSelectionList("'+listIdentifier+'")')
    cmds.iconTextButton(style='iconOnly', image1='trash.png', width=22, height=22, command='removeFromObjectSelectionList("'+listIdentifier+'")')
    cmds.text(label=label)
    parentToLayout()
    
    scrollList = cmds.textScrollList(listIdentifier, allowMultiSelection=True, height=90)
    parentToLayout()
    return scrollList

# File Browser

# 0     Any file, whether it exists or not.
# 1     A single existing file.
# 2     The name of a directory. Both directories and files are displayed in the dialog.
# 3     The name of a directory. Only directories are displayed in the dialog.
# 4     Then names of one or more existing files.

def browseForDirectory(identifier, mode):
    mode = int(mode)
    path = cmds.fileDialog2(fileMode=mode)
    cmds.textField(identifier, edit=True, text=path[0])

def addFileBrowser(identifier, mode, placeholderText, defaultText):
    cmds.rowLayout(numberOfColumns=2, columnAttach=[(1, 'left', 0), (2, 'right', 0)], adjustableColumn=1, height=22)
    textFieldControl = cmds.textField(identifier, placeholderText=placeholderText, text=defaultText)
    cmds.iconTextButton(style='iconOnly', image1='browseFolder.png', label='spotlight', command='browseForDirectory("'+identifier+'", '+str(mode)+')')
    cmds.setParent("..")
    return textFieldControl;

def newOptionMenu(identifier, label, cc=None):
    cmds.optionMenu(str(identifier), label=str(label), cc=str(cc))

def addMenuItem(identifier, label):
    cmds.menuItem(identifier, label=label)

def addOptionMenu(identifier:str,label:str,menuitems=["1","2","3"],cc=None):
    cmds.optionMenu(identifier, label=str(label),cc=str(cc))
    for i in menuitems:
        cmds.menuItem(label=str(i))
                    
def deleteIfOpen():  
    if cmds.window('windowObject', exists=True):
        cmds.deleteUI('windowObject')
        
def getCloseCommand():
    return('cmds.deleteUI(\"' + 'windowObject' + '\", window=True)')

def createWindow():
    cmds.window(
        'windowObject', 
        title=WINDOW_TITLE, 
        width=WINDOW_WIDTH,
        height=100,
        maximizeButton=False,
        resizeToFitChildren=True
    )
    addSpacer()
    addHeader('Call of Duty Redshift Material Setup')
    addText('Redshift Material Setup Tool for Call of Duty models')
    cmds.text(label='<span style=\"color:#ccc;text-decoration:none;font-size:px;font-family:courier new;font-weight:bold;\">' + "Created by <a href=\"https://twitter.com/MrChuse\" style=\"color:purple\"> MrChuse</a>" + '</span>', hyperlink=True)
    addSpacer()
        
    addDoubleRowLayout()
    addText('Render Engine: ')
    addOptionMenu("render","", ['Arnold', 'Redshift'])
    parentToLayout()
    addFrameColumnLayout('Material Attributes', False)

    addDoubleRowLayout()
    addText('Game: ')
    addOptionMenu("game","", ["Modern Warfare Remastered", "Black Ops 4", "Black Ops Cold War", "Vangaurd", "Modern Warfare II"])
    parentToLayout()
    addDoubleRowLayout()
    addText('Assets Folder: ')
    addFileBrowser("models_path", 2, 'Test placeholder text', 'Select assets folder')
    parentToLayout()

    addDoubleRowLayout()
    addSpacer()
    addCheckbox("image_folder", 'Images Use Image Folders')
    parentToLayout()

    addDoubleRowLayout()
    addSpacer()
    addCheckbox("gloss_or_rough", 'Convert Gloss Maps to Roughness Maps')
    parentToLayout()

    addDoubleRowLayout()
    addSpacer()
    addCheckbox("enable_alpha", 'Connect Alpha Channels')
    parentToLayout()

    addDoubleRowLayout()
    addText('Image Type: ')
    addOptionMenu('image_type', '', ["TIFF", "PNG", "DDS"])
    # newOptionMenu('image_type', '')
    # addMenuItem('.tiff', 'TIFF')
    # addMenuItem('.png', 'PNG')
    # addMenuItem('.dds', 'DDS')
    parentToLayout()

    addButton( 'Start', "Main()")
    addSpacer()

    addFrameColumnLayout('Other Options', True)
    parentToLayout()

    # addDoubleRowLayout()
    addSpacer()
    addButton( 'Setup Skin Materials', "setupSkin()")
    parentToLayout()
    
    cmds.showWindow('windowObject')
deleteIfOpen()
createWindow()