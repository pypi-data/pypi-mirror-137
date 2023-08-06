from datetime import date
import numpy

class MergerProcessorStimuliTestbenchWriter:
    """
    The TSFProcessorStimuliTestbenchWriter creates a testbench stimuli file for
    a vhdl hardware implemenation of a merger processor. The data block
    sizes is fixed to a 256 bit by use of the dword_size attribute.
    After object creation reference a CDCSequence to the TestbenchWriter and
    start the creation of the stimuli file by calling write_layer.
    ----------------------------------------------------------------------------
    Methods:
    ----------------------------------------------------------------------------
    set_sequence
        Accepts a CDCSequence object.
    write_layer
        Writes data of layer from previous defined CDCSequence to a stimuli
        file.
    """

    def __init__(self):
        self.mode = 'merger_processor_stimuli'
        self.dword_size = 256
        #TODO: Retrieve from Package
        self.version = 0.1
        self.date = '{:%Y-%m-%d}'.format(date.today())
        self.author = 'Marc Neu'
        self._intro_text = "#FileWriter V. {version} generating a {mode} file\n#\n#Author: {author}\n#Date: {date}\n#\n".format(version=self.version,date=self.date,author=self.author,mode=self.mode)
        self._outro_text = "#EOF."

    def set_sequence(self, sequence):
        """
        Configures CDCSequence which is used as data input for the test bench
        stimuli file.
        """
        self._sequence = sequence
        return self


    def _gen_line_layer_single(self,layer,segment_id):
        """
        Reads layer and converts data points of one segment into one data word.
        """
        seg = layer.get_tsf_segment(segment_id)
        dword_256 = numpy.zeros(self.dword_size,dtype=int)
        dword_256[0:80] = numpy.reshape(seg, 80)
        dword_256 = dword_256.tolist()
        dword_256.reverse()
        stimuli_string = ''.join('{:d}'.format(item) for item in dword_256)

        return stimuli_string


    def _write_layer_single(self,path,filename,layer_id,seg_id):
        """
        Writes a single segment of the specified layer to a file under <path>.
        """
        file_path = "{path}{filename}_{id:d}.dat".format(path=path,filename=filename,id=layer_id)

        with open(file_path,"w") as file_ptr:
            file_ptr.write(self._intro_text)

            for frame in self._sequence.get_frames():
                work_layer = frame.get_layer(layer_id)
                data_line = self._gen_line_layer_single(work_layer,seg_id)
                file_ptr.write(data_line + "\n")

            file_ptr.write(self._outro_text)


    def write_layer(self,path,filename,layer_id,segment_id=0):
        """
        Writes the sequence of one specified layer to a stimuli
        file under <path>.
        """
        self._write_layer_single(path,filename,layer_id,segment_id)
