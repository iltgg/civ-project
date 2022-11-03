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
    
    norm_l = (load_whl*(bdy1_whl1 + bdy1_whl2 + bdy2_whl1 + bdy2_whl2 + bdy3_whl1 + bdy3_whl2)+bridge["length"]*bridge["weight_dis"])/bridge["length"]
    norm_r = train["weight"] - norm_l
    return

def I(bridge):
    return 40**4/12

def V(x):
    global bdy1_whl1, bdy1_whl2, bdy2_whl1, bdy2_whl2, bdy3_whl1, bdy3_whl2
    if x > bridge["length"]:
        return None
            
    shear_force = 0
    for bdy_whl in load_list:
        if bdy_whl > x:
            shear_force += bdy_whl
    shear_force -= norm_l

def M(train, bridge, x_t, x):
    pass

def N(train, bridge, x_t, x):
    pass




if __name__ == '__main__':
    train = {"weight": 400, "height": 85, "width": 75, "whl_width": 10, "btw_whl": 176, "edge": 52, "btw_train_whl": 164}
    bridge = {"length": 1250, "weight_dis": 0}
    x_t = 10
