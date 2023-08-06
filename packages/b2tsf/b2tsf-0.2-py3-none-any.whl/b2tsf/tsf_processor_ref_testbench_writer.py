from datetime import date


class TSFProcessorRefTestbenchWriter:
    """
    TSFProcessorTestbenchWriter reads in a sequence of tsf hit lists and writes
    them to a specific path.
    ----------------------------------------------------------------------------
    Methods:
    ----------------------------------------------------------------------------
    set_sequence(data)
        Accepts 3rd order list of order hit_list = data[sequence_step,layer_id]
        as parameter <data>.

    write_layer(path,filename,layer_id,n_hits)
        Writes data defined with set_sequence before to a file named filename
        under path, writing only layer with layer_id and filling up hit_lists
        with 0s up to n_hits.
    """

    def __init__(self):
        """
        Basic setup of textual parameters.
        """
        self.mode = 'tsf_processor_ref'
        self.offset = 0
        #TODO: Retrieve from Package
        self.version = 0.1
        self.date = '{:%Y-%m-%d}'.format(date.today())
        self.author = 'Marc Neu'
        self._intro_text = "#FileWriter V. {version} generating a {mode} file\n#\n#Author: {author}\n#Date: {date}\n#\n".format(version=self.version,date=self.date,author=self.author,mode=self.mode)
        self._outro_text = "#EOF."


    def set_sequence(self, data):
        """
        Accepts 3rd order list of order hit_list = data[sequence_step,layer_id]
        as parameter <data>.
        """
        self._data = data
        return self


    def set_offset(self, offset):
        """
        Sets delay of output lines in the model checker
        compared to the actual stimuli values.
        Can be used to model latency.
        Empty lines are filled with 0's.
        """
        self._offset = offset


    def _gen_line(self,hit_ids,n_hits):
        """
        Reads tsf output data and creates a string in a predefined format
        (see thesis)
        """
        hit_list = hit_ids.copy()
        hit_list.reverse()
        hit_list = [0] * (n_hits - len(hit_ids)) + hit_list
        reference_string = ''.join(f'{item:0>10b}' for item in hit_list)

        return reference_string


    def _write_layer(self,path,filename,layer_id,n_hits):
        """
        Writes a all segments of the specified layer to a file under <path>
        """
        file_path = "{path}{filename}_{id:d}.dat".format(path=path,filename=filename,id=layer_id)

        with open(file_path,"w") as file_ptr:
            file_ptr.write(self._intro_text)

            for i in range(self._offset):
                file_ptr.write(f":empty\n")

            for sim_frame in self._data:
                hit_ids = sim_frame[layer_id]
                data_line = self._gen_line(hit_ids,n_hits)
                file_ptr.write(data_line + "\n")

            file_ptr.write(self._outro_text)

    def write_layer(self,path,filename,layer_id,n_hits):
        """
        Writes data defined with set_sequence before to a file named filename
        under path, writing only layer with layer_id and filling up hit_lists
        with 0s up to n_hits.
        """
        self._write_layer(path,filename,layer_id,n_hits)
