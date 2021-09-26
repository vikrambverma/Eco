# =============================================================================
"""

Owner Name    : Vikramsingh
Company Name  : ANA Software Limited
Owner Address : SP-106, Silver Palace Apartment, Shobhagpura, Udaipur,
              : Rajasthan, India, Pin Code - 313001
Created Date  : 28-July-2021
Licence       : MIT

"""

# -----------------------------------------------------------------------------
import UtilAna

# ============================================================================
class ChildTcpServerSocHndlAna:
    """
    """


    # ------------------------------------------------------------------------
    def __init__(self, i_my_id, i_parent_obj):
        self.s_my_id = i_my_id + 1
        self.s_timeout_count = 0
        self.s_parent_obj = i_parent_obj
        self.s_sock = None
        self.s_active = False
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
        self.s_parent_obj.pf_SaveRxEvents( self.s_my_id, i_event_id, i_event_data )


    # ------------------------------------------------------------------------
    def gf_IsFree(self):
        if None == self.s_sock:
            if None == self.s_tmr_thread:
                if None == self.s_read_thread:
                    if False == self.s_active:
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
        if True == self.s_active:
            self.pf_Close()
            self.s_active = False


    # ------------------------------------------------------------------------
    def pf_TmrThreadFun(self):
        self.s_active = True
        self.pf_Debug('TimeOut_Thread_START')
        self.s_timeout_count = 0
        tinactivitytimeout = self.s_parent_obj.s_inactivity_timeout
        while True == self.s_active:
            UtilAna.gf_Sleep(1)
            if 0 != tinactivitytimeout:
                self.s_timeout_count = self.s_timeout_count + 1
                if tinactivitytimeout < self.s_timeout_count:
                    self.s_active = False
        self.pf_Debug('TimeOut_Thread_STOP')
        self.pf_Close()


    # ------------------------------------------------------------------------
    def pf_ReadThreadFun(self):
        self.pf_Debug('Read_Thread_START')
        rd_thread_active = True
        self.pf_SendEvent('START')
        sc = self.s_sock
        while True == rd_thread_active:
            d = UtilAna.gf_RxdSocketAna(sc)
            if None != d:
                self.pf_SendEvent('DATA', d)
                self.s_timeout_count = 0
            else:
                rd_thread_active = False
        self.pf_Debug('Read_Thread_STOP')
        self.s_active = False
        while True:
            if self.s_tmr_thread.is_alive():
                UtilAna.gf_Sleep(1)
            else:
                break
        self.s_tmr_thread = None
        self.s_read_thread = None
        self.pf_SendEvent('STOP')
        

    # ------------------------------------------------------------------------
    def gf_StartThreads(self, i_sock):
        self.s_tmr_thread = UtilAna.gf_StartThreadAna( self.pf_TmrThreadFun )
        self.s_sock = i_sock
        self.s_read_thread = UtilAna.gf_StartThreadAna( self.pf_ReadThreadFun )


    # ------------------------------------------------------------------------
    def gf_SendOutMsg(self, i_out_msg):
        if False != self.s_active:
            if True == UtilAna.gf_TxdSocketAna(self.s_sock, i_out_msg):
                self.s_timeout_count = 0


