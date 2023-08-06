from b2tsf.tsf_processor_ref_testbench_writer import TSFProcessorRefTestbenchWriter
from b2tsf.tsf_processor_stimuli_testbench_writer import TSFProcessorStimuliTestbenchWriter
from b2tsf.merger_processor_ref_testbench_writer import MergerProcessorRefTestbenchWriter
from b2tsf.merger_processor_stimuli_testbench_writer import MergerProcessorStimuliTestbenchWriter

class TestbenchWriterFactory:
    """
    Factory class for independend use of TestbenchWriters. Mode defines the type
    of the writer as in
    mode == 'tsf_processor_ref'

    mode == 'merger_processor_ref'

    mode == 'tsf_processor_stimuli'

    mode == 'merger_processor_stimuli'
    """

    def __init__(self):
       pass


    def get_writer(self,mode='tsf_processor_stimuli'):
        if(mode == 'tsf_processor_ref'):
            return TSFProcessorRefTestbenchWriter()
        elif(mode == 'merger_processor_ref'):
            return MergerProcessorRefTestbenchWriter()
        elif(mode == 'tsf_processor_stimuli'):
            return TSFProcessorStimuliTestbenchWriter()
        elif(mode == 'merger_processor_stimuli'):
            return MergerProcessorStimuliTestbenchWriter()
        else:
            ValueError("TestbenchWriter of mode" + mode + "is unknown.")
