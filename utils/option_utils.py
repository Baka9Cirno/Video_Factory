

# Save current options
def save_options(options, file_path):
    f = open(file_path, "w")
    for attr, value in vars(options).items():
        line = attr + " " + str(value) + "\n"
        f.write(line)
    f.close()


# load options as dict. Notice that all value are str
def load_options(file_path):
    try:
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
    except:
        raise Exception("Failed to load arguments from file: " + file_path)
    
    options = dict()
    for line in lines:
        attr, value = line.split()
        options[attr] = value
    
    return options


# load options as command list
def load_options_as_commandlist(file_path):
    try:
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
    except:
        raise Exception("Failed to load arguments from file: " + file_path)
    
    cmd_list = []
    for line in lines:
        attr, value = line.split()
        cmd_list.extend([attr, value])
    
    return cmd_list