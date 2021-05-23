from agentModel import generate_agent


def main():
    dqn_agent = generate_agent()
    dqn_agent.save_weights("./blank_weights.h5")

if __name__ == "__main__":
    main()
