import mathutils
import bpy
import bpy_extras
import sys
import itertools
from . import mot

HEIGHT_CORRECTION = 1.055

def import_mot(mot, name):
    bpy.ops.object.mode_set(mode='POSE')

    arm = bpy.context.active_object
    bones = arm.pose.bones

    arm.animation_data_create()
    action = bpy.data.actions.new(name=name)
    arm.animation_data.action = action

    for (name, anim) in mot.anims.items():
        # if anim is None or name not in ["n_hara_cp", "kg_hara_y"]:
        if anim is None:
            continue
        # scale = 1./3. if "cl_momo" in name else 1.;
        scale = 1
        if anim.target:
            for (idx, target) in enumerate([anim.target.x, anim.target.y, anim.target.z]):
                if len(target) != 0:
                    curve = action.fcurves.new(data_path=f'pose.bones["{name}_target"].location', index=idx)
                    curve.keyframe_points.add(len(target))
                    for (i, frame) in enumerate(target):
                        index = int(frame.frame) if frame.frame else 0
                        curve.keyframe_points[i].co = (index, frame.value)
                        curve.keyframe_points[i].interpolation = 'LINEAR'
        if anim.position:
            # print(f"setting `{name}` position")
            if len(anim.position.x) != 0:
                curve = action.fcurves.new(data_path=f'pose.bones["{name}"].location', index=0)
                curve.keyframe_points.add(len(anim.position.x))
                for (i, frame) in enumerate(anim.position.x):
                    index = int(frame.frame) if frame.frame else 0
                    curve.keyframe_points[i].co = (index, frame.value)
                    curve.keyframe_points[i].interpolation = 'LINEAR'
            if len(anim.position.y) != 0:
                curve = action.fcurves.new(data_path=f'pose.bones["{name}"].location', index=2)
                curve.keyframe_points.add(len(anim.position.y))
                for (i, frame) in enumerate(anim.position.y):
                    index = int(frame.frame) if frame.frame else 0
                    value = frame.value - HEIGHT_CORRECTION if name == "n_hara_cp" else frame.value
                    curve.keyframe_points[i].co = (index, value)
                    curve.keyframe_points[i].interpolation = 'LINEAR'
            if len(anim.position.z) != 0:
                curve = action.fcurves.new(data_path=f'pose.bones["{name}"].location', index=1)
                curve.keyframe_points.add(len(anim.position.z))
                for (i, frame) in enumerate(anim.position.z):
                    index = int(frame.frame) if frame.frame else 0
                    curve.keyframe_points[i].co = (index, -1*frame.value)
                    curve.keyframe_points[i].interpolation = 'LINEAR'

        if anim.rotation:
            # print(f"setting `{name}` rotation")
            
            try:
                bone = bones[name]
                bone.rotation_mode = 'XYZ'
            except KeyError:
                print(F"Couldn't set `{name}`'s rotation mode. Bone not in rig, ignoring")
            anims = [anim.rotation.x, anim.rotation.z, anim.rotation.y]
            for (idx, target) in enumerate(anims):
                if len(target) != 0:
                    curve = action.fcurves.new(data_path=f'pose.bones["{name}"].rotation_euler', index=idx)
                    curve.keyframe_points.add(len(target))
                    for (i, frame) in enumerate(target):
                        index = int(frame.frame) if frame.frame else 0
                        frame = -1 * frame.value if idx == 1 else frame.value
                        curve.keyframe_points[i].co = (index, frame)
                        curve.keyframe_points[i].interpolation = 'LINEAR'

    bpy.ops.object.mode_set(mode='OBJECT')

    print("Imported a motion .bin successfully")
