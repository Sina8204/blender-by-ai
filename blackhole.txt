import bpy
import math
import mathutils
import random

# --- Clear scene safely ---
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- World setup: pure black background ---
world = bpy.data.worlds.new("BlackHoleWorld")
world.use_nodes = True
nodes_w = world.node_tree.nodes
links_w = world.node_tree.links

# Ensure Background exists
bg_node = nodes_w.get("Background")
if not bg_node:
    bg_node = nodes_w.new(type="ShaderNodeBackground")
output_w = nodes_w.get("World Output")
if not output_w:
    output_w = nodes_w.new(type="ShaderNodeOutputWorld")

bg_node.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
bg_node.inputs["Strength"].default_value = 0.0  # keep space dark
# Connect background to output
# Remove existing links and reconnect
for l in list(links_w):
    links_w.remove(l)
links_w.new(bg_node.outputs["Background"], output_w.inputs["Surface"])

bpy.context.scene.world = world

# --- Black Hole (Singularity) ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=128, ring_count=64, location=(0, 0, 0))
black_hole = bpy.context.object
black_hole.name = "BlackHole"
bpy.ops.object.shade_smooth()

# Material: pure black, no emission
mat_black_hole = bpy.data.materials.new(name="BlackHoleMaterial")
mat_black_hole.use_nodes = True
nodes_bh = mat_black_hole.node_tree.nodes
links_bh = mat_black_hole.node_tree.links

# Clean default nodes
for n in list(nodes_bh):
    nodes_bh.remove(n)

emission_bh = nodes_bh.new(type='ShaderNodeEmission')
emission_bh.inputs['Color'].default_value = (0.0, 0.0, 0.0, 1.0)
emission_bh.inputs['Strength'].default_value = 0.0

output_bh = nodes_bh.new(type="ShaderNodeOutputMaterial")
links_bh.new(emission_bh.outputs['Emission'], output_bh.inputs['Surface'])

black_hole.data.materials.append(mat_black_hole)

# --- Accretion Disk (glowing plasma ring) ---
bpy.ops.mesh.primitive_torus_add(
    major_radius=5.0,
    minor_radius=1.0,
    major_segments=256,
    minor_segments=64,
    location=(0, 0, 0),
    rotation=(math.radians(90), 0.0, 0.0)  # lay on XY plane
)
accretion_disk = bpy.context.object
accretion_disk.name = "AccretionDisk"
bpy.ops.object.shade_smooth()

# Emissive material with noise + color ramp
mat_accretion_disk = bpy.data.materials.new(name="AccretionDiskMaterial")
mat_accretion_disk.use_nodes = True
nodes_ad = mat_accretion_disk.node_tree.nodes
links_ad = mat_accretion_disk.node_tree.links

# Clean default nodes
for n in list(nodes_ad):
    nodes_ad.remove(n)

# Nodes
tex_coord = nodes_ad.new(type='ShaderNodeTexCoord')
mapping = nodes_ad.new(type='ShaderNodeMapping')
mapping.vector_type = 'POINT'

noise = nodes_ad.new(type='ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 5.0
noise.inputs['Detail'].default_value = 8.0
noise.inputs['Distortion'].default_value = 1.5

color_ramp = nodes_ad.new(type='ShaderNodeValToRGB')
# Configure ramp with 3 bands: orange -> yellow -> red
cr = color_ramp.color_ramp
# Ensure exactly 3 elements
while len(cr.elements) > 2:
    cr.elements.remove(cr.elements[-1])
cr.elements[0].position = 0.2
cr.elements[1].position = 0.8
cr.elements[0].color = (1.0, 0.5, 0.0, 1.0)  # Orange
cr.elements[1].color = (0.8, 0.1, 0.0, 1.0)  # Red
# Add middle yellow
mid = cr.elements.new(0.5)
mid.color = (1.0, 0.8, 0.0, 1.0)  # Yellow

emission_ad = nodes_ad.new(type='ShaderNodeEmission')
emission_ad.inputs['Strength'].default_value = 20.0

output_ad = nodes_ad.new(type='ShaderNodeOutputMaterial')

# Links (use Vector → Noise Fac → ColorRamp → Emission Color)
links_ad.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
links_ad.new(mapping.outputs['Vector'], noise.inputs['Vector'])
links_ad.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links_ad.new(color_ramp.outputs['Color'], emission_ad.inputs['Color'])
links_ad.new(emission_ad.outputs['Emission'], output_ad.inputs['Surface'])

accretion_disk.data.materials.append(mat_accretion_disk)

# --- Gravitational Lensing Halo (simple emissive ring) ---
bpy.ops.mesh.primitive_torus_add(
    major_radius=1.5,
    minor_radius=0.35,
    major_segments=128,
    minor_segments=64,
    location=(0, 0, 0),
    rotation=(math.radians(90), 0.0, 0.0)
)
lensing_halo = bpy.context.object
lensing_halo.name = "LensingHalo"
lensing_halo.scale = (1.5, 1.5, 1.5)
bpy.ops.object.shade_smooth()

mat_lensing_halo = bpy.data.materials.new(name="LensingHaloMaterial")
mat_lensing_halo.use_nodes = True
nodes_lh = mat_lensing_halo.node_tree.nodes
links_lh = mat_lensing_halo.node_tree.links

for n in list(nodes_lh):
    nodes_lh.remove(n)

tex_coord_lh = nodes_lh.new(type='ShaderNodeTexCoord')
mapping_lh = nodes_lh.new(type='ShaderNodeMapping')
mapping_lh.vector_type = 'POINT'

gradient_tex_lh = nodes_lh.new(type='ShaderNodeTexGradient')
gradient_tex_lh.gradient_type = 'RADIAL'

color_ramp_lh = nodes_lh.new(type='ShaderNodeValToRGB')
# White center to faint yellow edge
cr_lh = color_ramp_lh.color_ramp
cr_lh.elements[0].position = 0.2
cr_lh.elements[1].position = 0.9
cr_lh.elements[0].color = (1.0, 1.0, 1.0, 1.0)
cr_lh.elements[1].color = (1.0, 0.95, 0.7, 1.0)

emission_lh = nodes_lh.new(type='ShaderNodeEmission')
emission_lh.inputs['Strength'].default_value = 5.0

output_lh = nodes_lh.new(type='ShaderNodeOutputMaterial')

links_lh.new(tex_coord_lh.outputs['Object'], mapping_lh.inputs['Vector'])
links_lh.new(mapping_lh.outputs['Vector'], gradient_tex_lh.inputs['Vector'])
links_lh.new(gradient_tex_lh.outputs['Fac'], color_ramp_lh.inputs['Fac'])
links_lh.new(color_ramp_lh.outputs['Color'], emission_lh.inputs['Color'])
links_lh.new(emission_lh.outputs['Emission'], output_lh.inputs['Surface'])

lensing_halo.data.materials.append(mat_lensing_halo)

# --- Scattered Cosmic Dust and Glowing Particles ---
num_dust_particles = 500
num_glowing_particles = 100

# Base collection (optional)
coll = bpy.data.collections.new("BlackHoleParticles")
bpy.context.scene.collection.children.link(coll)

# Dust particles (dark gray)
for i in range(num_dust_particles):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.02, subdivisions=1, location=(0, 0, 0))
    dust_particle = bpy.context.object
    dust_particle.name = f"DustParticle_{i}"
    # Random placement
    dust_particle.location.x = random.uniform(-10, 10)
    dust_particle.location.y = random.uniform(-10, 10)
    dust_particle.location.z = random.uniform(-5, 5)
    # Move to collection
    for c in dust_particle.users_collection:
        c.objects.unlink(dust_particle)
    coll.objects.link(dust_particle)

    mat_dust = bpy.data.materials.new(name=f"DustMaterial_{i}")
    mat_dust.use_nodes = True
    nodes_dm = mat_dust.node_tree.nodes
    bsdf_dust = nodes_dm.get("Principled BSDF")
    if bsdf_dust:
        bsdf_dust.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)
        bsdf_dust.inputs['Roughness'].default_value = 0.8
    dust_particle.data.materials.append(mat_dust)

# Glowing particles (warm emission)
for i in range(num_glowing_particles):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05, subdivisions=1, location=(0, 0, 0))
    glow = bpy.context.object
    glow.name = f"GlowingParticle_{i}"
    angle = random.uniform(0.0, 2.0 * math.pi)
    radius = random.uniform(3.0, 7.0)
    glow.location.x = radius * math.cos(angle)
    glow.location.y = radius * math.sin(angle)
    glow.location.z = random.uniform(-1.0, 1.0)
    # Move to collection
    for c in glow.users_collection:
        c.objects.unlink(glow)
    coll.objects.link(glow)

    mat_glow = bpy.data.materials.new(name=f"GlowMaterial_{i}")
    mat_glow.use_nodes = True
    nodes_gm = mat_glow.node_tree.nodes
    links_gm = mat_glow.node_tree.links
    for n in list(nodes_gm):
        nodes_gm.remove(n)
    emission_glow = nodes_gm.new(type='ShaderNodeEmission')
    emission_glow.inputs['Color'].default_value = (1.0, 0.6, 0.1, 1.0)
    emission_glow.inputs['Strength'].default_value = 10.0
    output_glow = nodes_gm.new(type='ShaderNodeOutputMaterial')
    links_gm.new(emission_glow.outputs['Emission'], output_glow.inputs['Surface'])
    glow.data.materials.append(mat_glow)

# --- Camera Setup ---
bpy.ops.object.camera_add(location=(0, -15, 8))
camera = bpy.context.object
camera.name = "Camera"
look_at = mathutils.Vector((0, 0, 0))
direction = look_at - camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = camera

print("Black hole scene created.")
