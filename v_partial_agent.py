
import random

import constants as c
import graph_operations as g
import numpy as np

weight1 = []
weight12 = []
weight23 = []
weight34 = []
weight4 = []
lookup_table = []
infinity = 100000000

def agent():
    init_weights()
    g.pre_load_dist()
    is_alive = True
    is_win = False
    
    new_belief = init_belief()
    old_belief = new_belief.copy()

    # Loop until Agent CATCHES Prey or DIES or TIMES OUT
    while c.STEPS != c.TIME_OUT_STEPS and is_alive and not is_win:
        # Get all the nodes with max possibility of prey being there
        max_poss = [i for i, x in enumerate(new_belief) if x == max(new_belief)]
        # Randomly choose a node with max possibility
        max_poss_of_prey = random.choice(max_poss)

        # Survey the chosen node
        # If prey if found at surveyed node then change the probability of that node to 1 and rest all to 0
        if survey(max_poss_of_prey):
            new_belief = [0 for _ in range(c.SIZE)]
            new_belief[max_poss_of_prey] = 1
            c.PREY_CAUGHT_NUM += 1
        # Else change the probability of surveyed node to 0 and redistribute the probability
        else:
            new_belief = update_belief(new_belief, max_poss_of_prey)
        old_belief = new_belief.copy()
        
        # Function call for agent movement
        c.AGENT_POS = movement(c.AGENT_POS, new_belief, c.PREDATOR_POS.position)
        is_win = g.check_if_win()       # Function call to check if the agent won
        is_alive = g.check_if_alive()   # Function call to check if the agent is alive

        if is_win:                      # If agent dies then break loop and return False
            print("Sucess!!!")
            return True
        elif not is_alive:              # If agent is alive and catches the prey
            print("Fail!!!")            # then break loop and return True
            return False
        elif c.STEPS == c.TIME_OUT_STEPS:   # If agent times out then break loop and return False
            print("Fail!!!")
            return False

        new_belief = update_belief(new_belief, c.AGENT_POS)
        old_belief = new_belief.copy()

        is_win = c.PREY_POS.movement()       # Function call for prey movement
        if is_win:                           # If agent is alive and catches the prey
            print("Success!!!")              # then break loop and return True
            return True
        
        new_belief = redistribute_belief(new_belief, old_belief)
        old_belief = new_belief.copy()

        is_alive = c.PREDATOR_POS.movement(c.AGENT_POS) # Function call for predator movement
        if not is_alive:                     # If agent dies then break loop and return False
            print("Fail!!!")
            return False
        
    return False


def init_belief():
    belief = [( 1 / (c.SIZE-1) ) for _ in range(c.SIZE)]
    belief[c.AGENT_POS] = 0
    return belief


# Set the probability of the node to 0 and redistribute it
def update_belief(new_belief, node):
    temp = 1 - new_belief[node]
    new_belief[node] = 0
    for i in range(c.SIZE):
        new_belief[i] = new_belief[i] / temp

    return new_belief


# Redistribute the probabilities after prey's movement
def redistribute_belief(new_belief, old_belief):
    for i in range(c.SIZE):
        new_belief[i] = old_belief[i] / (len(c.GRAPH[i]) + 1)
        for neighbour in c.GRAPH[i]:
            new_belief[i] = new_belief[i] + (old_belief[neighbour] / (len(c.GRAPH[neighbour]) + 1))
    return update_belief(new_belief, c.AGENT_POS)


# Survey a node and return whether the prey is in that location or not
def survey(survey_node):
    return survey_node == c.PREY_POS.position


def init_weights():
    global weight1
    global weight12
    global weight23
    global weight34
    global weight4
    global lookup_table
    
    weight1 = [[ 1.16036439e+01, -1.27399226e+01, -1.45809460e+00,  2.01680133e+00],[ 5.40137389e+00, -6.27092292e+00,  1.66880577e+00,  5.58472658e-02],[ 3.55669657e+00, -3.09961916e+00, -9.79137868e-01, -2.49542245e-01],[ 1.11438801e+00,  1.00927597e+00, -7.11176369e-01, -1.72534783e+00],[ 2.08506914e-01,  5.31693392e-02,  1.25509743e+00,  7.24843068e-02],[ 5.60526734e-02, -4.41957532e-01,  4.86104427e-01,  8.02756254e-01],[ 2.44031663e-02,  1.60472665e+00,  6.04334669e-01,  4.48779471e-01],[ 2.37627662e-01,  9.49926615e-01,  1.30080799e+00,  6.94720209e-01],[-7.90044562e-02,  8.78834119e-01, -5.88944712e-01, -1.08006215e+00],[-3.98625444e-01,  3.50215895e-01, -7.84866773e-01, -7.30704584e-01],[-6.13734344e-01,  6.30260020e-01, -2.22603131e+00,  5.65473437e-01],[ 2.71512093e-01,  6.94909552e-01, -1.08839548e+00, -1.16277962e+00],[-1.69011220e+00,  1.57508842e+00,  1.23852427e+00,  1.96636027e-01],[ 4.46105366e-02, -4.24892775e-01, -8.93210661e-01, -9.26402199e-02],[-2.77189730e-01, -7.97456716e-01,  1.30943509e+00, -4.61586552e-01],[ 1.98968189e-01,  1.34510109e-01,  2.69368776e-02, -1.76691095e+00],[ 1.03931223e+00,  1.79581718e-01, -9.20431547e-01, -2.28816989e-01],[ 5.46718170e-01, -3.44426756e-01,  3.27377780e-01, -7.36250875e-01],[ 7.28649692e-01, -2.23440944e-01,  1.03806623e+00, -5.38694545e-02],[-1.92192303e+00,  4.18197353e-01, -4.71806189e-01, -1.73905373e+00],[-3.13646143e+00, -1.29174305e+00, -1.65542803e+00,  5.35722052e-01],[ 5.51526024e-01,  6.85284476e-01,  3.10143067e-01, -1.97489154e-01],[ 4.11986209e-01,  9.55449075e-01,  1.37097555e+00,  5.48791218e-01],[ 1.47573223e-02,  4.90961649e-01, -1.80415597e-02, -2.37892500e+00],[ 1.34853945e+00, -7.24525746e-02,  1.56488599e+00,  1.21230527e+00],[ 2.96995274e-01, -5.64806755e-01,  1.07977910e+00, -2.28698048e+00],[-5.69828126e-01, -7.42180764e-03,  1.03426270e+00,  1.15668636e+00],[-1.04054180e+00, -9.52127818e-01, -1.15938576e+00,  3.27398731e-01],[ 2.12762939e+00,  2.25304889e-01, -5.09655051e-01,  1.05303588e+00],[-1.81789064e+00, -6.93427037e-01,  6.15814353e-01,  7.80299460e-01],[-3.63791852e-01, -1.36424980e+00, -3.37896087e-01, -5.08653970e-01],[-1.09748557e+00,  7.09509885e-01, -9.36821857e-01, -5.19105435e-01],[ 1.25386486e+00,  1.53296565e-01, -1.68070276e-01,  2.80330999e-01],[ 3.64923805e-01,  1.74148460e+00,  1.12850836e+00,  3.92206499e-01],[-2.24694463e+00,  1.19046820e+00, -2.57034411e-01, -2.71569865e-01],[-1.66636091e+00,  5.24841908e-01, -2.06870528e-01,  6.92730308e-01],[-2.38621679e-01, -5.56857581e-01,  1.73254227e+00,  4.47345748e-01],[ 6.81387822e-01,  8.54925314e-01,  4.15926120e-01, -4.84827002e-01],[-1.01180766e+00, -1.05375595e+00, -9.98093793e-01, -1.49476320e+00],[ 1.13361592e+00,  2.94817237e-01, -1.51658352e+00,  7.68230294e-01],[-5.11992241e-01,  1.60206790e+00, -7.77991920e-01, -1.02427903e+00],[-4.06696069e-01,  1.72832169e-01, -6.11748739e-02,  4.67830667e-01],[ 3.50050786e-01, -9.96220783e-02, -1.19616847e+00, -1.17316676e-01],[ 9.10032825e-01,  8.26031518e-01,  2.81488936e-01,  1.06427728e-01],[ 6.64690296e-01, -1.28067494e+00,  1.86212880e-01, -1.18453632e+00],[ 1.94301713e+00,  6.94060196e-01,  8.02245759e-01,  1.96117584e+00],[ 8.35342516e-02,  4.55017254e-01, -6.51768460e-01, -4.13721482e-01],[-1.59780509e+00,  3.08951013e-01, -3.62971882e-01,  5.98621877e-02],[-7.19507586e-01,  3.65745726e-01, -1.09186365e+00,  7.23623292e-01],[-3.02162023e-01, -1.13581382e+00,  5.04198431e-01, -3.95714480e-01],[-1.33645574e+00,  2.62102619e+00, -4.15743308e-02, -6.18426161e-01],[-5.51579216e-01, -6.30795747e-01,  5.01689140e-01, -1.13940835e+00],[-1.02096246e+00,  5.21015250e-01,  1.21133866e+00, -7.67635411e-02]]
    weight12 = [[-2.47478700e+00,  3.07892241e-01, -3.10287867e+00, -1.46883480e+00],[ 1.32642527e+00,  7.02711353e-01, -3.25874021e-01, -1.33339640e+00],[-1.73583114e-03,  2.42848193e-01, -1.13922140e+00,  5.26582005e-01],[-2.59111003e-01, -1.47698411e+00, -1.53604868e+00, -2.66248391e-02]]
    weight23 = [[11.15777607,  9.26399957, 11.46800768,  9.62811966], [28.16042018, 29.89058788, 27.49118505, 28.82761253], [ 5.55317416,  2.38035423,  3.78205515,  1.83748147], [12.87954779, 13.66942787, 14.14253177, 11.80233554]]
    weight34 = [[26.25716099, 25.39039982, 25.73122641, 28.49113822], [29.75756807, 32.02095385, 31.49352881, 30.98810749], [23.54039439, 23.93723022, 23.06670316, 25.42765061], [18.93785368, 19.06510803, 19.44875568, 19.48793729]]
    weight4 = [[ 8.07956738], [21.62146907], [16.17002436], [39.21543762]]
    lookup_table = [(24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (22, 21), (26, 21), (26, 22), (26, 24), (23, 22), (23, 24), (27, 24), (27, 23), (28, 25), (39, 41), (35, 40), (38, 40), (34, 36), (33, 37), (29, 32), (31, 32), (30, 31), (30, 30), (25, 30), (23, 25), (25, 25), (24, 25), (22, 24), (22, 26), (24, 24), (24, 26), (21, 24), (21, 22), (18, 21), (20, 21), (16, 20), (19, 20), (15, 19), (14, 15), (20, 18), (28, 25), (30, 25), (29, 30), (31, 30), (25, 24), (25, 26), (25, 30), (30, 30), (30, 29), (30, 31), (30, 25), (32, 31), (28, 29), (28, 31), (28, 25), (31, 29), (31, 31), (31, 28), (31, 30), (31, 33), (33, 28), (33, 30), (33, 33), (32, 33), (38, 32), (38, 34), (32, 32), (32, 34), (37, 32), (37, 34), (5, 48), (5, 0), (4, 5), (6, 5), (0, 49), (0, 1), (0, 5), (5, 5), (3, 4), (3, 6), (3, 0), (5, 4), (5, 6), (5, 0), (7, 4), (7, 6), (4, 4), (0, 0), (5, 48), (5, 0), (20, 18), (20, 20), (22, 20), (21, 20), (30, 27), (30, 29), (30, 31), (32, 31), (28, 27), (28, 29), (28, 31), (31, 29), (31, 31), (31, 28), (33, 28), (41, 43), (41, 42), (40, 41), (39, 41), (39, 40), (38, 40), (3, 0), (3, 2), (5, 0), (5, 2), (6, 3), (4, 3), (7, 4), (9, 4), (12, 7), (8, 7), (13, 8), (11, 8), (14, 13), (16, 13), (15, 14), (16, 20), (19, 20), (18, 19), (18, 21), (18, 18), (20, 19), (20, 21), (20, 18), (15, 19), (19, 19), (19, 18), (14, 15), (16, 18), (16, 20), (16, 15), (19, 18), (19, 20), (19, 15), (15, 15), (15, 19), (14, 15), (13, 14), (21, 21), (18, 21), (20, 21), (39, 41), (35, 40), (38, 40), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (29, 31), (29, 33), (31, 31), (31, 33), (30, 31), (4, 4), (6, 6), (6, 4), (5, 6), (5, 4), (39, 37), (36, 37), (38, 32), (35, 32), (37, 37), (39, 37), (34, 31), (34, 33), (34, 37), (38, 37), (20, 19), (2, 2), (1, 2), (1, 48), (49, 49), (0, 47), (0, 49), (0, 3), (0, 0), (5, 48), (5, 0), (5, 5), (4, 5), (6, 4), (6, 6), (4, 4), (7, 4), (7, 6), (7, 7), (9, 7), (8, 7), (36, 40), (39, 40), (35, 40), (27, 27), (28, 25), (28, 27), (28, 28), (31, 28), (31, 29), (31, 31), (33, 29), (33, 31), (32, 31), (38, 32), (32, 32), (37, 32), (35, 37), (37, 37), (36, 37), (39, 36), (39, 38), (36, 36), (36, 38), (40, 36), (40, 40), (41, 40), (41, 41), (43, 41), (42, 41), (43, 42), (43, 43), (42, 42), (42, 43), (44, 42), (44, 43), (3, 0), (3, 2), (5, 0), (5, 2), (6, 5), (4, 5), (23, 25), (25, 25), (24, 25), (30, 30), (25, 30), (27, 27), (26, 27), (22, 25), (24, 25), (21, 24), (42, 41), (41, 41), (43, 41), (14, 13), (16, 13), (14, 14), (16, 14), (15, 14), (13, 13), (11, 13), (14, 13), (12, 8), (8, 8), (13, 8), (10, 7), (12, 7), (34, 32), (35, 32), (35, 37), (37, 37), (36, 37), (34, 36), (33, 37), (29, 32), (31, 32), (22, 25), (24, 25), (21, 24), (18, 21), (20, 21), (16, 20), (19, 20), (15, 19), (14, 15), (3, 3), (48, 3), (48, 5), (21, 21), (18, 21), (20, 21), (18, 20), (20, 20), (19, 20), (16, 19), (16, 18), (19, 19), (19, 18), (15, 19), (15, 15), (14, 15), (12, 14), (14, 14), (13, 14), (39, 40), (38, 40), (35, 39), (35, 36), (38, 39), (38, 36), (34, 36), (32, 37), (34, 35), (34, 37), (33, 37), (33, 32), (29, 32), (3, 48), (3, 0), (5, 48), (5, 0), (4, 5), (6, 5), (0, 49), (0, 1), (0, 5), (5, 5), (5, 4), (5, 6), (5, 0), (7, 4), (7, 6), (9, 4), (9, 6), (6, 4), (6, 6), (8, 7), (8, 9), (10, 7), (10, 9), (6, 5), (6, 7), (6, 9), (9, 7), (9, 9), (9, 8), (9, 10), (9, 6), (11, 8), (11, 10), (12, 8), (12, 10), (10, 8), (10, 10), (10, 9), (10, 11), (10, 12), (12, 9), (12, 11), (12, 12), (14, 11), (11, 11), (11, 12), (13, 11), (13, 13), (13, 10), (11, 11), (11, 13), (11, 10), (14, 11), (14, 13), (14, 14), (16, 14), (15, 14), (18, 15), (15, 15), (19, 15), (19, 19), (18, 19), (20, 19), (20, 18), (20, 20), (22, 20), (21, 20), (23, 21), (21, 21), (24, 21), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (25, 23), (25, 25), (30, 25), (30, 30), (31, 30), (31, 29), (31, 31), (33, 29), (33, 31), (32, 31), (38, 32), (32, 32), (37, 32), (35, 37), (37, 37), (36, 37), (39, 36), (39, 38), (36, 36), (36, 38), (40, 36), (11, 13), (11, 11), (12, 13), (12, 11), (10, 13), (10, 11), (4, 7), (4, 9), (6, 7), (6, 9), (3, 6), (5, 6), (7, 8), (7, 10), (7, 6), (4, 7), (4, 9), (3, 6), (3, 4), (30, 27), (28, 27), (31, 28), (33, 28), (32, 31), (35, 32), (37, 32), (39, 37), (36, 37), (40, 36), (23, 25), (25, 25), (24, 25), (22, 24), (22, 26), (24, 24), (24, 26), (21, 24), (21, 21), (18, 21), (20, 21), (12, 8), (8, 8), (13, 8), (11, 13), (13, 13), (10, 7), (10, 9), (10, 13), (12, 7), (12, 9), (12, 13), (10, 8), (10, 10), (12, 8), (12, 10), (11, 8), (11, 10), (13, 11), (13, 12), (11, 11), (11, 12), (14, 11), (14, 14), (16, 14), (15, 14), (41, 40), (30, 30), (25, 30), (23, 25), (25, 25), (24, 25), (22, 24), (22, 26), (24, 24), (24, 26), (21, 24), (10, 7), (12, 7), (48, 5), (4, 4), (3, 6), (3, 4), (7, 7), (4, 7), (4, 9), (6, 6), (5, 6), (5, 5), (0, 5), (0, 0), (49, 0), (46, 49), (46, 1), (49, 49), (45, 49), (45, 45), (44, 45), (42, 44), (44, 44), (43, 44), (14, 13), (16, 13), (15, 14), (17, 14), (16, 14), (16, 13), (16, 15), (16, 11), (18, 15), (17, 15), (17, 14), (17, 16), (17, 19), (19, 19), (20, 19), (18, 19), (19, 18), (19, 20), (19, 15), (21, 20), (18, 18), (18, 20), (18, 15), (20, 18), (20, 20), (20, 19), (20, 20), (22, 20), (21, 20), (23, 21), (21, 21), (24, 21), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (25, 23), (25, 25), (30, 25), (30, 27), (28, 27), (31, 28), (33, 28), (19, 15), (18, 15), (17, 14), (19, 15), (18, 15), (20, 19), (21, 20), (24, 21), (26, 21), (39, 40), (41, 40), (41, 42), (41, 43), (36, 40), (40, 40), (35, 39), (35, 36), (37, 36), (40, 39), (40, 41), (40, 36), (36, 39), (36, 36), (36, 38), (36, 40), (36, 35), (38, 38), (38, 40), (38, 35), (37, 38), (37, 35), (33, 37), (33, 34), (37, 37), (37, 34), (32, 37), (32, 34), (3, 3), (4, 3), (5, 48), (5, 2), (1, 1), (0, 1), (0, 3), (0, 47), (0, 0), (45, 46), (49, 0), (49, 46), (46, 49), (46, 1), (49, 49), (45, 49), (45, 45), (44, 45), (42, 44), (44, 44), (43, 44), (6, 4), (6, 6), (4, 4), (7, 4), (7, 6), (5, 5), (4, 5), (48, 48), (3, 48), (3, 0), (16, 20), (19, 20), (15, 19), (14, 15), (4, 3), (6, 3), (0, 47), (0, 49), (0, 3), (5, 2), (5, 4), (5, 48), (7, 4), (9, 4), (6, 4), (8, 7), (10, 7), (6, 3), (6, 5), (6, 7), (9, 7), (9, 4), (9, 6), (31, 28), (33, 28), (32, 31), (34, 31), (29, 29), (29, 31), (33, 29), (33, 31), (30, 31), (25, 30), (27, 30), (27, 28), (23, 25), (26, 25), (22, 25), (22, 24), (22, 26), (24, 24), (24, 26), (21, 24), (21, 22), (18, 21), (20, 21), (37, 35), (37, 37), (39, 35), (39, 37), (39, 40), (34, 35), (34, 37), (38, 35), (38, 37), (38, 40), (33, 32), (35, 36), (35, 38), (35, 32), (38, 36), (38, 38), (38, 32), (34, 36), (34, 38), (34, 32), (32, 31), (32, 33), (32, 37), (34, 31), (34, 33), (34, 37), (29, 31), (29, 33), (33, 31), (33, 33), (33, 37), (28, 28), (30, 30), (33, 30), (33, 32), (33, 28), (29, 30), (29, 32), (29, 28), (31, 30), (33, 30), (30, 30), (33, 30), (29, 30), (27, 27), (28, 25), (28, 27), (30, 30), (31, 30), (46, 45), (1, 45), (49, 46), (49, 49), (1, 46), (0, 49), (0, 0), (5, 48), (5, 0), (6, 3), (3, 3), (4, 3), (2, 2), (3, 0), (3, 2), (49, 49), (48, 49), (48, 1), (48, 5), (46, 46), (2, 2), (47, 0), (47, 2), (47, 46), (44, 45), (42, 44), (43, 44), (41, 43), (41, 42), (46, 44), (47, 45), (49, 45), (2, 49), (48, 49), (3, 48), (3, 0), (5, 48), (5, 0), (6, 5), (4, 5), (7, 4), (7, 6), (9, 4), (9, 6), (23, 25), (25, 25), (24, 25), (30, 30), (25, 30), (27, 27), (26, 27), (28, 28), (27, 30), (27, 28), (49, 49), (48, 49), (48, 1), (48, 5), (4, 4), (3, 4), (3, 6), (3, 0), (46, 47), (46, 49), (49, 49), (45, 49), (31, 28), (31, 30), (31, 33), (33, 28), (33, 30), (33, 33), (32, 33), (38, 32), (38, 34), (32, 32), (32, 34), (37, 32), (37, 34), (35, 35), (35, 38), (37, 35), (37, 38), (36, 35), (36, 38), (39, 36), (39, 39), (36, 36), (36, 39), (40, 36), (40, 39), (40, 40), (41, 40), (41, 41), (43, 41), (42, 41), (43, 42), (43, 43), (42, 42), (42, 43), (44, 42), (44, 43), (6, 6), (5, 6), (7, 7), (4, 7), (4, 9), (4, 4), (3, 6), (3, 4), (5, 5), (0, 5), (4, 4), (6, 6), (6, 4), (5, 6), (5, 4), (29, 28), (33, 28), (32, 31), (34, 31), (29, 29), (29, 31), (33, 29), (33, 31), (25, 23), (25, 25), (27, 23), (22, 23), (22, 25), (22, 21), (26, 23), (26, 25), (26, 21), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (15, 15), (14, 15), (12, 14), (14, 14), (13, 14), (13, 13), (13, 11), (8, 13), (8, 11), (8, 12), (7, 10), (4, 9), (3, 6), (11, 8), (13, 8), (10, 8), (12, 8), (9, 7), (12, 7), (10, 7), (10, 8), (12, 8), (11, 8), (45, 44), (49, 45), (1, 45), (0, 49), (5, 48), (5, 0), (6, 5), (39, 41), (41, 41), (41, 43), (40, 41), (38, 40), (40, 40), (35, 40), (39, 40), (39, 41), (35, 40), (38, 40), (39, 41), (28, 31), (30, 31), (33, 31), (33, 33), (33, 37), (29, 31), (29, 33), (29, 32), (29, 29), (31, 32), (31, 29), (30, 29), (30, 31), (12, 8), (12, 10), (8, 8), (13, 8), (13, 10), (0, 0), (46, 45), (1, 48), (1, 0), (1, 45), (31, 30), (33, 30), (30, 30), (33, 30), (29, 30), (39, 41), (35, 40), (38, 40), (34, 36), (6, 4), (4, 4), (7, 4), (5, 5), (7, 7), (9, 7), (6, 3), (6, 5), (6, 7), (29, 32), (31, 32), (11, 8), (11, 10), (13, 8), (13, 10), (10, 8), (10, 10), (12, 8), (12, 10), (12, 7), (12, 9), (8, 7), (8, 9), (13, 8), (13, 10), (11, 8), (11, 10), (14, 11), (16, 11), (6, 4), (4, 4), (7, 4), (7, 7), (9, 7), (8, 7), (12, 8), (8, 8), (13, 8), (46, 49), (46, 1), (49, 49), (45, 49), (45, 45), (44, 45), (7, 7), (9, 7), (9, 9), (8, 7), (8, 9), (12, 8), (12, 10), (8, 8), (13, 8), (13, 10), (13, 11), (13, 12), (11, 11), (11, 12), (14, 11), (4, 7), (4, 9), (3, 6), (3, 4), (39, 40), (38, 40), (35, 39), (35, 36), (38, 39), (38, 36), (34, 36), (49, 0), (49, 46), (1, 0), (1, 2), (1, 46), (5, 0), (5, 2), (0, 0), (48, 49), (48, 1), (48, 5), (0, 49), (0, 1), (0, 5), (45, 49), (49, 49), (49, 0), (29, 32), (31, 32), (16, 20), (19, 20), (18, 19), (18, 21), (18, 18), (20, 19), (20, 21), (20, 18), (15, 19), (19, 19), (19, 18), (14, 15), (16, 18), (16, 20), (16, 15), (19, 18), (19, 20), (19, 15), (15, 15), (13, 14), (15, 14), (15, 16), (15, 19), (11, 14), (14, 14), (14, 15), (13, 14), (8, 13), (8, 11), (7, 8), (4, 7), (4, 9), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (7, 4), (7, 6), (9, 4), (9, 6), (8, 7), (8, 9), (10, 7), (10, 9), (6, 5), (6, 7), (6, 9), (9, 7), (9, 9), (9, 8), (9, 10), (9, 6), (11, 8), (11, 10), (12, 8), (12, 10), (10, 8), (10, 10), (10, 7), (10, 9), (10, 13), (12, 7), (12, 9), (12, 13), (14, 13), (11, 13), (13, 8), (13, 10), (11, 8), (11, 10), (14, 11), (16, 11), (15, 14), (19, 15), (18, 15), (20, 19), (21, 20), (24, 21), (26, 21), (41, 40), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (25, 23), (25, 25), (27, 23), (22, 23), (22, 25), (22, 21), (26, 23), (26, 25), (26, 21), (24, 22), (24, 24), (26, 22), (26, 24), (26, 27), (30, 27), (25, 24), (3, 6), (5, 6), (7, 8), (7, 10), (7, 6), (4, 7), (4, 9), (3, 6), (3, 4), (0, 5), (2, 5), (47, 0), (1, 0), (46, 49), (46, 1), (49, 49), (45, 49), (45, 45), (44, 45), (42, 44), (44, 44), (43, 44), (42, 43), (42, 42), (43, 43), (43, 42), (41, 43), (41, 42), (39, 41), (41, 41), (41, 43), (40, 41), (35, 40), (40, 40), (36, 40), (21, 20), (22, 21), (24, 21), (23, 21), (26, 22), (26, 24), (23, 22), (23, 24), (27, 24), (27, 23), (28, 25), (30, 30), (31, 30), (31, 29), (31, 31), (33, 29), (33, 31), (32, 31), (31, 29), (31, 31), (33, 29), (33, 31), (32, 31), (0, 0), (1, 0), (3, 3), (2, 3), (2, 5), (48, 48), (2, 2), (47, 2), (47, 48), (6, 5), (4, 5), (7, 4), (9, 4), (8, 7), (10, 7), (6, 3), (6, 5), (6, 7), (9, 7), (9, 6), (9, 8), (9, 4), (11, 8), (12, 8), (10, 8), (10, 7), (10, 9), (12, 7), (12, 9), (13, 8), (13, 10), (11, 8), (11, 10), (14, 13), (16, 13), (15, 14), (22, 25), (24, 25), (21, 24), (23, 24), (23, 26), (26, 24), (26, 26), (22, 24), (22, 26), (9, 7), (9, 9), (12, 7), (12, 9), (10, 7), (10, 9), (10, 8), (10, 10), (12, 8), (12, 10), (11, 8), (11, 10), (13, 13), (11, 13), (14, 13), (48, 5), (0, 5), (49, 0), (1, 0), (5, 4), (5, 6), (5, 0), (0, 0), (46, 49), (46, 1), (49, 49), (45, 49), (0, 0), (45, 46), (49, 0), (49, 46), (5, 5), (0, 5), (0, 0), (49, 0), (46, 49), (46, 1), (49, 49), (45, 49), (45, 45), (44, 45), (42, 44), (44, 44), (43, 44), (42, 43), (42, 42), (43, 43), (43, 42), (41, 43), (41, 42), (39, 41), (41, 42), (41, 41), (40, 41), (35, 40), (40, 40), (36, 40), (13, 13), (11, 13), (14, 13), (12, 8), (12, 10), (8, 8), (13, 8), (13, 10), (39, 37), (36, 37), (38, 36), (38, 38), (38, 32), (40, 36), (35, 36), (35, 38), (35, 32), (39, 36), (39, 38), (38, 37), (38, 39), (38, 34), (40, 39), (39, 37), (39, 39), (3, 2), (3, 4), (3, 48), (5, 2), (5, 4), (5, 48), (7, 4), (4, 4), (6, 3), (6, 5), (6, 7), (8, 7), (4, 3), (4, 5), (4, 7), (7, 7), (7, 6), (7, 8), (7, 4), (9, 6), (9, 8), (9, 4), (13, 8), (8, 8), (12, 7), (12, 9), (12, 13), (14, 13), (8, 7), (8, 9), (8, 13), (13, 13), (13, 12), (13, 14), (13, 8), (15, 14), (11, 12), (11, 14), (11, 8), (14, 14), (14, 13), (14, 15), (14, 11), (16, 13), (16, 15), (16, 11), (19, 15), (15, 15), (18, 19), (20, 19), (15, 14), (15, 16), (15, 19), (19, 19), (48, 48), (2, 2), (47, 2), (47, 48), (47, 47), (1, 1), (46, 1), (46, 47), (46, 46), (49, 46), (49, 48), (45, 46), (45, 45), (44, 45), (42, 44), (44, 44), (43, 44), (31, 29), (31, 31), (33, 29), (33, 31), (32, 31), (38, 32), (32, 32), (37, 32), (35, 37), (37, 37), (36, 37), (7, 7), (9, 7), (9, 9), (6, 7), (6, 9), (33, 31), (33, 33), (33, 37), (35, 37), (38, 37), (34, 31), (34, 33), (34, 37), (34, 36), (34, 38), (34, 32), (36, 36), (36, 38), (39, 36), (39, 38), (35, 36), (35, 38), (35, 32), (5, 48), (5, 2), (49, 49), (0, 47), (0, 49), (0, 3), (12, 14), (14, 14), (13, 14), (46, 44), (47, 45), (49, 45), (13, 14), (12, 13), (12, 11), (14, 13), (14, 15), (14, 11), (8, 13), (8, 11), (13, 13), (13, 11), (11, 14), (13, 14), (12, 14), (11, 13), (11, 11), (12, 13), (12, 11), (10, 13), (10, 11), (8, 12), (8, 8), (10, 12), (10, 8), (9, 8), (7, 7), (9, 7), (9, 9), (6, 7), (6, 9), (20, 19), (20, 20), (22, 20), (21, 20), (44, 45), (4, 3), (6, 3), (0, 1), (0, 3), (0, 47), (32, 31), (35, 32), (37, 32), (39, 37), (36, 37), (40, 36), (41, 40), (43, 41), (42, 41), (44, 42), (44, 43), (45, 44), (49, 45), (1, 45), (45, 44), (46, 44), (46, 45), (47, 45), (15, 14), (19, 15), (18, 15), (38, 32), (32, 32), (37, 32), (37, 37), (39, 37), (34, 31), (34, 33), (34, 37), (38, 37), (38, 36), (38, 38), (38, 32), (40, 36), (35, 36), (35, 38), (35, 32), (39, 36), (39, 38), (39, 37), (39, 39), (36, 37), (36, 39), (40, 39), (40, 36), (41, 40), (43, 41), (42, 41), (44, 42), (44, 43), (13, 14), (8, 13), (8, 11), (10, 13), (10, 11), (7, 8), (9, 8), (8, 12), (8, 8), (10, 12), (10, 8), (9, 8), (11, 13), (11, 11), (12, 13), (12, 11), (10, 13), (10, 11), (8, 12), (8, 8), (10, 12), (10, 8), (9, 8), (7, 7), (9, 7), (9, 9), (6, 7), (6, 9), (6, 6), (5, 6), (5, 5), (0, 5), (0, 0), (49, 0), (3, 3), (48, 3), (48, 5), (48, 48), (49, 48), (5, 5), (0, 3), (0, 5), (5, 5), (0, 5), (4, 4), (6, 6), (6, 4), (5, 6), (5, 4), (5, 5), (0, 5), (0, 0), (49, 0), (49, 49), (48, 49), (48, 1), (48, 5), (48, 48), (3, 48), (3, 0), (5, 5), (4, 5), (6, 4), (6, 6), (4, 4), (7, 4), (7, 6), (7, 7), (9, 7), (9, 9), (8, 7), (8, 9), (12, 8), (8, 8), (13, 8), (0, 0), (5, 48), (5, 0), (9, 7), (9, 9), (11, 13), (12, 7), (12, 9), (12, 13), (10, 7), (10, 9), (10, 13), (8, 12), (8, 8), (10, 12), (10, 8), (9, 8), (7, 7), (9, 7), (9, 9), (6, 7), (6, 9), (26, 23), (26, 25), (26, 21), (28, 25), (23, 23), (23, 25), (23, 21), (27, 23), (27, 24), (49, 0), (45, 49), (1, 1), (46, 49), (46, 1), (46, 45), (48, 48), (47, 48), (47, 0), (47, 45), (13, 8), (11, 8), (12, 7), (12, 9), (12, 13), (14, 13), (8, 7), (8, 9), (8, 13), (13, 13), (13, 12), (13, 14), (13, 8), (15, 14), (11, 12), (11, 14), (11, 8), (14, 14), (14, 13), (14, 15), (14, 11), (16, 13), (16, 15), (16, 11), (19, 15), (15, 15), (18, 19), (20, 19), (15, 14), (15, 16), (15, 19), (19, 19), (19, 15), (18, 15), (20, 19), (21, 20), (24, 21), (26, 21), (16, 14), (17, 14), (17, 15), (19, 15), (18, 15), (19, 19), (18, 19), (20, 19), (20, 18), (20, 20), (22, 20), (21, 20), (23, 21), (21, 21), (24, 21), (24, 22), (24, 24), (26, 22), (26, 24), (25, 24), (25, 23), (25, 25), (30, 25), (30, 27), (28, 27), (31, 28), (33, 28), (29, 28), (33, 28), (18, 20), (20, 20), (19, 20), (17, 21), (20, 21), (18, 21), (18, 20), (20, 20), (19, 20), (16, 19), (16, 18), (19, 19), (19, 18), (15, 19), (15, 15), (14, 15), (37, 38), (37, 35), (39, 38), (39, 40), (39, 35), (34, 38), (34, 35), (38, 38), (38, 40), (38, 35), (33, 34), (35, 34), (35, 36), (35, 39), (38, 34), (38, 36), (38, 39), (34, 34), (34, 36), (32, 33), (34, 33), (34, 35), (34, 38), (29, 33), (33, 33), (28, 29), (30, 29), (33, 32), (33, 34), (33, 29), (29, 32), (29, 29), (29, 31), (29, 33), (31, 31), (31, 33), (30, 31), (30, 30), (25, 30), (23, 25), (25, 25), (24, 25), (22, 24), (22, 26), (24, 24), (24, 26), (21, 24), (35, 37), (37, 37), (36, 37), (34, 32), (35, 32), (33, 31), (33, 33), (33, 37), (35, 37), (38, 37), (34, 31), (34, 33), (34, 37), (37, 32), (34, 32), (38, 32), (36, 37), (38, 37), (32, 31), (32, 33), (32, 37), (37, 37), (35, 36), (35, 38), (35, 32), (37, 36), (37, 38), (37, 32), (40, 36), (36, 36), (36, 38), (39, 35), (39, 37), (39, 40), (41, 40), (36, 35), (36, 37), (36, 40), (40, 40), (40, 39), (40, 41), (40, 36), (42, 41), (43, 41), (41, 41), (41, 40), (41, 42), (41, 43), (43, 42), (43, 43), (44, 42), (44, 43), (42, 42), (42, 43), (43, 42), (43, 44), (43, 41), (45, 44), (42, 42), (42, 44), (42, 41), (44, 42), (44, 44), (44, 43), (44, 44), (46, 44), (45, 44), (45, 45), (49, 45), (49, 46), (49, 49), (1, 46), (0, 49), (0, 0), (5, 48), (5, 0), (6, 3), (38, 37), (35, 37), (39, 37), (37, 32), (37, 34), (34, 32), (34, 34), (38, 32), (38, 34), (36, 40), (38, 40), (35, 39), (35, 36), (37, 36), (40, 39), (40, 41), (40, 36), (36, 39), (36, 36), (33, 37), (35, 35), (35, 37), (35, 40), (38, 35), (38, 37), (38, 40), (34, 35), (34, 37), (32, 34), (34, 34), (34, 36), (33, 34), (33, 33), (29, 33), (29, 32), (29, 29), (31, 32), (31, 29), (30, 29), (3, 48), (3, 0), (5, 48), (5, 0), (3, 3), (4, 3), (4, 4), (6, 4), (5, 2), (5, 4), (5, 48), (5, 5), (0, 3), (0, 5), (48, 48), (49, 48), (46, 1), (46, 47), (49, 0), (46, 49), (46, 1), (49, 49), (45, 49), (4, 7), (4, 9), (6, 7), (6, 9), (3, 6), (3, 4), (5, 6), (5, 4), (7, 6), (7, 8), (7, 4), (4, 4), (2, 3), (2, 5), (4, 3), (4, 5), (4, 7), (48, 3), (48, 5), (3, 3), (47, 0), (49, 0), (3, 4), (3, 6), (3, 0), (48, 49), (48, 1), (48, 5), (0, 49), (0, 1), (0, 5), (45, 49), (49, 49), (46, 46), (49, 0), (49, 46), (45, 46), (45, 45), (44, 45), (42, 44), (44, 44), (43, 44), (42, 43), (42, 42), (43, 43), (43, 42), (41, 43), (41, 42), (39, 41), (41, 41), (41, 43), (40, 41), (35, 40), (40, 40), (36, 40), (36, 39), (36, 36), (38, 39), (38, 36), (37, 36), (33, 37), (37, 35), (37, 37), (32, 37), (32, 32), (31, 32), (29, 31), (29, 33), (31, 31), (31, 33), (30, 31), (30, 30), (25, 30), (25, 25), (22, 25), (26, 25), (21, 24), (23, 24), (23, 26), (26, 24), (26, 26), (22, 24), (22, 26), (22, 25), (22, 22), (24, 25), (24, 22), (21, 22), (21, 21), (18, 21), (20, 21), (21, 22), (20, 21), (22, 21), (22, 23), (22, 26), (24, 21), (24, 23), (24, 26), (21, 21), (21, 22), (18, 21), (20, 21), (16, 20), (19, 20), (40, 39), (6, 4), (6, 6), (9, 4), (9, 6), (44, 45), (42, 44), (43, 44), (41, 43), (41, 42), (40, 41), (36, 40), (38, 40), (37, 36), (32, 37), (29, 32), (31, 32), (30, 31)]


def movement(agent_pos, prey_belief, pred_pos):
    poss_moves = {}
    for m in c.GRAPH[agent_pos] + [agent_pos]:
        sum = 0
        for n in c.GRAPH[pred_pos]:
            sum += weighted_utility(m, prey_belief, n)
            poss_moves[(m, n)] = sum
            
    best_move = min(poss_moves, key=poss_moves.get)
    c.STEPS += 1
    return best_move[0]


def activation_function(x):
    return 1 / (1 + np.exp(-x))


def weighted_utility(agent, prey_belief, pred):
    if (agent, pred) in lookup_table:
        return infinity
    else:
        input = [agent, pred] + [c.FULL_DIST[agent][pred]] + prey_belief
        input_layer = np.dot(input, weight1)
        l2 = activation_function(input_layer)
        l3 = np.dot(l2, weight12)
        l4 = activation_function(l3)
        l5 = np.dot(l4, weight23)
        l6 = activation_function(l5)
        l7 = np.dot(l6, weight34)
        l8 = activation_function(l7)
        l9 = np.dot(l8, weight4)
        output = activation_function(l9)
        return output * 3

