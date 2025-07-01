import subprocess


# Add this when saving a python file
python_file_prefix = '''from agent_tools.tools import *\nimport json\n\n'''


def save_agent_python(code:str, filepath:str):
    file_content = python_file_prefix + code
    try:
        f = open(filepath, "wt")
        f.write(file_content)
    except Exception as e:
        print("Failed in writing agent python action code to file:" + filepath)
    else:
        f.close()


class CondaRun_Result():
    def __init__(self, has_error:bool, stdout:str = "", stderr:str = ""):
        self.has_error = has_error
        self.stdout = stdout
        self.stderr = stderr
    
    def __str__(self):
        if self.has_error:
            return self.stderr
        else:
            return self.stdout


# Run python in another conda environment
def run_with_conda_run(target_env:str, commandlist:list, working_dir:str=".", cuda_visible_devices:str=None): # cuda_visible_devices:str=None means all devices
    try:
        if cuda_visible_devices is not None:
            commandlist = ["export", "CUDA_VISIBLE_DEVICES="+cuda_visible_devices, "&&"] + commandlist
        command = subprocess.list2cmdline(commandlist)
        result = subprocess.run(["conda", "run", "-p", target_env, "bash", "-c", command], cwd=working_dir, # cwd: Working directory
                                capture_output=True,
                                text=True,
                                check=False) # If check==True, when error occurs, throw exception rather than change the return code.
    except Exception as e:
        retval = CondaRun_Result(has_error=True, stderr=str(e))
    else:
        if result.returncode == 0:
            retval = CondaRun_Result(has_error=False, stdout=result.stdout)
        else:
            retval = CondaRun_Result(has_error=True, stdout=result.stdout, stderr=result.stderr)

    return retval


# Run python file : return (obervation, has_error:bool)
def run_agent_python(filepath:str, target_env:str, working_dir="."):
    command_list = ["python3", filepath]
    result = run_with_conda_run(target_env, command_list, working_dir)
    
    if result.has_error:
        return "Existing stdout before failure: " + result.stdout + "\nPython failure: " + result.stderr, True
    else:
        return result.stdout, False


######## Debug Only #########
if __name__ == "__main__":
    code = '''story = """Once upon a time, in a small village nestled at the foot of a great mountain, lived a curious boy named Leo. One sunny afternoon, Leo decided to explore the mountain trails despite his mother's warnings. As he wandered deeper into the woods, the sun began to set, and Leo realized he was lost.

As darkness fell, Leo sat under a tree, frightened and alone. Suddenly, a kind-eyed rabbit hopped near him. "You look lost, little one," said the rabbit. "Follow me." The rabbit led Leo to a clearing where other animals had gathered - a wise old owl, a gentle deer, and a playful squirrel.

The owl hooted, "We shall help you find your way home." The deer offered to carry Leo on her back, while the squirrel ran ahead to scout the path. The rabbit kept Leo company, telling him stories to keep his spirits up.

Through the night, the animal friends guided Leo safely down the mountain. At dawn, they reached the village outskirts. "Thank you, my friends!" Leo cried as he hugged each animal. From that day on, Leo became the village's protector of animals, always remembering their kindness when he needed help the most."""

Save_Text("story.txt", story)
print("Story saved successfully!")
'''

    save_agent_python(code, "./agent_python_code.py")
