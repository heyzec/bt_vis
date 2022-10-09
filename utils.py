
def invert_action(action: list[list[int]]) -> list[list[int]]:
    src, dst = action
    return [[5 - src[0], src[1]], [5 - dst[0], dst[1]]]
