import sys, os, math

from moviepy import AudioFileClip, VideoFileClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, concatenate_audioclips
from moviepy.video.fx import MultiplySpeed, CrossFadeIn, CrossFadeOut
from utils.option_utils import load_options


# Video and Audio Editing

# Redirect print because VideoFileClip is noisy
class SuppressOutput():
    def __init__(self, file_name=os.devnull):
        self.file = open(file_name, 'w')
        self.original_stdout = sys.stdout
        # self.original_stderr = sys.stderr

    def __enter__(self):
        sys.stdout = self.file
        # sys.stderr = self.file

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.original_stdout
        # sys.stderr = self.original_stderr
        self.file.close()


def composite_audio_and_video(audio_file:str, video_file:str, result_video:str, is_voice:bool=False):
    options = load_options("./current_options.txt")
    workspace_audio_dir = options["workspace_dir"] + "/audio/"
    workspace_video_dir = options["workspace_dir"] + "/video/"
    tmp_m4a = workspace_audio_dir + "tmp.m4a"

    audio_file = os.path.join(workspace_audio_dir, audio_file)
    video_file = os.path.join(workspace_video_dir, video_file)
    result_video = os.path.join(workspace_video_dir, result_video)

    if not os.path.exists(audio_file):
        raise Exception(f"<tool system>: Failed to find audio: {audio_file}.")
    if not os.path.exists(video_file):
        raise Exception(f"<tool system>: Failed to find video: {video_file}.")
    
    try:
        with SuppressOutput():
            audio_clip = AudioFileClip(audio_file)
            video_clip = VideoFileClip(video_file)

        if is_voice:
            if video_clip.duration < audio_clip.duration:
                audio_clip = audio_clip.with_volume_scaled(1.2)
                video_clip = video_clip.with_effects([MultiplySpeed(final_duration=audio_clip.duration)])
        else: # is bgm
            if video_clip.duration > audio_clip.duration:
                audio_clip = audio_clip.with_volume_scaled(0.6)
                repeated_audio_clips = [audio_clip] * math.ceil(video_clip.duration / audio_clip.duration)
                audio_clip = concatenate_audioclips(repeated_audio_clips)
    
        # If there is already a audio clip in the video
        if video_clip.audio:
            original_audio_clip = video_clip.audio
            mixed_audio = CompositeAudioClip([original_audio_clip, audio_clip])
        else:
            mixed_audio = audio_clip

        final_video = video_clip.with_audio(mixed_audio)
        # video_clip.write_videofile(result_video, codec="libx264", audio_codec="aac",)
        final_video.write_videofile(result_video, codec="libx264", audio_codec="aac", temp_audiofile = tmp_m4a, write_logfile=False, logger=None)

        audio_clip.close()
        video_clip.close()
        mixed_audio.close()
        final_video.close()
    
    except Exception as e:
        e_str = str(e)
        raise Exception(f"<tool system>: Internal Error, Failed to add audio: {audio_file} to video: {video_file}! Internal Stderr: {e_str}")


def concatenate_videos(videos:list, result:str):
    options = load_options("./current_options.txt")
    workspace_video_dir = options["workspace_dir"] + "/video/"
    tmp_m4a = options["workspace_dir"] + "/audio/tmp.m4a"

    fade_duration = 1.0

    for i in range(len(videos)):
        videos[i] = os.path.join(workspace_video_dir, videos[i])
    result = os.path.join(workspace_video_dir, result)

    try:
        video_clips = []
        with SuppressOutput():
            for video in videos:
                video_clips.append(VideoFileClip(video))

            clip_ends = []
            clip_begins = []
            for i in range(len(video_clips)):
                video_clip = video_clips[i]
                clip_begin = video_clip.subclipped(0, fade_duration/2.0)
                audio_begin = clip_begin.audio.with_start(fade_duration/2.0)
                clip_middle = video_clip.subclipped(fade_duration/2.0, video_clip.duration-fade_duration/2.0)
                clip_end = video_clip.subclipped(video_clip.duration-fade_duration/2.0, video_clip.duration)
                audio_end = clip_end.audio.with_start(video_clip.duration)
                clip_begin = clip_begin.with_effects([MultiplySpeed(final_duration=fade_duration)])
                clip_begin = clip_begin.with_audio(audio_begin)
                clip_end = clip_end.with_effects([MultiplySpeed(final_duration=fade_duration)])
                clip_end = clip_end.with_audio(audio_end)
                video_clip = concatenate_videoclips([clip_begin, clip_middle, clip_end])
                video_clips[i] = video_clip

            next_start_time = 0.0
            for i in range(len(video_clips)):
                video_clips[i] = video_clips[i].with_start(next_start_time)
                next_start_time += (video_clips[i].duration - fade_duration)

            for i in range(len(video_clips)):
                effects = []
                if i > 0:
                    effects.append(CrossFadeIn(fade_duration))
                if i < len(video_clips) - 1:
                    effects.append(CrossFadeOut(fade_duration))
                video_clips[i].with_effects(effects)
            
            composite_video_clip = CompositeVideoClip(video_clips)

        final_clip = composite_video_clip

        with SuppressOutput():
            final_clip.write_videofile(result, codec="libx264", audio_codec="aac", temp_audiofile = tmp_m4a, write_logfile=False, logger=None)
    except Exception as e:
        e_str = str(e)
        e = Exception(f"<tool system>: Internal Error, Failed to concatenate videos. Internal Stderr: {e_str}")
        raise e