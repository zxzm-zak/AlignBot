def LM(self, prompt):
        response = openai.Completion.create(
            model=self.cfg['model'], 
            prompt=prompt, 
            max_tokens=self.cfg['max_tokens'], 
            temperature=self.cfg['temperature'], 
            stop=self.cfg['stop'], 
            logprobs=self.cfg['logprobs'], 
            frequency_penalty=self.cfg['frequency_penalty']
        )
        return response, response["choices"][0]["text"].strip()


def get_current_state_prompt(self):
    current_state_prompt = self.prompt_text['current_state_prompt']
    objs  = self.prompt_text['objs']
    state, asserts = current_state_prompt = current_state_prompt.split('\n\n')
    state = state.split(',')
    state = "You see: " +  ', '.join([i.strip() for i in state if any(element in i for element in objs)])
    current_state_prompt = f"{state}\n\n{asserts}"
    return current_state_prompt


def get_robot_state(self):
        robot_state = {
            "joint_angles": [0, 0, 0, 0, 0, 0],
            "gripper_state": "open",
            "end_effector_position": [0.5, 0.0, 0.5]
        }
        return robot_state

def clear_exec_hist(self):
        self.exec_hist = ''


def run_execution(plan):
    pass