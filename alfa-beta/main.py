import environment
import alfa_beta


env = environment.Environment()
ab = alfa_beta.AlfaBeta()

# while not env.finished() and env.epochs < 20:
#     print("Epoch:", env.epochs)
#     env.move_agents(ab)

#     env.epochs += 1
env.render()

for x in range(10):
    env.move_agents(ab)

    if env.mrx == env.agent1 or env.mrx == env.agent2:
        
        env.render()
        print("WIN")
        break

    
    env.move_mrx(ab)
    env.render()
