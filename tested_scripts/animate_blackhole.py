import bpy
import math
import mathutils
import random

# --- Animation Setup ---

# Ensure scene uses Cycles
bpy.context.scene.render.engine = 'CYCLES'

# Enable motion blur (Cycles)
bpy.context.scene.render.use_motion_blur = True

# Frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 500

# Get objects safely
black_hole = bpy.data.objects.get("BlackHole")
accretion_disk = bpy.data.objects.get("AccretionDisk")
lensing_halo = bpy.data.objects.get("LensingHalo")
camera = bpy.data.objects.get("Camera")
particles_collection = bpy.data.collections.get("BlackHoleParticles")

# --- Animation for AccretionDisk ---
if accretion_disk:
    accretion_disk.rotation_mode = 'XYZ'

    # Initial rotation (lay on XY plane) at frame 0
    accretion_disk.rotation_euler = (math.radians(90), 0.0, 0.0)
    accretion_disk.keyframe_insert(data_path="rotation_euler", frame=0)

    # One full revolution around Z by frame 250
    accretion_disk.rotation_euler.z = math.radians(360)
    accretion_disk.keyframe_insert(data_path="rotation_euler", frame=250)

    # Make rotation constant speed (linear) and loop
    if accretion_disk.animation_data and accretion_disk.animation_data.action:
        for fcurve in accretion_disk.animation_data.action.fcurves:
            if fcurve.data_path == "rotation_euler":
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'LINEAR'
                fcurve.modifiers.new(type='CYCLES')

    # Emission Strength pulsing (keyframe on the input socket)
    if accretion_disk.data.materials and accretion_disk.data.materials[0].use_nodes:
        mat_ad = accretion_disk.data.materials[0]
        nodes = mat_ad.node_tree.nodes

        # Find Emission node
        emission_node = None
        for n in nodes:
            if getattr(n, "type", "") == 'EMISSION':
                emission_node = n
                break

        if emission_node:
            emission_node.name = "AccretionEmission"
            strength_socket = emission_node.inputs[1]  # Strength socket

            # Keyframes on the socket itself
            strength_socket.default_value = 15.0
            strength_socket.keyframe_insert(data_path="default_value", frame=0)

            strength_socket.default_value = 25.0
            strength_socket.keyframe_insert(data_path="default_value", frame=125)

            strength_socket.default_value = 15.0
            strength_socket.keyframe_insert(data_path="default_value", frame=250)

            # Smoothing + looping via fcurves in the node tree action
            ad = mat_ad.node_tree.animation_data
            if ad and ad.action:
                for fcurve in ad.action.fcurves:
                    dp = fcurve.data_path
                    if 'nodes["AccretionEmission"]' in dp and dp.endswith('default_value'):
                        for kp in fcurve.keyframe_points:
                            kp.interpolation = 'BEZIER'
                        fcurve.modifiers.new(type='CYCLES')

# --- Animation for LensingHalo ---
if lensing_halo:
    lensing_halo.scale = (1.5, 1.5, 1.5)
    lensing_halo.keyframe_insert(data_path="scale", frame=0)

    lensing_halo.scale = (1.2, 1.2, 1.2)
    lensing_halo.keyframe_insert(data_path="scale", frame=100)

    lensing_halo.scale = (1.5, 1.5, 1.5)
    lensing_halo.keyframe_insert(data_path="scale", frame=200)

    if lensing_halo.animation_data and lensing_halo.animation_data.action:
        for fcurve in lensing_halo.animation_data.action.fcurves:
            if fcurve.data_path == "scale":
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'BEZIER'
                fcurve.modifiers.new(type='CYCLES')

# --- Animation for GlowingParticles ---
if particles_collection:
    glowing_particles = [obj for obj in particles_collection.objects if obj.name.startswith("GlowingParticle_")]
    for glow in glowing_particles:
        glow.rotation_mode = 'XYZ'

        # Random initial orbit radius and angle
        initial_radius = random.uniform(3.0, 7.0)
        initial_angle = random.uniform(0.0, 2.0 * math.pi)

        # Initial position
        glow.location.x = initial_radius * math.cos(initial_angle)
        glow.location.y = initial_radius * math.sin(initial_angle)
        glow.location.z = random.uniform(-1.0, 1.0)
        glow.keyframe_insert(data_path="location", frame=0)

        # Final position after 500 frames (two full orbits)
        final_angle = initial_angle + (2.0 * math.pi * 2.0)
        glow.location.x = initial_radius * math.cos(final_angle)
        glow.location.y = initial_radius * math.sin(final_angle)
        glow.keyframe_insert(data_path="location", frame=500)

        # Loop linear movement
        if glow.animation_data and glow.animation_data.action:
            for fcurve in glow.animation_data.action.fcurves:
                if fcurve.data_path == "location":
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = 'LINEAR'
                    fcurve.modifiers.new(type='CYCLES')

# --- Animation for Camera ---
if camera:
    camera.location = (0, -15, 8)
    camera.keyframe_insert(data_path="location", frame=0)

    camera.location = (0, -8, 5)
    camera.keyframe_insert(data_path="location", frame=300)

    if camera.animation_data and camera.animation_data.action:
        for fcurve in camera.animation_data.action.fcurves:
            if fcurve.data_path == "location":
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'BEZIER'

    # Camera pointing at origin across frames
    def look_at(obj, target):
        direction = mathutils.Vector(target) - obj.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        obj.rotation_euler = rot_quat.to_euler()

    look_at(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="rotation_euler", frame=0)

    bpy.context.scene.frame_set(300)
    look_at(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="rotation_euler", frame=300)

print("Animations added.")
