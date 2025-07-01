from openai import OpenAI

deepseek_apikey = "sk-3b9a199e38824180a13522ed72c1b3c9"
base_url = "https://api.deepseek.com"
# model = "deepseek-reasoner"
model = "deepseek-chat"

if __name__ == "__main__":

    with open("test_tool_installation/test_openai_api_prompt.txt", "rt", encoding="utf-8") as f:
        prompt = f.readline()

    client = OpenAI(api_key=deepseek_apikey, base_url=base_url)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": """You are a useful assistant. You are an LLM agent who is a professional writer who is good at poem and fairy tale composition. Now you are working in my video content generation company. Here is your workflow: 1. Write a story based on my request. Then save the story as "story.txt".\n 2. select a video style for your story and saved as "video_style.txt".\n 3. Split the story into a short shots, make a comprehensive description to each shot, for each shot, use the AI image generative tool to make an inital image. In addition, detailed description on characters is necessary and you should keep the consistency on character appearance between shots.\n 4. provide an comprehensive action description that characters and items in each shot will take. Use the action description as prompt to make video. In all steps, don't merge shots! describe them one by one! \nThe following is python-style functions you can use to assist your work. In these fuctions do not abbreviate any text, you must provide full-text if the argument type is str.\nFunctions:\n1. Save_Text(filename:str, content:str)  Note: save the text content to filename.txt. Example: Save_Text("1.txt", "I love you")\n2. Make_ShotImage(shot_id:int, prompt:str) Note: Privide the prompt to generate an image, the file will be saved as shot_id.jpg, 3-5 sentences is recommended for the prompt. Example: Make_ShotImage(3, "Sun rise, cartoon style")\n 3. Make_ShotVideo(shot_id:int, prompt:str) Note: video generator will convert shot_id.jpg to a video shot_id.mp4, based on the prompt you give to it. This fuction works better if you gives actions description to characters and items. Example: Make_ShotVideo(5, "Rapid river with silver currents. A chubby beaver in a waistcoat scowls on a log. Doge tilts head, paw raised."). To use these tools use the following format:\n'''python\nFunctionName(...)\n'''\nOnce you use a tool, stop and waiting for system's return."""},
            {"role": "user", "content": """Here is my requests: Make a video, the content is the famous poem: \"The Net to Catch the Moon\"."""},
        ],
        stream=False,
        max_tokens=8000
    )

    # print(response)

    # print(response.choices)
    # print(len(response.choices))
    if model == "deepseek-reasoner":
        print("\n\n============Reasoning=============")
        print(response.choices[0].message.reasoning_content)
    print("\n\n============Content=============")
    print(response.choices[0].message.content)


    if model == "deepseek-reasoner":
        with open("test_tool_installation/test_openai_api_reasoning_output.txt", "wt", encoding="utf-8") as f:
            f.write(response.choices[0].message.reasoning_content)
    with open("test_tool_installation/test_openai_api_output.txt", "wt", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)

    print("\n\n============Usage=============")
    print(response.usage)
    