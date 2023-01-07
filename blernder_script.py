import bpy
import pandas as pd
import os
from mathutils import Vector



os.chdir('G:\My Drive\Python\CodingLanguageBlender') #Change this to the location where the csv data resides...
df = pd.read_csv('data.csv')
df = df.sort_values('year')


barDist = 1.2
yearDist = 5
scaleFactor = 20 #overall scale
barYScale = 2 #bar length scale
animationSpeed = 50
startFrame = 200


#DELETE ANY EXISTING ITEMS IN COLLECTION
try: #if error then ignore - the collection may not exist
    collection = bpy.data.collections.get('PythonCollection')
    for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)
except:
    pass

#CREATE A COLLECTION FOR ALL ADDED ITEMS
collection = bpy.data.collections.new("PythonCollection")

##SCENE SET UP (OPTIONAL)##
#Light1
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2.8, -8, 14),)
obj = bpy.context.active_object
bpy.context.object.data.size = 0.5*scaleFactor
bpy.context.object.data.energy = 25*scaleFactor
bpy.data.collections['PythonCollection'].objects.link(obj)
#Light2
bpy.ops.object.light_add(type='AREA', align='WORLD', location=(1, 3, 6),)
obj = bpy.context.active_object
bpy.context.object.data.size = 0.2*scaleFactor
bpy.context.object.data.energy = 20*scaleFactor
bpy.data.collections['PythonCollection'].objects.link(obj)

#Plane
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(46.8, 0, 0), scale=(1, 1, 1))
obj = bpy.context.active_object
bpy.ops.transform.resize(value=(69.5006, 69.5006, 69.5006),)
bpy.data.collections['PythonCollection'].objects.link(obj)

#Camera:
#Transition to show each set of bars:
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0.6*scaleFactor, -0.1*scaleFactor, 0.5*scaleFactor), scale=(1*scaleFactor, 1*scaleFactor, 1*scaleFactor))
obj = bpy.context.active_object
bpy.data.collections['PythonCollection'].objects.link(obj)
bpy.context.object.data.type = 'ORTHO'
bpy.context.object.data.ortho_scale = 1.5*scaleFactor
bpy.ops.transform.rotate(value=-0.83, orient_axis='X',)
obj.keyframe_insert(data_path="location",frame = 50)
obj.keyframe_insert(data_path="rotation_euler",frame = 50)
bpy.ops.transform.rotate(value=3.14, orient_axis='Z',)
obj.keyframe_insert(data_path="rotation_euler",frame = 100)
obj.location=(0.6*scaleFactor, 0.3*scaleFactor, 0.5*scaleFactor)
obj.keyframe_insert(data_path="location",frame = 100)
#stop the camera for 50 frames:
obj.keyframe_insert(data_path="location",frame = 150)
obj.keyframe_insert(data_path="rotation_euler",frame = 150)
#back to facing the chart:
bpy.ops.transform.rotate(value=1.57001, orient_axis='Z',)
obj.keyframe_insert(data_path="rotation_euler",frame = 200)
bpy.ops.transform.rotate(value=0.83, orient_axis='Y',)
obj.keyframe_insert(data_path="rotation_euler",frame = 200)
obj.location=(obj.location[0]-7, 0, obj.location[2]+2,)
obj.keyframe_insert(data_path="location",frame = 200)




#end position
#bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0.4*scaleFactor, -0.1*scaleFactor, 1*scaleFactor), scale=(1*scaleFactor, 1*scaleFactor, 1*scaleFactor))
#bpy.ops.transform.rotate(value=-1.57001, orient_axis='Z',)

# store the location of current 3d cursor (for changing origin of cubes for rotation)
saved_location = bpy.context.scene.cursor.location  # returns a vector

PR_mat = bpy.data.materials.new('PRMat')
I_mat = bpy.data.materials.new('IMat')
Text_mat = bpy.data.materials.new('TextMat')

for i,year in enumerate(df.year.unique()):
    tmp = df.loc[df.year==year]
    tmp = tmp.sort_values('totalActivity',ascending=False)
    maxValue = tmp.totalActivity.max()*barYScale
    maxI     = tmp.countI.max()*barYScale*2
    maxPR    = tmp.countPR.max()*barYScale*2
    


    if i==0: #first year, set up the bars...
        #add year text:
        for yearCount, textYr in enumerate(df.year.unique()):
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(-3, -2, -yearDist*yearCount*2.5 + 2), scale=(1, 1, 1))
            obj = bpy.context.active_object
            bpy.context.active_object.name = "yearText_"+str(textYr)
            bpy.data.collections['PythonCollection'].objects.link(obj)
            bpy.ops.transform.rotate(value=-1.57001, orient_axis='Z',) #1.5708 is 90 degrees (radians)
            bpy.context.object.data.body = str(textYr)
            obj.keyframe_insert(data_path="location",frame = (i*animationSpeed)+startFrame) 

    
        row = 0
        for index,data in tmp.iterrows():
            #########build issues
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD',
            location=(barDist*row, (data.countI/maxI*scaleFactor)/2, -0.5),
            scale=(1, 1, 0.2))
            obj = bpy.context.active_object
            bpy.data.collections['PythonCollection'].objects.link(obj)
            obj.scale=(1, data.countI/maxI*scaleFactor, 0.2)
            obj.keyframe_insert(data_path="scale",frame = i*animationSpeed+startFrame)
            #origin for rotation
            bpy.context.scene.cursor.location = Vector((barDist*row,0,0))
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            #for naming
            bpy.context.active_object.name = str(data.codeName) + "_I"
            #rotate
            bpy.ops.transform.rotate(value=-0.75, orient_axis='X',)
            #color:
            obj.data.materials.append(I_mat)
            obj.active_material_index = len(obj.data.materials) - 1 
            obj.active_material.diffuse_color = (0.1,1,0.2,1)

            #######build pull requests
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD',
            location=(barDist*row, (data.countPR/maxPR*scaleFactor)/-2, -0.5),
            scale=(1, (data.countPR/maxPR*scaleFactor), 0.2))
            obj = bpy.context.active_object
            bpy.data.collections['PythonCollection'].objects.link(obj)
            obj.keyframe_insert(data_path="scale",frame = i*animationSpeed+startFrame)
            #origin for rotation
            bpy.context.scene.cursor.location = Vector((barDist*row,0,0))
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            #for naming
            bpy.context.active_object.name = str(data.codeName) +"_PR"
            #rotate:
            bpy.ops.transform.rotate(value=0.75, orient_axis='X',)
            #color:
            obj.data.materials.append(PR_mat)
            obj.active_material_index = len(obj.data.materials) - 1 
            obj.active_material.diffuse_color = (0.1,0.5,0.25,1)
            
            #Add text:
       
            #add text labels for bars
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(barDist*row+0.2, -2, 2), scale=(1, 1, 1))
            obj = bpy.context.active_object
            bpy.data.collections['PythonCollection'].objects.link(obj)
            bpy.ops.transform.rotate(value=-1.57001, orient_axis='Z',) #1.5708 is 90 degrees (radians)
            bpy.context.object.data.body = data.codeName
            obj.keyframe_insert(data_path="location",frame = i*animationSpeed+startFrame)
            #text color
            obj.data.materials.append(Text_mat)
            obj.active_material_index = len(obj.data.materials) - 1 
            obj.active_material.diffuse_color = (1,1,1,1)
            #text naming
            bpy.context.active_object.name = str(data.codeName) +"_text"
            
            row+=1 #add one to the row
    else: #for the remainder of the data we need to adjust the animation and scale
        row = 0
        for yearCount, textYr in enumerate(df.year.unique()):
            obj = bpy.data.objects["yearText_"+str(textYr)]
            obj.select_set(True)
            obj.location=(obj.location[0], obj.location[1], obj.location[2]+ yearDist*2.5,)
            obj.keyframe_insert(data_path="location",frame = (i*animationSpeed)+startFrame)
            
        for index,data in tmp.iterrows():
            for suffix in ['_I','_PR']:
                obj = bpy.data.objects[str(data.codeName)+suffix]
                obj.select_set(True)
                obj.scale=(1, data.countI/maxI*scaleFactor, 0.2)
                obj.keyframe_insert(data_path="scale",frame = i*animationSpeed+startFrame)
                obj.location=(barDist*row, obj.location[1], obj.location[2],)
                obj.keyframe_insert(data_path="location",frame = i*animationSpeed+startFrame)
            #Text:
            obj = bpy.data.objects[str(data.codeName)+"_text"]
            obj.select_set(True)
            obj.location=(barDist*row+0.2, obj.location[1], obj.location[2],)
            obj.keyframe_insert(data_path="location",frame = i*animationSpeed+startFrame)
            #year text:
            obj = bpy.data.objects[str(data.codeName)+"_text"]
            obj.select_set(True)            
            obj.keyframe_insert(data_path="location",frame = i*animationSpeed+startFrame)
            
            row +=1#add one to the row
                
        
    
# set 3dcursor location back to the stored location
bpy.context.scene.cursor.location = saved_location
