import os
import subprocess

hunyuanvideo_i2v_path = "./models/HunyuanVideo-I2V"
hunyuanvideo_working_directory = hunyuanvideo_i2v_path
hunyuanvideo_i2v_env = "HunyuanVideo-I2V-Py310"
hunyuanvideo_i2v_env_python = "/data/hdd2/huangguangji/development/python/miniconda/envs/HunyuanVideo-I2V-Py310/bin/python3"

source_image = "../../test_tool_installation/resources/1.png"
result_path = "../../test_tool_installation/results"

prompt = "The silver compass in the boy's hands begins to glow brighter, casting moving light patterns on his face and the autumn leaves around him. His eyes dart around with growing excitement as he turns the compass slowly. Morning mist swirls subtly between the village houses in the background."


def compose_hunyuanvideo_i2v_commandlist(prompt:str, image_path:str, save_path:str, i2v_resolution:str="720p", 
                                     infer_steps=50, video_length=129, flow_shift=7.0, seed=0, 
                                     embedded_cfg_scale=6.0, use_cpu_offload=True) -> list:

    command = ["python3", "sample_image2video.py"]
    command.extend(["--model", "HYVideo-T/2"])
    command.extend(["--prompt", prompt])
    command.extend(["--i2v-mode"])
    command.extend(["--i2v-image-path", image_path])
    command.extend(["--i2v-resolution", i2v_resolution])
    command.extend(["--video-size", "1280", "720"])
    command.extend(["--i2v-stability"])
    command.extend(["--infer-steps", str(infer_steps)])
    command.extend(["--video-length", str(video_length)])
    command.extend(["--flow-reverse"])
    command.extend(["--flow-shift", str(flow_shift)])
    command.extend(["--seed", str(seed)])
    command.extend(["--embedded-cfg-scale", str(embedded_cfg_scale)])
    if use_cpu_offload:
        command.extend(["--use-cpu-offload"])
    command.extend(["--save-path", save_path])

    return command


def run_with_conda_run(target_env, commandlist:list, working_dir:str=".", cuda_visible_devices:str=None):
    try:
        if cuda_visible_devices is not None:
            commandlist = ["export", "CUDA_VISIBLE_DEVICES="+cuda_visible_devices, "&&"] + commandlist
        command = subprocess.list2cmdline(commandlist)
        result = subprocess.run(["conda", "run", "-n", target_env, "bash", "-c", command], cwd=working_dir, # cwd: Working directory
                                capture_output=True,
                                text=True,
                                check=False) # If check==True, when error occurs, throw exception rather than change the return code.
            
        if result.returncode == 0:
            print("stdout")
            print(result.stdout)
            return result.stdout
        else:
            print("error")
            print(result.stderr)
            return None
    except Exception as e:
        print(f"error: \n{str(e)}")
        return None


if __name__ == "__main__":
    hunyuanvideo_i2v_commandlist = compose_hunyuanvideo_i2v_commandlist(prompt, source_image, result_path)
    retval = run_with_conda_run(target_env=hunyuanvideo_i2v_env, commandlist=hunyuanvideo_i2v_commandlist,
                                working_dir=hunyuanvideo_working_directory, cuda_visible_devices="1")
    if retval is not None:
        print("Success")