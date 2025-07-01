from OmniGen import OmniGenPipeline
import time, random
# import torch
# from diffusers import OmniGenPipeline

random.seed(time.time())

pipe = OmniGenPipeline.from_pretrained("./models/OmniGen/checkpoint")
pipe.to("cuda:4")
# Note: Your local model path is also acceptable, such as 'pipe = OmniGenPipeline.from_pretrained(your_local_model_path)', where all files in your_local_model_path should be organized as https://huggingface.co/Shitao/OmniGen-v1/tree/main

## Text to Image
# images = pipe(
#     prompt="Opening scene of the village at mountain's foot. Leo is a 10-year-old boy with messy brown hair, wearing a red cap and green vest. The village has small wooden houses with smoking chimneys, surrounded by autumn trees.", 
#     height=512, 
#     width=512, 
#     guidance_scale=2.5,
#     seed=204,
#     offload_model=False
# )
# images[0].save("./test_tool_installation/results/onmigen_i2t.png")  # save output PIL Image

## Multi-modal to Image
# In the prompt, we use the placeholder to represent the image. The image placeholder should be in the format of <img><|image_*|></img>
# You can add multiple images in the input_images. Please ensure that each image has its placeholder. For example, for the list input_images [img1_path, img2_path], the prompt needs to have two placeholders: <img><|image_1|></img>, <img><|image_2|></img>.
# images = pipe(
#     prompt="The boy in <img><|image_2|></img> walked towards the black forest, which was filled with the glitter of fireflies. The boy's expression was slightly frightened, and his body curled up slightly.",
#     input_images=["./test_tool_installation/resources/1.png", 
#                   "./test_tool_installation/resources/5.png"],
#     height=512,
#     width=512,
#     guidance_scale=2.5, # 2.5
#     img_guidance_scale=1.6, # 1.6
#     seed=204,
#     offload_model=False
# )
# images[0].save("./test_tool_installation/results/onmigen_tii2i.png")  # save output PIL image

images = pipe(
    prompt="The boy <img><|image_1|></img> in is in the lower left corner, walking towards the front right. He walked towards the black forest, which was filled with the glitter of fireflies. The boy's expression was slightly frightened, and his body curled up slightly.",
    input_images=["./test_tool_installation/resources/1.png"],
    height=720,
    width=720,
    guidance_scale=2.5, # 2.5
    img_guidance_scale=1.6, # 1.6
    seed=random.randint(0, 10000),
    offload_model=False
)
images[0].save("./test_tool_installation/results/onmigen_ti2i.png")  # save output PIL image