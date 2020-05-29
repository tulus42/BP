import environment
import alfa_beta
import alfa_beta_mrx
import time

env = environment.Environment()
ab = alfa_beta.AlfaBeta()
abx = alfa_beta_mrx.AlfaBeta()

######################################
# set sleep time after every move    #
sleep_time = 0.5        # in seconds #


for x in range(15):
    if env.mrx == env.agent1 or env.mrx == env.agent2:
        print("WIN in move", x)
        break

    time.sleep(sleep_time)
    print("Move:", x)
    env.render()

    # False = no possible move, True = mrx moved
    if env.move_mrx(abx) == False:
        print("WIN in move", x)
        break
    
    time.sleep(sleep_time)
    print("Move:", x)
    env.render()

    env.move_agents(ab)


env.render()