import os, argparse
import torch
from diffusers import FluxPipeline

# Script to run flux

if __name__ == "__main__":

    args = argparse.ArgumentParser("run_flux1_dev")
    args.add_argument("--save_as", type=str, default="./workspace/images/test.png")
    args.add_argument("--prompt", type=str, default="Sun rises between mountains, cartoon style.")
    args.add_argument("--height", type=int, default=1024)
    args.add_argument("--width", type=int, default=1024)
    args.add_argument("--guidance_scale", type=float, default=3.5)
    args.add_argument("--num_inference_steps", type=int, default=50)
    args.add_argument("--max_sequence_length", type=int, default=512)

    options = args.parse_args()

    pipe = FluxPipeline.from_pretrained("./models/FLUX1/checkpoints/FLUX1-dev", torch_dtype=torch.bfloat16)
    # pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power
    pipe.to("cuda")
    # pipe.to("cuda:0") # cpu_offload conflict to selecting a specific card

    prompt = options.prompt

    image = pipe(
        prompt="", prompt_2=options.prompt, # prompt_2 means using T5 encoder, prompt means CLIP encoder
        height=options.height,
        width=options.width,
        guidance_scale=5, # 1-7 recommend to be 2.4-4
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(204)
    ).images[0]

    image.save(options.save_as)
    # image.save("./test_tool_installation/results/flux_dev_result_-1.png")

