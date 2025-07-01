import os, sys, shutil, logging
from openai import OpenAI

import config as config
from utils.load_prompt import *
from utils.python_code_utils import *
from utils.option_utils import *
from utils.round import *
from utils.logger import *

AGENT_PYTHON_CODE = "agent_python_code.py"


def init_workspace_dir(workspace_dir:str="./workspace"):
    shutil.rmtree(workspace_dir, ignore_errors=True)
    os.mkdir(workspace_dir)
    os.mkdir(workspace_dir + "/audio")
    os.mkdir(workspace_dir + "/extra")
    os.mkdir(workspace_dir + "/final_video")
    os.mkdir(workspace_dir + "/image")
    os.mkdir(workspace_dir + "/temp")
    os.mkdir(workspace_dir + "/text")
    os.mkdir(workspace_dir + "/video")
    return


# Extract the thought and code field (end with \n).
def get_thought_and_code(text:str):
    thought = ""
    code = ""

    lines = text.strip().split("\n")

    # Extract thought field
    is_thought = False
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("Thought:"):
            is_thought = True
            line = line.replace("Thought:", "", 1).strip()
        if line.startswith("Code:") or line.startswith("Observation:"):
            break
        if is_thought:
            thought += (line + "\n")
    
    # Extract code field
    is_code = False
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("```py") or line.startswith("```PY") or line.startswith("```Py"): # It is `, not ascii '
            is_code = True
            continue
        elif line.startswith("```"): # It is `, not ascii '
            break
        if is_code:
            line = lines[i]
            if line.strip() != "":
                code += (line + "\n")

    return thought, code


if __name__ == "__main__":

    # Loading
    options = config.get_argparse()
    save_options(options, "./current_options.txt")

    # Make workspace dir
    init_workspace_dir(options.workspace_dir)

    # Init Logger
    llm_api_logger, agent_logger = get_loggers(options.log_dir)
    
    # Initialise openai-api client
    client = OpenAI(api_key=options.openai_token, base_url=options.openai_base_url)

    # Initial Round
    user_request = input("Your request: ")
    # user_request = "Make a fairy tale video that begins with an Eskimo little girl lost the way home on the mountain."
    # user_request = "以唐诗 村居 为题 制作少儿教育视频，展现诗歌的内容和意境。使用3d动画风格。"`
    # user_request = "Make a fairy tale video base on this story: There are many small animals living in the animal forest, and they all live happily and happily. But one day, the big tiger, which has always been fierce, came to this forest. The tiger threatens to eat a small animal every day. This scared all the critters. So the critters hurriedly gathered for an emergency meeting."
    # user_request = "Make a fary tale video based this story, in this story Lily is the only protagonist: Lily, a 13-year-old girl, ventures into the mountains to pick wildflowers for her grandmother. As she wanders deeper into the forest, she loses her way. The sun sets, and the forest grows dark and erie. Suddenly, she meets Whiskers the Fox, who offers to guide her. Along the way, Thumper the Rabbit helps her find berries to eat. When a storm hits, Shadow the Wolf appears, scaring Lily at first. But he leads her to a cave for shelter. The next morning, the animals work together to show Lily the path home. Grateful, Lily promises to always protect the forest and its creatures. She returns home safely, her heart full of new friendships."
    # user_request = "Make a video of FlintStone, a story of cavemans. The video style is american cartooon style. For exising materials, we have main characters Fred (man) and Wilma (woman) and their reference images are "Fred.png" and "Wilma.png", with corresponded desciption "Fred_Description.txt" and "Wilma_Description.txt". And here is the shot proposal for this story: 1. Wilma stands in the middle of house, waiting for Fred with a tray of food and drinks. 2. Fred walks into his house. 3. Fred\'s little pet ran down from the armchair. 4. Fred sat on the armchair and then watch the stone made television and eats food.  Let’s think step by step and generate the video step by step. Now Begin!"

    init_system_message = load_prompt(options.init_system_prompt)
    init_user_message = load_prompt(options.init_user_prompt_beginning) + ' ' + user_request + ' ' + load_prompt(options.init_user_prompt_ending)

    session_rounds = []
    init_round = Round(system_message=init_system_message, user_message=init_user_message)
    session_rounds.append(init_round)

    # Begin ReAct Cycle!
    sum_prompt_tokens = 0
    sum_completion_tokens = 0
    sum_total_tokens = 0
    last_round_code_field_has_error = False
    for round_idx in range(options.max_rounds):
        print("<<<<<< Round %d Begin >>>>>>" %(round_idx+1))

        # Create message to send to LLM
        message_2_llm = []

        for i, round in enumerate(session_rounds):
            message_2_llm.extend(round.get_round_message_list(omit_code=True, omit_str="(truncated)"))
            if i == len(session_rounds) - 1 and last_round_code_field_has_error:
                message_2_llm.extend(round.get_round_message_list(omit_code=False))
        
        if last_round_code_field_has_error and round_idx > 0:
            session_rounds = session_rounds[:-1]

        llm_api_logger.log(logging.INFO, f"\n<<<<<< Round {round_idx+1} >>>>>>\nSent message:\n{message_2_llm}\n")

        # Get response
        has_response = False
        for i in range(options.openai_max_retries):
            response = client.chat.completions.create(
                model=options.openai_model_name,
                messages=message_2_llm,
                stream=False,
                max_tokens=8192
            )
            if not response.choices[0].message.content:
                print("OpenAI API failed! Retrying.")
            else:
                has_response = True
                break
        if not has_response:
            raise Exception("ERROR: OpenAI API service is not available now!")
        
        
        # Log response
        content = response.choices[0].message.content
        sum_completion_tokens += response.usage.completion_tokens
        sum_prompt_tokens += response.usage.prompt_tokens
        sum_total_tokens += response.usage.total_tokens
        response.usage.prompt_tokens, response.usage.total_tokens
        llm_api_logger.log(logging.INFO, f"\nReceived message:\n{content}\n")
        llm_api_logger.log(logging.INFO, f"\nUsage: Round {round_idx+1}:\nprompt tokens: {response.usage.prompt_tokens}\ncompetion tokens: {response.usage.completion_tokens}\ntotal tokens: {response.usage.total_tokens}" + f"\nOverall Usage:\nprompt tokens: {sum_prompt_tokens}\ncompetion tokens: {sum_completion_tokens}\ntotal tokens: {sum_total_tokens}" )
        thought, code = get_thought_and_code(text=content)

        if thought:
            print("Thought:\n" + thought)
        if code:
            print("Code:\n'''Python\n" + code + "'''\n")

        # Operate action
        save_agent_python(code, AGENT_PYTHON_CODE)
        run_result, last_round_code_field_has_error = run_agent_python(AGENT_PYTHON_CODE, options.agent_env, working_dir=".")

        # Temporarily set obervation as run retval
        observation = run_result

        if observation:
            print(f"Observation:\n{observation}\n")

        # Save as history

        if round_idx == 0:
            session_rounds[round_idx].set_assistant_thought(thought)
            session_rounds[round_idx].set_assistant_code(code)
            session_rounds[round_idx].set_assistant_observation(observation)
        else:
            new_round = Round(assistant_thought=thought, assistant_code=code, assistant_observation=observation)
            session_rounds.append(new_round)

        # Log to agent.log
        try:
            agent_logger.log(logging.INFO, f"\n<<<<<< Round {round_idx+1} >>>>>>\n" + str(session_rounds[round_idx]))
        except:
            pass
        
        if observation.count("<STOP-AGENT>") > 0:
            print("--------- Task Finished! ---------")
            break