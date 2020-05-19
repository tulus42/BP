import environment
import alfa_beta

env = environment.Environment()
ab = alfa_beta.AlfaBeta()

# while not env.finished() and env.epochs < 20:
#     print("Epoch:", env.epochs)
#     env.move_agents(ab)

#     env.epochs += 1


for x in range(10):
    env.render()
    env.move_agents(ab)

    env.render()
    env.move_mrx(ab)
