

def load_prompt(file_path:str):
    try:
        f = open(file_path, "r", encoding="utf-8")
        content = f.read()
    except:
        raise FileNotFoundError("Failed to open the prompt file: " + file_path)
    else:
        f.close()
    return content.replace("\n", "\\n")

######## Debug Only ########
if __name__ == "__main__":
    prompt = load_prompt("./prompts/init_system.txt")
    print(prompt)