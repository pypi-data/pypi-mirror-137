#Author: Marc Neu
#Date: 01.12.2021

import numpy
from b2tsf.belle_CDC_layer import CDCLayer

class CDCFrame:
    """
    The class CDCFrame represents a whole detector data frame of the Belle-II
    Detector. Automatically instantiates all necessary layers.
    ---------------------------------------------------------------------------
    Attributes:
    ---------------------------------------------------------------------------
    _layer:    Internal data structure for layers

    event_id:   Contains event id. This attribute is
                used to create a data time series when simulating dynamic
                trigger characteristics.
    ---------------------------------------------------------------------------
    Methods:
    ---------------------------------------------------------------------------
    get_layer:      Get single layer by index

    get_layers:     Get all layers as list

    get_hit_list:   Returns list of all hits in eihter native format, e.g.
                    (layer_id,segment_id, row_id, column_id) or in export format
                    (layer_id,row_id,theta_id)

    get_number_of_hits:
                    Returns number of hits as length of get_hit_list()

    clear:          Sets internal frame buffer to zero

    copy:           Deep copy of frame supplied as parameter

    and:            logical and between frame and frame supplied as parameter

    populate:       Takes a list of hit addresses. This
                    addressing scheme fits the data supplied by MPG Group.
    """


    def __init__(self,event_id=0):
        self._layer = [ CDCLayer(i) for i in range(9)]
        self.event_id = event_id


    def __calc_index(self,extern_layer_id,extern_azimuth_id):
        #Init values
        layer_id = 0
        seg_id = 0
        row_id = 0
        col_id = 0
        temp_id = 0

        #Find superlayer
        for i in range(9):
            if(extern_layer_id < temp_id + self.get_layer(i).n_rows):
                layer_id = i
                break;
            else:
                temp_id = temp_id + self.get_layer(i).n_rows

        extern_layer_id = extern_layer_id - temp_id
        #Find Row
        row_id = extern_layer_id

        temp_id = 0
        #Read values from superlayer
        n_rows = self.get_layer(layer_id).n_rows
        n_cols = self.get_layer(layer_id).n_cols
        n_segs = self.get_layer(layer_id).n_segs

        #Find Segment
        for i in range(n_segs):
            if(extern_azimuth_id < temp_id + n_cols):
                seg_id = i
                break;
            else:
                temp_id = temp_id + n_cols

        extern_azimuth_id = extern_azimuth_id - temp_id
        #Find Column
        col_id = extern_azimuth_id

        return (int(layer_id), int(seg_id), int(row_id), int(col_id))


    def get_layers(self):
        return self._layer


    def get_layer(self,layer_id):
        return self._layer[layer_id]


    def get_hit_list(self,format='native',detect_hit=True,skip_inner_layer=False):
        if(format == 'native'):
            layer_id_list = []
            seg_id_list = []
            row_id_list = []
            col_id_list = []
            for i in range(skip_inner_layer,9):
                layer = self._layer[i]
                (seg_id,
                 row_id,
                 col_id) = numpy.nonzero(layer.get_segments() == detect_hit)
                l_hits = numpy.count_nonzero(layer.get_segments() == detect_hit)

                layer_id_list.extend(l_hits * [layer.layer_id])
                seg_id_list.extend(list(seg_id.astype(int)))
                row_id_list.extend(list(row_id.astype(int)))
                col_id_list.extend(list(col_id.astype(int)))

            result = (layer_id_list,seg_id_list,row_id_list,col_id_list)

        elif(format == 'r_theta'):
            layer_id_list = []
            row_id_list = []
            theta_id_list = []
            for i in range(skip_inner_layer,9):
                layer = self._layer[i]
                (seg_id,
                 row_id,
                 col_id) = numpy.nonzero(layer.get_segments() == detect_hit)
                theta_id = seg_id*layer.n_cols+col_id
                l_hits = numpy.count_nonzero(layer.get_segments() == detect_hit)

                layer_id_list.extend(l_hits * [layer.layer_id])
                row_id_list.extend(list(row_id.astype(int)))
                theta_id_list.extend(list(theta_id.astype(int)))

            result = (layer_id_list,row_id_list,theta_id_list)

        else:
            pass

        return result


    def get_number_of_hits(self):
        n_hits = 0
        for layer in self._layer:
            l_hits = numpy.count_nonzero(layer.get_segments())
            n_hits = n_hits + l_hits

        return n_hits

    def fill(self):
        for layer in self._layer:
            layer.fill()
        return self


    def clear(self):
        for layer in self._layer:
            layer.clear()
        return self


    def copy(self,other):
        for (layer,other_layer) in zip(self._layer,other.get_layers()):
            layer = layer.copy(other_layer)
        return self


    def logical_and(self,other):
        for (layer,other_layer) in zip(self._layer,other.get_layers()):
            layer =  layer.logical_and(other_layer)
        return self

    def logical_or(self,other):
        for (layer,other_layer) in zip(self._layer,other.get_layers()):
            layer =  layer.logical_or(other_layer)
        return self


    def populate(self,layer_id_list,azimuth_id_list):
        for extern_layer_id,extern_azimuth_id in zip(layer_id_list,azimuth_id_list):
            #Read data position
            (layer_id, seg_id, row_id, col_id) = self.__calc_index(extern_layer_id,extern_azimuth_id)
            #Write data
            self.get_layer(layer_id).get_segment(seg_id)[row_id,col_id] = 1
