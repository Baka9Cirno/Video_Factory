import os
import torch
from diffusers import FluxPipeline
import random,time

random.seed(time.time())

# os.environ["CUDA_VISIBLE_DEVICES"] = "4"

pipe = FluxPipeline.from_pretrained("./models/FLUX1/checkpoints/FLUX1-dev", torch_dtype=torch.bfloat16)
# pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power
pipe.to("cuda:5") # cpu_offload conflict to selecting a specific card

# prompt = "The ancient Heart Tree pulses with golden light as its bark repairs itself. The forest spirit dances joyfully while the hedgehog naps contentedly on roots. The boy holds a glowing seed carefully in both hands, his face lit with wonder. The tree's hollow seems to form a kind face smiling down at them."

# prompt = "In a photo album, the images are evenly distributed into 3 rows and 2 lines with 6 shots." 
# prompt += "A cheerful cartoon-style little boy, about 8 years old, with big round eyes, a wide smile, and messy hair. He wears a colorful t-shirt, shorts, and sneakers, standing in a playful pose with a bright, whimsical background. "
# prompt += "Top-left, Standing at the entrance of a vibrant forest with towering trees and sparkling vines, the boy points eagerly down a glowing path, his body leaning forward with curiosity. Sunlight filters through the canopy, casting colorful patterns on the ground."
# prompt += "Top-middle, Crouching on a mossy rock beside a winding path, the boy listens intently to a fluffy squirrel perched on a low branch, gesturing animatedly. The forest around them is lush, with oversized flowers and tiny glowing fireflies. "
# prompt += "Top-right, Gripping the ropes of a rickety wooden bridge, the boy takes a cautious step forward, glancing nervously at the bubbling stream below. The forest on both sides is dense, with vines dangling and mist rising from the water. "
# prompt += "Bottom-left, Standing in front of a cave entrance shimmering with colorful crystals, the boy raises a hand to shield his eyes from the bright glow, his other hand resting on his hip confidently. The surrounding forest is dark, with beams of light breaking through the trees. "
# prompt += "Bottom-middle, Kneeling beside an open wooden chest filled with glittering coins and sparkling gems, the boy claps his hands in delight, his face illuminated by the treasure’s glow. The cave walls are rugged, with faint crystal veins sparkling in the background. "
# prompt += "Bottom-right, Walking back along the glowing forest path at sunset, the boy waves happily over his shoulder at a squirrel perched on a tree stump. The sky is painted with warm oranges and pinks, and the forest glows softly behind him."

prompt = "A young anime boy with spiky jet-black hair, large emerald-green eyes, fair skin with freckles, wearing a white t-shirt, blue shorts, and red sneakers, standing confidently with hands on hips, blank background."


image = pipe(
    prompt="", prompt_2=prompt, # prompt_2 != "" means we use T5 encoder, prompt != "" means we use CLIP encoder
    height=640,
    width=960,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cpu").manual_seed(random.randint(0, 10000))
).images[0]

## When we do not use the guidance
# image = pipe(
#     prompt="", prompt_2=prompt, # prompt means using T5 encoder
#     height=1024,
#     width=1024,
#     guidance_scale=0.0,
#     num_inference_steps=30,
#     max_sequence_length=256,
#     generator=torch.Generator("cpu").manual_seed(12)
# ).images[0]

image.save("./test_tool_installation/results/boy.png")

