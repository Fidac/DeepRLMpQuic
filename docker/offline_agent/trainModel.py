import sys

from offlineEnvironment import OfflineEnvironment
from agentModel import generate_agent

env = OfflineEnvironment()
env.load_cvs(sys.argv[1])

nb_steps = env.num_steps()

dqn = generate_agent(nb_steps)

dqn.fit(env, nb_steps=nb_steps, log_interval=50000)

dqn.save_weights("./weights_%s_steps.h5" % nb_steps)