import os, argparse
from transformers import pipeline
import scipy

# https://huggingface.co/facebook/musicgen-large   huggingface 网站
# https://github.com/facebookresearch/audiocraft   github 网站

if __name__ == "__main__":
    args = argparse.ArgumentParser("run_music_gen")
    args.add_argument("--save_as", type=str, default="./workspace/audio/musicgen_bgm.wav")
    args.add_argument("--prompt", type=str, default="melodic, nostalgic atmosphere that stands out")
    options = args.parse_args()

    save_as = options.save_as
    prompt = options.prompt

    try:
        synthesiser = pipeline("text-to-audio", "./models/MusicGen-Large", device="cuda:0")
        music = synthesiser(prompt, forward_params={"do_sample": True})
        scipy.io.wavfile.write(save_as, rate=music["sampling_rate"], data=music["audio"])
    except Exception as e:
        raise(f"Internal error: {str(e)}")
