import sys,pygame
from SARSA import SARSA
class RLManager:
    def __init__:
RL_init() --> task_specification
agent_init(env_init())
This initializes everything, passing the environment’s task spec to the agent. This should be called
at the beginning of every trial.
    def start(self):
        o= env.start()
        a= agent.start(observation)
        self.nextAction = a
        return o, a
    def step():
        r, o, terminal = env.step(self.nextAction)
        if terminal:
            agent.end(r)
            return r, o, terminal
        else:
            a = agent.step(r, 0)
            self.nextAction = a
        return r, o, terminal, a

RL_episode(steps) --> terminal
num_steps = 0
o, a = RL_start()
num_steps = num_steps + 1
list = [o, a]
while o != terminal_observation
if(steps !=0 and num_steps >= steps)
return 0
else
r, o, a = RL_step()
list = list + [r, o, a]
num_steps = num_steps + 1
agent_end(r)
return 1
    
