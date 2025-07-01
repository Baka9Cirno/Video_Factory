import PIL.Image
import PIL.ImageOps
import torch, PIL
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

image = PIL.Image.open("./test_tool_installation/results/flux_dev_result_5.png")
image = PIL.ImageOps.exif_transpose(image) # Some image is 90d transposed
image = image.convert("RGB")

model_id = "./models/InstructPix2Pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
pipe.to("cuda")
pipe.enable_attention_slicing()
# `image` is an RGB PIL.Image
image = pipe("Remove the wings of the boy on the left", image=image).images[0]
image.save("./test_tool_installation/results/instructpix2pix_result.jpg") 