import argparse

def get_argparse(name="video_factory"):
    parser = argparse.ArgumentParser(name)

    # Logs
    parser.add_argument("--log_dir", type=str, default="./logs")

    # Agent Workspace
    parser.add_argument("--workspace_dir", type=str, default="./workspace")

    # Agent Hyper-parameters
    parser.add_argument("--max_rounds", type=int, default=40, help="The maxinum number of rounds for ReAct cycles that the agent can operate.")

    # OpenAI API Agent Configuration
    parser.add_argument("--openai_base_url", type=str, default="https://api.deepseek.com")
    parser.add_argument("--openai_token", type=str,default="sk-")
    parser.add_argument("--openai_model_name", type=str, default="deepseek-chat")
    parser.add_argument("--openai_model_max_tokens", type=int, default="8192")
    parser.add_argument("--openai_max_retries", type=int, default=3)

    # AliCloud Bailian API Configuration
    parser.add_argument("--aliapi_base_url", type=str, default="https://dashscope.aliyuncs.com/compatible-mode/v1")
    parser.add_argument("--aliapi_key", type=str, default="sk-a4d90996d4f840818474ad180f866fff")

    # Baidu API Configuration
    parser.add_argument("--baiduapi_app_id", type=str, default='0')
    parser.add_argument("--baiduapi_key", type=str, default='0')
    parser.add_argument("--baiduapi_secret_key", type=str, default='BshG4BoANJumUG4W43CffJ5JLbKYJisb')

    # Prompts
    parser.add_argument("--init_system_prompt", type=str, default="./prompts/init_system_prompt_with_omnigen_no_code.txt")
    parser.add_argument("--init_user_prompt_beginning", type=str, default="./prompts/init_user_prompt_prefix.txt")
    parser.add_argument("--init_user_prompt_ending", type=str, default="./prompts/init_user_prompt_surfix.txt")

    # Environments - RTX6000x8
    # parser.add_argument("--agent_env", type=str, default="/data/hdd/huangguangji/.conda/envs/Agent-Py312", help="Path to agent conda environment.")
    # parser.add_argument("--flux1_dev_env", type=str, default="/data/hdd/huangguangji/.conda/envs/Diffusers-Py312", help="Path to the conda environment of FLUX.1 dev.")
    # parser.add_argument("--omnigen_env", type=str, default="/data/hdd/huangguangji/.conda/envs/OmniGen-Py312", help="Path to the conda environment of OmniGen.")
    # parser.add_argument("--hunyuanvideo_i2v_env", type=str, default="/data/hdd/huangguangji/.conda/envs/HunyuanVideo-I2V-Py310", help="Path to the conda environment of HunyuanVideo-I2V.")

    # Environments - RTX6000x6
    parser.add_argument("--agent_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/Agent-Py312", help="Path to agent conda environment.")
    parser.add_argument("--flux1_dev_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/Diffusers-Py312", help="Path to the conda environment of FLUX.1 dev.")
    parser.add_argument("--omnigen_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/OmniGen-Py312", help="Path to the conda environment of OmniGen.")    
    parser.add_argument("--hunyuanvideo_i2v_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/HunyuanVideo-I2V-Py310", help="Path to the conda environment of HunyuanVideo-I2V.")
    parser.add_argument("--music_gen_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/MusicGen-Py39", help="Path to the conda environment of MusicGen.")
    parser.add_argument("--baiduapi_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/BaiduAPI-Py37", help="Path to the conda environment of BaiduAPI.")
    parser.add_argument("--bark_env", type=str, default="/data/hdd2/huangguangji/development/python/miniconda/envs/Bark-Py39", help="Path to the conda environment of Bark.")
    
    # Tool Overall Settings
    parser.add_argument("--video_height", type=int, default=720)
    parser.add_argument("--video_width", type=int, default=1280)
    parser.add_argument("--video_resolution", type=str, default="720p", help="video resolution: 720p or 360p")

    # Tool - FLUX.1 dev``
    # parser.add_argument("--flux1_img_h", type=int, default=1024)
    # parser.add_argument("--flux1_img_w", type=int, default=1024)
    parser.add_argument("--flux1_img_h", type=int, default=720)
    parser.add_argument("--flux1_img_w", type=int, default=1280)

    # Tool - OmniGen
    parser.add_argument("--omnigen_h", type=int, default=720)
    parser.add_argument("--omnigen_w", type=int, default=1280)

    # Tool - HunyuanVideo-I2V
    parser.add_argument("--hunyuanvideo_i2v_dir", type=str, default="./models/HunyuanVideo-I2V")

    # Hardware Info
    parser.add_argument("--max_cuda_devices", type=int, default=6, help="How many devices can be utlized when using parallel image/video generation.")

    args = parser.parse_args()
    return args
