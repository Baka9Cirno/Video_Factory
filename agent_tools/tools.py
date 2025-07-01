import os, sys, shutil, subprocess, math
import torch

from utils.option_utils import load_options
from utils.python_code_utils import run_with_conda_run
from utils.video_editing import *
from utils.simple_utils import list_filenames
from moviepy import AudioFileClip, VideoFileClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, concatenate_audioclips
from moviepy.video.fx import MultiplySpeed, CrossFadeIn, CrossFadeOut

######## Callable functions for Agent #########
# Save Text File
def save_textfile(filename:str, text:str):
    options = load_options("./current_options.txt")
    workspace_text_dir = options["workspace_dir"] + "/text/"
    filepath = workspace_text_dir + filename
    f = open(filepath, "w", encoding="utf-8")
    f.write(str(text))
    f.close()
    print("<tool system>: Text file:", filename, "is saved!")
    return


# Load Text File
def load_textfile(filename:str):
    options = load_options("./current_options.txt")
    workspace_text_dir = options["workspace_dir"] + "/text/"
    filenpath = workspace_text_dir + filename
    f = open(filenpath, "r", encoding="utf-8")
    txt = f.read()
    return txt


# Read Text File and put the text to observation
def observe_textfile(filename:str):
    try:
        options = load_options("./current_options.txt")
        workspace_text_dir = options["workspace_dir"] + "/text/"
        filepath = workspace_text_dir + filename
        f = open(filepath, "r", encoding="utf-8")
        txt = f.read()
        print("<tool system>: The content of", filename, "is:", txt)
    except:
        raise Exception(f"<tool system>: Cannot find {filename}.")
    return


# List all files
def observe_assets():
    options = load_options("./current_options.txt")
    workspace_text_dir = options["workspace_dir"] + "/text/"
    workspace_image_dir = options["workspace_dir"] + "/image/"
    workspace_audio_dir = options["workspace_dir"] + "/text/"
    workspace_video_dir = options["workspace_dir"] + "/image/"
    text_files = list_filenames(workspace_text_dir)
    image_files = list_filenames(workspace_image_dir)
    audio_files = list_filenames(workspace_audio_dir)
    video_files = list_filenames(workspace_video_dir)
    print("<tool system> We have the following assets:")
    print(f"- Text Files: {str(text_files)}")
    print(f"- Image Files: {str(image_files)}")
    print(f"- Audio Files: {str(audio_files)}")
    print(f"- Video Files: {str(video_files)}")
    return


# Image Generation
def generate_image(image_filename:str, prompt:str):
    if not image_filename.endswith(".png"):
        raise Exception("<tool system>: Faild to create image: " + image_filename + ". Currently only .png file is supported!")
    
    options = load_options("./current_options.txt")
    target_env = options["flux1_dev_env"]
    workspace_image_dir = options["workspace_dir"] + "/image/"
    save_path = workspace_image_dir + image_filename
    # image_height = options["flux1_img_h"]
    # image_width = options["flux1_img_w"]
    image_height = options["video_height"]
    image_width = options["video_width"]

    commandlist = ["python3", "./agent_tools/run_flux1_dev.py"]
    # print(commandlist, save_path)
    commandlist.extend(["--save_as", save_path])
    commandlist.extend(["--prompt", prompt])
    commandlist.extend(["--height", image_height]) # image_height is a str here
    commandlist.extend(["--width", image_width]) # image_width is a str here
    result = run_with_conda_run(target_env, commandlist, ".")
    
    if result.has_error:
        raise Exception("<tool system>: Faild to generated image: " + image_filename + "." + "stderr:" + result.stderr) # raise internal conda run error info
        # raise Exception("<tool system>: Faild to generated image: " + image_filename + ".")
    else:
        print("<tool system>: Image: " + image_filename + " has been generated!")
    return


# Image Generation in parallel
def generate_images_in_parallel(image_filenames:list, prompts:list):
    if not image_filenames or not isinstance(image_filenames, list):
        raise Exception("<tool system>: Faild to create image. image_filenames is not a list of filenames or is an empty list!")
    elif not prompts or not isinstance(prompts, list):
        raise Exception("<tool system>: Faild to create image. prompts is not a list of prompt strings or is an empty list!")
    elif len(image_filenames) != len(prompts):
        raise Exception("<tool system>: The length of image_filenames and prompts dosen't match!")
    
    options = load_options("./current_options.txt")
    target_env = options["flux1_dev_env"]
    max_cuda_devices = int(options["max_cuda_devices"])
    # image_height = options["flux1_img_h"]
    # image_width = options["flux1_img_w"]
    image_height = options["video_height"]
    image_width = options["video_width"]

    workspace_image_dir = options["workspace_dir"] + "/image/"

    # Run subprocess in parallel
    num_required_images = len(image_filenames)
    num_generated_images = 0
    while num_generated_images < num_required_images:
        num_processes = min(max_cuda_devices, num_required_images-num_generated_images)
        processes = [None] * num_processes
        for i in range(num_processes):
            image_filename = image_filenames[num_generated_images + i]
            save_path = workspace_image_dir + image_filename
            prompt = prompts[num_generated_images + i]

            commandlist = ["export", "CUDA_VISIBLE_DEVICES="+str(i), "&&"]
            commandlist.extend(["python3", "./agent_tools/run_flux1_dev.py"])
            commandlist.extend(["--save_as", save_path])
            commandlist.extend(["--prompt", prompt])
            commandlist.extend(["--height", image_height]) # image_height is a str here
            commandlist.extend(["--width", image_width]) # image_width is a str here
            command = subprocess.list2cmdline(commandlist)

            processes[i] = subprocess.Popen(["conda", "run", "-p", target_env, "bash", "-c", command], 
                                            cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        for i in range(num_processes):
            stdout, stderror = processes[i].communicate()
            if processes[i].returncode != 0:
                raise Exception("<tool system>: Cannot generate image:", image_filenames[num_generated_images + i], "Stderr: " + stderror.decode())
                # raise Exception("<tool system>: Cannot generate image:", image_filenames[i])
            else:
                print("<tool system>: Image: " + image_filenames[num_generated_images + i] + " has been generated!")
                
        num_generated_images += num_processes
    return

# Image Generation
def generate_image_from_reference_image(ref_filename:str, prompt:str, result_filename:str):
    if not ref_filename.endswith(".png"):
        raise Exception("<tool system>: File format error: " + result_filename + ". Currently only .png file is supported!")
    
    options = load_options("./current_options.txt")
    target_env = options["omnigen_env"]
    workspace_image_dir = options["workspace_dir"] + "/image/"
    ref_path = workspace_image_dir + ref_filename
    save_path = workspace_image_dir + result_filename
    # image_height = options["omnigen_h"]
    # image_width = options["omnigen_w"]
    image_height = options["omnigen_h"]
    image_width = options["omnigen_w"]

    if not os.path.exists(ref_path):
        raise Exception("<tool system>: Faild to find image: " + result_filename + ".")
    
    prompt = prompt.replace("<image>", "<img><|image_1|></img>")

    commandlist = ["python3", "./agent_tools/run_omnigen.py"]
    # print(commandlist, save_path)
    commandlist.extend(["--save_as", save_path])
    commandlist.extend(["--prompt", prompt])
    commandlist.extend(["--ref_image", ref_path])
    commandlist.extend(["--height", image_height]) # image_height is a str here
    commandlist.extend(["--width", image_width]) # image_width is a str here
    result = run_with_conda_run(target_env, commandlist, ".")
    
    if result.has_error:
        raise Exception("<tool system>: Faild to generated image: " + result_filename + "." + "stderr:" + result.stderr) # raise internal conda run error info
        # raise Exception("<tool system>: Faild to generated image: " + image_filename + ".")
    else:
        print("<tool system>: Image: " + result_filename + " has been generated!")
    return
            

# Video Generation
def generate_video_i2v(ref_image_filename:str, video_filename:str, prompt:str):
    if not ref_image_filename.endswith(".png"):
        raise Exception("<tool system>: Faild to load shot image: " + ref_image_filename + ". Currently only .png file is supported!")
    if not video_filename.endswith(".mp4"):
        raise Exception("<tool system>: Faild to create video: " + video_filename + ". Currently only .mp4 file is supported!")

    options = load_options("./current_options.txt")

    # ref_image => generate result xxx.mp4 in temp folder => rename xxx.mp4 by <shot_id>.mp4 and move to workspace_video_dir 

    target_env = options["hunyuanvideo_i2v_env"]
    working_dir = options["hunyuanvideo_i2v_dir"]
    workspace_image_dir = options["workspace_dir"] + "/image/"
    ref_image_path = workspace_image_dir + ref_image_filename
    relative_ref_image_path_from_working_dir = os.path.relpath(ref_image_path, working_dir)
    workspace_temp_dir = options["workspace_dir"] + "/temp/"
    relative_result_temp_dir_from_working_dir = os.path.relpath(workspace_temp_dir, working_dir)
    workspace_video_dir = options["workspace_dir"] + "/video/"
    result_video_path = workspace_video_dir + video_filename

    video_height = options["video_height"] # str
    video_width = options["video_width"] # str
    video_resolution = options["video_resolution"]

    prompt = prompt.replace("<image>", "")

    # Using single GPU
    # commandlist = ["export", "CUDA_VISIBLE_DEVICES="+str(4), "&&"]
    # commandlist.extend(["python3", "sample_image2video.py"])
    commandlist = ["python3", "sample_image2video.py"]
    # print(commandlist, save_path)
    commandlist.extend(["--model", "HYVideo-T/2"])
    commandlist.extend(["--prompt", prompt])
    commandlist.extend(["--i2v-mode"])
    commandlist.extend(["--i2v-image-path", relative_ref_image_path_from_working_dir])
    commandlist.extend(["--i2v-resolution", video_resolution])
    commandlist.extend(["--video-size", video_width, video_height])
    commandlist.extend(["--i2v-stability"])
    commandlist.extend(["--infer-steps", "50"])
    commandlist.extend(["--video-length", "129"])
    commandlist.extend(["--flow-reverse"])
    commandlist.extend(["--flow-shift", "13.0"])
    commandlist.extend(["--seed", "204"])
    commandlist.extend(["--embedded-cfg-scale", "6.0"])
    commandlist.extend(["--use-cpu-offload"])
    commandlist.extend(["--save-path", relative_result_temp_dir_from_working_dir])

    shutil.rmtree(workspace_temp_dir, ignore_errors=True)
    os.mkdir(workspace_temp_dir)
    result = run_with_conda_run(target_env, commandlist, working_dir)

    if result.has_error:
        raise Exception("<tool system>: Faild to create shot video: " + video_filename + "." + "stderr:" + result.stderr)
        # raise Exception("<tool system>: Faild to create shot video: " + video_filename + ".") # raise internal conda run error info
    else:
        files = os.listdir(workspace_temp_dir)
        videofile = None
        for f in files:
            if f.endswith(".mp4"):
                videofile = f
                break
        shutil.move(workspace_temp_dir + videofile, result_video_path)
        print("<tool system>: Video: " + video_filename + " has been generated!")
    shutil.rmtree(workspace_temp_dir, ignore_errors=True)
    os.mkdir(workspace_temp_dir)
    return


# Video Generation in parallel
def generate_videos_i2v_in_parallel(ref_image_filenames:str, video_filenames:str, prompts:str):
    if not ref_image_filenames or not isinstance(ref_image_filenames, list):
        raise Exception("<tool system>: Faild to create image. ref_image_filenames is not a list of filenames or is an empty list!")
    elif not video_filenames or not isinstance(video_filenames, list):
        raise Exception("<tool system>: Faild to create image. video_filenames is not a list of prompt strings or is an empty list!")
    elif not prompts or not isinstance(prompts, list):
        raise Exception("<tool system>: Faild to create image. prompts is not a list of prompt strings or is an empty list!")
    elif len(ref_image_filenames) != len(video_filenames) or len(ref_image_filenames) != len(prompts):
        raise Exception("<tool system>: The length of ref_image_filenames and video_filenames and prompts dosen't match!")
    
    for i in range(len(prompts)):
        prompt = prompt.replace("<image>", "")

    options = load_options("./current_options.txt")
    video_height = options["video_height"] # str
    video_width = options["video_width"] # str
    video_resolution = options["video_resolution"] # str like 720p

    # ref_image => generate result xxx.mp4 in temp folder => rename xxx.mp4 by <shot_id>.mp4 and move to workspace_video_dir 
    target_env = options["hunyuanvideo_i2v_env"]
    working_dir = options["hunyuanvideo_i2v_dir"]
    workspace_image_dir = options["workspace_dir"] + "/image/"
    workspace_temp_dir = options["workspace_dir"] + "/temp/"
    workspace_video_dir = options["workspace_dir"] + "/video/"

    max_cuda_devices = int(options["max_cuda_devices"])

    # Run subprocess in parallel
    shutil.rmtree(workspace_temp_dir, ignore_errors=True)
    os.mkdir(workspace_temp_dir)
    num_required_videos = len(video_filenames)
    num_generated_videos = 0
    while num_generated_videos < num_required_videos:
        num_processes = min(max_cuda_devices, num_required_videos-num_generated_videos)
        processes = [None] * num_processes
        for i in range(num_processes):
            prompt = prompts[num_generated_videos + i]
            ref_image_filename = ref_image_filenames[num_generated_videos + i]
            ref_image_path = workspace_image_dir + ref_image_filename
            relative_ref_image_path_from_working_dir = os.path.relpath(ref_image_path, working_dir)
            process_temp_dir = workspace_temp_dir + str(i) + "/"
            relative_process_temp_dir_from_working_dir = os.path.relpath(process_temp_dir, working_dir)

            commandlist = ["export", "CUDA_VISIBLE_DEVICES="+str(i), "&&"]
            # commandlist.extend(["python3", "run_debug.py" "&&"])
            commandlist.extend(["python3", "sample_image2video.py"])
            commandlist.extend(["--model", "HYVideo-T/2"])
            commandlist.extend(["--prompt", prompt])
            commandlist.extend(["--i2v-mode"])
            commandlist.extend(["--i2v-image-path", relative_ref_image_path_from_working_dir])
            commandlist.extend(["--i2v-resolution", video_resolution])
            commandlist.extend(["--video-size", video_width, video_height])
            commandlist.extend(["--i2v-stability"])
            commandlist.extend(["--infer-steps", "50"])
            commandlist.extend(["--video-length", "129"])
            commandlist.extend(["--flow-reverse"])
            commandlist.extend(["--flow-shift", "7.0"]) # 7-17
            commandlist.extend(["--seed", "204"])
            commandlist.extend(["--embedded-cfg-scale", "6.0"])
            commandlist.extend(["--use-cpu-offload"])
            commandlist.extend(["--save-path", relative_process_temp_dir_from_working_dir])
            command = subprocess.list2cmdline(commandlist)

            shutil.rmtree(process_temp_dir, ignore_errors=True)
            os.mkdir(process_temp_dir)
            processes[i] = subprocess.Popen(["conda", "run", "-p", target_env, "bash", "-c", command], 
                                            cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        for i in range(num_processes):
            process_temp_dir = workspace_temp_dir + str(i) + "/"
            video_filename = video_filenames[num_generated_videos + i]
            result_video_path = workspace_video_dir + video_filename

            stdout, stderror = processes[i].communicate()
            if processes[i].returncode != 0:
                raise Exception("<tool system>: Cannot generate video:", video_filenames[num_generated_videos + i], "Stderr: " + stderror.decode())
                # raise Exception("<tool system>: Cannot generate video:", video_filenames[num_generated_videos + i])
            else:
                files = os.listdir(process_temp_dir)
                videofile = None
                for f in files:
                    if f.endswith(".mp4"):
                        videofile = f
                        break
                shutil.move(process_temp_dir + videofile, result_video_path)
                shutil.rmtree(process_temp_dir, ignore_errors=True)
                os.mkdir(process_temp_dir)
                print("<tool system>: Video: " + video_filename + " has been generated!")

        num_generated_videos += num_processes

    return


# Generate human voice using Bark model
def generate_voice(content:str, audio_file:str, language:str="en"):
    if language not in ["en", "zh"]:
        raise Exception(f"Unsupported language: {language}")
    
    options = load_options("./current_options.txt")
    workspace_audio_dir = options["workspace_dir"] + "/audio/"
    audio_filepath = os.path.join(workspace_audio_dir, audio_file)
    
    if language == "en":
        target_env = options["bark_env"]
        commandlist = ["python3", "./agent_tools/run_bark.py"]
        commandlist.extend(["--save_as", audio_filepath])
        commandlist.extend(["--content", content])
    else:
        target_env = options["baiduapi_env"]
        commandlist = ["python3", "./agent_tools/run_baidu_sound.py"]
        commandlist.extend(["--save_as", audio_filepath])
        commandlist.extend(["--content", content])
    
    options = load_options("./current_options.txt")
    workspace_audio_dir = options["workspace_dir"] + "/audio/"
    audio_filepath = os.path.join(workspace_audio_dir, audio_file)

    result = run_with_conda_run(target_env, commandlist, ".")
    
    if result.has_error:
        raise Exception(f"<tool system>: Failed to generate voice: {audio_file}. stderr: {result.stderr}" ) # raise internal conda run error info
        # raise Exception("<tool system>: Faild to generate voice: " + image_filename + ".")
    else:
        print("<tool system>: Voice: " + audio_file + " has been generated!")
    return


# Background Music Generation
def generate_instrumental_music(audio_file:str, prompt:str):
    options = load_options("./current_options.txt")
    workspace_audio_dir = options["workspace_dir"] + "/audio/"
    audio_file = os.path.join(workspace_audio_dir, audio_file)
    
    target_env = options["music_gen_env"]
    commandlist = ["python3", "./agent_tools/run_music_gen.py"]
    commandlist.extend(["--save_as", audio_file])
    commandlist.extend(["--prompt", prompt])
    result = run_with_conda_run(target_env, commandlist, ".")
    
    if result.has_error:
        raise Exception(f"<tool system>: Failed to generate music: {audio_file}. stderr: {result.stderr}" ) # raise internal conda run error info
        # raise Exception("<tool system>: Faild to generated image: " + image_filename + ".")
    else:
        print("<tool system>: Music: " + audio_file + " has been generated!")
    return


def concatenate_final_video(videos:list, voices:list, bgm:str, result:str):    
    if not videos:
        raise Exception("<tool system>: concatenate_final_video failed: videos is empty.")
    if voices:
        for i in range(len(videos)):
            video = videos[i]
            voice = voices[i] 
            composite_audio_and_video(voice, video, "tmp"+str(i)+".mp4", True)
    else:
        for i in range(len(videos)):
            video = videos[i]
            shutil.copy(video, "tmp"+str(i)+".mp4")
    
    tmp_videos = []
    for i in range(len(videos)):
        tmp_videos.append("tmp"+str(i)+".mp4")
    if bgm:
        concatenate_videos(tmp_videos, "no_bgm_result.mp4")
        composite_audio_and_video(bgm, "no_bgm_result.mp4", result, False)
    else:
        concatenate_videos(tmp_videos, result)
    
    print(f"<tool system>: Final video {result} have been generated!")


def upload_final_video(video_filename:str):
    options = load_options("./current_options.txt")
    workspace_video_dir = options["workspace_dir"] + "/video/"
    final_dir = options["workspace_dir"] + "/final_video/"
    video_filepath = os.path.join(workspace_video_dir, video_filename)

    if os.path.exists(video_filepath):
        if video_filename.endswith(".mp4"):
            shutil.move(video_filepath,  final_dir)
            print("Final Video Uploaded!")
        else:
            raise Exception(f"<tool system>: {video_filename} is not a valid file format!")
    else:
        raise Exception(f"<tool system>: {video_filename} is not found!")


def final_answer(answer):
    answer = str(answer)
    print("<tool system>: The answer: \"", answer, "\" has been sent to user!")
    print("<STOP-AGENT>")
    return

