class LutConfig:
    """
    LutConfig creates a config class for LUT TrackSegmentFinder. It provides
    interfaces to save a configuration and to export it to a BRAM initialization
    file for Xilinx Ultrascale 7 FPGAs.
    """
    def __init__(self,size):
        if(size in range(16)):
            self._size = size
            self._n_bins = 2 ** size
            self._lutlist = [0 for i in range(self._n_bins)]
            self._patterns = []
        else:
            raise ValueError("size parameter to large or negativ. Choose a value in range(0,16).")

    def _list_from_file(self,path):
        """
        Helper function to read list object from file.
        """
        lines = []
        with open(path) as file_ptr:
            for line in file_ptr:
                line = line.strip()
                lines.append(line)
        return lines


    def _list_to_file(self,path,list_in):
        """
        Helper function to read list object from file.
        """
        with open(path, "w") as f:
            for line in list_in:
                f.write(f"{line}\n")


    def set_patterns(self,patterns):
        """
        Sets pattern object and updates internal data structure.
        """
        self._patterns = patterns
        for i in range(self._n_bins):
            self._lutlist[i] = f"{i:0{self._size:d}b}" in patterns


    def get_patterns(self):
        """
        Returns pattern object.
        """
        return self._patterns

    def add_pattern(self,pattern):
        """
        Adds a single pattern to the LutConfig Object.
        Parameter pattern: String with <size> number of chars, e.g.
        '1001' for size = 4.
        """
        self._patterns = self._patterns + [pattern]
        i = int(pattern, 2)
        self._lutlist[i] = 1


    def write_init(self,path):
        """
        Writes ram init configuration file for Xilinx Ultrascale 7 FPGAs.
        """
        file_path = f"{path}.init"
        with open(file_path,"w") as file_ptr:
            for data_line in self._lutlist:
                file_ptr.write(f"{data_line:1d}\n")


    def write_config(self,path):
        """
        Writes human readable config file under given <path>. Backwards
        compatible.
        """
        self._list_to_file(path,self._patterns)


    def read_config(self,path,n_patterns):
        """
        Reads human readable config file under given <path>. Backwards
        compatible. Read n patterns from file
        """
        new_patterns = self._list_from_file(path)[:n_patterns]
        if(self._n_bins >= n_patterns):
            self.set_patterns(new_patterns)
            return self
        else:
            raise ValueError("Config File length does not match LUTConfig size.")
