import matplotlib.pyplot as plt
import numpy as np
import scipy

def find_all_reaction(train, bridge, x_t):
    global bdy1_whl1, bdy1_whl2, bdy2_whl1, bdy2_whl2, bdy3_whl1, bdy3_whl2
    global load_whl, load_list
    global norm_r, norm_l

    bdy1_whl1 = x_t + train["edge"]
    bdy1_whl2 = bdy1_whl1 + train["btw_whl"]
    bdy2_whl1 = bdy1_whl2 + train["btw_train_whl"]
    bdy2_whl2 = bdy2_whl1 + train["btw_whl"]
    bdy3_whl1 = bdy2_whl2 + train["btw_train_whl"]
    bdy3_whl2 = bdy3_whl1 + train["btw_whl"]

    load_whl = train["weight"]/(3*2)
    load_list = [bdy1_whl1, bdy1_whl2, bdy2_whl1, bdy2_whl2, bdy3_whl1, bdy3_whl2]

    norm_l = (load_whl*(bdy1_whl1 + bdy1_whl2 + bdy2_whl1 + bdy2_whl2 + bdy3_whl1 + bdy3_whl2)+(bridge["weight_dis"]*bridge["length"]**2)/2)/bridge["length"]
    norm_r = train["weight"] + bridge["weight_dis"]*bridge["length"] - norm_l
    return

def I(bridge):
    return 40**4/12

def V(x):
    if x > bridge["length"]:
        return None

    shear_force = 0
    if x > 0:
        shear_force += norm_r
    for force_loc in load_list:
        if force_loc < x:
            shear_force -= load_whl
    if x == bridge["length"]:
        shear_force += norm_l

    return shear_force

def M1(x):
    if x > bridge["length"]:
        return None
    res, err = scipy.integrate.quad(V, 0, x)
    return res

def M(x):
    if x > bridge["length"]:
        return None
    if x == 0:
        return 0
    n = x
    dx = x/n
    moment = 0
    for i in range(0, x+1):
        moment += V(i)
    return moment


def N(train, bridge, x_t, x):
    pass

def plot(range_x, f_x):
    x = []
    y = []
    for i in range(range_x[0], range_x[1]+1):
        x.append(i)
        y.append(f_x(i))
    plt.plot(x, y)

def F(x):
    return x**2

if __name__ == '__main__':
    train = {"weight": 400, "height": 85, "width": 75, "whl_width": 10, "btw_whl": 176, "edge": 52, "btw_train_whl": 164}
    bridge = {"length": 1250, "weight_dis": 0}
    for x_t in range(700):
        find_all_reaction(train, bridge, x_t)
        plot((0, 1250), M)
    plt.show()
