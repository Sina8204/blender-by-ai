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
    
    # ORIGINAL frame_end = 30
    # To slow down the animation, increase the frame_end and scale keyframe times.
    frame_end = 60 # Doubled the frames for a slower animation
    
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.context.scene.frame_current = frame_start

    # Define keyframe data for a "Plants vs Zombies" style zombie walking animation
    # Rotations are defined in degrees and converted to radians
    # Frame numbers are scaled by a factor of (new_frame_end / original_frame_end) = (60 / 30) = 2
    keyframe_data = {
        "torso": {
            1*2:  {"location": (0.0, 0.0, 0.0),   "rotation": (math.radians(-10.0), 0.0, math.radians(3.0))},  # Lean forward, slight twist right
            8*2:  {"location": (0.0, 0.0, -0.02), "rotation": (math.radians(-12.0), 0.0, math.radians(-3.0))}, # Lean more, twist left
            15*2: {"location": (0.0, 0.0, 0.0),   "rotation": (math.radians(-10.0), 0.0, math.radians(3.0))},  # Back to original lean, twist right
            23*2: {"location": (0.0, 0.0, -0.02), "rotation": (math.radians(-12.0), 0.0, math.radians(-3.0))}, # Lean more, twist left
            30*2: {"location": (0.0, 0.0, 0.0),   "rotation": (math.radians(-10.0), 0.0, math.radians(3.0))}   # Same as frame 1
        },
        "head": {
            1*2:  {"location": (0.0, 0.0, 0.0),   "rotation": (math.radians(-20.0), 0.0, 0.0)}, # Drooped forward
            8*2:  {"location": (0.0, 0.0, 0.01),  "rotation": (math.radians(-18.0), 0.0, 0.0)}, # Slight lift, less droop
            15*2: {"location": (0.0, 0.0, 0.0),   "rotation": (math.radians(-20.0), 0.0, 0.0)}, # Drooped forward
            23*2: {"location": (0.0, 0.0, 0.01),  "rotation": (math.radians(-18.0), 0.0, 0.0)}, # Slight lift, less droop
            30*2: {"location": (0.0, 0.0, 0.0),   "rotation": (math.radians(-20.0), 0.0, 0.0)}  # Same as frame 1
        },
        "hand_right": {
            1*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}, # Slightly back
            8*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)},  # Slightly forward
            15*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}, # Slightly back
            23*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)},  # Slightly forward
            30*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}  # Same as frame 1
        },
        "hand_left": {
            1*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)},  # Slightly forward (opposite of right)
            8*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}, # Slightly back
            15*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)},  # Slightly forward
            23*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}, # Slightly back
            30*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)}   # Same as frame 1
        },
        "leg_right": {
            1*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-15.0), 0.0, 0.0)}, # Back, dragging
            8*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)},  # Moving forward, almost straight
            15*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(15.0), 0.0, 0.0)},  # Forward, planted
            23*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(5.0), 0.0, 0.0)},  # Moving back
            30*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-15.0), 0.0, 0.0)} # Same as frame 1
        },
        "leg_left": {
            1*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(15.0), 0.0, 0.0)},  # Forward, planted (opposite of right)
            8*2:  {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}, # Moving back, almost straight
            15*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-15.0), 0.0, 0.0)}, # Back, dragging
            23*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(-5.0), 0.0, 0.0)}, # Moving forward
            30*2: {"location": (0.0, 0.0, 0.0), "rotation": (math.radians(15.0), 0.0, 0.0)}  # Same as frame 1
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
