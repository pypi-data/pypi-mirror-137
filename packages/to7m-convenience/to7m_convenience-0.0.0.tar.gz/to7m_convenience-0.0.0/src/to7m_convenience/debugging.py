from time import sleep
import inspect

from .simple_functions import fnn


DPP_DELAY = 0
DPP_STR = "*** <delay-padded print at line {lineno}, in {filename}> ***"


def dpp(delay_before=None, delay_after=None, additional_frames=0):
    """
    Delay-padded print. Prints a string indicating line number, with an
    optional delay either side when dealing with other code which may also
    print.
    """

    sleep(fnn(delay_before, DPP_DELAY))
    frame = inspect.stack()[additional_frames + 1]
    print(DPP_STR.format(lineno=frame.lineno, filename=frame.filename))
    sleep(fnn(delay_after, delay_before, DPP_DELAY))
