from transformers import pipeline

# Initialize the text-to-speech pipeline
synthesiser = pipeline("text-to-speech", model="../models/bark/bark-small")

# Generate speech from text
speech = synthesiser("你好啊， If you are looking for our text-to-music models ，请告诉我。", forward_params={"do_sample": True})

# Check the structure of the speech object
import soundfile as sf
import numpy as np

# 提取音频数据和采样率
audio_data = speech['audio'].flatten()
sampling_rate = speech['sampling_rate']

# 将音频数据转换为16位整数
audio_data_int16 = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

# 保存为.wav文件
sf.write("./results/debug_bark.wav", audio_data_int16, sampling_rate)

print("音频已保存为 output.wav")
