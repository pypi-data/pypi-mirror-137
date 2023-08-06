from b2tsf.track_segment_finder_LUT5 import TrackSegmentFinderLUT5
from b2tsf.track_segment_finder_LUT9 import TrackSegmentFinderLUT9
from b2tsf.track_segment_finder_LUT12 import TrackSegmentFinderLUT12
from b2tsf.track_segment_finder_hourglas import TrackSegmentFinderHourglas

class TrackSegmentFinder:
    """
    Class TrackSegmentFinder instantiates any necessary track segment
    finders and returns them to the end user. Multiple functions are hidden
    behind generic caller functions and type of function call or track
    segment finder is defined by mode parameter.
    ---------------------------------------------------------------------------
    Possible modes for constructor:
    ---------------------------------------------------------------------------

    """
    def __init__(self,mode,**kwargs):
        """
        mode='Unger':   Not yet implemented

        mode='LUT':     Baseline algorithm implementing 5 bit bin look up tables.

        mode='LUT9':    Algorithm implementing 9 bit bin look up tables.

        mode='LUT12':   Algorithm implementing 12 bit bin look up tables.

        mode='Neuro':   Not yet implemented
        """
        if(mode == 'hourglas'):
            if 'lr_lut_path' in kwargs.keys():
                self._tsf = TrackSegmentFinderHourglas(lr_lut_path=kwargs['lr_lut_path'])
            else:
                warnings.warn("No 'lr_lut_path' declared. Fallback to default path.")
                self._tsf = TrackSegmentFinderHourglas()
        elif(mode == 'LUT5'):
            self._tsf = TrackSegmentFinderLUT5()
        elif(mode == 'LUT9'):
            self._tsf = TrackSegmentFinderLUT9()
        elif(mode == 'LUT12'):
            self._tsf = TrackSegmentFinderLUT12()
        else:
            raise ValueError(mode)
        self.mode = mode


    def set_patterns(self,binmode,patterns_lower,patterns_upper):
        """
        Callable from track segment finder in mode 'LUT9'. Throws warning
        otherwise. Gives access to dictionary setting of LUT9 track segement
        finder.
        """
        if(self.mode == 'LUT9'):
            self._tsf = self._tsf.set_patterns(binmode,
                                               patterns_lower,
                                               patterns_upper)
        elif(self.mode == 'LUT12'):
            self._tsf = self._tsf.set_patterns(binmode,
                                               patterns_lower,
                                               patterns_upper)
        else:
            warnings.warn("This TSF mode can not be configured.")
        return self


    def get_hit_list(self,format='native'):
        """
        Returns list of hits, e.g. datapoints of internal cdc frame. Data format
        can be choosen between 'native' and 'r_theta'.
        """
        return self._tsf.get_frame().get_hit_list(format)


    def get_number_of_hits(self):
        """
        Returns number of hits. Throws warning if mode is not set to 'hits' for
        track segment finder. In this case number of possible hit map hits would be
        reported.
        """
        n_hits = self._tsf.get_frame().get_number_of_hits()

        if(self._tsf.mode == 'hits'):
            pass
        else:
            warnings.warn("TSF mode is not set to 'hits'. This can lead to unwanted behavior.")

        return n_hits


    def detect(self,frame_in,mode='hits',edge_hit=True):
        """
        Detect hits and returns internal frame as out frame.
        """
        return self._tsf.detect(frame_in,mode,edge_hit)


    def get_segment_dword(self,segment_id):
        """
        Returns the output of one processed segment by natively given out a 32
        list with '0' or '1' whether the respective hit bin has been hit. For
        data format description see thesis.
        """
        return self._tsf.get_segment_dword(segment_id)


    def hit_compaction(self):
        """
        Performs stream compaction algorithm and returns resulting list of tsf
        hit ids. List for each layer returns up to n_tsout elements.
        """
        return self._tsf.hit_compaction()


    def get_n_tsout(self):
        """
        Returns hardware design parameter n_tsout. This resembles the maximum
        number of tsf hits that can be sent per layer per hw clock cycle.
        """
        if(self.mode == 'LUT5'):
            return self._tsf.get_n_tsout()
        elif(self.mode == 'LUT9'):
            return self._tsf.get_n_tsout()
        elif(self.mode == 'LUT12'):
            return self._tsf.get_n_tsout()
        else:
            ValueError(f"Function get_n_tsout not avaible for mode {self.mode}")


    def clear(self):
        """
        Clears data without recreating the TrackSegmentFinder object.
        """
        return self._tsf.clear()
