import maya.cmds as cmds
import random
import maya.mel as mel
import os as os
import csv
from pathlib import Path
import glob

textPath = ""
MatName = ""
MatDirectory = ""
MatList = []
FileType = ""


def GetFilePath():
    filename = cmds.fileDialog2(fileMode=1, caption="Import Text File")
    global textPath
    textPath = filename[0]


def SetupPaths():
    global textPath
    textPath = cmds.textField("text_path", q=True, tx=True)
    MatNameTemp = textPath.split("/")
    MatNameTemp = MatNameTemp[-1]

    if MatNameTemp.endswith("_images.txt"):
        MatNameTemp = MatNameTemp[:-len("_images.txt")]
    
    global MatDirectory
    global MatName
    MatName = MatNameTemp
    MatDirectory = textPath[:-len("/" + MatName + "_images.txt")]

def SetupMatList():
    global MatList
    MatPathList = glob.glob(MatDirectory + "/" + "*.txt") # Creates the list with paths
    MatListTemp = []
    j=0
    for i in MatPathList:
        MatListTemp.append(MatPathList[j].replace(MatDirectory + "\\", "")) # Removes path from string
        j = j + 1
    j=0
    for i in MatListTemp:
        MatList.append(MatListTemp[j].replace("_images.txt", ""))
        j = j + 1
    print("Material Names: ", MatList)
    



def ReplaceMaterial():
    global MatName
    if cmds.objExists(MatName):
       mel.eval('''rsCreateShadingNode "rendernode/redshift/shader/surface" "-asShader" "" RedshiftMaterial;''')
       cmds.rename(cmds.ls(selection=True), "rsTemp")
       print(MatName)
       cmds.nodeCast( MatName, "rsTemp", disconnectUnmatchedAttrs=True, force=True)
       cmds.delete(MatName)
       cmds.rename("rsTemp", MatName)
       print("Material Created: " + MatName)
       mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
       SetupMaterial()
    else:
        print(MatName, " does not exist.")

def ConvertGlossToRough():
    Boolvariable = cmds.checkBox("gloss_or_rough", q=True, v=True)
    if Boolvariable == True:
        i=0
        for materials in MatList:
            cmds.setAttr(str(MatList[i]) + ".refl_isGlossiness", 1)
            i = i + 1

def CreateImageNode(Node2d="Node2dTemp",Place2dNode="Place2dNodeTemp"):
    mel.eval('shadingNode -asTexture -isColorManaged file;')
    cmds.rename(cmds.ls(selection=True), str(Node2d))
    mel.eval('shadingNode -asUtility place2dTexture;')
    cmds.rename(cmds.ls(selection=True), str(Place2dNode))
    print(Place2dNode, Node2d)
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


def SetupMaterial():
    global MatName
    global FileType
    FileType = "." + cmds.optionMenu('image_type', q=True, v=True).lower()
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
    print("Material: " + MatName)
    textOpen = open(cFile, "r")
    fList = textOpen.readlines()
    sList = []
    i=0
    for lines in fList:
        semantic_temp = fList[i].split(",")
        semantic_replace = semantic_temp[1]
        semantic_temp[1] = semantic_replace[:-1]
        sList.append(semantic_temp)
        print(semantic_temp)
        i = i + 1
    sList[0].remove("semantic")
    print(sList)
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
            dnMap1 = sList[i][1]
        elif sList[i][0] == "detailNormal2":
            dnMap2 = sList[i][1]
        elif sList[i][0] == "detailNormal3":
            dnMap3 = sList[i][1]
        elif sList[i][0] == "detailNormal4":
            dnMap4 = sList[i][1]
        i = i + 1
    print("Colour Map: " + cMap + "\n" + "Normal Map: " + nMap + "\n" + "Occlusion Map: " + aoMap + "\n" + "Gloss Map: " + gMap)
    textOpen.close()
    
    # Make and connect colour map.
    cMapFP = MatDirectory + "/_images/"
    Boolvariable = cmds.checkBox("enable_alpha", q=True, v=True)
    # cmds.shadingNode("file", asTexture=True, name="textureMapTemp")
    
    if os.path.exists(cMapFP + cMap + FileType) and cMap != "$black_color":
        if not cmds.objExists(cMap):
            CreateImageNode(str(cMap),"Place2"+str(cMap))
        cmds.connectAttr(str(cMap) + ".outColor", MatName + ".diffuse_color")
        if Boolvariable == True:
            cmds.connectAttr(str(cMap) + ".outAlpha", MatName + ".opacity_colorR")
            cmds.connectAttr(str(cMap) + ".outAlpha", MatName + ".opacity_colorG")
            cmds.connectAttr(str(cMap) + ".outAlpha", MatName + ".opacity_colorB")
        cmds.setAttr(str(cMap) + ".fileTextureName", cMapFP + cMap + FileType, type="string")

    if os.path.exists(cMapFP + sMap + FileType) and sMap != "$specular":
        if not cmds.objExists(sMap):
            CreateImageNode(str(sMap),"Place2"+str(sMap))
        cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 1 - Colour Edge & Tint
        cmds.connectAttr(str(sMap) + ".outColor", MatName + ".refl_reflectivity")
        cmds.setAttr(str(sMap) + ".fileTextureName", cMapFP + sMap + FileType, type="string")
        cmds.setAttr(str(MatName) + ".refl_edge_tintR", 1, clamp=True)
        cmds.setAttr(str(MatName) + ".refl_edge_tintG", 1, clamp=True)
        cmds.setAttr(str(MatName) + ".refl_edge_tintB", 1, clamp=True)
    elif sMap == "$specular":
        cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 3 - IOR
        cmds.setAttr(str(MatName) + ".refl_reflectivity", 0.23)
    elif not os.path.exists(cMapFP + sMap + FileType):
        cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 3) # 3 - IOR

    if os.path.exists(cMapFP + aoMap + FileType) and aoMap != "$white_ao" and aoMap != "$occlusion_black" and aoMap != "$occlusion_50" and aoMap != "$occlusion":
        print("Occlusion map found")
        CreateImageNode(str(aoMap),"Place2"+str(aoMap))
        cmds.connectAttr(str(aoMap) + ".outColor", MatName + ".overall_color")
        cmds.setAttr(str(aoMap) + ".fileTextureName", cMapFP + aoMap + FileType, type="string")
    elif aoMap == "$black" or aoMap == "$occlusion_black":
        cmds.setAttr(str(MatName) + ".overall_color", 0, 0, 0)

    if os.path.exists(cMapFP + gMap + FileType) and gMap != "$gloss" and gMap != "$white_gloss" and gMap != "$black":
        print("Gloss Map is not $gloss")
        if not cmds.objExists(gMap + "loss"):
            CreateImageNode(str(gMap) + "loss","Place2"+str(gMap) + "loss")
            cmds.setAttr(str(gMap) + "loss" + ".fileTextureName", cMapFP + gMap + FileType, type="string")
            mel.eval('shadingNode -asTexture ramp;')
            cmds.rename(cmds.ls(selection=True), str(gMap) + "loss" + "_ramp")
            cmds.connectAttr(str(gMap) + "loss" + ".outColorR", str(gMap) + "loss" + "_ramp" + ".vCoord")
        cmds.connectAttr(str(gMap) + "loss" + "_ramp" + ".outColorR", MatName + ".refl_roughness")
        cmds.setAttr(str(gMap) + "loss" + ".colorSpace", "Raw", type="string")
    elif gMap == "$gloss":
        cmds.setAttr(str(MatName) + ".refl_roughness", 0.23)
    elif gMap == "$white_gloss":
        cmds.setAttr(str(MatName) + ".refl_roughness", 1)
    elif gMap == "$black":
        cmds.setAttr(str(MatName) + ".refl_roughness", 0)
    
    if os.path.exists(cMapFP + nMap + FileType) and nMap != "$identitynormalmap" and nMap != "$normal":
        if not cmds.objExists(nMap):
            CreateImageNode(str(nMap),"Place2"+str(nMap))
            cmds.setAttr(str(nMap) + ".fileTextureName", cMapFP + nMap + FileType, type="string")
        mel.eval('shadingNode -asTexture RedshiftBumpMap;')
        cmds.rename(cmds.ls(selection=True), str(MatName) + "_bump")
        cmds.setAttr(str(MatName) + "_bump.inputType", 1)
        cmds.setAttr(str(MatName) + "_bump.flipY", 1)
        cmds.setAttr(str(MatName) + "_bump.scale", 1)
        cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
        cmds.connectAttr(str(MatName) + "_bump" + ".out", MatName + ".bump_input")
        cmds.setAttr(str(nMap) + ".colorSpace", "Raw", type="string")
        if os.path.exists(cMapFP + dnMap + FileType) and dnMap != "$identitynormalmap" and dnMap != "$normal":
            if not cmds.objExists(dnMap):
                CreateImageNode(str(dnMap),"Place2"+str(dnMap))
                cmds.setAttr(str(dnMap) + ".fileTextureName", cMapFP + dnMap + FileType, type="string")
            cmds.disconnectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
            mel.eval('shadingNode -asTexture RedshiftColorLayer;')
            cmds.rename(cmds.ls(selection=True), str(MatName) + "_bumpLayer")
            cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bumpLayer" + ".base_color")
            cmds.connectAttr(str(dnMap) + ".outColor", str(MatName) + "_bumpLayer" + ".layer1_color")
            cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + ".input")
            cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_blend_mode", 1)
        elif os.path.exists(cMapFP + dnMask + FileType):
            cmds.disconnectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
            mel.eval('shadingNode -asTexture RedshiftColorLayer;')
            cmds.rename(cmds.ls(selection=True), str(MatName) + "_bumpLayer")
            cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bumpLayer" + ".base_color")
            if not cmds.objExists(dnMap1) and dnMap1 != "$identitynormalmap":
                CreateImageNode(str(dnMap1),"Place2"+str(dnMap1))
                cmds.setAttr(str(dnMap1) + ".fileTextureName", cMapFP + dnMap1 + FileType, type="string")
                cmds.setAttr(str(dnMap1) + ".colorSpace", "Raw", type="string")
            if not cmds.objExists(dnMap2) and dnMap2 != "$identitynormalmap":
                CreateImageNode(str(dnMap2),"Place2"+str(dnMap2))
                cmds.setAttr(str(dnMap2) + ".fileTextureName", cMapFP + dnMap2 + FileType, type="string")
                cmds.setAttr(str(dnMap2) + ".colorSpace", "Raw", type="string")
            if not cmds.objExists(dnMap3) and dnMap3 != "$identitynormalmap":
                CreateImageNode(str(dnMap3),"Place2"+str(dnMap3))
                cmds.setAttr(str(dnMap3) + ".fileTextureName", cMapFP + dnMap3 + FileType, type="string")
                cmds.setAttr(str(dnMap3) + ".colorSpace", "Raw", type="string")
            if not cmds.objExists(dnMap4) and dnMap4 != "$identitynormalmap":
                CreateImageNode(str(dnMap4),"Place2"+str(dnMap4))
                cmds.setAttr(str(dnMap4) + ".fileTextureName", cMapFP + dnMap4 + FileType, type="string")
                cmds.setAttr(str(dnMap4) + ".colorSpace", "Raw", type="string")
            CreateImageNode(str(dnMask),"Place2"+str(dnMask))
            cmds.setAttr(str(dnMask) + ".fileTextureName", cMapFP + dnMask + FileType, type="string")
            cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_enable", 0)
            if dnMap1 != "identitynormalmap":
                cmds.connectAttr(str(dnMap1) + ".outColor", str(MatName) + "_bumpLayer" + ".layer1_color")
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + ".layer1_alpha")
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_enable", 1)
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_blend_mode", 1)
            if dnMap2 != "identitynormalmap":
                cmds.connectAttr(str(dnMap1) + ".outColor", str(MatName) + "_bumpLayer" + ".layer2_color")
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + ".layer2_alpha")
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer2_enable", 1)
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer2_blend_mode", 1)
            if dnMap3 != "identitynormalmap":
                cmds.connectAttr(str(dnMap1) + ".outColor", str(MatName) + "_bumpLayer" + ".layer3_color")
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + ".layer3_alpha")
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer3_enable", 1)
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer3_blend_mode", 1)
            if dnMap4 != "identitynormalmap":
                cmds.connectAttr(str(dnMap1) + ".outColor", str(MatName) + "_bumpLayer" + ".layer4_color")
                cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + ".layer4_alpha")
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer4_enable", 1)
                cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer4_blend_mode", 1)
            cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + ".input")

            if os.path.exists(cMapFP + eMap + FileType) and cMap != "$black_color":
                if not cmds.objExists(eMap):
                    CreateImageNode(str(eMap),"Place2"+str(eMap))
                cmds.connectAttr(str(eMap) + ".outColor", MatName + ".emission_color")
                cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMap + FileType, type="string")
                cmds.setAttr(str(MatName) + ".emission_weight", 1)
    else:
        print("Image not found")


def Main():
    global MatName
    global MatList
    print("Text Path: ", textPath)
    SetupPaths()
    SetupMatList()
    mat=0
    for i in MatList:
        MatName = MatList[mat]
        print("Current material: ", MatName)
        ReplaceMaterial()
        mat=mat+1
    ConvertGlossToRough()


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
        
    addFrameColumnLayout('Material Attributes', True)

    addDoubleRowLayout()
    addText('Material Text File')
    addFileBrowser("text_path", 1, 'Test placeholder text', 'Select any of the material text files')
    parentToLayout()

    addDoubleRowLayout()
    addSpacer()
    addCheckbox("gloss_or_rough", 'Convert Gloss Maps to Roughness Maps')
    parentToLayout()

    addDoubleRowLayout()
    addSpacer()
    addCheckbox("enable_alpha", 'Connect Alpha Channels')
    parentToLayout()

    newOptionMenu('image_type', 'Image Type: ')
    addMenuItem('.tiff', 'TIFF')
    addMenuItem('.png', 'PNG')
    addMenuItem('.dds', 'DDS')

    addButton( 'Start', "Main()")

    cmds.showWindow('windowObject')
deleteIfOpen()
createWindow()