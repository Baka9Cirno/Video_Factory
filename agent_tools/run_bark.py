import argparse, os
from transformers import AutoProcessor, BarkModel, pipeline
import numpy as np
import scipy, torch

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import soundfile as sf
import numpy as np

if __name__ == "__main__":

    args = argparse.ArgumentParser("run_bark")
    args.add_argument("--save_as", type=str, default="./workspace/audio/debug_bark_voice.wav")
    args.add_argument("--content", type=str, default="The moon whispers secrets to the night, Stars gleam with dreams in softest light.")
    # args.add_argument("--content", type=str, default="月光轻洒，夜色如诗，星辰闪烁，梦境依稀。")
    options = args.parse_args()

    save_as = options.save_as
    content = options.content

    # Github version
    # device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # synthesiser = pipeline("text-to-speech", "./models/bark/bark-small", device=device)
    # speech = synthesiser(content, forward_params={"do_sample": True})

    # audio_data = speech['audio'].flatten()
    # sampling_rate = speech['sampling_rate']
    # audio_data_int16 = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
    # sf.write(save_as, audio_data_int16, sampling_rate)

    # 加载 bark-small 模型和处理器
    processor = AutoProcessor.from_pretrained("./models/bark/bark-small")
    model = BarkModel.from_pretrained("./models/bark/bark-small")

    # 输入文本和指定的 voice-preset
    voice_preset = "./models/bark/bark-small/assets/prompts/v2/en_speaker_1" # woman = 9

    # 处理输入
    inputs = processor(content, voice_preset=voice_preset, return_tensors="pt")

    # 生成音频
    with torch.no_grad():
        audio_array = model.generate(**inputs, do_sample=True)

    audio_array = audio_array.cpu().numpy().squeeze()

    sample_rate = model.generation_config.sample_rate
    write_wav(save_as, rate=sample_rate, data=audio_array)
    
