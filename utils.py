
def invert_action(action):
    src, dst = action
    return [[5 - src[0], src[1]], [5 - dst[0], dst[1]]]
