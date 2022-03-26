# -*- coding: utf-8 -*-
'''
-----------------------------------------------------------------------
Material Creator
-----------------------------------------------------------------------
Authors:        Roberto Menicatti
Email:          roberto.menicatti@gmail.it
Affiliation:    BigRock Institute of Magic Technologies
Version:        1.4 - January 2022
Tested on Maya: 2019, 2020
-----------------------------------------------------------------------
'''

import platform
import maya.cmds as my
import os
import maya.mel as mel
import re
import sys
import webbrowser

if platform.python_version().startswith('2'):  
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
elif platform.python_version().startswith('3'):
    from urllib.request import urlopen
    from html.parser import HTMLParser


##### REMEMBER TO UPDATE THIS AT EACH NEW RELEASE ##############################

VERSION = "1.4"
COMPATIBLE_VERSIONS = ["2019", "2020"]
REPOSITORY_WIKI = 'https://robertom89.github.io/MaterialCreator/'

################################################################################

WINDOW = "mat_creator"
ARNOLD = "Arnold"
VRAY = "VRay"
OCTANE = "Octane"

PREFIX = "prefix"
SUFFIX = "suffix"
NONE = "none"

NAME_FIELD = 'nameField'
FOLDER_FIELD = 'folderField'
ENGINE_FIELD = 'engineSelection'
ASSIGN_FIELD = 'assignCheckbox'
PREFSUF_FIELD = "prefixSuffixField"
PREFSUF_SEL = "prefixSuffixSelection"

MAT_SUFFIX = "_MAT"


class RepositoryParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.version = 0

    def handle_data(self, data):
        if data.startswith("Version"):
            self.version = data.split(" ")[1]


class Map():

    def __init__(self):
        self.set = []
        
    def isTiled(self):
        return len(self.set) > 1

    def getUdimNumber(self):
        return len(self.set)

    def getFirstUdim(self):
        for s in self.set:
            if "1001" in s:
                return s
        
        return self.set[0]

    def getUVGridSize(self):
        u = 0
        v = 0
        for s in self.set:
            match = re.match(r'.*(\d{4}).*', s)
            if match is not None:
                udim_number = match.group(1)
                if int(udim_number[-1]) > u:
                    u = int(udim_number[-1])
                if int(udim_number[-2]) > v:
                    v = int(udim_number[-2])
        v = v + 1  

        return [u, v]
    
    def exists(self):
        return not len(self.set) == 0


class MapColor(Map):

    field = "color"
    tags = ['color', 'diffuse', 'albedo', 'col']
    label = "Base Color"

    def __init__(self):
        Map.__init__(self)

class MapNormal(Map):

    field = "normal"
    tags = ['normal', 'norm', 'nrm']
    label = "Normal"

    def __init__(self):
        Map.__init__(self)

class MapBump(Map):

    field = "bump"
    tags = ['bump']
    label = "Bump"

    def __init__(self):
        Map.__init__(self)

class MapRoughness(Map):

    field = "roughness"
    tags = ['roughness', 'rough']
    label = "Roughness"

    def __init__(self):
        Map.__init__(self)

class MapGlossiness(Map):

    field = "glossiness"
    tags = ['glossiness', 'gloss']
    label = "Glossiness"

    def __init__(self):
        Map.__init__(self)

class MapMetalness(Map):

    field = "metal"
    tags = ['metallic', 'metalness', 'metal']
    label = "Metallic"

    def __init__(self):
        Map.__init__(self)

class MapDisplacement(Map):

    field = "displacement"
    tags = ['height', 'displacement', 'disp']
    label = "Displacement"
    
    def __init__(self):
        Map.__init__(self)

class MapAO(Map):

    field = "ao"
    tags = ['occlusion', 'ao']
    label = "AO"

    def __init__(self):
        Map.__init__(self)

class MapSpecular(Map):

    field = "specular"
    tags = ['specular', 'reflection', 'refl']
    label = "Specular"

    def __init__(self):
        Map.__init__(self)     

class MapOpacity(Map):

    field = "opacity"
    tags = ['opacity']
    label = "Opacity"

    def __init__(self):
        Map.__init__(self)

class MapEmissive(Map):

    field = "emissive"
    tags = ['emissive', 'glow', 'illumination']
    label = "Emissive"

    def __init__(self):
        Map.__init__(self)
        

class MapSET():

    def __init__(self):
        self.all = [MapColor, MapNormal, MapBump, MapRoughness, MapGlossiness, MapMetalness, MapDisplacement, MapAO, MapOpacity, MapEmissive, MapSpecular]
        self.fields = [s.field for s in self.all]
        self.tags = [s.tags for s in self.all]
        self.labels = [s.label for s in self.all]


class TextureSet():

    def __init__(self, gui):
        
        self.color = MapColor()
        self.normal = MapNormal()
        self.bump = MapBump()
        self.roughness = MapRoughness()
        self.glossiness = MapGlossiness()
        self.metalness = MapMetalness()
        self.displacement = MapDisplacement()
        self.ao = MapAO()
        self.specular = MapSpecular()
        self.opacity = MapOpacity()
        self.emissive = MapEmissive()

        self.gui = gui
        
        self.classes = [MapColor, MapNormal, MapBump, MapRoughness, MapGlossiness, MapMetalness, MapDisplacement, MapAO, MapOpacity, MapEmissive, MapSpecular]
        self.set = [self.color, self.normal, self.bump, self.roughness, self.glossiness, self.metalness, self.displacement, self.ao, self.opacity, self.emissive, self.specular]


    def loadTextures(self, path):

        self.path = path

        self.reset()
        
        for f in os.listdir(self.path):

            if not f.startswith("."):
                full_path = os.path.join(self.path, f)

                if os.path.isfile(full_path) and not full_path.split(".")[-1] == "tx":
                    if any(tag in f.lower() for tag in MapColor.tags):
                        self.color.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapNormal.tags):
                        self.normal.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapBump.tags):
                        self.bump.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapRoughness.tags):
                        self.roughness.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapGlossiness.tags):
                        self.glossiness.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapDisplacement.tags):
                        self.displacement.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapAO.tags):
                        self.ao.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapSpecular.tags):
                        self.specular.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapOpacity.tags):
                        self.opacity.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapEmissive.tags):
                        self.emissive.set.append(full_path)
                    elif any(tag in f.lower() for tag in MapMetalness.tags):
                        self.metalness.set.append(full_path)

        self.printSet()

    def reset(self):
        for s in self.set:
            s.set = []
        
        self.gui.resetGUI(name=False, path=False)
            # if my.textField(s.field, exists=1):
            #     my.textField(s.field, edit=True, text="")
            # if my.checkBox(s.field + "_checkbox", exists=1):
            #     my.checkBox(s.field + "_checkbox", edit=True, value=0)
        

    def printSet(self):
        
        for s in self.set:
            print(s.set)
            # print(s.getUVGridSize())


    def getMapInstanceFromString(self, string):

        for index, c in enumerate(self.classes):
            if string == c.field:
                return self.set[index]


class MatCreatorWindow():

    def __init__(self):
        self.map_set = MapSET()
        self.texture_set = TextureSet(self)
        self.makeWindow()

    def makeWindow(self):
        w = 510
        h = 140
        button_w = 168

        if my.window(WINDOW, query=True, exists=True):
            self.closeWindow()
        window = my.window(WINDOW, title="Material Creator %s" % VERSION, width=w)
        
        menuLayout = my.menuBarLayout(width=w)
        my.menu(label="Help", helpMenu=True)
        my.menuItem(label="About", command=about)
        my.menuItem(label="Changelog", command=changelog)
        my.menuItem(label="Help", command=helpmenu)
        my.menuItem(label="Online Guide", command=onlineGuide)

        mainColLayout = my.columnLayout(width=w)

        SeparatorGUI(parent=mainColLayout, width=w)

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=2, 
                        cal=[(1,'left'), (2, 'left')],
                        columnWidth=[(1, 384), (2, 100)], 
                        columnSpacing=[(1, 10), (2, 6)],
                        rowOffset=[(1, 'top', 10), (1, 'bottom', 5), (2, 'bottom', 10)])

        my.text(label="Assign name to new material")
        my.text(label="")
        my.textField(NAME_FIELD, placeholderText="Enter material name")
        my.text(label="")

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=2, 
                        cal=[(1,'left'), (2, 'left')],
                        columnWidth=[(1, 384), (2, 100)], 
                        columnSpacing=[(1, 10), (2, 6)],
                        rowOffset=[(1, 'bottom', 5), (2, 'bottom', 10)])

        my.text(label="Add prefix or suffix (underscore is added automatically)")
        my.text(label="")
        my.textField(PREFSUF_FIELD, text="MAT")
        my.text(label="")

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=4,
                        cal=[(1,'left'), (2, 'left'), (3, 'left'), (4, 'left')], 
                        columnSpacing=[(1, 10)],
                        columnWidth=[(1, 140), (2, 140), (3, 140), (4, 90)],
                        rowOffset=[(1, 'bottom', 10)])
        my.radioCollection(PREFSUF_SEL)
        my.radioButton(PREFIX, label='Add Prefix')
        my.radioButton(SUFFIX, label='Add Suffix', select=True)
        my.radioButton(NONE, label='None')
        my.text(label="")

        SeparatorGUI(parent=mainColLayout, width=w)

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=2, 
                        cal=[(1,'left'), (2, 'left')],
                        columnWidth=[(1, 384), (2, 100)], 
                        columnSpacing=[(1, 10), (2, 6)],
                        rowOffset=[(1, 'bottom', 5), (2, 'bottom', 10)])

        my.text(label="Select textures folder")
        my.text(label="")
        my.textField(FOLDER_FIELD)
        my.iconTextButton(style='iconOnly', image='fileOpen.png', command=self.selectFolder)
        # my.button(label="Browse", w=100, command=self.selectFolder) 

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=4, 
                        cal=[(1,'left'), (2, 'left'), (3, 'left'), (4, 'left')], 
                        columnSpacing=[(1, 10), (4, 6)],
                        columnWidth=[(1, 20), (2, 84), (3, 280), (4, 100)])

        self.map_rows = []
        for s in self.map_set.all[:-1]:
            msg = MapSelectorGUI(label=s.label, field=s.field, texture_set=self.texture_set)
            self.map_rows.append(msg)

        SeparatorGUI(parent=mainColLayout, width=w)

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=2, 
                        cal=[(1,'left'), (2, 'left')],
                        columnWidth=[(1, 394), (2, 100)], 
                        columnSpacing=[(1, 10), (2, 6)],
                        rowOffset=[(1, 'top', 40), (1, 'bottom', 5)])
        my.text(label="Select render engine")
        my.text(label="")
        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=4,
                        cal=[(1,'left'), (2, 'left'), (3, 'left'), (4, 'left')], 
                        columnSpacing=[(1, 10)],
                        columnWidth=[(1, 140), (2, 140), (3, 140), (4, 90)],
                        rowOffset=[(1, 'bottom', 10)])
        my.radioCollection(ENGINE_FIELD)
        my.radioButton(ARNOLD, label='Arnold', select=True)
        my.radioButton(VRAY, label='VRay')
        my.radioButton(OCTANE, label='Octane')
        my.text(label="")

        SeparatorGUI(parent=mainColLayout, width=w)
        
        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=2, 
                        cal=[(1,'left'), (2, 'left')],
                        columnWidth=[(1, 394), (2, 100)], 
                        columnSpacing=[(1, 10), (2, 6)],
                        rowOffset=[(1, 'top', 10), (1, 'bottom', 10), (2, 'bottom', 5)])
        my.text(label="Assign new material to selected elements")
        my.text(label="")
        my.checkBox(ASSIGN_FIELD, label="")
        my.text(label="")

        SeparatorGUI(parent=mainColLayout, width=w)

        my.rowColumnLayout(parent=mainColLayout, numberOfColumns=3, 
                        rowOffset=[(1, 'bottom', 5), (1, 'top', 5)], 
                        columnSpacing=[(2, 3), (3, 3)])
        my.button(label="Create and Close", w=button_w, command=self.createCommand) 
        my.button(label="Create", w=button_w, command=self.applyCommand) 
        my.button(label="Close", w=button_w, command=self.closeWindow) 

        my.setParent( '..' )
        my.showWindow( window )

    def createCommand(self, *args):
        self.applyCommand()
        self.closeWindow()

    def applyCommand(self, *args):
        my.refreshEditorTemplates()
        if validateName() and validateFolder():
            createMaterial(self.texture_set)
            self.texture_set.reset()
            self.resetGUI()

    def closeWindow(self, *args):
        my.deleteUI(WINDOW)

    def selectFolder(self, *args):
        path = my.fileDialog2(fileMode=2)[0]
        my.textField(FOLDER_FIELD, edit=True, text=path)

        if validateFolder():
            
            self.texture_set.loadTextures(path)

            for ts in self.texture_set.set:
                if ts.exists():
                    text = ts.getFirstUdim()
                    ## Display file name only, not full path
                    text = os.path.split(text)[1]
                    if ts.isTiled():
                        text = text + " (%s UDIM)" % ts.getUdimNumber()
                    my.textField(ts.field, edit=True, text=text)
                    my.checkBox(ts.field + "_checkbox", edit=True, value=1)

    def resetGUI(self, name=True, path=True):
        if name:
            my.textField(NAME_FIELD, edit=True, text="")
        if path:
            my.textField(FOLDER_FIELD, edit=True, text="")

        for s in self.texture_set.set:
            if my.textField(s.field, exists=1):
                my.textField(s.field, edit=True, text="")
            if my.checkBox(s.field + "_checkbox", exists=1):
                my.checkBox(s.field + "_checkbox", edit=True, value=0)


class MapSelectorGUI():

    def __init__(self, label, field, texture_set):
        self.label = label
        self.field = field
        self.texture_set = texture_set
        self.check_label = self.field + "_checkbox"
        self.button = self.field + "_button"

        my.checkBox(self.check_label, label="")
        my.text(label=self.label)
        my.textField(self.field)  
        my.button(self.button, label="Change", w=100, command=self.selectFile)

    def selectFile(self, *args):
        path = my.fileDialog2(fileMode=1)[0]
        head_tail = os.path.split(path)

        dir = head_tail[0]
        file_name = head_tail[1]

        ts = self.texture_set.getMapInstanceFromString(self.field)

        ts.set = []

        if "1001" in file_name:
            string_parts = file_name.split("1001")

            for f in os.listdir(dir):

                if string_parts[0] in f and string_parts[1] in f:
                    ts.set.append(os.path.join(dir, f))
        else:
            ts.set.append(path)

        text = ts.getFirstUdim()
        text = os.path.split(text)[1]
        if ts.isTiled():
            text = text + " (%s UDIM)" % ts.getUdimNumber()

        my.textField(self.field, edit=True, text=text)
        my.checkBox(self.field + "_checkbox", edit=True, value=1)

        self.texture_set.printSet()
        

    def enable(self):
        my.checkBox(self.check_label, edit=True, enable=True)
        my.textField(self.field, edit=True, editable=True)
        my.button(self.button, edit=True, enable=True)

    def tick(self):
        my.checkBox(self.check_label, edit=True, value=1)


class SeparatorGUI():

    def __init__(self, parent, width):
        
        self.parent = parent
        self.width = width

        self.form = my.formLayout(parent=self.parent, width=self.width)
        self.separator = my.separator(style="in", height=3)

        my.formLayout(self.form, edit=True, attachForm=[(self.separator, 'top', 5), 
                                                            (self.separator, 'left', 0), 
                                                            (self.separator, 'right', 0),
                                                            (self.separator, 'bottom', 5)])
#######################

def composeFullName():
    name = my.textField(NAME_FIELD, query=True, text=True)
    prefsuf_choice = my.radioCollection(PREFSUF_SEL, query=True, select=True)
    prefsuf = my.textField(PREFSUF_FIELD, query=True, text=True)

    if prefsuf_choice == NONE:
        full_name = name
    elif prefsuf_choice == PREFIX:
        full_name = prefsuf + "_" + name
    elif prefsuf_choice == SUFFIX:
        full_name = name + "_" + prefsuf

    return full_name


def validateName():
    name = my.textField(NAME_FIELD, query=True, text=True)
    
    full_name = composeFullName()

    my.textField(NAME_FIELD, edit=True, text=name.replace(" ", "_"))
    name = name.replace(" ", "_")
    if name == "":
        my.warning("Please enter a name for the new material.")
        return False
    elif my.objExists(full_name):
        my.warning("A node named '%s' exists already. Please enter a different name for the material." % full_name)
        return False
    elif not mel.eval('isValidObjectName "%s";' % name):
        my.warning("Material name contains invalid characters. Please enter a different name for the material.")
        return False
    return True
    
def validateFolder():
    directory = my.textField(FOLDER_FIELD, query=True, text=True)
    if directory == "":
        my.warning("Cannot find the selected texture directory. Please select a valid path.")
        return False
    if not os.path.exists(directory):
        my.warning("Cannot find the selected texture directory. Please select a valid path.")
        return False

    return True


def createMaterial(texture_set):

    sel = my.ls(selection=True)

    print(sel)
    
    mat_name = my.textField(NAME_FIELD, query=True, text=True)
    directory = my.textField(FOLDER_FIELD, query=True, text=True)
    engine = my.radioCollection(ENGINE_FIELD, query=True, select=True)
    assign = my.checkBox(ASSIGN_FIELD, query=True, value=True)

    if engine == ARNOLD:
        mat = ArnoldMat(name=mat_name, directory=directory, textureset=texture_set)
    elif engine == VRAY:
        mat = VrayMat(name=mat_name, directory=directory, textureset=texture_set)
    elif engine == OCTANE:
        mat = OctaneMat(name=mat_name, directory=directory, textureset=texture_set)
    else:
        return
    
    if assign:
        my.select(sel)
        my.hyperShade(assign=mat.full_name)

##############################################################

class Mat():

    def __init__(self, name, directory, textureset):
        
        self.name = name
        #if not self.name.endswith(MAT_SUFFIX):
        #    self.name = self.name + MAT_SUFFIX

        self.full_name = composeFullName()

        self.directory = directory
        self.engine = None
        self.texture_set = textureset

        self.base_color_file = self.name + "_baseColorFile"
        self.normal_file = self.name + "_normalFile"
        self.bump_file = self.name + "_bumpFile"
        self.roughness_file = self.name + "_roughnessFile"
        self.glossiness_file = self.name + "_glossinessFile"
        self.metalness_file = self.name + "_metalnessFile"
        self.displacement_file = self.name + "_displacementFile"
        self.ao_file = self.name + "_aoFile"
        self.specular_file = self.name + "_specularFile"
        self.opacity_file = self.name + "_opacityFile"
        self.emissive_file = self.name + "_emissiveFile"

    def logCreation(self):
        line = "New %s material %s created." % (self.engine, self.name)
        command = 'print "%s"' % line
        mel.eval(command)

    def isMapSelected(self, map):
        if my.checkBox(map.field + "_checkbox", exists=1):
            return my.checkBox(map.field + "_checkbox", query=True, value=True)
        else:
            return False

    def createSelected(self):
        if self.isMapSelected(self.texture_set.color):
            self.createColor()
        if self.isMapSelected(self.texture_set.normal):
            self.createNormal()
        if self.isMapSelected(self.texture_set.bump):
            self.createBump()
        if self.isMapSelected(self.texture_set.roughness):
            self.createRoughness()
        if self.isMapSelected(self.texture_set.glossiness):
            self.createGlossiness()
        if self.isMapSelected(self.texture_set.metalness):
            self.createMetalness()
        if self.isMapSelected(self.texture_set.displacement):
            self.createDisplacement()
        if self.isMapSelected(self.texture_set.ao):
            self.createAO()
        if self.isMapSelected(self.texture_set.specular):
            self.createSpecular()
        if self.isMapSelected(self.texture_set.opacity):
            self.createOpacity()
        if self.isMapSelected(self.texture_set.emissive):
            self.createEmissive()

    def connect2DTextureNode(self, texture_node, file_node):

        my.connectAttr(texture_node + ".coverage", file_node + ".coverage", force=True)
        my.connectAttr(texture_node + ".translateFrame", file_node + ".translateFrame", force=True)
        my.connectAttr(texture_node + ".rotateFrame", file_node + ".rotateFrame", force=True)
        my.connectAttr(texture_node + ".mirrorU", file_node + ".mirrorU", force=True)
        my.connectAttr(texture_node + ".mirrorV", file_node + ".mirrorV", force=True)
        my.connectAttr(texture_node + ".stagger", file_node + ".stagger", force=True)
        my.connectAttr(texture_node + ".wrapU", file_node + ".wrapU", force=True)
        my.connectAttr(texture_node + ".wrapV", file_node + ".wrapV", force=True)
        my.connectAttr(texture_node + ".repeatUV", file_node + ".repeatUV", force=True)
        my.connectAttr(texture_node + ".offset", file_node + ".offset", force=True)
        my.connectAttr(texture_node + ".rotateUV", file_node + ".rotateUV", force=True)
        my.connectAttr(texture_node + ".noiseUV", file_node + ".noiseUV", force=True)
        my.connectAttr(texture_node + ".vertexUvOne", file_node + ".vertexUvOne", force=True)
        my.connectAttr(texture_node + ".vertexUvTwo", file_node + ".vertexUvTwo", force=True)
        my.connectAttr(texture_node + ".vertexUvThree", file_node + ".vertexUvThree", force=True)
        my.connectAttr(texture_node + ".vertexCameraOne", file_node + ".vertexCameraOne", force=True)
        my.connectAttr(texture_node + ".outUV", file_node + ".uv")
        my.connectAttr(texture_node + ".outUvFilterSize", file_node + ".uvFilterSize")

    def addFileNode(self, engine, tmap, node_name):

        if engine == OCTANE:
            if not tmap.isTiled():
                file_path = tmap.getFirstUdim()
                file_node = my.shadingNode('octaneImageTexture', name=node_name, asTexture=True)
                my.setAttr(file_node + '.File', file_path, type='string')
            else: 
                file_node = my.shadingNode('octaneImageTilesTexture', name=node_name, asTexture=True)

                grid_size = tmap.getUVGridSize()

                for index, file_path in enumerate(tmap.set):
                    my.setAttr(file_node + '.explicitUvTiles[%s].explicitUvTileName' % index, file_path, type='string')
                 
                    my.setAttr(file_node + '.GridSize0', grid_size[0])
                    my.setAttr(file_node + '.GridSize1', grid_size[1])

        else:

            file_path = tmap.getFirstUdim()
            file_node = my.shadingNode('file', name=node_name, asTexture=True, isColorManaged=True)
            my.setAttr(file_node + '.fileTextureName', file_path, type='string')

            if tmap.isTiled():
                my.setAttr(file_node + '.uvTilingMode', 3)

            self.connect2DTextureNode(self.texture_node, file_node)

        return file_node


class ArnoldMat(Mat):
    
    def __init__(self, name, directory, textureset):
        Mat.__init__(self, name, directory, textureset)
        self.engine = ARNOLD
        self.create()
        self.logCreation()

    def create(self):
        self.mat_node = my.shadingNode('aiStandardSurface', name=self.full_name, asShader=True)
        self.sg = my.sets(name="%sSG" % self.full_name, empty=True, renderable=True, noSurfaceShader=True)
        my.connectAttr("%s.outColor" % self.full_name, "%s.surfaceShader" % self.sg)
        self.texture_node = my.shadingNode('place2dTexture', n=self.name + "_2dTexture", asUtility=True)
        self.createSelected()

    def createColor(self):
        file_node = self.addFileNode(self.engine, self.texture_set.color, self.base_color_file)
        
        my.connectAttr(file_node + '.outColor', self.mat_node + '.baseColor')
        
    def createNormal(self):
        file_node = self.addFileNode(self.engine, self.texture_set.normal, self.normal_file)

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        normal_map_node = my.shadingNode('aiNormalMap', n=self.name + '_normalMap', asShader=True)       
       
        my.connectAttr(file_node + '.outColor', normal_map_node + '.input')
        my.connectAttr(normal_map_node + '.outValue', self.mat_node + '.normalCamera') 

    def createBump(self):
        file_node = self.addFileNode(self.engine, self.texture_set.bump, self.bump_file)

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        normalBump = my.shadingNode('bump2d', n=self.name + '_normalBump', asUtility=True )
        my.setAttr(normalBump + '.aiFlipR', True)
        my.setAttr(normalBump + '.aiFlipG', True)
        my.connectAttr(file_node + '.outAlpha', normalBump + '.bumpValue')
        my.connectAttr(normalBump + '.outNormal', self.mat_node + '.normalCamera')   
        
    def createRoughness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.roughness, self.roughness_file)     

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)

        my.connectAttr(file_node + '.outAlpha', self.mat_node + '.specularRoughness')  

    def createGlossiness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.glossiness, self.glossiness_file)     

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)
        invert_node = my.shadingNode('aiColorCorrect', n=self.name + "_glossInvert", asUtility=True)
        my.connectAttr(file_node + '.outColor', invert_node + '.input')
        my.setAttr(invert_node + '.invert', 1)
        my.connectAttr(invert_node + '.outColorR',  self.mat_node + '.specularRoughness')

    def createMetalness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.metalness, self.metalness_file)    

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)

        my.connectAttr(file_node + '.outAlpha', self.mat_node + '.metalness')

    def createDisplacement(self):
        file_node = self.addFileNode(self.engine, self.texture_set.displacement, self.displacement_file)   

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)

        disp_shader_node = my.shadingNode('displacementShader', n=self.name + '_dispShader', asShader=True)
        my.connectAttr(file_node + '.outAlpha', disp_shader_node + '.displacement')
        my.connectAttr(disp_shader_node + '.displacement', self.sg + '.displacementShader')  

    def createAO(self):
        file_node = self.addFileNode(self.engine, self.texture_set.ao, self.ao_file)     

        colorcomp_node = my.shadingNode('colorComposite', n=self.name + '_colorComp', asShader=True)  
        my.connectAttr(file_node + '.outColor', colorcomp_node + '.colorB')
        my.connectAttr(self.base_color_file + '.outColor', colorcomp_node + '.colorA')

        my.setAttr(colorcomp_node + '.operation', 3)

        my.connectAttr(colorcomp_node + '.outColor', self.mat_node + '.baseColor', force=True)

    def createSpecular(self):
        file_node = self.addFileNode(self.engine, self.texture_set.specular, self.specular_file)   

    def createOpacity(self):
        file_node = self.addFileNode(self.engine, self.texture_set.opacity, self.opacity_file)   

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)
        my.connectAttr(file_node + '.outColor', self.mat_node + '.opacity')      

    def createEmissive(self):
        file_node = self.addFileNode(self.engine, self.texture_set.emissive, self.emissive_file)   

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)
        my.connectAttr(file_node + '.outAlpha', self.mat_node + '.emission')


class VrayMat(Mat):

    def __init__(self, name, directory, textureset):
        Mat.__init__(self, name, directory, textureset)
        self.engine = VRAY
        self.create()
        self.logCreation()
        
    def create(self):
        self.mat_node = my.shadingNode('VRayMtl', name=self.full_name, asShader=True)
        self.sg = my.sets(name="%sSG" % self.full_name, empty=True, renderable=True, noSurfaceShader=True)
        my.connectAttr("%s.outColor" % self.full_name, "%s.surfaceShader" % self.sg)
        self.texture_node = my.shadingNode('place2dTexture', n=self.name + "_2dTexture", asUtility=True)
        self.createSelected()
    
    def createColor(self):
        file_node = self.addFileNode(self.engine, self.texture_set.color, self.base_color_file)
        
        my.connectAttr(file_node + '.outColor', self.mat_node + '.color')

    def createNormal(self):
        file_node = self.addFileNode(self.engine, self.texture_set.normal, self.normal_file)

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.connectAttr(file_node + ".outColor", self.mat_node + ".bumpMap")
        my.setAttr(self.mat_node + '.bumpMapType', 1) ## corresponds to: Normal map in tangent space 

    def createBump(self):
        file_node = self.addFileNode(self.engine, self.texture_set.bump, self.bump_file)

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.connectAttr(file_node + ".outColor", self.mat_node + ".bumpMap")

    def createRoughness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.roughness, self.roughness_file)  

        my.setAttr(self.mat_node + ".useRoughness", 1)
        my.setAttr(self.mat_node + ".reflectionColorR", 1)
        my.setAttr(self.mat_node + ".reflectionColorG", 1)
        my.setAttr(self.mat_node + ".reflectionColorB", 1)

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)

        my.connectAttr(file_node + '.outAlpha', self.mat_node + '.reflectionGlossiness')

    def createGlossiness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.glossiness, self.glossiness_file)     

        my.setAttr(self.mat_node + ".reflectionColorR", 1)
        my.setAttr(self.mat_node + ".reflectionColorG", 1)
        my.setAttr(self.mat_node + ".reflectionColorB", 1)

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)

        my.connectAttr(file_node + '.outAlpha', self.mat_node + '.reflectionGlossiness')      

    def createMetalness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.metalness, self.metalness_file)
        
        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)  

        my.connectAttr(file_node + '.outAlpha', self.mat_node + '.metalness')    

    def createDisplacement(self):
        file_node = self.addFileNode(self.engine, self.texture_set.displacement, self.displacement_file)   

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)

        disp_shader_node = my.shadingNode('displacementShader', n=self.name + '_dispShader', asShader=True)
        my.connectAttr(file_node + '.outAlpha', disp_shader_node + '.displacement')
        my.connectAttr(disp_shader_node + '.displacement', self.sg + '.displacementShader')

    def createAO(self):
        file_node = self.addFileNode(self.engine, self.texture_set.ao, self.ao_file)   

    def createSpecular(self):
        file_node = self.addFileNode(self.engine, self.texture_set.specular, self.specular_file)   

    def createOpacity(self):
        file_node = self.addFileNode(self.engine, self.texture_set.opacity, self.opacity_file)   

        my.setAttr(file_node + '.colorSpace', 'Raw', type='string')
        my.setAttr(file_node + '.alphaIsLuminance', True)
        my.connectAttr(file_node + '.outColor', self.mat_node + '.opacityMap')        

    def createEmissive(self):
        file_node = self.addFileNode(self.engine, self.texture_set.emissive, self.emissive_file) 

        my.connectAttr(file_node + '.outColor', self.mat_node + '.illumColor')

        

class OctaneMat(Mat):

    def __init__(self, name, directory, textureset):
        Mat.__init__(self, name, directory, textureset)
        self.engine = OCTANE
        self.create()
        self.logCreation()

    def create(self):
        self.mat_node = my.shadingNode('octaneUniversalMaterial', name=self.full_name, asShader=True)
        self.sg = my.sets(name="%sSG" % self.full_name, empty=True, renderable=True, noSurfaceShader=True)
        my.connectAttr("%s.outColor" % self.full_name, "%s.surfaceShader" % self.sg)

        self.createSelected()
    
    def createColor(self):
        file_node = self.addFileNode(self.engine, self.texture_set.color, self.base_color_file)

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Albedo')

    def createNormal(self):
        file_node = self.addFileNode(self.engine, self.texture_set.normal, self.normal_file)

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Normal')

    def createBump(self):
        file_node = self.addFileNode(self.engine, self.texture_set.bump, self.bump_file)

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Bump')

    def createRoughness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.roughness, self.roughness_file)  

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Roughness')

    def createGlossiness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.glossiness, self.glossiness_file)  

    def createMetalness(self):
        file_node = self.addFileNode(self.engine, self.texture_set.metalness, self.metalness_file)   

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Metallic')

    def createDisplacement(self):
        file_node = self.addFileNode(self.engine, self.texture_set.displacement, self.displacement_file)   

        disp_node = my.shadingNode('octaneDisplacementNode', name=self.name + '_dispNode', asTexture=True)
        my.connectAttr(file_node + '.outTex', disp_node + '.Texture')
        my.connectAttr(disp_node + '.outDisp', self.mat_node + ".Displacement")

    def createAO(self):
        file_node = self.addFileNode(self.engine, self.texture_set.ao, self.ao_file)   

    def createSpecular(self):
        file_node = self.addFileNode(self.engine, self.texture_set.specular, self.specular_file)   

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Specular')

    def createOpacity(self):
        file_node = self.addFileNode(self.engine, self.texture_set.opacity, self.opacity_file)   

        my.connectAttr(file_node + '.outTex', self.mat_node + '.Opacity')

    def createEmissive(self):
        file_node = self.addFileNode(self.engine, self.texture_set.emissive, self.emissive_file) 
        
        my.connectAttr(file_node + '.outTex', self.mat_node + '.Emission')


## MENU ##################################################


def about(*args):
    '''
    This function shows a window with the info about MaterialCreator.
    '''

    w = 450
    h = 140
    window = my.window( title="About", width=w)
    my.columnLayout( adjustableColumn=True )
    my.text(label="\nMaterialCreator - for Autodesk Maya\n", font='fixedWidthFont')
    sep = my.separator(style="in", height=3) 
    my.text(label="\nAuthors: Roberto Menicatti\n", font='fixedWidthFont')
    sep = my.separator(style="in", height=3) 
    my.text(label="\nVersion: %s\n" % VERSION, font='fixedWidthFont')
    my.setParent( '..' )
    my.showWindow( window )


def getScriptPath():

    pathList = sys.path
    rootpath = None

    ## Look for icons folder
    for path in pathList:
        try:
            dir = os.listdir(path)
            for subdir in dir:
                if "MaterialCreator" in subdir:
                    rootpath = path
                    break
        except:
            pass

    return os.path.join(rootpath, "MaterialCreator")


def helpmenu(*args):
    '''
    This function shows a window with the help of MaterialCreator.
    '''

    with open(os.path.join(getScriptPath(), "Help.txt"), 'r') as readme:
        
        content = readme.readlines()

    readme_text = "".join(content[21:])

    w = 800
    h = 300
    window = my.window( title="Help", widthHeight=(w, h), sizeable=True)
    ml = my.columnLayout(adjustableColumn=True )
    my.text(label="\nMaterialCreator - for Autodesk Maya - HELP\n", width=w, font='fixedWidthFont')
    

    form = my.formLayout(parent=ml, width=w)
    sep = my.separator(style="in", height=3, width=w) 
    scrollLayout = my.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16, enableBackground=True, backgroundColor=[0.17, 0.17 , 0.17], borderVisible=True, childResizable=True)
    
    my.formLayout(form, edit=True, attachForm=[(sep, 'top', 5), 
                                                (sep, 'left', 0), 
                                                (sep, 'right', 0),
                                                    
                                                (scrollLayout, 'top', 10),
                                                (scrollLayout, 'left', 5), 
                                                (scrollLayout, 'right', 5),
                                                (scrollLayout, 'bottom', 30)])
    
    my.text(label=readme_text, align='left', font='fixedWidthFont')
    my.setParent( '..' )
    my.showWindow( window )


def changelog(*args):
    '''
    This function shows a window with the changelog of MaterialCreator.
    '''

    with open(os.path.join(getScriptPath(), "Changelog.txt"), 'r') as cl:
        
        content = cl.readlines()

    cl_text = "".join(content)

    w = 700
    h = 300
    window = my.window( title="Changelog", widthHeight=(w, h), sizeable=True)
    ml = my.columnLayout(adjustableColumn=True )
    my.text(label="\nMaterialCreator - for Autodesk Maya - CHANGELOG\n", width=w, font='fixedWidthFont')
    

    form = my.formLayout(parent=ml, width=w)
    sep = my.separator(style="in", height=3, width=w) 
    scrollLayout = my.scrollLayout(height=h-70, horizontalScrollBarThickness=16, verticalScrollBarThickness=16, enableBackground=True, backgroundColor=[0.17, 0.17 , 0.17], borderVisible=True)
    
    my.formLayout(form, edit=True, attachForm=[(sep, 'top', 5), 
                                                (sep, 'left', 0), 
                                                (sep, 'right', 0),
                                                    
                                                (scrollLayout, 'top', 10),
                                                (scrollLayout, 'left', 5), 
                                                (scrollLayout, 'bottom', 5), 
                                                (scrollLayout, 'right', 5)])
    
    my.text(label=cl_text, align='left', font='fixedWidthFont')
    my.setParent( '..' )
    my.showWindow( window )


def onlineGuide(*args):
    webbrowser.open(REPOSITORY_WIKI)


def goToSite(*args):
    onlineGuide()
    my.deleteUI("updaterMC", window=True)


def closeNotifier(*args):
    my.deleteUI("updaterMC", window=True)


def showUpdateNotifier(new_version):
    w = 360
    h = 140
    window = my.window("updaterMC", title="MaterialCreator Update", width=w)
    my.columnLayout( adjustableColumn=True )
    my.text(label="\nA newer version of MaterialCreator, is available!\n", font='fixedWidthFont')
    my.text(label="\nDo you want to proceed to download page?\n", font='fixedWidthFont')

    my.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 177), (2, 177)], columnSpacing=[(2, 6)])
    my.button(label="OK", w=177, command=goToSite) 
    my.button(label="Not now", w=177, command=closeNotifier) 

    my.setParent( '..' )
    my.showWindow( window )


def main():
    
    try:
        response = urlopen(REPOSITORY_WIKI)
        parser = RepositoryParser()
        parser.feed(response.read().decode('utf-8'))

        if float(parser.version) > float(VERSION):
            showUpdateNotifier(parser.version)
    except:
        pass

    MatCreatorWindow()


if __name__ == '__main__':

    main()

