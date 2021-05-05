import csv


def to_tuple(string):
    ret = []
    string = string.replace('[','').replace(']','').replace(' ',',')
    for item in string.split(','):
        if item != '':
            ret.append(float(item))
    return tuple(ret)


class Episode:

    def __init__(self):
        self.steps = []

    def append(self, reward=0., state=(), action=0, done=False):
        step = {'reward': reward,
                'state': state,
                'action': action,
                'done': done}
        self.steps.append(step)

    def num_steps(self):
        return len(self.steps)-1


class OfflineEnvironment:

    def __init__(self):
        self.episodes = []
        self.running_episode = None
        self.current_state = ()
        self.next_action = 0
        self.current_step = {}

    def num_steps(self):
        steps = 0
        for episode in self.episodes:
            steps += episode.num_steps()
        return steps

    def load_cvs(self, filename):
        with open(filename, 'r') as csvfile:
            env_data = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for row in env_data:
                if row[0] == 'START':
                    current_episode = Episode()
                    current_episode.append(state=to_tuple(row[1]), action=int(row[2]))
                elif row[2] == 'END':
                    current_episode.append(reward=float(row[0]), state=to_tuple(row[1]), done=True)
                    self.episodes.append(current_episode)
                else:
                    current_episode.append(reward=float(row[0]), state=to_tuple(row[1]), action=int(row[2]))

    def reset(self):
        self.running_episode = self.episodes.pop(0)

        step = self.running_episode.steps.pop(0)

        self.current_state = step['state']
        self.next_action = step['action']

        return self.current_state

    def get_current_action(self):
        return self.next_action

    def step(self, _):

        step = self.running_episode.steps.pop(0)
        reward = step['reward']
        done = step['done']
        next_state = step['state']
        self.next_action = step['action']

        return next_state, reward, done, {}


if __name__ == '__main__':
    env = OfflineEnvironment()
    env.load_cvs('./example.csv')
    print(len(env.episodes))