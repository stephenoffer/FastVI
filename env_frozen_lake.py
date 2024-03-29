import pickle
import sys
from contextlib import closing
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
from gym import utils
from gym.envs.toy_text import discrete
from six import StringIO

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize, precision=2)
TransitionProb = [0.7, 0.1, 0.1, 0.1]


def generate_row(length, h_prob):
    row = np.random.choice(2, length, p=[1.0 - h_prob, h_prob])
    row = ''.join(list(map(lambda z: 'F' if z == 0 else 'H', row)))
    return row


def generate_map(shape):
    """

    :param shape: Width x Height
    :return: List of text based map
    """
    h_prob = 0.1
    grid_map = []

    for h in range(shape[1]):

        if h == 0:
            row = 'SF'
            row += generate_row(shape[0] - 2, h_prob)
        elif h == 1:
            row = 'FF'
            row += generate_row(shape[0] - 2, h_prob)

        elif h == shape[1] - 1:
            row = generate_row(shape[0] - 2, h_prob)
            row += 'FG'
        elif h == shape[1] - 2:
            row = generate_row(shape[0] - 2, h_prob)
            row += 'FF'
        else:
            row = generate_row(shape[0], h_prob)

        grid_map.append(row)
        del row

    return grid_map


MAPS = {

    "4x4": [
        "SFFF",
        "FHFH",
        "FFFH",
        "HFFG"
    ],
    "8x8": [
        "SFFFFFFF",
        "FFFFFFFF",
        "FFFHFFFF",
        "FFFFFHFF",
        "FFFHFFFF",
        "FHHFFFHF",
        "FHFFHFHF",
        "FFFHFFFG"
    ],
    "16x16": [
        "SFFFFFFFFHFFFFHF",
        "FFFFFFFFFFFFFHFF",
        "FFFHFFFFHFFFFFFF",
        "FFFFFFFFHFFFFFFF",
        "FFFFFFFFFFFFFFFF",
        "FFHHFFFFFFFHFFFH",
        "FFFFFFFFFFFFFFFF",
        "FFFFFHFFFFFFHFFF",
        "FFFFFHFFFFFFFFFH",
        "FFFFFFFHFFFFFFFF",
        "FFFFFFFFFFFFHFFF",
        "FFFFFFHFFFFFFFFF",
        "FFFFFFFFHFFFFFFF",
        "FFFFFFFFFHFFFFHF",
        "FFFFFFFFFFHFFFFF",
        "FFFHFFFFFFFFFFFG",
    ],

    "32x32": [
        'SFFHFFFFFFFFFFFFFFFFFFFFFFHFFFFF',
        'FFHFHHFFHFFFFFFFFFFFFFFFFFHFFFFF',
        'FFFHFFFFFFFFHFFHFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFH',
        'FFFFHFFFFFFFFFFFFFFFHFHFFFFFFFHF',
        'FFFFFHFFFFFFFFFFHFFFFFFFFFFHFFFF',
        'FFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFFFFFFFFHFFFHFHFFFFFFFFHFF',
        'FFFFHFFFFFFHFFFFHFHFFFFFFFFFFFFH',
        'FFFFHHFHFFFFHFFFFFFFFFFFFFFFFFFF',
        'FHFFFFFFFFFFHFFFFFFFFFFFHHFFFHFH',
        'FFFHFFFHFFFFFFFFFFFFFFFFFFFFHFFF',
        'FFFHFHFFFFFFFFHFFFFFFFFFFFFHFFHF',
        'FFFFFFFFFFFFFFFFHFFFFFFFHFFFFFFF',
        'FFFFFFHFFFFFFFFHHFFFFFFFHFFFFFFF',
        'FFHFFFFFFFFFHFFFFFFFFFFHFFFFFFFF',
        'FFFHFFFFFFFFFHFFFFHFFFFFFHFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFFFHFFFFF',
        'FFFFFFFFHFFFFFFFHFFFFFFFFFFFFFFH',
        'FFHFFFFFFFFFFFFFFFHFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFHFFFFHFFFFFFFHFFF',
        'FFHFFFFHFFFFFFFFFHFFFFFFFFFFFHFH',
        'FFFFFFFFFFHFFFFHFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFHHFFHHHFFFHFFFF',
        'FFFFFFFFFFFFFFHFFFFHFFFFFFFHFFFF',
        'FFFFFFFHFFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFHFFFFFFFFFFFFFFFFHFFHFFFFFF',
        'FFFFFFFHFFFFFFFFFHFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFF',
        'FFFFFFFFFFFFFFFHFFFFFFFFHFFFFFFG',
    ],

    "64x64": [
        'SFFHFFFFFFFFFFFFFFFFFFFFFFHFFFFFSFFHFFFFFFFFFFFFFFFFFFFFFFHFFFFF',
        'FFHFHHFFHFFFFFFFFFFFFFFFFFHFFFFFFFHFHHFFHFFFFFFFFFFFFFFFFFHFFFFF',
        'FFFHFFFFFFFFHFFHFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFH',
        'FFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFHFFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFH',
        'FFFFHFFFFFFFFFFFFFFFHFHFFFFFFFHFFFFFHFFFFFFFFFFFFFFFHFHFFFFFFFHF',
        'FFFFFHFFFFFFFFFFHFFFFFFFFFFHFFFFFFFFFHFFFFFFFFFFHFFFFFFFFFFHFFFF',
        'FFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFFFFFFFFHFFFHFHFFFFFFFFHFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFHFFFFFFHFFFFHFHFFFFFFFFFFFFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFHHFHFFFFHFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FHFFFFFFFFFFHFFFFFFFFFFFHHFFFHFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFHFFFFFFFFFFFFFFFFFFFFHFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFHFFFFFFFFHFFFFFFFFFFFFHFFHFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFHFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFHFFFFFFFFHHFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFHFFFFFFFFFHFFFFFFFFFFHFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFFFFFFFHFFFFHFFFFFFHFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFHFFFFFFFHFFFFFFFFFFFFFFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFHFFFFFFFFFFFFFFFHFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFHFFFFHFFFFFFFHFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFHFFFFHFFFFFFFFFHFFFFFFFFFFFHFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFHFFFFHFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFHHFFHHHFFFHFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFHFFFFHFFFFFFFHFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFHFFFFFFFFFFFFFFFFHFFHFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFHFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFHFFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFH',
        'FFFHFFFFFFFFFFFFFFFFFFFFFFHFFFFFSFFHFFFFFFFFFFFFFFFFFFFFFFHFFFFF',
        'FFHFHHFFHFFFFFFFFFFFFFFFFFHFFFFFFFHFHHFFHFFFFFFFFFFFFFFFFFHFFFFF',
        'FFFHFFFFFFFFHFFHFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFH',
        'FFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFHFFFFFFFFFFFFFFHFHHFHFHFFFFFHFFFH',
        'FFFFHFFFFFFFFFFFFFFFHFHFFFFFFFHFFFFFHFFFFFFFFFFFFFFFHFHFFFFFFFHF',
        'FFFFFHFFFFFFFFFFHFFFFFFFFFFHFFFFFFFFFHFFFFFFFFFFHFFFFFFFFFFHFFFF',
        'FFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFFFFFFFFHFFFHFHFFFFFFFFHFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFHFFFFFFHFFFFHFHFFFFFFFFFFFFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFHHFHFFFFHFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FHFFFFFFFFFFHFFFFFFFFFFFHHFFFHFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFHFFFFFFFFFFFFFFFFFFFFHFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFHFFFFFFFFHFFFFFFFFFFFFHFFHFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFHFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFHFFFFFFFFHHFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFHFFFFFFFFFHFFFFFFFFFFHFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFHFFFFFFFFFHFFFFHFFFFFFHFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFHFFFFFFFHFFFFFFFFFFFFFFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFHFFFFFFFFFFFFFFFHFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFHFFFFHFFFFFFFHFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFHFFFFHFFFFFFFFFHFFFFFFFFFFFHFHFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFHFFFFHFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFHHFFHHHFFFHFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFHFFFFHFFFFFFFHFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFFFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFHFFFFFFFFFFFFFFFFHFFHFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFHFFFFFFFFFHFFFFFFFFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFFFFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFF',
        'FFFFFFFFFFFFFFFHFFFFFFFFHFFFFFFFFFHHFFFFHFFFFFFFFFFFFFFFFFFFFFFG',
    ]
}


def generate_random_map(size=8, p=0.8):
    """Generates a random valid map (one that has a path from start to goal)
    :param size: size of each side of the grid
    :param p: probability that a tile is frozen
    """
    valid = False

    # BFS to check that it's a valid path.
    def is_valid(arr, r=0, c=0):
        if arr[r][c] == 'G':
            return True

        tmp = arr[r][c]
        arr[r][c] = "#"

        # Recursively check in all four directions.
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for x, y in directions:
            r_new = r + x
            c_new = c + y
            if r_new < 0 or r_new >= size or c_new < 0 or c_new >= size:
                continue

            if arr[r_new][c_new] not in '#H':
                if is_valid(arr, r_new, c_new):
                    arr[r][c] = tmp
                    return True

        arr[r][c] = tmp
        return False

    while not valid:
        p = min(1, p)
        res = np.random.choice(['F', 'H'], (size, size), p=[p, 1 - p])
        res[0][0] = 'S'
        res[-1][-1] = 'G'
        valid = is_valid(res)
    return ["".join(x) for x in res]


class FrozenLakeEnv(discrete.DiscreteEnv):
    """
    Winter is here. You and your friends were tossing around a frisbee at the park
    when you made a wild throw that left the frisbee out in the middle of the lake.
    The water is mostly frozen, but there are a few holes where the ice has melted.
    If you step into one of those holes, you'll fall into the freezing water.
    At this time, there's an international frisbee shortage, so it's absolutely imperative that
    you navigate across the lake and retrieve the disc.
    However, the ice is slippery, so you won't always move in the direction you intend.
    The surface is described using a grid like the following

        SFFF
        FHFH
        FFFH
        HFFG

    S : starting point, safe
    F : frozen surface, safe
    H : hole, fall to your doom
    G : goal, where the frisbee is located

    The episode ends when you reach the goal or fall in a hole.
    You receive a reward of 1 if you reach the goal, and zero otherwise.

    """

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, desc=None, map_name="4x4", is_slippery=True):
        if desc is None and map_name is None:
            desc = generate_random_map()
        elif desc is None:
            desc = MAPS[map_name]
        self.desc = desc = np.asarray(desc, dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.reward_range = (0, 1)

        nA = 4
        nS = nrow * ncol

        isd = np.array(desc == b'S').astype('float64').ravel()
        isd /= isd.sum()

        rew_hole = -1000
        rew_goal = 1000
        rew_step = -1

        P = {s: {a: [] for a in range(nA)} for s in range(nS)}
        self.TransitProb = np.zeros((nA, nS + 1, nS + 1))
        self.TransitReward = np.zeros((nS + 1, nA))

        def to_s(row, col):
            return row * ncol + col

        def inc(row, col, a):
            if a == LEFT:
                col = max(col - 1, 0)
            elif a == DOWN:
                row = min(row + 1, nrow - 1)
            elif a == RIGHT:
                col = min(col + 1, ncol - 1)
            elif a == UP:
                row = max(row - 1, 0)
            return (row, col)

        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(4):
                    li = P[s][a]
                    letter = desc[row, col]
                    if letter in b'H':
                        li.append((1.0, s, 0, True))
                        self.TransitProb[a, s, nS] = 1.0
                        self.TransitReward[s, a] = rew_hole
                    elif letter in b'G':
                        li.append((1.0, s, 0, True))
                        self.TransitProb[a, s, nS] = 1.0
                        self.TransitReward[s, a] = rew_goal
                    else:
                        if is_slippery:
                            # for b in [(a-1)%4, a, (a+1)%4]:
                            for b, p in zip([a, (a + 1) % 4, (a + 2) % 4, (a + 3) % 4], TransitionProb):
                                newrow, newcol = inc(row, col, b)
                                newstate = to_s(newrow, newcol)
                                newletter = desc[newrow, newcol]
                                done = bytes(newletter) in b'GH'
                                # rew = float(newletter == b'G')
                                # li.append((1.0/10.0, newstate, rew, done))
                                if newletter == b'G':
                                    rew = rew_goal
                                elif newletter == b'H':
                                    rew = rew_hole
                                else:
                                    rew = rew_step
                                li.append((p, newstate, rew, done))
                                self.TransitProb[a, s, newstate] += p
                                self.TransitReward[s, a] = rew_step
                        else:
                            newrow, newcol = inc(row, col, a)
                            newstate = to_s(newrow, newcol)
                            newletter = desc[newrow, newcol]
                            done = bytes(newletter) in b'GH'
                            rew = float(newletter == b'G')
                            li.append((1.0, newstate, rew, done))

        super(FrozenLakeEnv, self).__init__(nS, nA, P, isd)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["Left", "Down", "Right", "Up"][self.lastaction]))
        else:
            outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc) + "\n")

        if mode != 'human':
            with closing(outfile):
                return outfile.getvalue()

    def GetSuccessors(self, s, a):
        next_states = np.nonzero(self.TransitProb[a, s, :])
        probs = self.TransitProb[a, s, next_states]
        return [(s, p) for s, p in zip(next_states[0], probs[0])]

    def GetTransitionProb(self, s, a, ns):
        return self.TransitProb[a, s, ns]

    def GetReward(self, s, a):
        return self.TransitReward[s, a]

    def GetStateSpace(self):
        return self.TransitProb.shape[1]

    def GetActionSpace(self):
        return self.TransitProb.shape[0]


def evaluate_policy(env, policy, trials=1000):
    total_reward = 0
    #     epoch = 10
    for _ in range(trials):
        env.reset()
        done = False
        observation, reward, done, info = env.step(policy[0])
        total_reward += reward
        while not done:
            observation, reward, done, info = env.step(policy[observation])
            total_reward += reward
    return total_reward / trials


def evaluate_policy_discounted(env, policy, discount_factor, trials=1000):
    epoch = 10
    reward_list = []

    for _ in range(trials):
        total_reward = 0
        trial_count = 0
        env.reset()
        done = False
        observation, reward, done, info = env.step(policy[0])
        total_reward += reward
        while not done:
            observation, reward, done, info = env.step(policy[observation])
            total_reward += (discount_factor ** trial_count) * reward
            trial_count += 1
        reward_list.append(total_reward)

    return mean(reward_list)


def print_results(v, pi, map_size, env, beta, name):
    v_np, pi_np = np.array(v), np.array(pi)
    print("\nState Value:\n")
    print(np.array(v_np[:-1]).reshape((map_size, map_size)))
    print("\nPolicy:\n")
    print(np.array(pi_np[:-1]).reshape((map_size, map_size)))
    print("\nAverage reward: {}\n".format(evaluate_policy(env, pi)))
    print("Avereage discounted reward: {}\n".format(evaluate_policy_discounted(env, pi, discount_factor=beta)))
    print("State Value image view:\n")
    plt.imshow(np.array(v_np[:-1]).reshape((map_size, map_size)))

    pickle.dump(v, open(name + "_" + str(map_size) + "_v.pkl", "wb"))
    pickle.dump(pi, open(name + "_" + str(map_size) + "_pi.pkl", "wb"))


def save_and_print_results(v, pi, MAP, env, beta, name, show_val=False, show_pi=False,
                           results_dir="results/frozen_lake/"):
    map_size = len(MAP)
    v_np, pi_np = np.array(v), np.array(pi)
    if (show_val):
        print("\nState Value:\n")
        print(np.array(v_np[:-1]).reshape((map_size, map_size)))
    if (show_pi):
        print("\nPolicy:\n")
        print(np.array(pi_np[:-1]).reshape((map_size, map_size)))
    print("\nAverage reward: {}\n".format(evaluate_policy(env, pi)))
    print("Avereage discounted reward: {}\n".format(evaluate_policy_discounted(env, pi, discount_factor=beta)))
    print("State Value image view:\n")

    plt.imshow(np.array(v_np[:-1]).reshape((map_size, map_size)))

    # print(np.array(v_np[:-1]).reshape((map_size, map_size)).shape)
    # print(rescale_data(np.array(v_np[:-1]).reshape((map_size, map_size))).shape)
    # #     input()
    plt.imsave(results_dir + "value_" + str(map_size) + ".png", rescale_data(np.array(v_np[:-1]).reshape((map_size, map_size))))
    pickle.dump(v, open(results_dir + name + "_" + str(map_size) + "_v.pkl", "wb"))
    pickle.dump(pi, open(results_dir + name + "_" + str(map_size) + "_pi.pkl", "wb"))

    plot_and_save_policy_image(v,pi,MAP,results_dir)

def save_results(v, map_size):
    v_np = np.array(v)
    plt.imsave("latest_fig.png", np.array(v_np[:-1]).reshape((map_size, map_size)), dpi=400)

def rescale_data(data):
    scale = int(800/len(data))
    new_data = np.zeros(np.array(data.shape) * scale)
    for j in range(data.shape[0]):
        for k in range(data.shape[1]):
            new_data[j * scale: (j+1) * scale, k * scale: (k+1) * scale] = data[j, k]
    return new_data


def plot_and_save_policy_image(value, pi, MAP, results_dir="results/frozen_lake/"):
    best_value = np.array(value[:-1]).reshape(len(MAP), len(MAP))
    best_policy = np.array(pi[:-1]).reshape(len(MAP), len(MAP))

    print("\n\nBest Q-value and Policy:\n")
    fig, ax = plt.subplots()
    im = ax.imshow(best_value)

    for i in range(best_value.shape[0]):
        for j in range(best_value.shape[1]):
            if MAP[i][j] in 'GH':
                arrow = MAP[i][j]
            elif best_policy[i, j] == 0:
                arrow = '<'
            elif best_policy[i, j] == 1:
                arrow = 'v'
            elif best_policy[i, j] == 2:
                arrow = '>'
            elif best_policy[i, j] == 3:
                arrow = '^'
            if MAP[i][j] in 'S':
                arrow = 'S ' + arrow
            text = ax.text(j, i, arrow,
                           ha="center", va="center", color="black")

    cbar = ax.figure.colorbar(im, ax=ax)

    fig.tight_layout()
    plt.savefig(results_dir + "policy_" + str(len(MAP)) + ".png",)  # , rescale_data(np.array(v_np[:-1]).reshape((map_size, map_size))))
    plt.show()


