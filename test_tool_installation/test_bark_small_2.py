import torch
import soundfile as sf
import numpy as np
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write as write_wav

# 设置设备（GPU 或 CPU）
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 bark-small 模型和处理器
processor = AutoProcessor.from_pretrained("./models/bark/bark-small")
model = BarkModel.from_pretrained("./models/bark/bark-small")

# 输入文本和指定的 voice-preset
text = "我的狗比你的狗更加可爱"
voice_preset = "./models/bark/bark-small/assets/prompts/v2/zh_speaker_9"

# 处理输入
inputs = processor(text, voice_preset=voice_preset, return_tensors="pt")

# 生成音频
with torch.no_grad():
    audio_array = model.generate(**inputs, do_sample=True)

audio_array = audio_array.cpu().numpy().squeeze()

sample_rate = model.generation_config.sample_rate
write_wav("test_tool_installation/results/debug_bark.wav", rate=sample_rate, data=audio_array)

# # 将音频从 tensor 转换为 numpy 数组


# # 将音频数据转换为16位整数
# audio_data_int16 = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

# # 保存为.wav文件
# sf.write("./results/debug_bark.wav", audio_data_int16, sampling_rate)


# print("音频已生成并保存为 output_audio.wav")