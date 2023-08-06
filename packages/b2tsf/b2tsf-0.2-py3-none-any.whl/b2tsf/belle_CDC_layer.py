#Author: Marc Neu
#Date: 01.12.2021

import numpy

class CDCLayer:
    """
    The class CDCLayer represents a superlayer inside the Belle-II Detector.
    The hit data is packed into a numpy array for better performance. Mind
    that the data format is choosen to keep a direct connection to the hardware
    implementation. Therefore segments for each layer are defined.
    ---------------------------------------------------------------------------
    Attributes:
    ---------------------------------------------------------------------------
    layer_id:   Defines physical position inside the detector. Belle-II
                detector currently features 9 superlayers with predefined
                segment numbers.

    n_rows:     Number of rows. Predefined to 6 for inner layer and 8 for outer
                layers.

    n_cols:     16 columns per segment. Predefined by trigger data format

    n_segs:     Number of segemnts. Defined by layer ID.

    n_wires:    Total number of wires inside specified layer

    _segments: Data storage for hit values. 3D numpy arrays contains data for
                the whole layer. Indices are [segment_id,row_id,column_id].
    """

    def __init__(self, layer_id=0):
        self.layer_id = layer_id
        self.n_rows = self.get_nrows(layer_id)
        self.n_cols = 16
        self.n_segs = self.get_nsegs(layer_id)
        self.n_wires = self.n_rows*self.n_cols*self.n_segs
        self._segments = numpy.zeros(shape=(self.n_segs,self.n_rows,self.n_cols),dtype=int)

    def get_nrows(self,layer_id):
        if(layer_id == 0):
            return 8
        elif(layer_id == 1):
            return 6
        elif(layer_id == 2):
            return 6
        elif(layer_id == 3):
            return 6
        elif(layer_id == 4):
            return 6
        elif(layer_id == 5):
            return 6
        elif(layer_id == 6):
            return 6
        elif(layer_id == 7):
            return 6
        elif(layer_id == 8):
            return 6
        else:
            raise InitializationError('CDCLayer ID out of predefined boundary 0 to 8.')

    def get_nsegs(self,layer_id):
        if(layer_id == 0):
            return 10
        elif(layer_id == 1):
            return 10
        elif(layer_id == 2):
            return 12
        elif(layer_id == 3):
            return 14
        elif(layer_id == 4):
            return 16
        elif(layer_id == 5):
            return 18
        elif(layer_id == 6):
            return 20
        elif(layer_id == 7):
            return 22
        elif(layer_id == 8):
            return 24
        else:
            raise InitializationError('CDCLayer ID out of predefined boundary 0 to 8.')


    def get_tsf_segment_list(self):
        """
        get_tsf_segment_list returns a list of all segments in the layer. Each segment consists of a 2D array.
        Only returns the 5 layers which are used for the trigger detection.
        """
        new_list = [self._segments[j,0:5,:] for j in range(self.n_segs)]
        return new_list

    def get_segment_list(self):
        """
        Returns a list of all segemnts in the layer. Each segment consists of a 2D array.
        """
        new_list = [self._segments[j,:,:] for j in range(self.n_segs)]
        return new_list


    def get_tsf_segments(self):
        """
        Native access to data. Only returns 5 layers which are used for the trigger detection
        """
        return self._segments[:,0:5,:]


    def get_segments(self):
        """
        Return reference to interal data structure
        """
        return self._segments


    def get_tsf_segment(self,segment_id):
        """
        Native access to data. Only returns 5 layers which are used for the trigger detection
        """
        return self._segments[segment_id,0:5,:]


    def get_segment(self,segment_id):
        """
        Return reference to interal data structure
        """
        return self._segments[segment_id,:,:]

    def fill(self):
        """
        Fills hit data from layer by setting all wires to 1.
        """
        self._segments.fill(1)
        return self


    def clear(self):
        """
        Clear hit data from layer by filling all values with 0.
        """
        self._segments.fill(0)
        return self


    def copy(self,other):
        """
        Deep copy of <other> layer data (no reference).
        """
        self.layer_id = other.layer_id
        self.n_rows = self.get_nrows(other.layer_id)
        self.n_cols = 16
        self.n_segs = self.get_nsegs(other.layer_id)
        self.n_wires = self.n_rows*self.n_cols*self.n_segs
        self._segments = numpy.copy(other.get_segments())
        return self


    def logical_and(self,other):
        """
        Perform elementwise logical and on layer hit data and save result in this frame.
        """
        numpy.logical_and(self._segments,other.get_segments(),out=self._segments)
        return self


    def logical_or(self, other):
        """
        Perform elementwise logical or on layer hit data and save result in this frame.
        """
        numpy.logical_or(self._segments,other.get_segments(),out=self._segments)
        return self
