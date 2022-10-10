"""Useful helper functions."""

def invert_action(action: list[list[int]]) -> list[list[int]]:
    """Given a raw action, returns its inverted form.

    The inverted form is one that correctly applies the move to an inverted board.
    """
    src, dst = action
    return [[5 - src[0], src[1]], [5 - dst[0], dst[1]]]
