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
import DevEcoAppAna_CfgClass
import TcpClientAna_ParentSocHndl
import random

# (0, 65535)
gv_E1M = 60000
gv_E1R = 5000

gv_E2M = 5000
gv_E2R = 5000

gv_NM = 32767
gv_NR = 2000

gv_SmpleCount = 1024
gv_EveSmplCnt = 100
gv_Eve1Smples = [random.randint(gv_E1M-gv_E1R,gv_E1M+gv_E1R) for i in range(gv_EveSmplCnt)]
gv_Eve2Smples = [random.randint(gv_E2M-gv_E2R,gv_E2M+gv_E2R) for i in range(gv_EveSmplCnt)]
gv_NoiceSmples = [random.randint(gv_NM-gv_NR,gv_NM+gv_NR) for i in range(gv_SmpleCount)]

# ============================================================================
class RxDataFrameAna:
    def __init__(self, i_max_size):
        self.s_rxd = bytearray(i_max_size)
        self.s_rx_idx = i_max_size
        self.s_rx_wlen = 0
        self.s_max_size = i_max_size
    def gf_Clear(self):
        self.s_rx_idx = self.s_max_size
    def gf_GetFrame(self, i_soc_id, i_data, i_fun):
        dlen = len(i_data)
        for i in range(0, dlen, 1):
            if self.s_rx_idx > self.s_max_size - 1:
                self.s_rx_idx = 0
                self.s_rx_wlen = 2
            self.s_rxd[self.s_rx_idx] = i_data[i]
            self.s_rx_idx += 1
            if self.s_rx_idx == self.s_rx_wlen:
                if 2 == self.s_rx_wlen:
                    self.s_rx_wlen = UtilAna.gf_BinaryLiToInt(self.s_rxd[0:2], 2)
                    if self.s_rx_wlen < 5 or self.s_rx_wlen > self.s_max_size-5:
                        self.s_rx_idx = self.s_max_size
                        return
                else:
                    self.s_rx_idx = self.s_max_size
                    i_fun(i_soc_id, self.s_rxd[0:self.s_rx_wlen])
            
        

# ============================================================================
class DevAppAna:
    def __init__(self, i_max_bufsize, i_debug_active):
        self.s_cfg = DevEcoAppAna_CfgClass.AppConfigAna()
        self.s_debug_active = i_debug_active
        self.s_max_bufsize = i_max_bufsize
        self.s_clt_obj = TcpClientAna_ParentSocHndl.ParentTcpClientSocHndlAna(\
                                            'Device_TcpClient', False)
        self.s_rxq_thread_active = False
        self.s_rxq_thread = None
        self.s_soc_max = 0
        self.s_soc_state = []
        self.s_soc_tmr = []
        self.s_soc_event_send_tmr = []
        self.s_soc_macid = []
        self.s_soc_frame_obj = []
        self.s_out_msg_buf = bytearray(self.s_max_bufsize)
        self.s_app_thread_active = False
        self.s_app_thread = None
        self.s_ticks = 0
    
    # ------------------------------------------------------------------------
    def pf_Debug(self, i_id, i_eve_id):
        if True == self.s_debug_active:
            s = 'Dev ' + str(i_id) + '_' + i_eve_id
            UtilAna.gf_DebugLog( s )

    # ------------------------------------------------------------------------
    def pf_AddSocParam(self):
        self.s_soc_state.append(0)
        self.s_soc_tmr.append(0)
        self.s_soc_event_send_tmr.append(0)
        self.s_soc_macid.append(0)
        self.s_soc_frame_obj.append(RxDataFrameAna(self.s_max_bufsize))
        self.s_soc_max += 1


    # ------------------------------------------------------------------------
    def pf_ClearAllParam(self):
        for i in  range(0, self.s_soc_max, 1):
            self.s_soc_state.pop(0)
            self.s_soc_tmr.pop(0)
            self.s_soc_macid.pop(0)
            self.s_soc_frame_obj.pop(0)
        self.s_soc_max = 0


    # ------------------------------------------------------------------------
    def pf_FillLenTypeMacCrcAndSend(self, i_sock_id, i_len, i_type, i_mac):
        i_len += 2
        self.s_out_msg_buf[0:2] = UtilAna.gf_FillUintToBinaryLi(i_len, 2)
        self.s_out_msg_buf[2] = i_type
        self.s_out_msg_buf[3:9] = UtilAna.gf_FillUintToBinaryLi(i_mac, 6)
        self.s_out_msg_buf[i_len-2:i_len] = [0]*2
        self.s_clt_obj.gf_SendOutMsg(i_sock_id, self.s_out_msg_buf[0:i_len])
    

    # ------------------------------------------------------------------------
    def pf_FillWave(self, i_soc_id, i_etmr):
        global gv_SmpleCount
        global gv_NoiceSmples
        global gv_Eve1Smples
        global gv_Eve2Smples
        j = 13
        t = random.randint(0,1)
        k0 = 0
        ps = random.randint(0,(gv_SmpleCount-gv_EveSmplCnt))
        pe = ps + gv_EveSmplCnt - 1
        for i in range( 0, gv_SmpleCount, 1):
            if i < ps or i > pe:
                k0 = int(gv_NoiceSmples[i])
            else:
                if 0 ==i_etmr:
                    if 0 == t:
                        k0 = int(gv_Eve1Smples[i-ps])
                    else:
                        k0 = int(gv_Eve2Smples[i-ps])
                else:
                    k0 = int(gv_NoiceSmples[i])
                
            k1 = int( int(k0) % 256 )
            k2 = int( int(k0) / 256 )
            self.s_out_msg_buf[j] = k1
            self.s_out_msg_buf[j+1] = k2
            j += 2

    # ------------------------------------------------------------------------
    def pf_SendInfoFrame(self, i):
        self.pf_FillLenTypeMacCrcAndSend(i, 9, 9, i)
    

    # ------------------------------------------------------------------------
    def pf_SendDataFrame(self, i, etmr):
        global gv_SmpleCount
        self.s_out_msg_buf[9:13] = UtilAna.gf_FillUintToBinaryLi(self.s_ticks, 4)
        self.pf_FillWave(i, etmr)
        self.pf_FillLenTypeMacCrcAndSend(i, gv_SmpleCount*2+13, 8, i)

    # ------------------------------------------------------------------------
    def pf_ExeCmds(self, i_soc_id, i_data):
        inDevMacId = UtilAna.gf_BinaryLiToInt(i_data[3:9], 6)
        if 0 == inDevMacId:
            self.s_clt_obj.gf_Close(i_soc_id+1)
            return
        if inDevMacId != self.s_soc_macid[i_soc_id]:
            self.s_soc_macid[i_soc_id] = inDevMacId

    # ------------------------------------------------------------------------
    def pf_ThreadFun_IncommingEve(self):
        self.s_rxq_thread_active = True
        while True == self.s_rxq_thread_active:
            UtilAna.gf_Sleep(0.5)
            while True:
                rxSocId, rxEveId, rxEveData = self.s_clt_obj.gf_GetEvents()
                if None == rxSocId or 0 == rxSocId:
                    break
                rxSocId -= 1
                if rxSocId >= self.s_soc_max:
                    self.s_clt_obj.gf_Close(rxSocId+1)
                else:
                    if 'DATA' == rxEveId:
                        self.pf_Debug(rxSocId+1, rxEveId)
                        self.s_soc_frame_obj[rxSocId].gf_GetFrame(rxSocId, rxEveData, self.pf_ExeCmds)
    
                    elif 'STOP' == rxEveId:
                        self.pf_Debug(rxSocId+1, rxEveId)
                        self.s_soc_state[rxSocId] = 0
                        self.s_soc_tmr[rxSocId] = 0
                        self.s_soc_macid[rxSocId] = 0
                        self.s_soc_frame_obj[rxSocId].gf_Clear()
        
                    elif "START" == rxEveId:
                        self.pf_Debug(rxSocId+1, rxEveId)
                        self.s_soc_state[rxSocId] = 2
                        self.s_soc_tmr[rxSocId] = 0
                        self.s_soc_macid[rxSocId] = 0
                        self.s_soc_frame_obj[rxSocId].gf_Clear()
    
                    else:
                        self.pf_Debug(rxSocId+1, rxEveId)
                        self.s_clt_obj.gf_Close(rxSocId+1)
                    
    # ------------------------------------------------------------------------
    def pf_ThreadFun_App(self):
        self.s_app_thread_active = True
        while True == self.s_app_thread_active:
            UtilAna.gf_Sleep(0.990)
            self.s_ticks += 1
            for i in range(0, self.s_soc_max, 1):
                s = self.s_soc_state[i]
                m = self.s_soc_tmr[i]
                if 0 == s:
                    m = m + 1
                    if m > 5:
                        self.s_clt_obj.gf_ConnectReq(i+1)
                        m = 0
                        self.s_soc_state[i] = 1
                    self.s_soc_tmr[i] = m
                elif 1 == s:
                    pass
                elif 2 == s:
                    m = m + 1
                    if m > 0:
                        self.pf_SendInfoFrame(i+1)
                        m = 0
                        self.s_soc_state[i] = 3
                    self.s_soc_tmr[i] = m
                else:
                    m = m + 1
                    if m > 0:
                        etmr = self.s_soc_event_send_tmr[i]
                        etmr = etmr + 1
                        if etmr > (60 + random.randint(0, 60)):
                            etmr = 0
                        self.s_soc_event_send_tmr[i] = etmr
                        self.pf_SendDataFrame(i+1, etmr)
                    self.s_soc_tmr[i] = m

    # ------------------------------------------------------------------------
    def gf_Start(self):
        self.s_cfg.gf_LoadConfig()
        for i in range(0, self.s_cfg.s_dev_max, 1):
            self.pf_AddSocParam()
        self.s_rxq_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_IncommingEve)
        self.s_app_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_App)
        ih = self.s_cfg.s_host
        ip = self.s_cfg.s_port
        ic = self.s_cfg.s_dev_max
        it = self.s_cfg.s_inactivity_timeout
        self.s_clt_obj.gf_Start(ih, ip, ic, it, 15)

    # ------------------------------------------------------------------------
    def gf_Stop(self):
        self.s_app_thread_active = False
        while True == self.s_app_thread.is_alive():
            UtilAna.gf_Sleep(1)
        self.s_app_thread = None

        self.s_clt_obj.gf_Stop()

        self.s_rxq_thread_active = False
        while True == self.s_rxq_thread.is_alive():
            UtilAna.gf_Sleep(1)
        self.s_rxq_thread = None
        self.pf_ClearAllParam()

# ============================================================================
# end of file
