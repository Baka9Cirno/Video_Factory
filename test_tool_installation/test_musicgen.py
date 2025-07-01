from transformers import pipeline
import scipy

# https://huggingface.co/facebook/musicgen-large   huggingface 网站
# https://github.com/facebookresearch/audiocraft   github 网站

if __name__ == "__main__":

    synthesiser = pipeline("text-to-audio", "../models/MusicGen-Large")

    music = synthesiser("lo-fi music with a soothing melody", forward_params={"do_sample": True})

    scipy.io.wavfile.write("./results/musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])