from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyAZ4ONtz2pgQSuXzblNoT5xL3KT-o4ebaQ")
sys_instruction = (
    "You are an assistant specialized in generating Blender Python (`bpy`) scripts from 3D model descriptions.",
    "Your task is to take a user prompt describing a 3D object or scene and output clean, modular, and executable Python code using the Blender API (`bpy`) compatible with Blender 2.80.",
    "Guidelines:",
    "1. Always produce **valid Python code** that runs inside Blender 2.80’s scripting editor.",
    "2. Use **bpy.ops** and **bpy.data** methods to create meshes, modifiers, materials, lights, and cameras as needed.",
    "3. Structure the code in a **step-by-step, modular way**:",
    "- Define objects (meshes, curves, modifiers).",
    "- Apply transformations using `location` and `rotation` in the operator call.",
    "- Apply `scale` only after object creation via `object.scale = (...)`.",
    "- For thickness/extrusion, prefer modifiers (e.g., Solidify) instead of edit-mode extrude operators.",
    "- Add materials using `use_nodes=True`. For simple colors, set Principled BSDF Base Color. For emissive/glowing surfaces, use a ShaderNodeEmission connected to the Material Output.",
    "- Set up animation or rigging if requested.",
    "4. Include **comments** in the code explaining each major step.",
    "5. Ensure the output is **self-contained** (no external dependencies beyond Blender’s built-in API).",
    "6. Do not use operators that require UI context (e.g., `bpy.ops.wm.revert_mainfile`, or delete with unsupported parameters).",
    "7. If the user prompt is ambiguous, make reasonable assumptions but keep the design simple and editable.",
    "8. Output only the Python code block, no extra text.",
    "Example workflow:",
    "- Input: 'A cartoon-style sunflower with a green stem and yellow petals.'",
    "- Output: Python code using `bpy` that creates a stem (cylinder), petals (scaled planes or extruded meshes), and a center (sphere), with appropriate node-based materials (Principled BSDF for stem, Emission shader for glowing petals if requested).",
    "Your role:",
    "Convert every user prompt into Blender 2.80-ready Python code that builds the described 3D asset without using unsupported parameters or UI-only operators."
)
code = ""
with open("blackhole.txt" , "r+" , encoding="utf-8") as file:
    code = file.read()

content = (
    "I already created a Blender 2.80 project with these objects:",
    "- BlackHole (central sphere)",
    "- AccretionDisk (torus with emissive material)",
    "- LensingHalo (outer torus with glowing material)",
    "- DustParticle_* (small dark spheres)",
    "- GlowingParticle_* (small emissive spheres)",
    "- Camera (pointing at the origin)",
    f"and i writed this code : \n{code}",
    "Now animate them:",
    "- AccretionDisk should rotate continuously around the black hole, completing one revolution every 250 frames.",
    "- Emission strength of the AccretionDisk should pulse between 15 and 25 in a sinusoidal pattern over time.",
    "- LensingHalo should oscillate its scale between 1.2 and 1.5 over 200 frames.",
    "- GlowingParticles should orbit around the black hole with random speeds, each following a circular path.",
    "- Camera should dolly-in slowly from (0, -15, 8) to (0, -8, 5) over 300 frames.",
    "- Use Cycles render engine with motion blur enabled.",
    "- Output Python code using bpy that adds keyframes for these animations."
)
ris_con = ""
for i in content:
    ris_con += f"\n{i}"

#gemini-2.5-flash-lite
#gemini-2.5-flash
response = client.models.generate_content(
    model="gemini-2.5-flash-lite", 
    config=genai.types.GenerateContentConfig(system_instruction=sys_instruction),
    contents=ris_con
)
print(response.text)


#black hole promt : "Create a highly detailed 3D black hole scene:\n- Central black sphere representing the singularity, perfectly smooth and absorbing all light.\n- Surrounding accretion disk: a glowing, swirling disk of plasma with bright orange, yellow, and red colors, slightly warped as if being pulled by gravity.\n- Add relativistic effects: light bending around the black hole, creating a faint gravitational lensing halo.\n- Include scattered cosmic dust and small glowing particles orbiting around the disk.\n- Background: deep space with subtle stars, pure black environment to emphasize contrast.\n- Lighting: strong emission from the accretion disk, no external light sources, realistic glow illuminating nearby particles.\n- Camera angle: slightly tilted above the disk, showing both the black hole core and the glowing swirl.\n- Style: cinematic, high contrast, physically inspired but artistically enhanced for dramatic effect."