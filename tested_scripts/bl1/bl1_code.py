import bpy
import math

# --- Configuration ---
armature_name = 'Armature'
fps = 24
running_duration_seconds = 2
running_frames = running_duration_seconds * fps
jump_start_frame = running_frames + 1

# Store animation data
animation_data = {}

# --- Helper to add keyframe data ---
def add_keyframe_data(bone_name, frame, loc=None, rot=None, scale=None):
    if bone_name not in animation_data:
        animation_data[bone_name] = {'location': {}, 'rotation': {}, 'scale': {}}
    
    if loc is not None:
        animation_data[bone_name]['location'][frame] = loc
    if rot is not None:
        animation_data[bone_name]['rotation'][frame] = rot
    if scale is not None:
        animation_data[bone_name]['scale'][frame] = scale

# --- Running Animation Data (Frames 1 to running_frames) ---
leg_swing_angle = math.radians(20)
arm_swing_angle = math.radians(20)
head_tilt_angle = math.radians(5)
cycle_speed_factor = 2 # Number of full cycles in the running_frames

# Generate running animation for each frame
for frame_offset in range(running_frames):
    frame = 1 + frame_offset
    t = (frame_offset / running_frames) * (2 * math.pi * cycle_speed_factor)
    
    # Torso bob
    torso_loc_z = 0.02 * math.sin(t) + 0.02
    add_keyframe_data('torso', frame, loc=(0, 0, torso_loc_z))

    # Legs: alternate swing
    leg_right_rot_x = -leg_swing_angle * math.cos(t)
    leg_left_rot_x = leg_swing_angle * math.cos(t)
    add_keyframe_data('leg_right', frame, rot=(leg_right_rot_x, 0, 0))
    add_keyframe_data('leg_left', frame, rot=(leg_left_rot_x, 0, 0))

    # Hands (arms): opposite to legs
    hand_right_rot_x = arm_swing_angle * math.cos(t)
    hand_left_rot_x = -arm_swing_angle * math.cos(t)
    add_keyframe_data('hand_righ', frame, rot=(hand_right_rot_x, 0, 0))
    add_keyframe_data('hand_left', frame, rot=(hand_left_rot_x, 0, 0))

    # Head tilt
    head_rot_x = head_tilt_angle * math.sin(t * 0.5)
    add_keyframe_data('head', frame, rot=(head_rot_x, 0, 0))
    
    # Default scale for all bones during running
    for bone_name in ["torso", "head", "hand_righ", "hand_left", "leg_right", "leg_left"]:
        add_keyframe_data(bone_name, frame, scale=(1, 1, 1))

# --- Jumping Animation Data (From jump_start_frame onwards) ---

# Torso (Z is global, X rotation is local bend)
add_keyframe_data('torso', jump_start_frame,      loc=(0,0,0),    rot=(math.radians(5),0,0))
add_keyframe_data('torso', jump_start_frame + 6,  loc=(0,0,-0.2), rot=(math.radians(25),0,0))
add_keyframe_data('torso', jump_start_frame + 9,  loc=(0,0,0.5),  rot=(math.radians(-10),0,0))
add_keyframe_data('torso', jump_start_frame + 16, loc=(0,0,0.9),  rot=(0,0,0))
add_keyframe_data('torso', jump_start_frame + 23, loc=(0,0,-0.1), rot=(math.radians(20),0,0))
add_keyframe_data('torso', jump_start_frame + 29, loc=(0,0,0),    rot=(0,0,0))

# Legs (symmetric for jump)
add_keyframe_data('leg_right', jump_start_frame,      rot=(math.radians(20),0,0))
add_keyframe_data('leg_left', jump_start_frame,       rot=(math.radians(20),0,0))
add_keyframe_data('leg_right', jump_start_frame + 6,  rot=(math.radians(70),0,0))
add_keyframe_data('leg_left', jump_start_frame + 6,   rot=(math.radians(70),0,0))
add_keyframe_data('leg_right', jump_start_frame + 9,  rot=(math.radians(-10),0,0))
add_keyframe_data('leg_left', jump_start_frame + 9,   rot=(math.radians(-10),0,0))
add_keyframe_data('leg_right', jump_start_frame + 16, rot=(math.radians(10),0,0))
add_keyframe_data('leg_left', jump_start_frame + 16,  rot=(math.radians(10),0,0))
add_keyframe_data('leg_right', jump_start_frame + 23, rot=(math.radians(60),0,0))
add_keyframe_data('leg_left', jump_start_frame + 23,  rot=(math.radians(60),0,0))
add_keyframe_data('leg_right', jump_start_frame + 29, rot=(0,0,0))
add_keyframe_data('leg_left', jump_start_frame + 29,  rot=(0,0,0))

# Hands (symmetric for jump)
add_keyframe_data('hand_righ', jump_start_frame,      rot=(math.radians(-10),0,0))
add_keyframe_data('hand_left', jump_start_frame,      rot=(math.radians(-10),0,0))
add_keyframe_data('hand_righ', jump_start_frame + 6,  rot=(math.radians(-30),0,0))
add_keyframe_data('hand_left', jump_start_frame + 6,  rot=(math.radians(-30),0,0))
add_keyframe_data('hand_righ', jump_start_frame + 9,  rot=(math.radians(30),0,0))
add_keyframe_data('hand_left', jump_start_frame + 9,  rot=(math.radians(30),0,0))
add_keyframe_data('hand_righ', jump_start_frame + 16, rot=(math.radians(15),0,0))
add_keyframe_data('hand_left', jump_start_frame + 16, rot=(math.radians(15),0,0))
add_keyframe_data('hand_righ', jump_start_frame + 23, rot=(math.radians(-20),0,0))
add_keyframe_data('hand_left', jump_start_frame + 23, rot=(math.radians(-20),0,0))
add_keyframe_data('hand_righ', jump_start_frame + 29, rot=(0,0,0))
add_keyframe_data('hand_left', jump_start_frame + 29, rot=(0,0,0))

# Head
add_keyframe_data('head', jump_start_frame,      rot=(math.radians(5),0,0))
add_keyframe_data('head', jump_start_frame + 6,  rot=(math.radians(15),0,0))
add_keyframe_data('head', jump_start_frame + 9,  rot=(math.radians(-5),0,0))
add_keyframe_data('head', jump_start_frame + 16, rot=(0,0,0))
add_keyframe_data('head', jump_start_frame + 23, rot=(math.radians(10),0,0))
add_keyframe_data('head', jump_start_frame + 29, rot=(0,0,0))

# Calculate max_frame from actual data
max_frame = 0
for bone_name, data in animation_data.items():
    for transform_type in data:
        if data[transform_type]:
            max_frame = max(max_frame, max(data[transform_type].keys()))

# Ensure all bones have scale (1,1,1) if not explicitly set for a frame.
for bone_name, data in animation_data.items():
    all_frames_for_bone = set()
    for transform_type in ['location', 'rotation', 'scale']:
        all_frames_for_bone.update(data[transform_type].keys())
    
    for frame in all_frames_for_bone:
        if frame not in data['scale']:
            data['scale'][frame] = (1,1,1)

# --- Apply animation to Blender ---
bpy.context.scene.render.fps = fps

try:
    armature = bpy.data.objects[armature_name]
    if armature.type == 'ARMATURE':
        if armature.animation_data:
            armature.animation_data_clear() # Clears any existing action on the armature

        for bone_name, data in animation_data.items():
            if bone_name in armature.pose.bones:
                pb = armature.pose.bones[bone_name]

                # No need to clear animation data on individual pose bones
                # as armature.animation_data_clear() handles it.
                # PoseBone objects in 2.80 do not have an 'animation_data' attribute.

                pb.rotation_mode = 'XYZ'

                frames_in_order = sorted(set(list(data['location'].keys()) + list(data['rotation'].keys()) + list(data['scale'].keys())))
                
                for frame in frames_in_order:
                    bpy.context.scene.frame_set(frame)

                    if frame in data['location']:
                        pb.location = data['location'][frame]
                        pb.keyframe_insert(data_path="location", index=-1)

                    if frame in data['rotation']:
                        pb.rotation_euler = data['rotation'][frame]
                        pb.keyframe_insert(data_path="rotation_euler", index=-1)

                    if frame in data['scale']:
                        pb.scale = data['scale'][frame]
                        pb.keyframe_insert(data_path="scale", index=-1)
            else:
                pass # Bone not found in armature, as per rule F.

    else:
        pass # Object is not an armature, as per rule F.

except KeyError:
    pass # Armature object not found, as per rule F.

# Set frame range and current frame
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = max_frame
bpy.context.scene.frame_current = 1
