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
import TcpClientAna_ChildSocHndl

# ============================================================================
class ParentTcpClientSocHndlAna:
    """
    """


    # ------------------------------------------------------------------------
    def __init__(self, i_my_str, i_debug_active):
        # common parameters
        self.s_my_str = i_my_str + ' '
        self.s_debug_active = i_debug_active
        self.s_host = None
        self.s_port = None
        self.s_inactivity_timeout = 15
        self.s_connection_timeout = 15
        self.s_event_rxq = []
        # clients parameters
        self.s_child_max = 0   # number of clients
        self.s_child_obj = []
        self.pf_Debug(0, 'OBJECT_CREATED')


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
    def pf_SaveRxEvents(self, i_id, i_event_id, i_event_data = None):
        self.s_event_rxq.append([i_id, i_event_id, i_event_data])
        self.pf_Debug(i_id, i_event_id)


    # ------------------------------------------------------------------------
    def pf_IsValidChildId(self, i_child_id):
        return UtilAna.gf_ChkRange1ToMax(i_child_id, self.s_child_max)


    # ------------------------------------------------------------------------
    def gf_ConnectReq(self, i_child_id):
        if True == self.pf_IsValidChildId(i_child_id):
            self.s_child_obj[(i_child_id - 1)].gf_ConnectReq()
        else:
            self.pf_Error(0, 'INALID_CONNECT_REQ' + str(i_child_id))
        
            
    # ------------------------------------------------------------------------
    def pf_ClosingReq(self):
        for i in range(0, self.s_child_max, 1):
            self.s_child_obj[i].gf_ClosingReq()
        for i in range(0, self.s_child_max, 1):
            while True:
                if True == self.s_child_obj[0].gf_IsFree():
                    self.s_child_obj.pop(0)
                    break
                UtilAna.gf_Sleep(1)
        self.s_child_max = 0


    # ------------------------------------------------------------------------
    def gf_Start(self, i_host, i_port, i_child_max, i_inactivity_timeout, i_connection_timeout):
        if 0 == self.s_child_max:
            UtilAna.gf_SocHostMsg(self.s_my_str, i_host, i_port, i_child_max, i_inactivity_timeout)
            self.s_host = i_host
            self.s_port = i_port
            self.s_inactivity_timeout = i_inactivity_timeout
            self.s_connection_timeout = i_connection_timeout
            for i in range(0, i_child_max, 1):
                c = TcpClientAna_ChildSocHndl.ChildTcpClientSocHndlAna(i, self)
                self.s_child_obj.append(c)
            self.s_child_max = i_child_max
        else:
            self.pf_Error(0, 'INALID_START_REQ')


    # ------------------------------------------------------------------------
    def gf_Stop(self):
        if 0 != self.s_child_max:
            self.pf_ClosingReq()

    # ------------------------------------------------------------------------
    def gf_Close(self, i_child_id):
        if True == self.pf_IsValidChildId(i_child_id):
            self.s_child_obj[(i_child_id - 1)].gf_ClosingReq()
        else:
            self.pf_Error(0, 'INALID_STOP_REQ' + str(i_child_id))


    # ------------------------------------------------------------------------
    def gf_SendOutMsg(self, i_child_id, in_out_msg):
        if True == self.pf_IsValidChildId(i_child_id):
            self.s_child_obj[(i_child_id - 1)].gf_SendOutMsg(in_out_msg)
        else:
            self.pf_Error(0, 'INALID_SEND_OUT_MSG_REQ' + str(i_child_id))

    # ------------------------------------------------------------------------
    def gf_GetEvents(self):
        elen = len(self.s_event_rxq)
        if elen > 0:
            eSocId, eEveId, eEveData = self.s_event_rxq.pop(0)
            return eSocId, eEveId, eEveData
        else:
            return None, None, None


# ============================================================================
# end of file

