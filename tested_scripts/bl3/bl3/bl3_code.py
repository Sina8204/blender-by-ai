import bpy
import math

# Find the armature object in the scene
armature_obj = None
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        armature_obj = obj
        break

if armature_obj:
    # Clear existing animation data for the armature object
    # This will clear the active action linked to the armature.
    if armature_obj.animation_data:
        armature_obj.animation_data.action = None
    else:
        armature_obj.animation_data_create() # Create animation data if it doesn't exist

    # Set up animation frames
    frame_start = 1
    frame_end = 30 # A simple 30-frame walk cycle
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.context.scene.frame_current = frame_start

    # Define keyframe data for a basic walking animation
    # Rotations are defined in degrees and converted to radians
    keyframe_data = {
        "torso": {
            1: {"location": (0.0, 0.0, 0.0), "rotation": (0.0, 0.0, math.radians(5.0))},
            8: {"location": (0.0, 0.0, -0.05), "rotation": (0.0, 0.0, math.radians(-5.0))},
            15: {"location": (0.0, 0.0, 0.0), "rotation": (0.0, 0.0, math.radians(-5.0))},
            23: {"location": (0.0, 0.0, -0.05), "rotation": (0.0, 0.0, math.radians(5.0))},
            30: {"location": (0.0, 0.0, 0.0), "rotation": (0.0, 0.0, math.radians(5.0))}
        },
        "head": {
            1: {"location": (0.0, 0.0, 0.0), "rotation": (0.0, 0.0, 0.0)},
            8: {"location": (0.0, 0.0, 0.02), "rotation": (0.0, 0.0, 0.0)},
            15: {"location": (0.0, 0.0, 0.0), "rotation": (0.0, 0.0, 0.0)},
            23: {"location": (0.0, 0.0, 0.02), "rotation": (0.0, 0.0, 0.0)},
            30: {"location": (0.0, 0.0, 0.0), "rotation": (0.0, 0.0, 0.0)}
        },
        "hand_right": {
            1: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(20.0), 0.0, 0.0)},
            8: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-10.0), 0.0, 0.0)},
            15: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-20.0), 0.0, 0.0)},
            23: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(10.0), 0.0, 0.0)},
            30: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(20.0), 0.0, 0.0)}
        },
        "hand_left": {
            1: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-20.0), 0.0, 0.0)},
            8: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(10.0), 0.0, 0.0)},
            15: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(20.0), 0.0, 0.0)},
            23: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-10.0), 0.0, 0.0)},
            30: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-20.0), 0.0, 0.0)}
        },
        "leg_right": {
            1: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-30.0), 0.0, 0.0)},
            8: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(15.0), 0.0, 0.0)},
            15: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(30.0), 0.0, 0.0)},
            23: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-15.0), 0.0, 0.0)},
            30: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-30.0), 0.0, 0.0)}
        },
        "leg_left": {
            1: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(30.0), 0.0, 0.0)},
            8: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-15.0), 0.0, 0.0)},
            15: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-30.0), 0.0, 0.0)},
            23: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(15.0), 0.0, 0.0)},
            30: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(30.0), 0.0, 0.0)}
        }
    }

    # Apply keyframes
    for bone_name, frames_data in keyframe_data.items():
        if bone_name in armature_obj.pose.bones:
            pb = armature_obj.pose.bones[bone_name]

            # Set rotation mode before inserting keyframes
            pb.rotation_mode = 'XYZ'

            for frame, data in frames_data.items():
                bpy.context.scene.frame_set(frame)

                # Location
                pb.location = data["location"]
                pb.keyframe_insert(data_path="location", index=-1)

                # Rotation
                pb.rotation_euler = data["rotation"]
                pb.keyframe_insert(data_path="rotation_euler", index=-1)

                # Scale (assuming no change from default 1.0, 1.0, 1.0)
                pb.scale = (1.0, 1.0, 1.0)
                pb.keyframe_insert(data_path="scale", index=-1)

    # Reset current frame to the start
    bpy.context.scene.frame_set(frame_start)
else:
    print("No armature object found in the scene to animate.")
