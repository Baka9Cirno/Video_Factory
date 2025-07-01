
class Round():
    def __init__(self, system_message = None, user_message = None, 
                 assistant_thought = None, assistant_code = None, assistant_observation = None, subscribed_observation = None):
        self.system_message = system_message
        self.user_message = user_message
        self.assistant_thought = assistant_thought
        self.assistant_code = assistant_code
        self.assistant_observation = assistant_observation
        self.subscribed_observation = subscribed_observation

    def has_system_message(self):
        if self.system_message is None or self.system_message == "":
            return False
        else:
            return True
    
    def has_user_message(self):
        if self.user_message is None or self.user_message == "":
            return False
        else:
            return True
    
    def has_assistant_thought(self):
        if self.assistant_thought is None or self.assistant_thought == "":
            return False
        else:
            return True
    
    def has_assistant_code(self):
        if self.assistant_code is None or self.assistant_code == "":
            return False
        else:
            return True
    
    def has_assistant_observation(self):
        if self.assistant_observation is None or self.assistant_observation == "":
            return False
        else:
            return True
    
    def has_subscribed_observation(self):
        if self.subscribed_observation is None or self.subscribed_observation == "":
            return False
        else:
            return True
        
    def get_system_message(self):
        return self.system_message
    
    def get_user_message(self):
        return self.user_message
    
    def get_assistant_thought(self):
        return self.assistant_thought
    
    def get_assistant_code(self):
        return self.assistant_code
    
    def get_assistant_observation(self):
        return self.assistant_observation
    
    def set_system_message(self, msg):
        self.system_message = msg
    
    def set_user_message(self, msg):
        self.user_message = msg
    
    def set_assistant_thought(self, msg):
        self.assistant_thought = msg
    
    def set_assistant_code(self, msg):
        self.assistant_code = msg
    
    def set_assistant_observation(self, msg):
        self.assistant_observation = msg

    def set_subscribed_observation(self, msg):
        self.subscribed_observation = msg

    def get_round_message_list(self, omit_code=False, omit_str="The code has run successfully, so omitted.", get_subscribed_observation=False): 
        retval = []

        if self.has_system_message():
            retval.append({"role": "system", "content": self.system_message})

        if self.has_user_message():
            retval.append({"role": "user", "content": self.user_message})
        
        if self.has_assistant_thought() or self.has_assistant_code() or self.has_assistant_observation():
            assistant_message = ""
            if self.has_assistant_thought():
                assistant_message += "Thought:" + self.assistant_thought
            if self.has_assistant_code():
                if omit_code:
                    assistant_message += "Code:\n '''Python\n" + omit_str + "\n'''\n"
                else:
                    assistant_message += "Code:\n '''Python\n" + self.assistant_code + "\n'''\n"
            if self.has_assistant_observation():
                assistant_message += "Observation: " + self.assistant_observation
                if self.has_subscribed_observation() and get_subscribed_observation:
                    assistant_message += "\n" + self.subscribed_observation
            retval.append({"role": "assistant", "content": assistant_message})

        return retval
    
    def __str__(self):
        retval = ""
        if self.has_system_message():
            retval += "======== System Message ========\n"
            retval += str({"role": "system", "content": self.system_message})
        if self.has_user_message():
            retval += "\n======== User Message ========\n"
            retval += str({"role": "system", "content": self.system_message})
        if self.has_assistant_thought() or self.has_assistant_code() or self.has_assistant_observation():
            retval += "\n======== Assistant Message ========\n"
            if self.has_assistant_thought():
                retval += "Thought: " + self.assistant_thought
            if self.has_assistant_code():
                retval += "Code:\n '''Python\n" + self.assistant_code + "\n'''\n"
            if self.has_assistant_observation():
                retval += "Observation: " + self.assistant_observation
                if self.has_subscribed_observation():
                    retval += "\n" + self.subscribed_observation + "\n"
            
        return retval
    

def print_rounds_to_user(rounds:list, print_sys_msg:bool=False):
    for i, round in enumerate(rounds):
        print("<<<<<<<<<< Round %d >>>>>>>>>>" % i+1)
        if print_sys_msg:
            if round.has_system_message():
                print("======== System Message ========")
                print(round.get_system_message)
                print("======== End of System Message ========")

        if round.has_user_message():
            print("======== User Message ========")
            print(round.get_user_message())
            print("======== End of User Message ========")

        if round.has_assistant_thought() or round.has_assistant_code() or round.has_assistant_observation():
            print("======== Assistant Message ========")
            if round.has_assistant_thought():
                print("Thought:\n", sep="")
                print(round.get_assistant_thought())
            if round.has_assistant_code():
                print("Code:\n'''Python")
                print(round.get_assistant_code())
                print("'''")
            if round.has_assistant_observation():
                print("Observation:\n")
                print(round.get_assistant_observation())
                if round.has_subscribed_observation():
                    print(round.get_subscribed_observation())
            print("======== End of Assistant Message ========")
        print(">>>>>>>> End of Round %d <<<<<<<<" % i+1)
        