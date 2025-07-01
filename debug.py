from agent_tools import tools
from utils.option_utils import *
import config
import time

if __name__ == "__main__":
    # Loading and transport options to agent_code working env
    options = config.get_argparse()
    save_options(options, "./current_options.txt")


    ####### Tool Testing ######
    # tools.generate_image("debug_boy.png", "a small child with bright, curious eyes that sparkle like polished emeralds. Their hair is a tousled mop of golden curls, catching sunlight like a halo. Freckles dust their rosy cheeks, and a mischievous grin reveals a single missing tooth. They wear a patched but colorful tunic, with tiny boots scuffed from endless adventures. The image has a white blank background.")
    # tools.generate_image_from_reference_image("debug_boy.png", "A majestic deer with large antlers standing beside the boy <image> as they walk through the forest at dawn. The deer gently nudges her forward while she pets its neck. Sunlight begins to filter through the trees, creating a hopeful atmosphere. In the distance, the rooftops of a village can be seen. The style remains consistent with soft colors and detailed rendering.", "debug_shot1.png")
    # tools.generate_image_from_reference_image("debug_boy.png", "The boy <image> running into the arms of her relieved parents at the edge of the forest at sunrise. Her mother wears an apron and her father has a kind face. The fox, owl and deer watch from the forest edge, smiling. The village houses have thatched roofs and smoke rising from chimneys. The style completes the fairy tale with a warm, happy ending.", "debug_shot2.png")

    # tools.generate_video_i2v("debug_shot1.png", "debug_shot1_s.mp4", "The boy running into the arms of her relieved parents at the edge of the forest at sunrise. Her mother wears an apron and her father has a kind face. The fox, owl and deer watch from the forest edge, smiling. The village houses have thatched roofs and smoke rising from chimneys. The style completes the fairy tale with a warm, happy ending.")
    # tools.generate_video_i2v("debug_shot2.png", "debug_shot2_s.mp4", "The boy running into the arms of her relieved parents at the edge of the forest at sunrise. Her mother wears an apron and her father has a kind face. The fox, owl and deer watch from the forest edge, smiling. The village houses have thatched roofs and smoke rising from chimneys. The style completes the fairy tale with a warm, happy ending.")
    
    tools.generate_videos_i2v_in_parallel(["debug_shot1.png", "debug_shot2.png"], ["debug_shot1.mp4", "debug_shot2.mp4"], ["A majestic deer with large antlers standing beside the boy <image> as they walk through the forest at dawn. The deer gently nudges her forward while she pets its neck. Sunlight begins to filter through the trees, creating a hopeful atmosphere. In the distance, the rooftops of a village can be seen. The style remains consistent with soft colors and detailed rendering.", "The boy running into the arms of her relieved parents at the edge of the forest at sunrise. Her mother wears an apron and her father has a kind face. The fox, owl and deer watch from the forest edge, smiling. The village houses have thatched roofs and smoke rising from chimneys. The style completes the fairy tale with a warm, happy ending."])
    
    # tools.save_text("122.txt", "hello\tworld!")
    # tools.load_text("122.txt")
    # tools.read_text("122.txt")
    # image_names = ["d1.png", "d2.png", "d3.png"]
    # prompts = ["A Sun rise, cyberpunk style.", "A Sun rise, anime style.", "A Sun rise, realistics style."]
    # video_names = ["d1.mp4", "d2.mp4", "d3.mp4"]
    # video_prompt = ["the sun rises up in a slow speed."] * 3
    # tools.generate_images_in_parallel(image_filenames=image_names, prompts=prompts)
    # tools.generate_video_i2v("d1.png", "d1.mp4", "the sun rises up in a slow speed.")
    # tools.generate_video_i2v("d2.png", "d2.mp4", "the sun rises up in a slow speed.")
    # tools.generate_video_i2v("d3.png", "d3.mp4", "the sun rises up in a slow speed.")
    # tools.generate_video_i2v_in_parallel(image_names, video_names, prompts)
    # tools.concatenate_videos(["d1.mp4", "d2.mp4", "d3.mp4"], [], "", "debug_result.mp4")
    # tools.concatenate_videos(["shot_1.mp4", "shot_2.mp4", "shot_3.mp4", "shot_4.mp4", "shot_5.mp4", "shot_6.mp4"], "debug_result.mp4")
    # tools.concatenate_final_video(["shot1.mp4", "shot2.mp4", "shot3.mp4", "shot4.mp4", "shot5.mp4"],
    #                               ["narration_1.wav", "narration_2.wav", "narration_3.wav", "narration_4.wav", "narration_5.wav"],
    #                               "bgm.wav", "final.mp4")

    # tools.generate_voice("The group moves through the forest - the squirrel points ahead with its tiny paw, the deer walks steadily beside Leo, the rabbit hops playfully while talking, and the owl glides silently above. They carefully step across stones in the brook as glowing mushrooms pulse softly.", "debug_voicegen_en.wav", "en")
    # tools.generate_voice("月光轻洒，夜色如诗，星辰闪烁，梦境依稀。风过林梢，悄诉衷肠，天地无声，心绪悠长。", "debug_voicegen_zh.wav", "zh")
    # tools.generate_instrumental_music("debug_gen_music.mp3", "It’s a gentle, flowing piano piece that evokes a sense of calm and introspection, with its delicate melodies and emotional depth.")

    # tools.concatenate_final_video(["shot1.mp4","shot2.mp4","shot3.mp4","shot4.mp4","shot5.mp4"],
    #                               ["narration_1.wav", "narration_2.wav", "narration_3.wav", "narration_4.wav", "narration_5.wav"],
    #                                "bgm.wav", "final.mp4")