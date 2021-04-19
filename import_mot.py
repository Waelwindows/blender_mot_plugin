import mathutils
import bpy
import bpy_extras
import sys
import itertools
from . import mot

HEIGHT_CORRECTION = 1.055

def import_mot(mot):
    bpy.ops.object.mode_set(mode='POSE')

    arm = bpy.context.active_object
    bones = arm.pose.bones

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
    target_parent = bpy.context.active_object
    target_parent.name = "target_parent"
    target_parent.empty_display_size = 0.1

    print(f"{mot.anims.keys()}")

    for (name, anim) in mot.anims.items():
        if anim is None or name not in ["n_hara_cp", "kg_hara_y"]:
        # if anim is None:
            continue
        # scale = 1./3. if "cl_momo" in name else 1.;
        scale = 1
        if anim.target:
            bone = bones[f"{name}_target"]
            for frame in anim.target.x:
                bone.location.x = frame.value * scale
                index = int(frame.frame) if frame.frame else 0
                bone.keyframe_insert(data_path="location", frame=index, index=0)    
            for frame in anim.target.y:
                bone.location.y = frame.value * scale
                index = int(frame.frame) if frame.frame else 0
                bone.keyframe_insert(data_path="location", frame=index, index=1)    
            for frame in anim.target.z:
                bone.location.z = frame.value * scale
                index = int(frame.frame) if frame.frame else 0
                bone.keyframe_insert(data_path="location", frame=index, index=2)    
        try:
            bone = bones[name]
            if anim.position:
                print(f"setting `{name}` position")
                for frame in anim.position.x:
                    bone.location.x = frame.value
                    index = int(frame.frame) if frame.frame else 0
                    bone.keyframe_insert(data_path="location", frame=index, index=0)    
                for frame in anim.position.y:
                    bone.location.z = frame.value
                    if name == "n_hara_cp":
                        bone.location.z -= HEIGHT_CORRECTION;
                    index = int(frame.frame) if frame.frame else 0
                    bone.keyframe_insert(data_path="location", frame=index, index=2)    
                for frame in anim.position.z:
                    bone.location.y = -1 * frame.value
                    index = int(frame.frame) if frame.frame else 0
                    bone.keyframe_insert(data_path="location", frame=index, index=1)    

            if anim.rotation:
                print(f"setting `{name}` rotation")

                bone.rotation_mode = 'XYZ'
                # print(f"rotation x: {len(anim.rotation.x)}")
                for frame in anim.rotation.x:
                    bone.rotation_euler.x = frame.value
                    index = int(frame.frame) if frame.frame else 0
                    bone.keyframe_insert(data_path="rotation_euler", frame=index, index=0)    
                # print(f"rotation y: {len(anim.rotation.y)}")
                for frame in anim.rotation.z:
                    bone.rotation_euler.y = frame.value
                    index = int(frame.frame) if frame.frame else 0
                    bone.keyframe_insert(data_path="rotation_euler", frame=index, index=1)    
                # print(f"rotation z: {len(anim.rotation.z)}")
                for frame in anim.rotation.y:
                    bone.rotation_euler.z = frame.value
                    index = int(frame.frame) if frame.frame else 0
                    bone.keyframe_insert(data_path="rotation_euler", frame=index, index=2)    
        except KeyError:
            continue
            # print(f"`{name}` not found in rig, but in mot. Ignoring")

    target_parent.rotation_euler.x += 1.57079632679
    bpy.ops.object.mode_set(mode='OBJECT')

    print("Imported a motion .bin successfully")
