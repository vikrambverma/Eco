# ============================================================================
"""

Owner Name    : Vikramsingh
Company Name  : ANA Software Limited
Owner Address : SP-106, Silver Palace Apartment, Shobhagpura, Udaipur,
              : Rajasthan, India, Pin Code - 313001
Created Date  : 07-Aug-2021
Licence       : MIT

"""

# ----------------------------------------------------------------------------
import UtilAna

# ============================================================================
class ChildTcpClientSocHndlAna:
    """
    """


    # ------------------------------------------------------------------------
    def __init__(self, i_my_id, i_parent_obj):
        self.s_my_id = i_my_id + 1
        self.s_parent_obj = i_parent_obj
        self.s_timeout_count = 0
        self.s_sock = None
        self.s_state = 0
        self.s_tmr_thread = None
        self.s_read_thread = None
        self.pf_Debug( "OBJ_CREATE" )
      

    # ------------------------------------------------------------------------
    def pf_Debug(self, i_msg):
        self.s_parent_obj.pf_Debug(self.s_my_id, i_msg)


    # ------------------------------------------------------------------------
    def pf_Error(self, i_msg):
        self.s_parent_obj.pf_Error(self.s_my_id, i_msg)


    # ------------------------------------------------------------------------
    def pf_SendEvent(self, i_event_id, i_event_data = None):
        self.s_parent_obj.pf_SaveRxEvents(self.s_my_id, i_event_id, i_event_data)


    # ------------------------------------------------------------------------
    def gf_IsFree(self):
        if 0 == self.s_state:
            if None == self.s_tmr_thread:
                if None == self.s_read_thread:
                    return True
        return False


    # ------------------------------------------------------------------------
    def pf_Close(self):
        if None != self.s_sock:
            if False == UtilAna.gf_CloseSocketAna(self.s_sock):
                self.pf_Error('SOCKET Close Fails')
            self.s_sock = None


    # ------------------------------------------------------------------------
    def gf_ClosingReq(self):
        if 0 != self.s_state:
            self.pf_Close()


    # ------------------------------------------------------------------------
    def pf_TmrThreadFun(self):
        while self.s_state < 1:
            UtilAna.gf_Sleep(0.025)
        self.s_state = 2
        self.pf_Debug('TimeOut_Thread_START')
        self.s_timeout_count = 0
        ttimeoutcnt = self.s_parent_obj.s_connection_timeout * 4
        while 2 == self.s_state:
            UtilAna.gf_Sleep( 0.250 )
            self.s_timeout_count = self.s_timeout_count + 1
            if ttimeoutcnt < self.s_timeout_count:
                self.s_timeout_count = 0
                self.pf_Close()
        self.s_timeout_count = 0
        ttimeoutcnt = self.s_parent_obj.s_inactivity_timeout
        while 3 == self.s_state:
            UtilAna.gf_Sleep( 1 )
            if 0 != ttimeoutcnt:
                self.s_timeout_count = self.s_timeout_count + 1
                if ttimeoutcnt < self.s_timeout_count:
                    self.s_timeout_count = 0
                    self.pf_Close()
        self.pf_Debug('TimeOut_Thread_STOP')
        self.pf_Close()
        self.s_tmr_thread = None
        self.s_state = 0
        self.pf_SendEvent('STOP')


    # ------------------------------------------------------------------------
    def pf_ReadThreadFun(self):
        self.s_state = 1
        self.pf_Debug('Read_Thread_START')
        while self.s_state < 2:
            UtilAna.gf_Sleep(0.025)
            
        sc = UtilAna.gf_ConnectSocketAna(self.s_parent_obj.s_host, self.s_parent_obj.s_port)
        if None != sc:
            self.s_state = 3
            self.s_sock = sc
            self.pf_SendEvent('START')
            while 3 == self.s_state:
                d = UtilAna.gf_RxdSocketAna(sc)
                if None != d:
                    self.pf_SendEvent('DATA', d)
                    self.s_timeout_count = 0
                else:
                    break
        self.s_read_thread = None
        self.s_state = 4
        self.pf_Debug('Read_Thread_STOP')


    # ------------------------------------------------------------------------
    def pf_StartReadThreads(self):
        self.s_read_thread = UtilAna.gf_StartThreadAna( self.pf_ReadThreadFun )
        self.s_tmr_thread = UtilAna.gf_StartThreadAna( self.pf_TmrThreadFun )


    # ------------------------------------------------------------------------
    def gf_ConnectReq(self):
        if 0 == self.s_state:
            self.pf_StartReadThreads()
        else:
            self.pf_Error('All ready connected')


    # ------------------------------------------------------------------------
    def gf_SendOutMsg(self, i_out_msg):
        if 3 == self.s_state:
            if True == UtilAna.gf_TxdSocketAna(self.s_sock, i_out_msg):
                self.s_timeout_count = 0


# ============================================================================
# end of file

