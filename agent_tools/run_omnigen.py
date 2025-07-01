from OmniGen import OmniGenPipeline
import time, random
import os, argparse


if __name__ == "__main__":
    args = argparse.ArgumentParser("run_music_gen")
    args.add_argument("--save_as", type=str, default="./workspace/audio/musicgen_bgm.wav")
    args.add_argument("--prompt", type=str, default="")
    args.add_argument("--ref_image", type=str, default="./test_tool_installation/resources/boy.png")

    args.add_argument("--height", type=int, default=1024)
    args.add_argument("--width", type=int, default=1024)
    args.add_argument("--guidance_scale", type=float, default=3.5)
    args.add_argument("--img_guidance_scale", type=float, default=1.0)
    args.add_argument("--num_inference_steps", type=int, default=50)
    args.add_argument("--max_sequence_length", type=int, default=512)
    options = args.parse_args()

    random.seed(time.time())

    pipe = OmniGenPipeline.from_pretrained("./models/OmniGen/checkpoint")
    pipe.to("cuda")

    images = pipe(
        prompt=options.prompt,
        input_images=[options.ref_image],
        height=options.height,
        width=options.width,
        guidance_scale=2.5, # 2.5
        img_guidance_scale=1.6, # 1.6
        seed=random.randint(0, 10000),
        offload_model=False
    )

images[0].save(options.save_as)  # save output PIL image