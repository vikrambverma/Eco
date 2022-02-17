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
import TcpServerAna_ChildSocHndl

# ============================================================================
class ParentTcpServerSocHndlAna:
    """
    """


    # ------------------------------------------------------------------------
    def __init__(self, i_my_str, i_debug_active):
        # common parameters
        self.s_my_str = i_my_str + ' '
        self.s_debug_active = i_debug_active
        self.s_rxdata_process_hndl = None
        self.s_inactivity_timeout = 60
        self.s_child_max = 0
        self.s_child_obj = []

        # server parameters
        self.s_host = None
        self.s_port = None
        self.s_sock = None
        self.s_event_rxq = []
        self.s_listen_thread = None
        self.s_listen_active = False
        self.pf_Debug(0,'Created')


    # ------------------------------------------------------------------------
    def pf_Debug(self, i_id, i_msg):
        if False != self.s_debug_active:
            s = self.s_my_str + str(i_id) + '_' + i_msg
            UtilAna.gf_DebugLog(s)


    # ------------------------------------------------------------------------
    def pf_Error(self, i_id, i_msg):
        s = 'ERROR : ' + self.s_my_str + str(i_id) + '_' + i_msg
        UtilAna.gf_DebugLog(s)


    # ------------------------------------------------------------------------
    def pf_CloseSock(self):
        if None != self.s_sock:
            if False == UtilAna.gf_CloseSocketAna(self.s_sock):
                self.pf_Error(0, 'SOCKET Close Fails')
            self.s_sock = None


    # ------------------------------------------------------------------------
    def pf_SaveRxEvents(self, i_id, i_event_id, i_event_data = None):
        self.s_event_rxq.append([i_id, i_event_id, i_event_data])
        self.pf_Debug(i_id, i_event_id)


    # ------------------------------------------------------------------------
    def pf_IsValidChildId(self, i_child_id):
        return UtilAna.gf_ChkRange1ToMax(i_child_id, self.s_child_max)


    # ------------------------------------------------------------------------
    def pf_GetFreeChildId(self):
        for i in range(0, self.s_child_max, 1):
            if True == self.s_child_obj[ i ].gf_IsFree():
                return i
        return self.s_child_max


    # ------------------------------------------------------------------------
    def pf_ClosingReq(self):
        if True == self.s_listen_active:
            self.s_listen_active = False
            self.pf_CloseSock()
        else:
            self.pf_Error(0, 'NOT_RUNING')

    # ------------------------------------------------------------------------
    def pf_ThreadFun_SrvListen(self):
        srvsock = UtilAna.gf_SetListenSocketAna(self.s_host, self.s_port, self.s_child_max)
        if None == srvsock:
            self.pf_Error(0, 'Listen Start Fails')
        self.s_sock = srvsock
        self.pf_SaveRxEvents(0, 'START')
        self.s_listen_active = True
        while False != self.s_listen_active:
            cltsock = UtilAna.gf_AcceptSocketAna(srvsock)
            if None != cltsock:
                i = self.pf_GetFreeChildId()
                if i < self.s_child_max:
                    self.s_child_obj[i].gf_StartThreads(cltsock)
                else:
                    UtilAna.gf_CloseSocketAna(cltsock)
            else:
                self.pf_CloseSock()
                if True == self.s_listen_active:
                    self.s_listen_active = False
        self.pf_CloseSock()
        self.pf_SaveRxEvents(0, 'STOP')
        for i in range(0, self.s_child_max, 1):
            self.s_child_obj[i].gf_ClosingReq()
        UtilAna.gf_Sleep(1)
        for i in range(0, self.s_child_max, 1):
            while True:
                if True == self.s_child_obj[0].gf_IsFree():
                    self.s_child_obj.pop(0)
                    break
                UtilAna.gf_Sleep(1)
        self.s_child_max = 0
        self.s_listen_active = False
        self.s_sock = None
        self.s_listen_thread = None


    # ------------------------------------------------------------------------
    def pf_IsClosed(self):
        if False == self.s_listen_active:
            if None == self.s_listen_thread:
                return True
        return False


    # ------------------------------------------------------------------------
    def gf_Start(self, i_host, i_port, i_child_max, i_inactivity_timeout):
        if True == self.pf_IsClosed():
            UtilAna.gf_SocHostMsg(self.s_my_str, i_host, i_port, i_child_max, i_inactivity_timeout)
            self.s_host = i_host
            self.s_port = i_port
            self.s_inactivity_timeout = i_inactivity_timeout
            for i in range(0, i_child_max, 1):
                c = TcpServerAna_ChildSocHndl.ChildTcpServerSocHndlAna(i, self)
                self.s_child_obj.append(c)
                self.s_child_max += 1
            self.s_listen_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_SrvListen)
        else:
            self.pf_Error(0, 'RUNING')
            

    # ------------------------------------------------------------------------
    def gf_Stop(self):
        self.pf_ClosingReq()
        while True:
            if True == self.pf_IsClosed():
                break
            UtilAna.gf_Sleep(1)


    # ------------------------------------------------------------------------
    def gf_CloseClient(self, i_client_id):
        if True == self.pf_IsValidChildId( i_client_id ):
            self.s_child_obj[(i_client_id - 1)].gf_ClosingReq()
        else:
            self.pf_Error(0, 'INALID_STOP_REQ_' + str(i_client_id))


    # ------------------------------------------------------------------------
    def gf_SendOutMsg(self, i_client_id, in_out_msg):
        if True == self.pf_IsValidChildId( i_client_id ):
            self.s_child_obj[ (i_client_id - 1) ].gf_SendOutMsg( in_out_msg )
        else:
            self.pf_Error(0, 'INALID_SEND_OUT_MSG_REQ_' + str(i_client_id))


    # ------------------------------------------------------------------------
    def gf_GetEvents(self):
        elen = len(self.s_event_rxq)
        if elen > 0:
            eSocId, eEveId, eEveData = self.s_event_rxq.pop(0)
            return eSocId, eEveId, eEveData
        else:
            return None, None, None
               
        
