
## Material Converter for Maya by MrChuse
## https://twitter.com/MrChuse


## Version 1.0.8.2

# Fixed issue with gloss maps not working
# Added option to disable detail maps
# Added Arnold support for skin materials
# Added Arnold support for reflection presets

## This script is designed to convert materials from the Call of Duty games to Maya materials.



## TODO
# Create json to store settings
# Check current render engine in R settings
# Make a plugin?
# Add github check for version


import maya.cmds as cmds
import maya.mel as mel
import os as os

RestartMaya = False
try:
    from PIL import Image
except:
    os.system("mayapy -m pip install Pillow")
    from PIL import Image
    RestartMaya = True
try:
    import numpy
except:
    os.system("mayapy -m pip install numpy")
    import numpy
    RestartMaya = True

if RestartMaya == True:
    DR = cmds.confirmDialog(title="Material Converter", 
                            message="It seems you haven't installed this library to your Maya. Would you like to install it and restart Maya?", 
                            button=["Yes","No"], defaultButton="Yes")
    if DR == "Yes":
        cmds.quit()

textPath = ""
MatName = ""
MatDirectory = ""
MatList = []
FileType = ""
Game = ''
REngine = ''
NoNormals = []
PROJECT = cmds.workspace(fn=True)
MatDiffuse={
    "Redshift":".diffuse_color",
    "Arnold":".baseColor",
    "USD": ".diffuseColor",
    "RenderMan": ".diffuseColor",
    "RenderManDis": ".baseColor"
}

MatSpec={
    "Redshift":".refl_weight",
    "Arnold":".specular",
    "RenderManDis": ".specular"
}

MatSpecColor={
    "Redshift":".refl_reflectivity",
    "Arnold":".specularColor",
    "USD": ".specularColor",
    "RenderMan": ".specularFaceColor"
}

MatIOR ={
    "Redshift": ".refl_ior",
    "Arnold": ".specularIOR",
    "USD": ".ior",
    "RenderMan": ".ior" # ????
}

MatMetallic={
    "Redshift":".refl_metalness",
    "Arnold":".metalness",
    "USD": ".metallic",
    "RenderManDis": ".metallic"
}

MatRough={
    "Redshift":".refl_roughness",
    "Arnold":".specularRoughness",
    "USD": ".roughness",
    "RenderMan": ".specularRoughness",
    "RenderManDis": ".roughness"
}

MatSheen={
    "Redshift":".sheen_weight",
    "Arnold":".sheen",
    "RenderManDis": ".sheen"
}

MatSheenRough={
    "Redshift":".sheen_roughness",
    "Arnold":".sheenRoughness",
    "RenderMan": ".roughSpecularRoughness"
}

MatBump={
    "Redshift":".bump_input",
    "Arnold":".normalCamera",
    "USD": ".normal",
    "RenderMan": ".bumpNormal",
    "RenderManDis": ".bumpNormal"
}

MatBumpY={
    "Redshift":".flipY",
    "Arnold":".invertY",
    "RenderMan": ".flipY",
    "RenderManDis": ".flipY"
}

MatBumpIn={
    "Redshift":".input",
    "Arnold":".input",
    "RenderMan": ".inputRGB",
    "RenderManDis": ".inputRGB"
}

MatBumpOut={
    "Redshift":".out",
    "Arnold":".outValue",
    "RenderMan": ".resultN",
    "RenderManDis": ".resultN"
}

BumpL1={
    "Redshift":".base_color",
    "Arnold":".input1",
    "USD": ".normal0",
    "RenderMan": ".baselayer_bumpNormal",
    "RenderManDis": ".baselayer_bumpNormal"
}
BumpL2={
    "Redshift":".layer1_color",
    "Arnold":".input2",
    "RenderMan": ".layer1_bumpNormal",
    "RenderManDis": ".layer1_bumpNormal"
}
BumpL3={
    "Redshift":".layer2_color",
    "Arnold":".input3",
    "RenderMan": ".layer2_bumpNormal",
    "RenderManDis": ".layer2_bumpNormal"
}
BumpL4={
    "Redshift":".layer3_color",
    "Arnold":".input4",
    "RenderMan": ".layer3_bumpNormal",
    "RenderManDis": ".layer3_bumpNormal"
}

BumpMixL1={
    "Redshift":".layer1_mask",
    "Arnold":".mix2",
    "RenderMan": ".layer1Mask",
    "RenderManDis": ".layer1Mask"
}
BumpMixL2={
    "Redshift":".layer2_mask",
    "Arnold":".mix3",
    "RenderMan": ".layer2Mask",
    "RenderManDis": ".layer2Mask"
}
BumpMixL3={
    "Redshift":".layer3_mask",
    "Arnold":".mix4",
    "RenderMan": ".layer3Mask",
    "RenderManDis": ".layer3Mask"
}

BumpE1={
    "Redshift":".layer1_enable",
    "Arnold":".enable2",
    "RenderMan": ".layer1Enabled",
    "RenderManDis": ".layer1Enabled"
}

BumpE2={
    "Redshift":".layer2_enable",
    "Arnold":".enable3",
    "RenderMan": ".layer2Enabled",
    "RenderManDis": ".layer2Enabled"
}
BumpE3={
    "Redshift":".layer3_enable",
    "Arnold":".enable4",
    "RenderMan": ".layer3Enabled",
    "RenderManDis": ".layer3Enabled"
}
MatOpacity={
    "Redshift":".opacity_color",
    "Arnold":".opacity",
    "USD": ".opacity",
    "RenderMan": ".presence",
    "RenderManDis": ".presence",
}

MatEmmision={
    "Redshift":".emission_color",
    "Arnold":".emissionColor",
    "USD": ".emissiveColor",
    "RenderMan": ".glowColor",
    "RenderManDis": ".glowColor"
}

MatEmmisionStrength={
    "Redshift":".emission_weight",
    "Arnold":".emission",
}
OSLNodeText={
    "Redshift":".sourceText",
    "Arnold":".code",
}
def Main():
    global modelsPath
    global MatList
    global Game
    global MatName
    global MatDirectory
    global FileType
    global REngine
    
    MatProgress = 0
    while True:
        modelsPath = cmds.textField("models_path", q=True, tx=True)
        modelsFolders = os.listdir(str(modelsPath))
        # print(modelsFolders)
        FileType = "." + cmds.optionMenu('image_type', q=True, v=True).lower()
        Game = cmds.optionMenu('game', q=True, v=True)
        REngine = cmds.optionMenu('render', q=True, v=True)
        if REngine == 'RenderMan' and Game == 'Modern Warfare II':
            REngine = 'RenderManDis'
        # print("FileType: " + FileType)
        
        models = []
        for folder in modelsFolders:
            if not folder.__contains__('.'):
                models.append(folder)
        print("Number of models: ", len(models))

        cmds.progressWindow( title='Material Converter',progress=0,status='Importing...',isInterruptable=True )
        
        print(models)
        for model in models:
            
            print("Model: ", model)
            if not model.__contains__('.'):
                modelFiles = os.listdir(str(modelsPath + '/' + model))
                for file in modelFiles:
                    if file.endswith("_images.txt"):
                        MatList.append(str(file[:-len("_images.txt")]))
                
                # print('Materials: ', MatList)

            for MatName in MatList:
                MatDirectory = modelsPath + '/' + model
                # print("Material: ", MatName)
                if  cmds.objExists(MatName) and MatName != "lambert1":
                    if cmds.nodeType(MatName) != "aiStandardSurface" and cmds.nodeType(MatName) != "RedshiftMaterial" and cmds.nodeType(MatName) != "transform" and cmds.nodeType(MatName) != 'shadingEngine' and cmds.nodeType(MatName) != 'RedshiftSkin':
                        if REngine == 'Redshift':
                            materialNode = cmds.shadingNode('RedshiftMaterial', asShader=True)
                        elif REngine == 'Arnold':
                            materialNode = cmds.shadingNode('aiStandardSurface', asShader=True)
                            # print(modelSG)
                        elif REngine == 'USD':
                            materialNode = cmds.shadingNode('usdPreviewSurface', asShader=True)
                        elif REngine == 'RenderMan':
                            materialNode = cmds.shadingNode('PxrSurface', asShader=True)
                        elif REngine == 'RenderManDis':
                            materialNode = cmds.shadingNode('PxrDisney', asShader=True)
                        
                        modelSG = cmds.listConnections(MatName + '.outColor', destination=True)[0]
                        
                        cmds.connectAttr(str(materialNode + '.outColor'), str(modelSG + '.surfaceShader'), force=True)
                        cmds.delete(MatName)
                        cmds.rename(materialNode, MatName)
                        print("Material Created: " + MatName)
                        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

                        if Game == "Black Ops III / 4 / CW":
                            SetupMaterialTreyarch()
                        if Game in ("Modern Warfare 2019", "Vangaurd", "Modern Warfare II", "Infinite Warfare"):
                            SetupMaterial_S4_IW9()
                        if Game == "Modern Warfare Remastered":
                            SetupMaterialH1()
                        
                        
                else:
                    print(MatName, " does not exist.")
                    
            MatList.clear()
            print("Thse Materials have no Normal Maps: \n", NoNormals)

            MatProgress = MatProgress + 1
            cmds.progressWindow( edit=True, status='Current Model: ' + model)
            cmds.progressWindow( edit=True,progress=int((MatProgress/len(models))* 100))
                        
            if cmds.progressWindow(query=True, isCancelled=True) == True:
                break
        
        cmds.progressWindow(endProgress=1)
        break

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

def CreateTex(Tex='', ImageFP='', InTex='', Channel=''):


    def CreateNormalTex(G, A):
        # convert to float
        
        G = G.convert("F")
        A = A.convert("F")

        # get numpy arrays
        
        X = numpy.array(G)
        Y = numpy.array(A)
        # remap from [0, 255] to [0, 1]
        
        X = X / 255.0
        Y = Y / 255.0

        # remap floats to [-1, 1] range
        
        X = (X * 2) - 1
        Y = (Y * 2) - 1

        NX = (X + Y) * 0.5
        NY = (X - Y) * 0.5
        # calculates the up vector from the other 2
        NZ = 1 - numpy.abs(NX) - numpy.abs(NY)
        # eval 1 - R
        # calculate the length of the vector
        LEN = numpy.sqrt((NX*NX) + (NY*NY) + (NZ*NZ))

        # normalize vector
        NX = NX / LEN
        NY = NY / LEN
        NZ = NZ / LEN

        # remap floats to [0, 1] range
        
        NX = (NX * 0.5) + 0.5
        NY = (NY * 0.5) + 0.5
        NZ = (NZ * 0.5) + 0.5

        # remap from [0, 1] to [0, 255] and convert to image
        
        NormalX = Image.fromarray(NX * 255)
        NormalY = Image.fromarray(NY * 255)
        NormalZ = Image.fromarray(NZ * 255)

        # convert to 8 bit channels and merge to RGB image
        Normal = Image.merge('RGB', (NormalX.convert("L"), NormalY.convert("L"), NormalZ.convert("L")))
        
        print(FP + InTex + "." + (NGO.format).lower())
        Normal.save(FP + InTex + "." + (NGO.format).lower())
        
    def CreateRoughnessTex(R):
        if Channel == 'R' or Channel == '':
            R = R.convert("F")
            W = numpy.array(R)
        if Channel == 'A':
            A = A.convert("F")
            W = numpy.array(A)
        W = W / 255.0
        W = 1 - W
        Rough = Image.fromarray(W * 255)
        Roughness = Image.merge('RGB', (Rough.convert("L"), Rough.convert("L"), Rough.convert("L")))
        # print(FP + InTex + "." + (NGO.format).lower())
        Roughness.save(FP + InTex + "." + (NGO.format).lower())

    if Tex == 'Gloss' or Tex == 'Normal':
        FP = ImageFP.split("\\")
        FP.remove(FP[-1])
        FP = "\\".join(FP.copy())
        NGO = Image.open(ImageFP)

    if Tex == 'Normal':
        R, G, B, A = NGO.split()
        CreateNormalTex(G, A)

    if Tex == 'Gloss':
        if Game == 'Modern Warfare Remastered':
            # try:
            R, G, B, A = NGO.split()
                
            # except:
            #     print("Failed to create texture") 
            CreateRoughnessTex(A)
        else:  
            try:
                R, G, B = NGO.split()
                CreateRoughnessTex(R)
            except:
                print("Failed to create texture")

def Filter(map):
    return map.replace("~","").replace("-","_").replace("$","").replace("&","__")

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

def useGlossCheck():
    if cmds.checkBox('gloss_rough', q=True, v=True):
        return True
    
def SetupMaterialTreyarch():
    cMap = ""
    aoMap = ""
    nMap = ""
    gMap = ""
    sMap = ""
    eMap = ""
    dnMap = ""
    dnMask = ""
    dnMap2 = ""
    dnMap3 = ""
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
            cMap:str = sList[i][1]
        elif sList[i][0] == "normalMap":
            nMap = sList[i][1]
        elif sList[i][0] == "aoMap":
            aoMap = sList[i][1]
        elif sList[i][0] == "glossMap":
            gMap = sList[i][1]
            rMap = gMap[:-1] + str("roughness")
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
    if os.path.exists(str(cMapFP + cMap + FileType)) and cMap != "$black_color" and cMap != "$white_diffuse" and cMap != "$blacktransparent_color" and cMap != "$color_black_40":
        try:
            if not cmds.objExists(cMap):
                CreateImageNode(str(cMap),"Place2"+str(cMap))
                cmds.setAttr(str(cMap) + ".fileTextureName", cMapFP + cMap + FileType, type="string")
                # print("Color Map created")
            cmds.connectAttr(str(cMap) + ".outColor", MatName + str(MatDiffuse[REngine]))
            if cmds.checkBox("enable_alpha", q=True, v=True) == True and has_transparency(Image.open(cMapFP + cMap + FileType)) == True:
                if REngine == 'Arnold' or REngine == 'Redshift':
                    cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'R'))
                    cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'G'))
                    cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'B'))
                else:
                    cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine]))
        except:
            print("Color Map failed")
    elif cMap == "$white_diffuse":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 1, 1, 1)
    elif cMap == "$black_diffuse" or cMap == "$black" or cMap == "$black_color" or cMap == "$color_black_40":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 0, 0, 0)

    # Specular Map
    if os.path.exists(cMapFP + sMap + FileType) and sMap != "$specular" and sMap != "$white_specular" and sMap != "$specular_mask":
        try:
            if not cmds.objExists(sMap):
                CreateImageNode(str(sMap),"Place2"+str(sMap))
                cmds.setAttr(str(sMap) + ".fileTextureName", cMapFP + sMap + FileType, type="string")
                
            if REngine == 'Redshift':
                cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 1 - Colour Edge & Tint
                cmds.setAttr(str(MatName) + ".refl_edge_tintR", 1, clamp=True)
                cmds.setAttr(str(MatName) + ".refl_edge_tintG", 1, clamp=True)
                cmds.setAttr(str(MatName) + ".refl_edge_tintB", 1, clamp=True)
            
            cmds.connectAttr(str(sMap) + ".outColor", MatName + str(MatSpecColor[REngine]))
        except:
            print("Specular Map failed")
    elif sMap == "$specular" or sMap == '':
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        if REngine != 'RenderMan':
            cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 0.23, 0.23, 0.23)
        else:
            cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 0.04, 0.04, 0.04)
    elif sMap == "$white_specular" or sMap == "$specular_mask":
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 1, 1, 1)
    elif not os.path.exists(cMapFP + sMap + FileType):
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 3) # 3 - IOR

    # AO Map
    if os.path.exists(cMapFP + aoMap + FileType) and aoMap != "$white_ao" and aoMap != "$occlusion_black" and aoMap != "$occlusion_50" and aoMap != "$occlusion":
        if REngine == 'Redshift' or REngine == 'USD':
            try:
                if not cmds.objExists(aoMap):
                    CreateImageNode(str(aoMap),"Place2"+str(aoMap))
                    cmds.setAttr(str(aoMap) + ".fileTextureName", cMapFP + aoMap + FileType, type="string")
                if REngine == 'Redshift':
                    cmds.connectAttr(str(aoMap) + ".outColor", MatName + ".overall_color")
                elif REngine == 'RenderMan' or REngine == 'Arnold':
                    if cmds.objExists(cMap):
                        cmds.shadingNode('multiplyDivide', name=str(MatName) + '_AOMult', asShader=True)
                        cmds.connectAttr(str(cMap) + '.outColor', str(MatName) + '_AOMult' + '.input1')
                        cmds.connectAttr(str(aoMap) + '.outColor', str(MatName) + '_AOMult' + '.input2')
                        cmds.connectAttr(str(MatName) + '_AOMult' + '.output', MatName + MatDiffuse[REngine], force=True)
                elif REngine == 'USD':
                    cmds.connectAttr(str(aoMap) + ".outColorR", MatName + ".occlusion")   
            except:
                print("Occlusion map failed")
    elif aoMap == "$black" or aoMap == "$occlusion_black":
        cmds.setAttr(str(MatName) + ".overall_color", 0, 0, 0)

    ## Gloss Map
    if os.path.exists(cMapFP + gMap + FileType) and gMap != "$gloss" and gMap != "$white_gloss" and gMap != "$black" and gMap != "$black_gloss" and gMap != "$gray" and gMap != "$color_black_40":
        try:
            if REngine != 'USD':
                if not cmds.objExists(gMap):
                    CreateImageNode(str(gMap),"Place2"+str(gMap))
                    cmds.setAttr(str(gMap) + ".fileTextureName", cMapFP + gMap + FileType, type="string")
                    cmds.setAttr(str(gMap) + ".colorSpace", "Raw", type="string")
                    glossNode = mel.eval('shadingNode -asTexture ramp;')
                    cmds.rename(glossNode, str(gMap) + "_ramp")
                    cmds.setAttr(str(gMap) + "_ramp.colorEntryList[1].position", 1)
                    cmds.setAttr(str(gMap) + "_ramp.colorEntryList[1].color", 1, 1, 1)
                    cmds.setAttr(str(gMap) + "_ramp.colorEntryList[2].position", 0)
                    cmds.setAttr(str(gMap) + "_ramp.colorEntryList[2].color", 0, 0, 0)

                    # If the roughness maps are gloss maps, reverse and connect it 
                    if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                        # if REngine in ['Redshift', 'Arnold', 'RenderMan']:
                            reverseNode = mel.eval('shadingNode -asTexture reverse;')
                            cmds.rename(reverseNode, str(gMap) + '_reverse')
                            cmds.connectAttr(str(gMap) + ".outColorR", str(gMap) + '_reverse.inputX')
                            cmds.connectAttr(str(gMap) + '_reverse.outputX', str(gMap) + "_ramp" + ".vCoord", f=True)
                    # If not, just connect it 
                    else:
                        cmds.connectAttr(str(gMap) + ".outColorR", str(gMap) + "_ramp" + ".vCoord")

                # Connect the ramp to material roughness   
                cmds.connectAttr(str(gMap) + "_ramp" + ".outColorR", MatName + str(MatRough[REngine]))
                
            else:
                if not cmds.objExists(rMap) and bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                    CreateTex('Gloss', (cMapFP + "\\" + gMap + FileType), rMap)
                if not cmds.objExists(rMap):
                    CreateImageNode(str(rMap),"Place2"+str(rMap))
                    cmds.setAttr(str(rMap) + ".fileTextureName", cMapFP + rMap + FileType, type="string")
                    cmds.setAttr(str(rMap) + ".colorSpace", "Raw", type="string")
                cmds.connectAttr(rMap + ".outColorR", MatName + MatRough[REngine])
        except:
            print("Gloss Map failed")

    elif gMap == "$gloss" or gMap == "gray" or gMap == "$color_black_40":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.77)
    elif gMap == "$white_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.001)
    elif gMap == "$black" or gMap == "$black_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 1)
    
    if os.path.exists(cMapFP + nMap + FileType) and nMap != "$identitynormalmap" and nMap != "$normal":
        try:
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
            elif REngine == 'RenderMan':
                bumpNode = mel.eval('shadingNode -asTexture PxrNormalMap')
            
            if REngine == 'Arnold' or REngine == 'Redshift' or REngine == 'RenderMan':
                cmds.rename(bumpNode, str(MatName) + "_bump")
                cmds.setAttr(str(MatName) + '_bump' + str(MatBumpY[REngine]), 1)
                cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + MatBumpIn[REngine])
                cmds.connectAttr(str(MatName) + "_bump" + str(MatBumpOut[REngine]), MatName + str(MatBump[REngine]))
            
            else:
                cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + MatBump[REngine])
            # print('Attempting to create detail map')
        except:
            print("Normal Map failed")

    if (not cmds.objExists(str(MatName) + "_bumpLayer")) and (os.path.exists((cMapFP + dnMask + FileType).replace('\\','\\\\')) or os.path.exists((cMapFP + dnMap + FileType).replace('\\','\\\\'))) and bool(cmds.checkBox('enable_detail', q=True, v=True)):
        # print('Function starting..')
        try:
            if not cmds.objExists(str(MatName) + "_bumpLayer") and REngine != 'USD':
                    if REngine == 'Redshift':
                        detailNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
                        cmds.setAttr(detailNode + ".layer1_blend_mode", 1)
                    if REngine == 'Arnold':
                        detailNode = mel.eval('shadingNode -asTexture aiLayerRgba')
                        cmds.setAttr(str(detailNode) + '.enable2', 1)
                    if REngine == 'RenderMan':
                        detailNode = mel.eval('shadingNode -asTexture PxrLayerMixer')
                    ## To do: add Repeat UVs and detail map multiplier
                    cmds.rename(detailNode, str(MatName) + "_bumpLayer")
                    # print("Layer node renamed: ", detailNode)
                    cmds.disconnectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + MatBumpIn[REngine])
                    cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
                    if REngine != 'RenderMan':
                        cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + MatBumpIn[REngine])
                    else:
                        cmds.connectAttr(str(MatName) + "_bumpLayer" + ".pxrMaterialOut_bumpNormal", str(MatName) + "_bump" + MatBumpIn[REngine])
        except:
            print("Detail Map Layer failed")      
        if os.path.exists(cMapFP + dnMap + FileType) and dnMap != "$identitynormalmap" and dnMap != "$normal" and dnMap != '':
            try:
                if not cmds.objExists(dnMap):
                    CreateImageNode(str(dnMap),"Place2"+str(dnMap))
                    cmds.setAttr(str(dnMap) + ".fileTextureName", cMapFP + dnMap + FileType, type="string")
                    cmds.setAttr(str(dnMap) + ".colorSpace", "Raw", type="string")
                    cmds.setAttr('Place2' + dnMap + '.repeatUV', 8, 8)
                    # print('Detail Map Created')

                if REngine != 'USD':
                    cmds.connectAttr(str(dnMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL2[REngine]))
                    cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE1[REngine]), 1)
            except:
                print('Detail Map "' + dnMap + '" failed')
            
        if os.path.exists(cMapFP + dnMap2 + FileType) and dnMap2 != "$identitynormalmap" and dnMap2 != "$normal" and dnMap2 != '':
            try:
                if not cmds.objExists(dnMap2):
                    CreateImageNode(str(dnMap2),"Place2"+str(dnMap2))
                    cmds.setAttr(str(dnMap2) + ".fileTextureName", cMapFP + dnMap2 + FileType, type="string")
                    cmds.setAttr(str(dnMap2) + ".colorSpace", "Raw", type="string")
                    cmds.setAttr('Place2' + dnMap2 + '.repeatUV', 8, 8)
                    # print('Detail Map Created')

                if REngine != 'USD':
                    cmds.connectAttr(str(dnMap2) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL3[REngine]))
                    cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE2[REngine]), 1)
            except:
                print('Detail Map "' + dnMap2 + '" failed')

        if os.path.exists(cMapFP + dnMap3 + FileType) and dnMap3 != "$identitynormalmap" and dnMap3 != "$normal" and dnMap3 != '':
            try:
                if not cmds.objExists(dnMap3):
                    CreateImageNode(str(dnMap3),"Place2"+str(dnMap3))
                    cmds.setAttr(str(dnMap3) + ".fileTextureName", cMapFP + dnMap3 + FileType, type="string")
                    cmds.setAttr(str(dnMap3) + ".colorSpace", "Raw", type="string")
                    cmds.setAttr('Place2' + dnMap3 + '.repeatUV', 8, 8)
                    # print('Detail Map Created')

                if REngine != 'USD':
                    cmds.connectAttr(str(dnMap3) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL4[REngine]))
                    cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE3[REngine]), 1)
            except:
                print('Detail Map "' + dnMap3 + '" failed')

        if os.path.exists(cMapFP + dnMask + FileType) and dnMask != "$mask" and dnMask != "$black_multimask":
            try:
                if not cmds.objExists(dnMask) and dnMask != '$mask':
                    CreateImageNode(str(dnMask),"Place2"+str(dnMask))
                    cmds.setAttr(str(dnMask) + ".fileTextureName", cMapFP + dnMask + FileType, type="string")
                    if REngine != 'USD':
                        cmds.shadingNode('multiplyDivide', name=str(dnMask) + '_multiplier', asShader=True)
                        cmds.connectAttr(str(dnMask) + ".outColor",str(dnMask) + '_multiplier' + '.input1')
                        cmds.setAttr(str(dnMask) + '_multiplier' + '.input2', 0.6, 0.6, 0.6)
                        cmds.connectAttr(str(dnMask) + '_multiplier' + '.output.outputX', str(MatName) + "_bumpLayer" + str(BumpMixL1[REngine]))
                        cmds.connectAttr(str(dnMask) + '_multiplier' + '.output.outputY', str(MatName) + "_bumpLayer" + str(BumpMixL2[REngine]))
                        cmds.connectAttr(str(dnMask) + '_multiplier' + '.output.outputZ', str(MatName) + "_bumpLayer" + str(BumpMixL3[REngine]))        
            except:
                print("Detail Mask failed")

        if os.path.exists(cMapFP + eMap + FileType) and cMap != "$black_color":
            try:
                if not cmds.objExists(eMap):
                    CreateImageNode(str(eMap),"Place2"+str(eMap))
                cmds.connectAttr(str(eMap) + ".outColor", MatName + MatEmmision[REngine])
                cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMap + FileType, type="string")
                cmds.setAttr(str(MatName) + ".emission_weight", 1)
            except:
                print("Emmissive Map failed")

OSLText = '''
        color Transformer(float R, float G){


        float NR = (R + G) * 0.5;
        float NG = (R - G) * 0.5;
        float NB = 1.0 - abs(NR) - abs(NG);
		float LEN = sqrt((NR*NR) + (NG*NG) + (NB*NB));

		float NX = NR / LEN;
		float NY = NG / LEN;
		float NZ = NB / LEN;

        return color(NX * 0.5 + 0.5,NY * -1 * 0.5 + 0.5,NZ * 0.5 + 0.5);
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
    isSkinMaterial = False

    colorSemantic = {
    'Infinite Warfare': 'colorMap',
    'Modern Warfare 2019': 'unk_semantic_0x0',
    'Vangaurd': 'unk_semantic_0x0',
    'Modern Warfare II': 'unk_semantic_0x0'}

    ngoSemantic = {
        'Infinite Warfare': 'normalMap',
        'Modern Warfare 2019': 'unk_semantic_0x9',
        'Vangaurd': 'unk_semantic_0x8',
        'Modern Warfare II': 'unk_semantic_0x4'}

    opacitySemantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'unk_semantic_0x1B',
        'Vangaurd': 'unk_semantic_0x18',
        'Modern Warfare II': 'unk_semantic_0xC'}

    emmisiveSemantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'TEMP',
        'Vangaurd': 'unk_semantic_0x10',
        'Modern Warfare II': 'INSERT_EMMISIVE_HERE'}

    subsurfaceSemantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'TEMP',
        'Vangaurd': 'unk_semantic_0x6F',
        'Modern Warfare II': 'unk_semantic_0x26'}

    detailMaskSemantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'TEMP',
        'Vangaurd': 'unk_semantic_0x9F',
        'Modern Warfare II': 'INSERT_MASK_HERE'}

    detail1Semantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'TEMP',
        'Vangaurd': 'unk_semantic_0x9',
        'Modern Warfare II': ''}
    detail2Semantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'TEMP',
        'Vangaurd': 'unk_semantic_0xA',
        'Modern Warfare II': ''}
    detail3Semantic = {
        'Infinite Warfare': 'TEMP',
        'Modern Warfare 2019': 'TEMP',
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
            ngoMap = sList[i][1].replace('~','').partition("&")[0] + 'go'
            ngoMapUF = sList[i][1]
            nMap = sList[i][1].replace('~','').partition("&")[0]
            gMap = sList[i][1].partition("&")[2].partition("~")[0]
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

    ## Color Map
    if os.path.exists(cMapFP + csMapUF + FileType) and csMap != "$black" and isSkinMaterial == False:
        try:
            if not cmds.objExists(csMap):
                CreateImageNode(str(csMap),"Place2"+str(csMap))
                cmds.setAttr(str(csMap) + ".fileTextureName", cMapFP + csMapUF + FileType, type="string")
            if REngine == 'Redshift':
                cmds.setAttr(MatName + MatSheen[REngine], 0.1)
            if REngine == 'Arnold':
                cmds.setAttr(MatName + MatSheen[REngine], 0.1)
            if REngine == 'RenderManDis':
                cmds.setAttr(MatName + MatSheen[REngine], 0.4)
            cmds.connectAttr(str(csMap) + ".outColor", MatName + str(MatDiffuse[REngine]))
            if has_transparency(Image.open(cMapFP + csMapUF + FileType)):
                cmds.connectAttr(str(csMap) + ".outAlpha", MatName + MatMetallic[REngine])
                if REngine == 'Redshift':
                    cmds.setAttr(MatName + '.refl_fresnel_mode', 2)
                    cmds.setAttr(MatName + '.refl_brdf', 1)
            if REngine != 'USD' and REngine != 'RenderManDis':
                cmds.setAttr(MatName + MatSpec[REngine], 0)
            # print("Color Layer connected")
        except:
            print("Color Map failed")
    elif csMap == "$black":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 0, 0, 0)

    ## Gloss Map
    if os.path.exists(cMapFP + ngoMapUF + FileType) and gMap != "$black":
        try:
            if REngine != 'USD':
                if not cmds.objExists(ngoMap):
                    CreateImageNode(str(ngoMap),"Place2"+str(ngoMap))
                    cmds.setAttr(str(ngoMap) + ".fileTextureName", cMapFP + ngoMapUF + FileType, type="string")
                    cmds.setAttr(str(ngoMap) + ".colorSpace", "Raw", type="string")
            if REngine != 'USD':
                if not cmds.objExists(str(ngoMap) + '_ramp'):
                    rampNode = mel.eval('shadingNode -asTexture ramp;')
                    cmds.rename(rampNode, str(ngoMap) + "_ramp")
                    cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[1].position", 1)
                    cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[1].color", 1, 1, 1)
                    cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[2].position", 0)
                    cmds.setAttr(str(ngoMap) + "_ramp.colorEntryList[2].color", 0, 0, 0)
                if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                    # if REngine =='Arnold' or REngine == 'RenderManDis' :
                        if not cmds.objExists(str(ngoMap) + '_reverse'):
                            reverseNode = mel.eval('shadingNode -asTexture reverse;')
                            cmds.rename(reverseNode, str(ngoMap) + '_reverse')
                            cmds.connectAttr(str(ngoMap) + ".outColorR", str(ngoMap) + '_reverse.inputX')
                            cmds.connectAttr(str(ngoMap) + '_reverse.outputX', str(ngoMap) + "_ramp" + ".vCoord")
                            print('Reverse Node created: ', reverseNode)
                        # cmds.connectAttr(str(ngoMap) + "_ramp" + ".outColorR", MatName + str(MatRough[REngine]))
                        # 
                if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                    cmds.connectAttr(str(ngoMap) + "_ramp" + ".outColorR", MatName + str(MatRough[REngine]))
                    if REngine != 'RenderManDis':
                        cmds.connectAttr(str(ngoMap) + "_ramp" + ".outColorR", MatName + str(MatSheenRough[REngine]))
                else:
                    cmds.connectAttr(str(ngoMap) + ".outColorR", MatName + MatRough[REngine])
            else:
                if not cmds.objExists(gMap):
                    CreateTex('Gloss', (cMapFP + "\\" + ngoMapUF + FileType), gMap)
                    CreateImageNode(str(gMap),"Place2"+str(gMap))
                    cmds.setAttr(str(gMap) + ".fileTextureName", cMapFP + gMap + FileType, type="string")
                    cmds.setAttr(str(gMap) + ".colorSpace", "Raw", type="string")
                cmds.connectAttr(gMap + ".outColorR", MatName + MatRough[REngine])
        except:
            print("Gloss Map failed")

    ## Normal Map
    if os.path.exists(cMapFP + ngoMapUF + FileType) and ngoMap != "$normal":
        try:
            if REngine == 'USD' or REngine == 'Arnold':
                if not os.path.exists(cMapFP + nMap + FileType):
                    CreateTex('Normal', (cMapFP + "\\" + ngoMapUF + FileType), nMap)
            if REngine != 'USD':
                if not cmds.objExists(str(ngoMap) + '_bump'):
                    if REngine == 'Redshift':
                        bumpNode = mel.eval('shadingNode -asTexture RedshiftBumpMap;')
                        cmds.setAttr(bumpNode + ".inputType", 1)
                        cmds.setAttr(bumpNode + ".scale", 1)
                    if REngine == 'Arnold':
                        bumpNode = mel.eval('shadingNode -asTexture aiNormalMap;')
                    if REngine == 'RenderManDis':
                        bumpNode = mel.eval('shadingNode -asTexture PxrNormalMap;')
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
            if REngine == 'Arnold' or REngine == 'USD' or REngine == 'RenderManDis':
                if not cmds.objExists(nMap):
                    CreateImageNode(str(nMap),"Place2"+str(nMap))
                    cmds.setAttr(str(nMap) + ".fileTextureName", cMapFP + nMap + FileType, type="string")
                    cmds.setAttr(str(nMap) + ".colorSpace", "Raw", type="string")
                if REngine == 'Arnold':
                    cmds.connectAttr(str(nMap) + '.outColor', str(MatName) + "_bump" + '.input')
                if REngine == 'RenderManDis':
                    cmds.connectAttr(str(nMap) + '.outColor', str(MatName) + "_bump" + MatBumpIn[REngine])
            if REngine != 'USD':
                cmds.connectAttr(str(MatName) + "_bump" + str(MatBumpOut[REngine]), MatName + str(MatBump[REngine]))
            else:
                cmds.connectAttr(str(nMap) + ".outColor", MatName + str(MatBump[REngine]))
        except:
            print("Normal Map failed")
        
        if os.path.exists(cMapFP + dnMap1UF + FileType) and dnMap1 != "$black" and REngine != 'USD' and bool(cmds.checkBox('enable_detail', q=True, v=True)):
            try:
                if REngine == 'Redshift':
                    if not cmds.objExists(dnMap1):
                        CreateImageNode(str(dnMap1),"Place2"+str(dnMap1))
                        cmds.setAttr(str(dnMap1) + ".fileTextureName", cMapFP + dnMap1UF + FileType, type="string")
                        cmds.setAttr(str(dnMap1) + ".colorSpace", "Raw", type="string")
                        oslNode = mel.eval('shadingNode -asShader RedshiftOSLShader;')   
                        cmds.rename(oslNode, str(dnMap1) + "_OSLConverter")
                        cmds.setAttr(str(dnMap1) + "_OSLConverter" + ".sourceText", OSLText, type="string")
                        cmds.connectAttr(str(dnMap1) + ".outColorG", str(dnMap1) + "_OSLConverter" + ".inColorR")
                        cmds.connectAttr(str(dnMap1) + ".outAlpha", str(dnMap1) + "_OSLConverter" + ".inColorG")
                    cmds.disconnectAttr(str(ngoMap) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bump" + ".input")
                    detailLayerNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
                    cmds.rename(detailLayerNode, str(MatName) + "_bumpLayer")
                    cmds.connectAttr(str(ngoMap) + "_OSLConverterCC" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
                    cmds.connectAttr(str(dnMap1) + "_OSLConverter" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL2[REngine]))
                    cmds.connectAttr(str(MatName) + "_bumpLayer" + ".outColor", str(MatName) + "_bump" + ".input")
                    cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer1_blend_mode", 1)
                if os.path.exists(cMapFP + dnMap2UF + FileType) and dnMap2 != "$black" and REngine != 'USD':
                    if REngine == 'Redshift':
                        if not cmds.objExists(dnMap2):
                            CreateImageNode(str(dnMap2),"Place2"+str(dnMap2))
                            cmds.setAttr(str(dnMap2) + ".fileTextureName", cMapFP + dnMap2UF + FileType, type="string")
                            cmds.setAttr(str(dnMap2) + ".colorSpace", "Raw", type="string")
                            detail2Node = mel.eval('shadingNode -asShader RedshiftOSLShader;')   
                            cmds.rename(detail2Node, str(dnMap2) + "_OSLConverter")
                            cmds.setAttr(str(dnMap2) + "_OSLConverter" + ".sourceText", OSLText, type="string")
                            cmds.connectAttr(str(dnMap2) + ".outColorG", str(dnMap2) + "_OSLConverter" + ".inColorR")
                            cmds.connectAttr(str(dnMap2) + ".outAlpha", str(dnMap2) + "_OSLConverter" + ".inColorG")
                        cmds.connectAttr(str(dnMap2) + "_OSLConverter" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL3[REngine]))
                        cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE2[REngine]), 1)
                        cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer2_blend_mode", 1)
                if os.path.exists(cMapFP + dnMap3UF + FileType) and dnMap3 != "$black" and REngine != 'USD':
                    if REngine == 'Redshift':
                        if not cmds.objExists(dnMap3):
                            CreateImageNode(str(dnMap3),"Place2"+str(dnMap3))
                            cmds.setAttr(str(dnMap3) + ".fileTextureName", cMapFP + dnMap3UF + FileType, type="string")
                            cmds.setAttr(str(dnMap3) + ".colorSpace", "Raw", type="string")
                            detail3Node = mel.eval('shadingNode -asShader RedshiftOSLShader;')   
                            cmds.rename(detail3Node, str(dnMap3) + "_OSLConverter")
                            cmds.setAttr(str(dnMap3) + "_OSLConverter" + ".sourceText", OSLText, type="string")
                            cmds.connectAttr(str(dnMap3) + ".outColorG", str(dnMap3) + "_OSLConverter" + ".inColorR")
                            cmds.connectAttr(str(dnMap3) + ".outAlpha", str(dnMap3) + "_OSLConverter" + ".inColorG")
                        cmds.connectAttr(str(dnMap3) + "_OSLConverter" + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL4[REngine]))
                        cmds.setAttr(str(MatName) + "_bumpLayer" + str(BumpE3[REngine]), 1)
                        cmds.setAttr(str(MatName) + "_bumpLayer" + ".layer3_blend_mode", 1)
                if os.path.exists(cMapFP + dnMaskUF + FileType) and dnMask != "$black" and REngine != 'USD':
                    CreateImageNode(str(dnMask),"Place2"+str(dnMask))
                    cmds.setAttr(str(dnMask) + ".fileTextureName", cMapFP + dnMaskUF + FileType, type="string")
                    if dnMap1 != "$black":
                        cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL1[REngine]))
                    if dnMap2 != "$black":
                        cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL2[REngine]))
                    if dnMap3 != "$black":
                        cmds.connectAttr(str(dnMask) + ".outColorR", str(MatName) + "_bumpLayer" + str(BumpMixL3[REngine]))
            except:
                print("Detail Map failed")

        ## Emmisive Map
        if os.path.exists(cMapFP + eMapUF + FileType) and eMap != "$black":
            try:
                if not cmds.objExists(eMap):
                    CreateImageNode(str(eMap),"Place2"+str(eMap))
                    cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMapUF + FileType, type="string")
                cmds.connectAttr(str(eMap) + ".outColor", MatName + str(MatEmmision[REngine]))
                if REngine != 'USD' and REngine != 'RenderManDis':
                    cmds.setAttr(str(MatName) + MatEmmisionStrength[REngine], 1)
            except:
                print("Emmissive map failed")

        # ## Opacity Map
        print(oMap)
        if os.path.exists(cMapFP + oMapUF + FileType) and oMap != "$black" and oMap != 'ximage_3c29eeff15212c37' and isSkinMaterial == False:
            try:
                if REngine == 'Redshift' or REngine == 'USD':
                    if not cmds.objExists(oMap):
                        CreateImageNode(str(oMap),"Place2"+str(oMap))
                        cmds.setAttr(str(oMap) + ".fileTextureName", cMapFP + oMapUF + FileType, type="string")
                    if REngine != 'USD':
                        cmds.connectAttr(str(oMap) + ".outColor", str(MatName) + str(MatOpacity[REngine]))
                    else:
                        cmds.connectAttr(str(oMap) + ".outColorR", str(MatName) + str(MatOpacity[REngine]))
            except:
                print("Opacity map fialed")
                
    else:
        NoNormals.append(MatName)

def SetupMaterialH1():
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
                CreateImageNode(str(Filter(cMap)),"Place2"+str(Filter(cMap)))
                cmds.setAttr(str(cMap) + ".fileTextureName", cMapFP + cMap + FileType, type="string")
            cmds.connectAttr(str(cMap) + ".outColor", MatName + str(MatDiffuse[REngine]), force=True)
            if has_transparency(Image.open(cMapFP + cMap + FileType)):
                if cmds.checkBox("enable_alpha", q=True, v=True) == True:
                    if REngine != 'USD' and REngine != 'RenderMan':
                        cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'R'), force=True)
                        cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'G'), force=True)
                        cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine] + 'B'), force=True)
                    else:
                        cmds.connectAttr(str(cMap) + ".outAlpha", MatName + str(MatOpacity[REngine]))
        except:
            print("Color Map failed")
    elif cMap == "$white_diffuse":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 1, 1, 1)
    elif cMap == "$black_diffuse" or cMap == "$black" or cMap == "$black_color":
        cmds.setAttr(str(MatName) + str(MatDiffuse[REngine]), 0, 0, 0)
    
    # Specular Map
    if os.path.exists(cMapFP + sMap + FileType) and not sMap.__contains__("$white"):
        try:
            if not cmds.objExists(Filter(sMap)):
                CreateImageNode(str(Filter(sMap)),"Place2"+str(Filter(sMap)))
                cmds.setAttr(str(Filter(sMap)) + ".fileTextureName", cMapFP + sMap + FileType, type="string")
            cmds.connectAttr(str(Filter(sMap)) + ".outColor", MatName + str(MatSpecColor[REngine]))
            if REngine == 'Redshift':
                cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1) # 1 - Colour Edge & Tint
                cmds.setAttr(str(MatName) + ".refl_edge_tintR", 1, clamp=True)
                cmds.setAttr(str(MatName) + ".refl_edge_tintG", 1, clamp=True)
                cmds.setAttr(str(MatName) + ".refl_edge_tintB", 1, clamp=True)
        except:
            print("Specular Map failed")
    elif sMap == "$specular":
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 0.23, 0.23, 0.23)
    elif sMap.find("&white") == -1:
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 1)
        cmds.setAttr(str(MatName) + str(MatSpecColor[REngine]), 0.23, 0.23, 0.23)
    elif not os.path.exists(cMapFP + sMap + FileType):
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".refl_fresnel_mode", 3) # 3 - IOR

    # Occlusion Map
    if os.path.exists(cMapFP + aoMap + FileType) and aoMap != "$white_ao" and aoMap != "$occlusion_black" and aoMap != "$occlusion_50" and aoMap != "$occlusion":
        if REngine == 'Redshift' or REngine == 'USD':
            try:
                if not cmds.objExists(Filter(aoMap)):
                    CreateImageNode(str(Filter(aoMap)),"Place2"+str(Filter(aoMap)))
                    cmds.setAttr(str(Filter(aoMap)) + ".fileTextureName", cMapFP + aoMap + FileType, type="string")
                if REngine != 'USD':
                    cmds.connectAttr(str(Filter(aoMap)) + ".outColor", MatName + ".overall_color", force=True)
                else:
                    cmds.connectAttr(str(Filter(aoMap)) + ".outColorR", MatName + ".occlusion", force=True)
            except:
                print("Occlusion Map failed")
    elif aoMap == "$black" or aoMap == "$occlusion_black":
        if REngine == 'Redshift':
            cmds.setAttr(str(MatName) + ".overall_color", 0, 0, 0)

    # Gloss Map
    if os.path.exists(cMapFP + gMap + FileType) and gMap != "$gloss" and gMap != "$white_gloss" and gMap != "$black" and gMap != "$black_gloss":
        try:
            if has_transparency(Image.open(cMapFP + gMap + FileType)):
            
                if REngine == 'USD':
                    try:
                        CreateTex('Gloss', (cMapFP + "\\" + gMap + FileType), Filter(gMap))
                    except:
                        print("Error creating texture")
                
                if not cmds.objExists(Filter(gMap)):
                    CreateImageNode(str(Filter(gMap)),"Place2"+str(Filter(gMap)))
                    cmds.setAttr(str(Filter(gMap)) + ".fileTextureName", cMapFP + gMap + FileType, type="string")
                    cmds.setAttr(str(Filter(gMap)) + ".colorSpace", "Raw", type="string")
                if REngine != 'USD':
                    if REngine == 'Arnold' or REngine == 'RenderMan':
                        if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                            reverseNode = mel.eval('shadingNode -asTexture reverse;')
                            cmds.rename(reverseNode, str(Filter(gMap)) + '_reverse')
                            cmds.connectAttr(str(Filter(gMap)) + ".outAlpha", str(Filter(gMap)) + '_reverse.inputX')

                    if not cmds.objExists(Filter(gMap) + "_Ramp"):
                        rampNode = mel.eval('shadingNode -asTexture ramp;')
                        cmds.rename(rampNode, str(Filter(gMap)) + "_Ramp")
                        rampNode = str(Filter(gMap)) + "_Ramp"
                        cmds.setAttr(rampNode + ".colorEntryList[1].position", 1)
                        cmds.setAttr(rampNode + ".colorEntryList[1].color", 1, 1, 1)
                        cmds.setAttr(rampNode + ".colorEntryList[2].position", 0)
                        cmds.setAttr(rampNode + ".colorEntryList[2].color", 0, 0, 0)
                if REngine == 'Redshift':
                    cmds.connectAttr(str(Filter(gMap)) + ".outAlpha", str(Filter(gMap)) + "_Ramp" + ".vCoord")
                    
                if not cmds.objExists(Filter(gMap) + '_reverse'):
                    print("Reverse not desn't exist yet")
                    if REngine =='Arnold' or REngine == 'RenderMan':
                        if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                            reverseNode = mel.eval('shadingNode -asTexture reverse;')
                            cmds.rename(reverseNode, str(Filter(gMap)) + '_reverse')
                            cmds.connectAttr(str(Filter(gMap)) + ".outAlpha", str(Filter(gMap)) + '_reverse.inputX')

                if bool(cmds.checkBox("gloss_or_rough", q=True, v=True)) == True:
                    if REngine =='Arnold' or REngine == 'RenderMan':
                        cmds.connectAttr(str(Filter(gMap)) + '_reverse.outputX', str(Filter(gMap)) + "_Ramp" + ".vCoord")
                if REngine != 'USD':
                    cmds.connectAttr(str(Filter(gMap)) + "_Ramp" + ".outColorR", MatName + str(MatRough[REngine]))
                else:
                    cmds.connectAttr(str(Filter(gMap)) + ".outAlpha", MatName + str(MatRough[REngine]))
        except:
            print("Gloss Map failed")
            
    elif gMap == "$gloss":
        if REngine != 'USD':
            cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.23)
        else:
            cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.77)
    elif os.path.exists(cMapFP + gMap + FileType):
        if not has_transparency(Image.open(cMapFP + gMap + FileType)):
            if REngine != 'USD':
                cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.23)
            else:
                cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0.77)
    elif gMap == "$white_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 1)
    elif gMap == "$black" or gMap == "$black_gloss":
        cmds.setAttr(str(MatName) + str(MatRough[REngine]), 0)

    # Normal Map
    if os.path.exists(cMapFP + nMap + FileType) and nMap != "$identitynormalmap" and nMap != "$normal":
        try:
            if not cmds.objExists(nMap):
                CreateImageNode(str(nMap),"Place2"+str(nMap))
                cmds.setAttr(str(nMap) + ".fileTextureName", cMapFP + nMap + FileType, type="string")
                cmds.setAttr(str(nMap) + ".colorSpace", "Raw", type="string")
            if REngine == 'Redshift':
                normalNode = mel.eval('shadingNode -asTexture RedshiftBumpMap;')
                cmds.setAttr(str(MatName) + "_bump.inputType", 1)
                # cmds.setAttr(str(MatName) + '_bump' + str(MatBumpY[REngine]), 1)
                cmds.setAttr(str(MatName) + "_bump.scale", 1)
            if REngine == 'Arnold':
                normalNode = mel.eval('shadingNode -asTexture aiNormalMap;')
            if REngine == 'RenderMan':
                normalNode = mel.eval('shadingNode -asTexture PxrNormalMap;')
            if REngine != 'USD':
                cmds.rename(normalNode, str(MatName) + "_bump")
                cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + MatBumpIn[REngine])
                cmds.connectAttr(str(MatName) + "_bump" + str(MatBumpOut[REngine]), MatName + str(MatBump[REngine]))
            else:
                cmds.connectAttr(str(nMap) + ".outColor", MatName + str(MatBump[REngine]))
            
            if os.path.exists(cMapFP + dnMap + FileType) and dnMap != "$identitynormalmap" and dnMap != "$normal":
                if not cmds.objExists(dnMap):
                    CreateFileNode(str(dnMap))
                    cmds.setAttr(str(dnMap) + ".fileTextureName", cMapFP + dnMap + FileType, type="string")
                    cmds.setAttr(str(dnMap) + ".colorSpace", "Raw", type="string")
                    
                if REngine == 'Redshift':
                    normalLayerNode = mel.eval('shadingNode -asTexture RedshiftColorLayer;')
                    detailNode = mel.eval('shadingNode -asShader RedshiftOSLShader;')
                    cmds.setAttr(detailNode + ".sourceText", OSLText, type="string")
                    cmds.connectAttr(str(dnMap) + ".outColor", detailNode + ".inColor")
                    cmds.setAttr(normalLayerNode + ".layer1_blend_mode", 1)
                    cmds.rename(detailNode, str(dnMap) + "_OSLConverter")
                if REngine == 'Arnold':
                    normalLayerNode = mel.eval('shadingNode -asTexture aiLayerRgba;')
                if REngine != 'USD':
                    cmds.rename(normalLayerNode, str(MatName) + "_bumpLayer")
                    cmds.disconnectAttr(str(nMap) + ".outColor", str(MatName) + "_bump" + ".input")
                    cmds.connectAttr(str(nMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL1[REngine]))
                    cmds.connectAttr(str(dnMap) + ".outColor", str(MatName) + "_bumpLayer" + str(BumpL2[REngine]))
                    # cmds.connectAttr(str(dnMap) + ".outColorR", str(MatName) + "_bumpLayer" + ".layer1_colorR")
                    # cmds.connectAttr(str(dnMap) + ".outColorG", str(MatName) + "_bumpLayer" + ".layer1_colorG")
                    # cmds.connectAttr(str(dnMap) + ".outColorB", str(MatName) + "_bumpLayer" + ".layer1_colorB")
                    cmds.connectAttr(str(MatName) + "_bumpLayer" + '.outColor', str(MatName) + "_bump" + ".input")
                else:
                    cmds.connectAttr(str(dnMap) + ".outColor", str(MatName) + str(MatBump[REngine]))  
        except:
            print("Normal Map failed")

    # Emissive Map
    if os.path.exists(cMapFP + eMap + FileType) and cMap != "$black_color":
        try:
            if not cmds.objExists(eMap):
                CreateImageNode(str(eMap),"Place2"+str(eMap))
                cmds.setAttr(str(eMap) + ".fileTextureName", cMapFP + eMap + FileType, type="string")
            cmds.connectAttr(str(eMap) + ".outColor", MatName + str(MatEmmision[REngine]))
            if REngine != 'USD':
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

def checkREngine(engines:list):
    REngine = cmds.optionMenu('render', q=True, v=True)
    for engine in engines:
        if engine == REngine:
            return True
        
def setupSkin():

    # If the render engine isn't supported
    if checkREngine(['USD', 'RenderMan']):
        cmds.confirmDialog(title="Warning", message=f"{REngine} does not support setting up skin at the moment")
        return
        
    Mats = []

    # If the object is a mesh, get its material
    for object in cmds.ls(selection=True):
        if cmds.nodeType(object) in ['RedshiftMaterial', 'aiStandardSurface']:
            Mats.append(object)
        elif cmds.nodeType(object) == 'transform':
            if (mesh:=cmds.ls(object, dag=True, type="mesh")) != None:
                shadeEng = cmds.listConnections(mesh , type = "shadingEngine")[0]
                meshMat = cmds.ls(cmds.listConnections(shadeEng), materials = True)[0]
                Mats.append(meshMat)

    # Setup 
    for mat in Mats:
        if cmds.nodeType(mat) == 'RedshiftMaterial':
            # Get the color texture attached to the material
            if cmds.nodeType(cmds.listConnections(str(mat) + '.diffuse_color')[0]) == 'RedshiftColorLayer':
                colorNode = cmds.listConnections(str(cmds.listConnections(str(mat) + '.diffuse_color')[0]) + '.layer1_color')[0]
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
        
            if bumpNode != None:
                cmds.connectAttr(str(bumpNode) + '.out', str(mat) + '.bump_input')
            if glossNode != None:
                cmds.connectAttr(str(glossNode) + '.outColorR', str(mat) + '.refl_gloss0')
            else:
                cmds.setAttr('.refl_gloss0', 0.4)

            cmds.connectAttr(str(mat) + '.outColor', str(shadingNode) + '.surfaceShader', force=True)

            cmds.setAttr(str(mat) + '.refl_weight0', 0.6)

            # mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
            cmds.delete(str(mat) + '_RM')

        elif cmds.nodeType(mat) == 'aiStandardSurface':
            if cmds.nodeType(cmds.listConnections(str(mat) + '.baseColor')[0]) == 'file':
                colorNode = cmds.listConnections(str(mat) + '.baseColor')[0]

            if not cmds.objExists((str(mat) + '_ColorCorrect')):
                colorCorrectNode = cmds.shadingNode('aiColorCorrect', name=(str(mat) + '_ColorCorrect'), asShader=True)
                cmds.connectAttr(colorNode + '.outColor', colorCorrectNode + '.input')
                # Setup color correct node
                cmds.setAttr(colorCorrectNode + '.hueShift', -0.04)
                cmds.setAttr(colorCorrectNode + '.saturation', 1.3)
            else:
                colorCorrectNode = str(mat) + '_ColorCorrect'
            
            # Connect the color correct node to the material
            cmds.connectAttr(colorCorrectNode + '.outColor', str(mat) + '.subsurfaceColor', force=True)

            # Set subsurface settings
            cmds.setAttr(mat + '.subsurfaceScale', 0.07)
            cmds.setAttr(mat + '.subsurface', 0.4)
        
        else:
            cmds.confirmDialog(title="Warning", message="This material is not supported")


def SetupShadingOld(preset):
    Meshes = cmds.ls(selection=True, dag=True, s=True, ext='mesh')
    REngine = cmds.optionMenu('render', q=True, v=True)
    Mats = []
    # print(Meshes)
    for mesh in Meshes:
        SG = cmds.listConnections(mesh, type='shadingEngine')
        if SG != None and SG != 'None':
            Material = cmds.ls(cmds.listConnections(SG), materials = True)
            Mats.append(Material[0])
    print(Mats)
    # print(Mats)
    if preset == 'Plastic':
        if REngine == 'Redshift':
            for mat in Mats:
                cmds.setAttr(mat + '.refl_weight', 0.6)
                cmds.setAttr(mat + '.refl_brdf', 0)
                cmds.setAttr(mat + '.refl_fresnel_mode', 3)
                cmds.setAttr(mat + '.refl_ior', 1.46)
    if preset == "Cloth":
        if REngine == 'Redshift':
            for mat in Mats:
                cmds.setAttr(mat + '.refl_weight', 0.4)
                cmds.setAttr(mat + '.refl_brdf', 0)
                cmds.setAttr(mat + '.refl_fresnel_mode', 3)
                cmds.setAttr(mat + '.refl_ior', 1.53)
    if preset == 'Hair':
        if REngine == 'Redshift':
            for mat in Mats:
                cmds.setAttr(mat + '.refl_weight', 0.8)
                cmds.setAttr(mat + '.refl_brdf', 0)
                cmds.setAttr(mat + '.refl_fresnel_mode', 3)
                cmds.setAttr(mat + '.refl_ior', 1.55)
                cmds.setAttr(mat + '.sheen_weight', 0.4)



def SetupShading(preset):
    # If the render engine isn't supported
    REngine = cmds.optionMenu('render', q=True, v=True)

    if checkREngine(['RenderMan']):
        cmds.confirmDialog(title="Warning", message=f"{REngine} does not support setting up skin at the moment")
        return

    def checkSetAttr(nodeAttr, value):
        if cmds.listConnections(nodeAttr) == None:  
            cmds.setAttr(nodeAttr, value)
    
    def setRedshiftIOR(mat, REngine):
        if REngine == 'Redshift':
            cmds.setAttr(mat + '.refl_brdf', 0)
            cmds.setAttr(mat + '.refl_fresnel_mode', 3)

    Mats = []

    # If the object is a mesh, get its material
    for object in cmds.ls(selection=True):
        if cmds.nodeType(object) in ['RedshiftMaterial', 'aiStandardSurface']:
            Mats.append(object)
        elif cmds.nodeType(object) == 'transform':
            if (mesh:=cmds.ls(object, dag=True, type="mesh")) != None:
                shadeEng = cmds.listConnections(mesh , type = "shadingEngine")[0]
                meshMat = cmds.ls(cmds.listConnections(shadeEng), materials = True)[0]
                Mats.append(meshMat)

    for mat in Mats:
        
            if preset == 'Plastic':
                    checkSetAttr(mat + MatSpec[REngine], 0.6)
                    checkSetAttr(mat + MatIOR[REngine], 1.46)
                    checkSetAttr(mat + MatRough[REngine], 0.6)
                    setRedshiftIOR(mat, REngine)
            elif preset == 'Cloth':
                    checkSetAttr(mat + MatSpec[REngine], 0)
                    checkSetAttr(mat + MatSheen[REngine], 0.4)
                    checkSetAttr(mat + MatSheenRough[REngine], 0.8)
            elif preset == 'Hair':
                    checkSetAttr(mat + MatSpec[REngine], 0.8)
                    checkSetAttr(mat + MatIOR[REngine], 1.55)
                    checkSetAttr(mat + MatRough[REngine], 0.8)
                    setRedshiftIOR(mat, REngine)
            
            


WINDOW_TITLE = "Call of Duty Material Tool"
WINDOW_WIDTH = 400

ROW_SPACING = 2
PADDING = 5

def addColumnLayout():
    cmds.columnLayout(adjustableColumn=True, columnAttach=('both', PADDING))
    
def addFrameColumnLayout(label, collapsable, collapse=True):
    cmds.frameLayout(collapsable=collapsable, label=label, collapse=collapse)
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
    addHeader('Call of Duty Material Setup')
    addText('Material Setup Tool for Call of Duty models')
    cmds.text(label='<span style=\"color:#ccc;text-decoration:none;font-size:px;font-family:courier new;font-weight:bold;\">' + "Created by <a href=\"https://twitter.com/MrChuse\" style=\"color:purple\"> MrChuse</a>" + '</span>', hyperlink=True)
    addSpacer()
        
    addDoubleRowLayout()
    addText('Render Engine: ')
    addOptionMenu("render","", ['RenderMan', 'Arnold', 'Redshift', 'USD'])
    parentToLayout()
    addFrameColumnLayout('Material Attributes', False)

    addDoubleRowLayout()
    addText('Game: ')
    # addOptionMenu("game","", ["Infinite Warfare", "Modern Warfare Remastered", "Black Ops 4", "Modern Warfare 2019", "Black Ops Cold War", "Vangaurd", "Modern Warfare II"])
    addOptionMenu("game","", ["Infinite Warfare", "Modern Warfare Remastered", "Black Ops III / 4 / CW", "Modern Warfare 2019", "Vangaurd", "Modern Warfare II"])
    parentToLayout()
    addDoubleRowLayout()
    addText('Assets Folder: ')
    addFileBrowser("models_path", 2, 'Select the path to your assets folder', PROJECT + '/assets')
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
    parentToLayout()

    addButton( 'Start', "Main()")
    addSpacer()

    menuAdvancedTab = cmds.frameLayout(label='Advanced Material Attributes', collapsable=True, collapse=True, la='center')
    menuAdvancedGrid = cmds.rowLayout(
        numberOfColumns=2, 
        adjustableColumn2=2, 
        columnWidth2=[150, 20],
        columnAlign2=['right', 'left'], 
        columnAttach2=['right', 'left'], width=20
    )
    
    # addFrameColumnLayout('Advanced Material Attributes', True)
    parentToLayout()
    parentToLayout()

    cmds.checkBox('enable_detail', label='Connect Detail Maps', parent=menuAdvancedGrid, value=True)

    # addCheckbox("enable_detail", 'Connect Alpha Channels')
    # parentToLayout()


    addFrameColumnLayout('Other Options', True)
    parentToLayout()

    
    # addDoubleRowLayout()
    addSpacer()
    addButton( 'Setup Skin Materials', "setupSkin()")
    addButton( 'Setup Materials as Plastic', "SetupShading('Plastic')")
    addButton( 'Setup Materials as Cloth', "SetupShading('Cloth')")
    addButton( 'Setup Materials as Hair', "SetupShading('Hair')")
    parentToLayout()
    
    cmds.showWindow('windowObject')
    
    
    
deleteIfOpen()
createWindow()