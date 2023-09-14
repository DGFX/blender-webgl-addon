import bpy
import time
import json
import math
import os
from mathutils import Quaternion, Euler

def arrayToString(ar):
    str1 = ''
    for i in ar:
        str1 += str(i)
        str1 += "."
    return str1[:-1]

#------------ SPACER ---------------------
def tupleToString(tup):
    str1 = ''
    for i in tup:
        str1 += str(i)
        str1 += "."
    return str1[:-1]
    
#------------ SPACER ---------------------

#Round Values
def rd(e):
    return round(e, bpy.context.scene.precision)
def crd(e,precison):
    return round(e, precison)

#------------ SPACER ---------------------

#Get a Property from an Object
def getproperty(object,property):
    check = True
    try:
        get = object[property]
    except:
        check = False
    
    if(check):
        value = rd(object[property])
        return  value
    else:
        return False

#------------ SPACER ---------------------

#Force Select Objects
def forceselect(e): 
    #bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    e.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[e.name]


#------------ SPACER ---------------------

#Force Objects to Be visible
def forceSelectable(e):
    coll = e.users_collection[0]
    collName = coll.name
    e.hide_select = False
    bpy.data.collections[collName].hide_select = False


#------------ SPACER ---------------------

def findCollection(collName):
    for coll in bpy.data.collections:
        if (coll.name == collName):
            return coll

def findObject(obName):
    for ob in bpy.data.objects:
        if (ob.name == obName):
            return ob
        
def findObjects(names):
    matching_objects = [None] * len(names)
    for obj in bpy.context.scene.objects:
        if obj.name in names:
            index = names.index(obj.name)
            matching_objects[index] = obj
    return matching_objects


def findCollectionWithString(string):
    for coll in bpy.data.collections:
        if string in coll.name:
            return coll

#------------ SPACER ---------------------

def setFolderStructure():
    folderpath = bpy.context.scene.saveFolderPath
    folderName = "models"
    modelsFolder =os.path.join(folderpath, folderName)
    folderName = "textures"
    textFolder =os.path.join(folderpath, folderName)

    if os.path.exists(modelsFolder) == False :
        os.mkdir(modelsFolder)
    if os.path.exists(textFolder) == False :
        os.mkdir(textFolder)

#------------ SPACER ---------------------


def pollcheckExport():
    check = ["Objects","Instances","Empties","Rigged Objects"]
    for name in check:
        coll = findCollectionWithString(name)
        if(coll):
            collName = coll.name
            path = bpy.context.scene.saveFolderPath
            #len(coll.objects) != 0
            if(name in collName and path !=""):
                return True
        return False    

#------------ SPACER ---------------------

def namingConvention(string):
    string = string.lower()
    string = string.replace(".", "-")
    string = string.replace("_", "-")
    string = string.replace(" ", "-")
    return string

#------------ SPACER ---------------------

def geoCleaner(ob,skinned):

    forceselect(ob)
    print("TBA-5",ob.name)
    prevLoc = ob.location.copy()
    prevRot = ob.rotation_euler.copy()
    prevSac = ob.scale.copy()
    
    #------------ SPACER ---------------------
    ob.location = (0,0,0)
    ob.rotation_euler =(0,0,0)
    ob.scale = (1,1,1)

    #------------ SPACER ---------------------
    bpy.ops.object.shade_smooth()
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.average_normals(average_type='FACE_AREA')
    bpy.ops.object.editmode_toggle()

    #------------ SPACER ---------------------
    if(skinned):
        parent = ob.parent
        forceselect(parent)
        parentprevLoc = parent.location.copy()
        parentprevRot = parent.rotation_euler.copy()
        parentprevSac = parent.scale.copy()
        parent.location = (0,0,0)
        parent.rotation_euler =(0,0,0)
        parent.scale = (1,1,1)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        prevLoc = parentprevLoc
        prevRot = parentprevRot
        prevSac = parentprevSac

    return prevLoc,prevRot,prevSac

    


def getunic(mylist):
    seen = set()
    dupes = [x for x in mylist if x in seen or seen.add(x)]  
    srtDupes = sorted(list(set(dupes)))
    revDup = list(dict.fromkeys(mylist))
    return revDup


#------------ SPACER ---------------------
def getPathPoints(ob):
    for subcurve in ob.data.splines:
        curvetype = subcurve.type
        points = []
        #------------------------
        if curvetype == 'NURBS':
            count = 0
            for nurbspoint in subcurve.points:
                points.append([rd(nurbspoint.co[0]),rd(nurbspoint.co[2]),-rd(nurbspoint.co[1])])
                count += 1 
        #------------------------  
        if curvetype == 'BEZIER':
            count = 0  
            for bezpoint in subcurve.bezier_points:
                points.append([rd(bezpoint.co[0]),rd(bezpoint.co[2]),-rd(bezpoint.co[1])])
                count += 1  

    return points


#------------ Fetch Collections ---------------------
def getCollections(string):
    colls = []
    for coll in  bpy.data.collections:
        if string in coll.name:
            colls.append(coll)
    return colls

def getDifNamesColl(array):
    colls = []
    for coll in  bpy.data.collections:
        for name  in array:
            if name in coll.name:
                colls.append(coll)
    return colls
       
       
#------------ Fetch Collections ---------------------

def nameMatchScene(name,cname):
    cname = cname[0]
    name = cname + "-" + name
    return name

#------------ Fetch Children Collections ---------------------
def getChildCollections(collParent):
    colls = []
    for coll in  collParent.children:
            colls.append(coll)
    return colls

def getNamedChildCollections(string, collParent):
    colls = []
    for coll in collParent.children:
        if(string in coll.name):
            colls.append(coll)
    return colls

#------------ Fetch Children Collections ---------------------
#def isObjectupdated(ob):
    #dep = bpy.context.evaluated_depsgraph_get()




#------------ SPACER ---------------------  

def reload_textures():
    print("UPDATING TEXTURES")
    ob = bpy.context.view_layer.objects.active
    if ob is not None and ob.type == "MESH":
        if len(ob.material_slots) > 0:
            mat = ob.material_slots[0].material
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        if node.image:
                            node.image.reload()
       
#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

def restUpdateState():
    nameArray = ["Objects","Rigged Objects","Instances Manual","Instances Nodes"]
    allColls = getDifNamesColl(nameArray)
    if len(allColls) > 0:
        for coll in allColls:
            if coll.name in nameArray:
                if("Instances" in coll.name):
                    for cc in coll.children:
                        if("Instanced Geometry" in cc.name):     
                            for ob in cc.objects:
                                createProp(ob,"updated",1)
                            for ccc in cc.children:
                                for ob in ccc.objects:
                                    createProp(ob,"updated",1)
                        else:
                            count = 0
                            for ob in cc.objects:
                                if(count == 0):
                                    createProp(ob,"updated",1)
                else:
                    for ob in coll.objects:
                        if(ob.type == 'MESH'):
                            createProp(ob,"updated",1)


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

def fitTo01(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

def flipAxis(coords):
    x, y, z, t = coords
    return [x, z, -y, t]

def flipScale(coords):
    x, y, z, t = coords
    return [x, z, y, t]

def getAnimationValues(ob,type,prop):
    
    data = []
    name = ob.name
    prop = prop.replace("'", '"')

    if ob.animation_data.action:
        print(name,prop,"HAS ANIMATION DATA")
        fcurves = [fcurve for fcurve in ob.animation_data.action.fcurves if fcurve.data_path == prop]
        print("TBA-ANITEST-0",fcurves)
        ftotal = len(fcurves)+1
        end = bpy.context.scene.frame_end


        # Create a list of lists for keyframe_points coordinates
        keyframe_points = [[] for _ in range(ftotal)]
        for fcurve in fcurves:
            index = fcurve.array_index
            for keyframe in fcurve.keyframe_points:
                frame = keyframe.co.x
                frame = fitTo01(frame,1,end)
                value = keyframe.co.y
                if type == "vector":
                     keyframe_points[index].append(rd(value))
                     if(index>1):
                        keyframe_points[index+1].append(rd(frame))
                else:
                     value = [rd(value),rd(frame)]
                     data.append(value)
                   

        if type == "vector" and prop == "location":
            data = [[keyframe_points[i][j] for i in range(ftotal)] for j in range(len(keyframe_points[0]))]
            data = [flipAxis(coords) for coords in data]
        
        if type == "vector" and prop == "scale":
            data = [[keyframe_points[i][j] for i in range(ftotal)] for j in range(len(keyframe_points[0]))]
            data = [flipScale(coords) for coords in data]
        

        if type == "vector" and prop == "rotation_euler":
            print("TBA-ANITEST-1")
             # Convert the list of keyframe points
            data = [[keyframe_points[i][j] for i in range(ftotal)] for j in range(len(keyframe_points[0]))]
            
            # Convert rotation to quaternions and adjust the order
            new_data = []
            print("TBA-ANITEST-2",data)
            for coords in data:
                # Extracting the x, y, z rotation values from coords
                x, y, z, t = coords
                euler_rotation = Euler((x, y, z), 'XYZ')
                rot = euler_rotation.to_quaternion()
                rot.normalize()
                rot = Quaternion((rot[0], rot[1], rot[3], -rot[2]))
                # Adjusting the quaternion order and appending 't' at the end
                quat_data = [rd(rot[1]), rd(rot[2]), rd(rot[3]), rd(rot[0]), t]
                new_data.append(quat_data)
                print("TBA-ANITEST-3")
            
            data = new_data 


        # Remove repeated values
       
 
    else:
        print(name,"NO ANIMATION DATA")
        if type == "vector":
            loc = ob.location.copy()
            data.append(loc)
        else:
            if prop == 'lens':
                val = [rd(ob.lens),0.0]
                data.append(val)   
    return data  
                 


#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

def createProp(ob,propName,val): 
    ob.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[ob.name]
    current_mode = bpy.context.mode
    if current_mode == "OBJECT":
        bpy.props.FloatProperty(name=propName)
        bpy.context.object[propName] = val
    return val

def createWorldProp(e,propName,val): 
    bpy.props.FloatProperty(name=propName)
    e[propName] = val
    return val
  
def getproperty(object,property):
    check = True
    try:
        get = object[property]
    except:
        check = False
        
    if(check):
        if(object.type == 'MESH'):    
            value = object[property]
        else:
            value = object[property]
        
        return  value
    else:
        return False

def getworldProperty(e,property):
    check = True
    
    try:
        get = e[property]
    except:
        check = False
        
    if(check):
        value = e[property]
        return  value
    else:
        return False



def checkForUpdates(e):
    if isinstance(e, bpy.types.World):
        print("CHECK-WORLD:")
        try:
            prop = getworldProperty(e,"updated")
            return prop
        except:
            prop = createWorldProp(e,"updated",0)
            return prop
    else:
        print("CHECK-OBJECT:")
        try:
            prop = getproperty(e,"updated")
            return prop
        except:
            prop = createProp(e,"updated",0)
            return prop

#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

def openDocumentation():
    url = "https://www.notion.so/unseenstudio/UNSEEN-BWE-ADDON-3db2fe9c730b48a1a8b587054845eb3f?pvs=4"
    os.system(f"start {url}")  # For Windows
    
#------------ SPACER ---------------------
#------------ SPACER ---------------------
#------------ SPACER ---------------------

def isTransformAni(obj):
    if obj.animation_data:
        for fcurve in obj.animation_data.action.fcurves:
            if any(x in fcurve.data_path for x in ("location", "rotation", "scale")):
                return True
    return False
