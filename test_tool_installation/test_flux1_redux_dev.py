import torch
from diffusers import FluxPriorReduxPipeline, FluxPipeline
from transformers import CLIPTextModel, CLIPTokenizer, T5EncoderModel, T5TokenizerFast
from diffusers.utils import load_image
import time, random
from PIL import Image

device = "cuda:5"
dtype = torch.bfloat16

flux_model_path = "./models/FLUX1/checkpoints/FLUX1-dev"
redux_model_path = "./models/FLUX1/checkpoints/FLUX1-Redux-dev"
gen_model_path = "./models/FLUX1/checkpoints/FLUX1-dev"

random.seed(time.time())

prompt = "the boy becomes 12 years old with a blue T-shirt and red shorts."
negative_prompt = "blurry, low quality, distorted"

text_encoder = CLIPTextModel.from_pretrained(
    flux_model_path,
    subfolder="text_encoder",
    torch_dtype=dtype,
)
text_encoder_2 = T5EncoderModel.from_pretrained(
    flux_model_path,
    subfolder="text_encoder_2",
    torch_dtype=dtype,
)
tokenizer = CLIPTokenizer.from_pretrained(
    flux_model_path,
    subfolder="tokenizer",
)
tokenizer_2 = T5TokenizerFast.from_pretrained(
    flux_model_path,
    subfolder="tokenizer_2",
)

pipe_prior_redux = FluxPriorReduxPipeline.from_pretrained(redux_model_path,
                                                          text_encoder=text_encoder,
                                                          text_encoder_2=text_encoder_2,
                                                          tokenizer=tokenizer,
                                                          tokenizer_2=tokenizer_2,
                                                          torch_dtype=dtype).to(device)
pipe = FluxPipeline.from_pretrained(
    gen_model_path, 
    torch_dtype=dtype
).to(device)

# 打开图像文件
image = Image.open("./test_tool_installation/resources/boy.png")  # 替换为你的文件路径
# 转换为 RGB 模式
rgb_image = image.convert("RGB")
image = load_image(rgb_image)

pipe_prior_output = pipe_prior_redux(
    image,
    prompt="The boy is in the lower left corner, walking towards the front right walks towards the black forest, which was filled with the glitter of fireflies, the expression was slightly frightened, and his body curled up slightly.",
)

images = pipe(
    guidance_scale=7, # 2.5
    num_inference_steps=75,
    generator=torch.Generator("cpu").manual_seed(random.randint(0, 10000)),
    **pipe_prior_output,
).images
images[0].save("./test_tool_installation/results/flux-dev-redux.png")