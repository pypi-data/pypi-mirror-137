from b2tsf.belle_CDC_frame import CDCFrame

class CDCSequence:
    """
    Sequence of CDC data frames in time domain.

    ---------------------------------------------------------------------------
    Methods:
    ---------------------------------------------------------------------------

    """

    def __init__(self,frame_list=None,t_step=1):
        if(frame_list is None):
            self._frame_list = []
            self._n_steps = 0
        else:
            self._frame_list = frame_list
            self._n_steps = len(frame_list)
        self._t_step = t_step
        self._t_min = 0
        self._t_max = self._t_step*self._n_steps


    def get_sequence_time_range(self):
        return (self._t_min,self._t_max)


    def get_sequence_step_range(self):
        return (0, self._n_steps)


    def get_frame_by_id(self,id):
        return self._frame_list[id]


    def get_frames(self):
        return self._frame_list


    def append_frames(self,frames):
        self._frame_list.extend(frames)
        self._n_steps = self._n_steps + len(frames)
        self._t_max = self._t_step*self._n_steps

    def append_frame(self,frame):
        self._frame_list.append(frame)
        self._n_steps = self._n_steps + 1
        self._t_max = self._t_step*self._n_steps

    def append_empty(self,n=1):
        for i in range(n):
            self._frame_list.append(CDCFrame())
            self._n_steps = self._n_steps + 1
            self._t_max = self._t_step*self._n_steps

    def append_full(self,n=1):
        for i in range(n):
            self._frame_list.append(CDCFrame().fill())
            self._n_steps = self._n_steps + 1
            self._t_max = self._t_step*self._n_steps
