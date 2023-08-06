import time
from typing import NewType

return_value = NewType("retval", any)

class SupportedInstruction(object):

    """
    This is a(n) implementation of a Supported Instruction

    var: 'sequence' making it a supported task, used to define functions to call
    var: 'value' corresponding to the processes output result, if any

    the only restriction you are limited to, is making sure sequence is defined
    """

    def __init__(self):
        """ DO NOT INITIALIZE THIS CLASS """
        self.instruction_cycle = hex(int(time.time())).replace("0x", "")
        self.sequence = [lambda: None, lambda: 1, lambda: 2]
        self.value : return_value = -1

class Instruction(object):

    @property
    def IsFinished(self):
        return self.sequence_cycle == len(self.sequence)

    def __call__(self):
        """[ New instruction for a Pipeline ]

        The Instruction Object is sent as the FIRST parameter of the function, that way we can set the instructions output value [self.value]
        """
        if(self.sequence_cycle == len(self.sequence)): return 

        else:
            self.value = self.sequence[self.sequence_cycle](self)
            self.sequence_cycle += 1

    def __init__(self, clock_cycle: int, sequence: list):
        self.instruction_cycle = clock_cycle
        self.sequence = sequence

        self.sequence_cycle = 0
        self.value : return_value = -1
