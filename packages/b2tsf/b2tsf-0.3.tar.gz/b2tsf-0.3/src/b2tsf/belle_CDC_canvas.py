import pkg_resources
import numpy
from pandas import read_csv
from plotly.io import write_image
import plotly.graph_objects as go
from plotly.graph_objs import Layout
from b2tsf.belle_CDC_frame import CDCFrame


class CDCCanvas:
    """
    Class containing a plotly canvas for visualization of data and track segment
    finder algorithm results. Handles all the low level things for drawing nice
    pictures. When setting up specify:
        - path to the coordinate lookup table (wire_dict_path).

        - to draw the inner layer (skip_inner_layer).

        - whether to scale markers for a more clear visualization at a cost of
          physical accuracy (scale_wires).
    ----------------------------------------------------------------------------
    Methods:
    ----------------------------------------------------------------------------
    draw:   Draws CDCFrame data onto the canvas in a mode specified. The
            following modes are available (mode=):

            -'normal' Draws hit and no hit data is predefined marker and color
                      schemes. Use this to draw input data.

            -'tsf'    Draw tsf hit data. Best pratice is to draw the data in
                      'normal' mode first and then include tsf hit data on top.

    plot:   Plot canvas to file specified in path. Caution: Files might be large
            depending on datapoints. The following modes are available(mode=):

            -'all'
                plot the whole 360° frame

            -'top','bottom','left','right'
                plot 180° of a frame

            -'top/bottom'-'left/right'
                plot 90° of a frame

    clear:  Clears the canvas from all data.

    """

    def __init__(self,
                 wire_dict_path='data/tsf_coordinates_translation.txt',
                 skip_inner_layer=False,
                 scale_wires=True):
        self._no_hit_color='#4664AA'
        self._wire_hit_color='#009682'
        self._tsf_hit_color='#A3107C'
        self._skip_inner_layer=skip_inner_layer
        self._scale_wires=scale_wires
        self._figure = go.Figure()
        self._frame = CDCFrame(0)

        file_path = pkg_resources.resource_filename(__name__, 'data/tsf_coordinates_translation.txt')
        co_data = read_csv(file_path,delimiter=',')
        keys = []
        values_x = []
        values_y = []
        for index, row in co_data.iterrows():
            new_key = (row['superlayer id'],row['ilayer id'],row['azimuthal id'])
            keys.append(new_key)
            values_x.append(row['x'])
            values_y.append(row['y'])

        self._x_dict = dict(zip(keys,values_x))
        self._y_dict = dict(zip(keys,values_y))


    def _retrieve_x_coordinates(self,tupel_id):
        return self._x_dict[tupel_id]

    def _retrieve_y_coordinates(self,tupel_id):
        return self._y_dict[tupel_id]

    def _draw_normal(self):
        hits = list(zip(*self._frame.get_hit_list(format='r_theta',
            detect_hit=True, skip_inner_layer=self._skip_inner_layer)))
        x = list(map(self._retrieve_x_coordinates,hits))
        y = list(map(self._retrieve_y_coordinates,hits))
        if(self._scale_wires is True):
            r = numpy.sqrt(numpy.array(x)**2+numpy.array(y)**2)
        else:
            r = 0

        self._figure.add_trace(go.Scatter(
            name = 'Wire hit',
            legendgroup = 'Wire hit',
            x = x,
            y = y,
            mode = 'markers',
            marker_symbol='circle',
            marker_size=6 + r/180,
            marker_color=self._wire_hit_color,
            marker_line_color=self._wire_hit_color,
            showlegend = False,
        ))

        hits = list(zip(*self._frame.get_hit_list(format='r_theta',
            detect_hit=False, skip_inner_layer=self._skip_inner_layer)))
        x = list(map(self._retrieve_x_coordinates,hits))
        y = list(map(self._retrieve_y_coordinates,hits))
        if(self._scale_wires is True):
            r = numpy.sqrt(numpy.array(x)**2+numpy.array(y)**2)
        else:
            r = 0

        self._figure.add_trace(go.Scatter(
             name = 'No hit',
             legendgroup =  'No hit',
             x = x,
             y = y,
             mode = 'markers',
             marker_symbol='circle-open',
             marker_size=6 + r/180,
             marker_color=self._no_hit_color,
             showlegend=False,
        ))

    def _draw_tsf(self):
        hits = list(zip(*self._frame.get_hit_list(format='r_theta',
            detect_hit=True, skip_inner_layer=self._skip_inner_layer)))
        x = list(map(self._retrieve_x_coordinates,hits))
        y = list(map(self._retrieve_y_coordinates,hits))
        if(self._scale_wires is True):
            r = numpy.sqrt(numpy.array(x)**2+numpy.array(y)**2)
        else:
            r = 0

        self._figure.add_trace(go.Scatter(
             name = 'TSF hit',
             legendgroup =  'TSF hit',
             x = x,
             y = y,
             mode = 'markers',
             marker_symbol='circle-x-open',
             marker_size=6 + r/180,
             marker_color=self._tsf_hit_color,
             showlegend=False,
        ))


    def draw(self,frame,hit_type='normal'):
        self._frame = frame
        if(hit_type == 'normal'):
            self._draw_normal()
            return self
        elif(hit_type == 'tsf'):
            self._draw_tsf()
            return self
        else:
            return ValueError(hit_type)


    def plot(self,path='../out/new_plot.pdf',mode='all'):
        if(mode == 'all'):
            x_range = [-1200,1200]
            y_range = [-1200,1200]
            x_width = 2500
            y_width = 2500
        elif(mode == 'top-right'):
            x_range = [-0,1200]
            y_range = [0,1200]
            x_width = 1250
            y_width = 1250
        elif(mode == 'top-left'):
            x_range = [-1200,0]
            y_range = [-1200,0]
            x_width = 1250
            y_width = 1250
        elif(mode == 'bottom-right'):
            x_range = [-0,1200]
            y_range = [-0,1200]
            x_width = 1250
            y_width = 1250
        elif(mode == 'bottom-left'):
            x_range = [-1200,0]
            y_range = [-1200,0]
            x_width = 1250
            y_width = 1250
        elif(mode == 'top'):
            x_range = [-1200,1200]
            y_range = [0,1200]
            x_width = 2500
            y_width = 1250
        elif(mode == 'bottom'):
            x_range = [-1200,0]
            y_range = [-1200,1200]
            x_width = 2500
            y_width = 1250
        elif(mode == 'right'):
            x_range = [0,1200]
            y_range = [-1200,1200]
            x_width = 1250
            y_width = 2500
        elif(mode == 'left'):
            x_range = [-1200,0]
            y_range = [-1200,1200]
            x_width = 1250
            y_width = 2500
        else:
            return ValueError(mode)

        self._figure.update_xaxes(
            dtick = 100,
            range = x_range,
            tickfont_size= 20,
            title_text = "x in mm",
            title_font = {"size": 32},
            title_standoff = 25)

        self._figure.update_yaxes(
            dtick = 100,
            range = y_range,
            tickfont_size = 20,
            title_text = "y in mm",
            title_font = {"size": 32},
            title_standoff = 25)

        layout = Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(70,100,170,0.1)',

        )
        self._figure.update_layout(layout)
        write_image(self._figure,path,width=x_width,height=y_width)

    def clear(self):
        self._frame = CDCFrame(0)
        self._figure = go.Figure()
