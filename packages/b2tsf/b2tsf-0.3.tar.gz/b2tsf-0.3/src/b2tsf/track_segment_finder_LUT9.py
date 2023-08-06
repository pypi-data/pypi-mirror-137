import numpy
from bitarray import bitarray
from bitarray import frozenbitarray
import warnings
from b2tsf.belle_CDC_frame import CDCFrame

class TrackSegmentFinderLUT9:
    """
    Track Segement Finder implementing a 9 bit look up table solution.

    ---------------------------------------------------------------------------
    Methods:
    ---------------------------------------------------------------------------
    detect:     Detects hits in incoming frame <frame_in> and saves result in
                internal data strucutre. Two possible detetction modes are
                available. 'hits' returns real hardware hits whereas 'candidates'
                returns all hit candidates of a hit bin.

    get_frame:  Retruns internal data frame as reference.

    clear:      Clears internal data structure.

    """
    def __init__(self):
        self._frame_out = CDCFrame(0)
        self._binsize = 9
        self._binnumber = 16
        self._binlayer = 2
        self.mode = 'hits'

        self._init = False
        self._frame_in = None
        self._frame_in_delayed = None
        self._cooldown_array = None
        self._cooldown = 64
        self._n_tsout = 24


    def _init_patterns(self,patterns):
        """
        Configure detection patterns during track segment finder construction. True
        candidate patterns are given as string list in the format defined in thesis
        documenation. As keys must be constant to be hashable this function must be
        be called seperately.
        Returns dict of bit patterns.
        """
        keys = []
        values = []
        for i in range(2**self._binsize):
            key_pattern = f'{i:09b}'
            keys.append(frozenbitarray(key_pattern))
            values.append(key_pattern in patterns)
        return dict(zip(keys,values))


    def _detect_hit(self,hitmap_zip,seg_hits):
        """
        Implementation of per bin detetion algorithm, e.g. checking against
        look up table in form of a hash map. hitmap_zip contains both bins
        for upper and lower hitmap.
        This function requires a predefined array for performance reasons. This
        way the creation of many small arrays can be avoided by slicing.
        """
        hitmap_lower, hitmap_upper = hitmap_zip
        if(self._binmode == 'lower' or self._binmode == 'both'):
            for i in range(self._binnumber):
                seg_hits[0,i] = self._patterns_lower[hitmap_lower[i]]
        if(self._binmode == 'upper' or self._binmode == 'both'):
            for i in range(self._binnumber):
                seg_hits[1,i] = self._patterns_upper[hitmap_upper[i]]
        return seg_hits


    def _populate_bin(self,seg_pre, seg_act, seg_suc, edge_hit):
        """
        Populate bins for detection algorithm. Each segment has got 16 bins in 2 layers
        as specified in the alogrithm description in thesis. Furthermore edge_hits of
        sectors can be toggeled on/off.
        This function returns bins of a layer segment.
        """
        hit_bin_lower = [self._binsize * bitarray() for i in range(self._binnumber)]
        hit_bin_upper = [self._binsize * bitarray() for i in range(self._binnumber)]
        #Fill lower bins
        if(self._binmode == 'lower' or self._binmode == 'both'):
            if(edge_hit):
                hit_bin_lower[0] = frozenbitarray([
                    seg_act[2,1],seg_act[2,0],
                    seg_act[1,1],seg_act[1,0],seg_pre[1,15],
                    seg_act[0,2],seg_act[0,1],seg_act[0,0],seg_pre[0,15]])
                hit_bin_lower[14] = frozenbitarray([
                    seg_act[2,15],seg_act[2,14],
                    seg_act[1,15],seg_act[1,14],seg_act[1,13],
                    seg_suc[0,0],seg_act[0,15],seg_act[0,14],seg_act[0,13]])
                hit_bin_lower[15] = frozenbitarray([
                    seg_suc[2,0],seg_act[2,15],
                    seg_suc[1,0],seg_act[1,15],seg_act[1,14],
                    seg_suc[0,1],seg_suc[0,0],seg_act[0,15],seg_act[0,14]])
            else:
                hit_bin_lower[0] = frozenbitarray([
                    seg_act[2,1],seg_act[2,0],
                    seg_act[1,1],seg_act[1,0],0,
                    seg_act[0,2],seg_act[0,1],seg_act[0,0],0])
                hit_bin_lower[14] = frozenbitarray([
                    seg_act[2,15],seg_act[2,14],
                    seg_act[1,15],seg_act[1,14],seg_act[1,13],
                    0,seg_act[0,15],seg_act[0,14],seg_act[0,13]])
                hit_bin_lower[15] = frozenbitarray([
                    0,seg_act[2,15],
                    0,seg_act[1,15],seg_act[1,14],
                    0,0,seg_act[0,15],seg_act[0,14]])

            for i in range(1,self._binnumber-2):
                hit_bin_lower[i] = frozenbitarray([
                    seg_act[2,i+1],seg_act[2,i],
                    seg_act[1,i+1],seg_act[1,i],seg_act[1,i-1],
                    seg_act[0,i+2],seg_act[0,i+1],seg_act[0,i],seg_act[0,i-1]])
        #Fill upper bins
        if(self._binmode == 'upper' or self._binmode == 'both'):
            if(edge_hit):
                hit_bin_upper[0] = frozenbitarray([
                    seg_act[4,2],seg_act[4,1],seg_act[4,0],seg_pre[4,15],
                    seg_act[3,1],seg_act[3,0],seg_pre[3,15],
                    seg_act[2,1],seg_act[2,0]])
                hit_bin_upper[14] = frozenbitarray([
                    seg_suc[4,0],seg_act[4,15],seg_act[4,14],seg_act[4,13],
                    seg_act[3,15],seg_act[3,14],seg_act[3,13],
                    seg_act[2,15],seg_act[2,14]])
                hit_bin_upper[15] = frozenbitarray([
                    seg_suc[4,1],seg_suc[4,0],seg_act[4,15],seg_act[4,14],
                    seg_suc[3,0],seg_act[3,15],seg_act[3,14],
                    seg_suc[2,0],seg_act[2,15]])
            else:
                hit_bin_upper[0] = frozenbitarray([
                    seg_act[4,2],seg_act[4,1],seg_act[4,0],0,
                    seg_act[3,1],seg_act[3,0],0,
                    seg_act[2,1],seg_act[2,0]])
                hit_bin_upper[14] = frozenbitarray([
                    0,seg_act[4,15],seg_act[4,14],seg_act[4,13],
                    seg_act[3,15],seg_act[3,14],seg_act[3,13],
                    seg_act[2,15],seg_act[2,14]])
                hit_bin_upper[15] = frozenbitarray([
                    0,0,seg_act[4,15],seg_act[4,14],
                    0,seg_act[3,15],seg_act[3,14],
                    0,seg_act[2,15]])

            for i in range(1,self._binnumber-2):
                hit_bin_upper[i] = frozenbitarray([
                    seg_act[4,i+2],seg_act[4,i+1],seg_act[4,i],seg_act[4,i-1],
                    seg_act[3,i+1],seg_act[3,i],seg_act[3,i-1],
                    seg_act[2,i+1],seg_act[2,i]])

        return (hit_bin_lower,hit_bin_upper)


    def _check_layer_hit(self,layer_in, edge_hit):
        """
        Checks frame layer <layer_in> for hits. Using edge_hit True/False segment edge mode can be
        choosen. For production use edge_hit=True as non edge_hit is only used for hardware module
        testing.
        """
        n_segs = layer_in.n_segs
        hits = numpy.zeros(shape=(n_segs,self._binlayer,self._binnumber),dtype=int)
        #Segment 0
        seg_pre = layer_in.get_segment(n_segs-1)
        seg_act = layer_in.get_segment(0)
        seg_suc = layer_in.get_segment(1)
        hit_bin = self._populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
        hits[0,:,:] = self._detect_hit(hit_bin, hits[0,:,:])
        #Inner segments
        for i in range (1,n_segs-1):
            seg_pre = layer_in.get_segment(i-1)
            seg_act = layer_in.get_segment(i)
            seg_suc = layer_in.get_segment(i+1)
            hit_bin = self._populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
            hits[i,:,:] = self._detect_hit(hit_bin, hits[i,:,:])
        #Segment n_seg
        seg_pre = layer_in.get_segment(n_segs-2)
        seg_act = layer_in.get_segment(n_segs-1)
        seg_suc = layer_in.get_segment(0)
        hit_bin = self._populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
        hits[-1,:,:] = self._detect_hit(hit_bin, hits[-1,:,:])

        return hits

    def _detect_hits(self,frame_in,edge_hit=True):
        """
        Detects hits of all layers in <frame_in> and saves output in tsf frame.
        Hardcoded to layer 1...8, because hardware implementation for layer 0 is
        non existent. This feature could be implemented later.

        Step 1: Calculate hits for each layer. Returns 2D Array of hits
                with indices <segment_id> whose range depends on the layer
                and 0...31 for each checked hit bin inside the dection algorithm.
                E.g. Bin 5 in Segment 3 was hit => hits[2,4] == True

        Step 2: Find all hits and fill output frame accordingly.
        """
        self._frame_in = frame_in
        for layer_id in range(1,9):
            layer_in = frame_in.get_layer(layer_id)
            layer_segments = self._frame_out.get_layer(layer_id).get_tsf_segments()
            #Calculate hits of layer
            hits = self._check_layer_hit(layer_in,edge_hit)
            (seg_id_list,row_id_list,col_id_list) = numpy.nonzero(hits)
            for seg_id,up_lo_id,col_id in zip(seg_id_list,row_id_list,col_id_list):
                #Remove if row_id
                layer_segments[seg_id,1+2*up_lo_id,col_id] = 1
        return self._frame_out

    def _detect_candidates(self,frame_in,edge_hit=True):
        """
        Detects hits of all layers in <frame_in> and saves output in tsf frame.
        Hardcoded to layer 1...8, because hardware implementation for layer 0 is
        non existent. This feature could be implemented later.

        Step 1: Calculate hits for each layer. Returns 2D Array of hits
                with indices <segment_id> whose range depends on the layer
                and 0...31 for each checked hit bin inside the dection algorithm.
                E.g. Bin 5 in Segment 3 was hit => hits[2,4] == True

        Step 2: Find all hits and fill output frame accordingly.

        Identical to _detect_hits() except that it populates all hit bin
        candidates to the internal output data frame.
        """
        self._frame_in = frame_in
        for layer_id in range(1,9):
            layer_in = frame_in.get_layer(layer_id)
            layer_segments = self._frame_out.get_layer(layer_id).get_tsf_segments()
            #Calculate hits of layer
            hits = self._check_layer_hit(layer_in,edge_hit)
            (seg_id_list,up_lo_id,col_id_list) = numpy.nonzero(hits)
            for seg_id,up_lo_id,col_id in zip(seg_id_list,up_lo_id,col_id_list):
                if(up_lo_id == 0):
                    if(col_id == 0):
                        layer_segments[seg_id-1,0,15] = 1
                        layer_segments[seg_id,0,0:3] = 1
                        layer_segments[seg_id-1,1,15] = 1
                        layer_segments[seg_id,1,0:2] = 1
                        layer_segments[seg_id,2,0:2] = 1
                    elif(col_id == 14):
                        layer_segments[seg_id,0,13:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,0,0] = 1
                        layer_segments[seg_id,1,13:] = 1
                        layer_segments[seg_id,2,14:] = 1
                    elif(col_id == 15):
                        layer_segments[seg_id,0,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,0,0:2] = 1
                        layer_segments[seg_id,1,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,1,0] = 1
                        layer_segments[seg_id,2,15] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,2,0] = 1
                    else:
                        layer_segments[seg_id,0,col_id-1:col_id+3] = 1
                        layer_segments[seg_id,1,col_id-1:col_id+2] = 1
                        layer_segments[seg_id,2,col_id:col_id+2] = 1
                if(up_lo_id == 1):
                    if(col_id == 0):
                        layer_segments[seg_id-1,4,15] = 1
                        layer_segments[seg_id,4,0:3] = 1
                        layer_segments[seg_id-1,3,15] = 1
                        layer_segments[seg_id,3,0:2] = 1
                        layer_segments[seg_id,2,0:2] = 1
                    elif(col_id == 14):
                        layer_segments[seg_id,4,13:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,4,0] = 1
                        layer_segments[seg_id,3,13:] = 1
                        layer_segments[seg_id,2,14:] = 1
                    elif(col_id == 15):
                        layer_segments[seg_id,4,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,4,0:2] = 1
                        layer_segments[seg_id,3,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,3,0] = 1
                        layer_segments[seg_id,2,15] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,2,0] = 1
                    else:
                        layer_segments[seg_id,4,col_id-1:col_id+3] = 1
                        layer_segments[seg_id,3,col_id-1:col_id+2] = 1
                        layer_segments[seg_id,2,col_id:col_id+2] = 1
        return self._frame_out


    def _detect_hw_model(self,frame_in,edge_hit=True):
        """
        Detects hit in a sequence, if Track Segment Finder is called multiple
        times. Returns frame with hit data.
        """
        if(not self._init):
            self._frame_in_delayed = CDCFrame(0)
            #24 is the maximum number of segments, e.g. n_segs in layer 9.
            self._cooldown_array = numpy.zeros(shape=(9,
                                                      24,
                                                      self._binlayer,
                                                      self._binnumber),
                                               dtype=int)
            self._init = True
        else:
            self._frame_in_delayed = self._frame_in_delayed.copy(self._frame_in)
            self._cooldown_array = numpy.where(self._cooldown_array == 0,
                                                self._cooldown_array,
                                                self._cooldown_array-1)
        self._frame_in = frame_in
        frame_work = self._frame_in_delayed.logical_or(frame_in)

        self._frame_out.clear()

        for layer_id in range(1,9):
            #frame_work
            layer_in = frame_work.get_layer(layer_id)
            layer_segments = self._frame_out.get_layer(layer_id).get_tsf_segments()
            #Calculate hits of layer
            hits = self._check_layer_hit(layer_in,edge_hit)
            (seg_id_list,row_id_list,col_id_list) = numpy.nonzero(hits)
            for seg_id,up_lo_id,col_id in zip(seg_id_list,row_id_list,col_id_list):
                if(self._cooldown_array[layer_id,seg_id,up_lo_id,col_id] == 0):
                    self._cooldown_array[layer_id,seg_id,up_lo_id,col_id] = self._cooldown
                    layer_segments[seg_id,1+up_lo_id*2,col_id] = 1
        return self._frame_out


    def get_frame(self):
        return self._frame_out


    def get_n_tsout(self):
        return self._n_tsout


    def set_patterns(self,binmode,patterns_lower,patterns_upper):
        """
        Creates patterns for lower and upper hit bins. Caution: This function is
        computational expensive!
        """
        self._binmode = binmode
        if(binmode != 'lower' and binmode != 'upper' and binmode != 'both'):
            raise ValueError(binmode)
        self._patterns_lower = self._init_patterns(patterns_lower)
        self._patterns_upper = self._init_patterns(patterns_upper)
        return self


    def detect(self,frame_in,mode='hits',edge_hit=True):
        """
        Interface function for detection algorithm.
        """
        self.mode = mode
        if(mode == 'hits'):
            return self._detect_hits(frame_in,edge_hit)
        elif(mode == 'candidates'):
            return self._detect_candidates(frame_in,edge_hit)
        elif(mode == 'hw_model'):
            return self._detect_hw_model(frame_in,edge_hit)
        else:
            raise ValueError('Mode: ' + mode + 'does not exist. See documentation for valid arguments.')

    def get_segment_dword(self,segment_id):
        """
        Returns list of segment hits as described in thesis.
        """
        dword_layer_list = []
        for work_layer in self._frame_out.get_layers():
            work_seg = work_layer.get_tsf_segment(segment_id)

            dword = numpy.zeros(self._binlayer*self._binnumber,dtype=int)
            dword[:self._binnumber] = work_seg[1,:]
            dword[self._binnumber:self._binnumber*self._binlayer] = work_seg[3,:]

            dword_layer_list.append(dword.tolist())

        return dword_layer_list


    def hit_compaction(self):
        """
        Returns compact list of hits, models stream compaction implementation.
        See master thesis for description of id sorting.
        Works on internal frame which is poulated by callind detect()
        beforehand.
        Returns:
            List of hit list of layers 0 to 9.
        """
        (layer_id_list,
         seg_id_list,
         row_id_list,
         col_id_list) = self._frame_out.get_hit_list(format='native',
                                                      detect_hit=True,
                                                      skip_inner_layer=True)
        hit_list = [[] for i in range(0,9)]

        for (layer_id,seg_id,row_id,col_id) in zip(layer_id_list,seg_id_list,row_id_list,col_id_list):
            if(row_id < 2):
                hardware_id = seg_id*self._binnumber*self._binlayer + col_id + 1
            else:
                hardware_id = seg_id*self._binnumber*self._binlayer + col_id + self._binnumber + 1
            hit_list[layer_id].append(hardware_id)


        #Hardware is only able to process n_tsout number of track segemnts. All other segments
        #are discarded

        hit_list = [hit_list[i][:self._n_tsout] for i in range(0,9)]

        return hit_list


    def clear(self):
        """
        Clears track segment finder internal files. Resets hardware sequential
        model. Returns empty output frame.
        """
        self._frame_out = self._frame_out.clear()
        self._init = False
        return self._frame_out
