from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten

from keras.optimizers import Adam

from rl.policy import BoltzmannQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory
from offlineAgent import OfflineDQNAgent


def generate_model():
    model = Sequential()

    model.add(Flatten(input_shape=(1, 6)))
    model.add(Dense(8))
    model.add(Activation('relu'))
    model.add(Dense(8))
    model.add(Activation('relu'))
    model.add(Dense(2))
    model.add(Activation('linear'))
    print(model.summary())

    return model


def generate_agent(steps=1000):
    memory = SequentialMemory(limit=steps, window_length=1)

    policy = LinearAnnealedPolicy(inner_policy=BoltzmannQPolicy(),
                                  attr="tau",
                                  value_max=1.,
                                  value_min=0.01,
                                  value_test=0.001,
                                  nb_steps=steps * 0.8)

    model = generate_model()

    dqn = OfflineDQNAgent(model=model, nb_actions=2, memory=memory, nb_steps_warmup=200,
                          target_model_update=1e-4, policy=policy, enable_double_dqn=False)

    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    return dqn
