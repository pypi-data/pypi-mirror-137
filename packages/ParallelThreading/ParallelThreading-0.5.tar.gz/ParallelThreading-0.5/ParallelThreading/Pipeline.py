import time
from threading import Thread
from InstructionImplement import SupportedInstruction, Instruction

class Registry(object):

    def __init__(self):
        self.data_section = {}

    def NewEntry(self, instruction: object):
        self.data_section.update({instruction: instruction.value})

class ParallelPipeline(Thread):

    @property
    def isIdling(self):
        """
        Returns:
            [bool]: A boolean is returned representing whether or not the pipeline is idling
        """
        return self.p_Idling

    @property
    def Closed(self):
        """
        Returns:
            [bool]: A boolean is returned representing whether or not the pipeline is closed
        """
        return self.p_Closed
    
    @property
    def Population(self):
        """
        Returns:
            [int]: Length of Pipeline Material
        """
        return len(self.p_Material)

    @property
    def WindowSize(self):
        return self.p_InstructionWindow

    def __init__(self, instruction_window: int = -1):
        """[ Constructor for Pipeline ]

        Args:
            instruction_window ([int]): how many instructions to process at a given time, -1 to cycle the entire material window
        """
        Thread.__init__(self, name="PPT->" + hex(id(self)))
        
        self.p_Idling = True
        self.p_Closed = False

        self.p_Material = []
        self.p_InstructionWindow = instruction_window

        self.p_Registry = Registry()

    def SetWindowSize(self, x: int):
        self.p_InstructionWindow = x

    def Close(self):
        """[ Close the Pipeline from Processing anymore Instructions ]
        """
        self.p_Closed = True

    def Destroy(self, instruction: SupportedInstruction):
        """[ Destroys Materialized Instruction ]

        Args:
            instruction (SupportedInstruction): a given instruction to be removed, regardless if it has processed completely or not
        """
        if(instruction in self.p_Material): self.p_Material.remove(instruction)

    def Materialize(self, instruction: SupportedInstruction):
        """[ Materliazes Instruction to Pipeline for Processing ]

        Args:
            instruction (SupportedInstruction): a given instruction that is supported to store in the data register

        Raises:
            AttributeError: raised if the instruction does not have a sequence attribute to fetch from
        """
        if(not hasattr(instruction, 'sequence')):
            raise AttributeError("instruction does not have a sequence[list] attribute")

        self.p_Material.append(instruction)

    def _IdleThread(self):
        """ DO NOT CALL THIS FUNCTION | This is to be called internally when the pipeline lays idle, reducing the time at how fast it iterates in the loop."""
        self.p_Idling = True
        time.sleep(0.0000000000000000000000000001)

    def run(self):
        while(not self.p_Closed):
            if(len(self.p_Material) == 0):
                self._IdleThread()

            finished_instructions = [
                [print(instruction.value), instruction][1]
                for instruction in self.p_Material
                if(hasattr(instruction, 'IsFinished') and instruction.IsFinished)
            ]
            
            [self.Destroy(instruction) for instruction in finished_instructions]
            [self.p_Registry.NewEntry(instruction) for instruction in finished_instructions]

            [instruction_stage_execute() for instruction_stage_execute in self.p_Material[:self.p_InstructionWindow if(self.p_InstructionWindow != -1) else len(self.p_Material)]]


def NewInstruction(pipeline: ParallelPipeline, process_sequence: list):
    """[ Returns new Instruction Set ]

    Args:
        process_sequence (list[function, ]): List of functions to process in an instruction
    """

    inst = Instruction(hex(int(time.time())).replace("0x", ""), process_sequence)
    pipeline.Materialize(inst)
    return inst

p = ParallelPipeline()
p.start()

[NewInstruction(p, [lambda x: x.value + 5, lambda x: x.value + 15]) for _ in range(1024)]
