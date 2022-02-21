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
import SrvEcoAppAna_CfgClass
import TcpServerAna_ParentSocHndl

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
class SrvDevAppAna:
    def __init__(self, i_parent_obj, i_max_bufsize, i_debug_active):
        self.s_parent_obj = i_parent_obj
        self.s_cfg = self.s_parent_obj.s_cfg
        self.s_debug_active = i_debug_active
        self.s_max_bufsize = i_max_bufsize
        self.s_srv_obj = TcpServerAna_ParentSocHndl.ParentTcpServerSocHndlAna(\
                                            'Device_TcpServer', False)
        self.s_rxq_thread_active = False
        self.s_rxq_thread = None
        self.s_soc_max = 0
        self.s_soc_active = []
        self.s_soc_macid = []
        self.s_soc_usrids = []
        self.s_soc_frame_obj = []
        self.s_out_msg_buf = bytearray(self.s_max_bufsize)
    
    # ------------------------------------------------------------------------
    def pf_Debug(self, i_id, i_eve_id):
        if True == self.s_debug_active:
            s = 'DEV_SOC_' + str(i_id) + '_' + i_eve_id
            UtilAna.gf_DebugLog( s )

    # ------------------------------------------------------------------------
    def pf_AddSocParam(self):
        self.s_soc_active.append(False)
        self.s_soc_macid.append(0)
        self.s_soc_usrids.append([])
        self.s_soc_frame_obj.append(RxDataFrameAna(self.s_max_bufsize))
        self.s_soc_max += 1


    # ------------------------------------------------------------------------
    def pf_ClearAllParam(self):
        for i in  range(0, self.s_soc_max, 1):
            self.s_soc_active.pop(0)
            self.s_soc_macid.pop(0)
            self.s_soc_usrids.pop(0)
            self.s_soc_frame_obj.pop(0)
        self.s_soc_max = 0


    # ------------------------------------------------------------------------
    def pf_GetDevSocId(self, i_mac_id):
        for i in range(0, self.s_soc_max, 1):
            if True == self.s_soc_active[i]:
                if i_mac_id == self.s_soc_macid[i]:
                    return i
        return self.s_soc_max

    # ------------------------------------------------------------------------
    def pf_Forward_UsrToDevie(self, i_mac, i_data):
        if 0 != i_mac:
            socid = self.pf_GetDevSocId(i_mac)
            if socid < self.s_soc_max:
                self.s_srv_obj.gf_SendOutMsg(socid, i_data)
        
    # ------------------------------------------------------------------------
    def pf_ExeCmds(self, i_soc_id, i_data):
        inDevMacId = UtilAna.gf_BinaryLiToInt(i_data[3:9], 6)
        if 0 == inDevMacId:
            self.s_srv_obj.gf_Close(i_soc_id)
            return
        if inDevMacId != self.s_soc_macid[i_soc_id]:
            self.s_soc_macid[i_soc_id] = inDevMacId
            self.s_soc_usrids[i_soc_id] = self.s_cfg.gf_GetMacIdToUserIdList(inDevMacId)
            if 0 == len(self.s_soc_usrids[i_soc_id]):
                self.s_srv_obj.gf_CloseClient(i_soc_id)
                return
        self.s_parent_obj.s_usr_obj.pf_Forward_DevToUser(self.s_soc_usrids[i_soc_id], i_data)

    # ------------------------------------------------------------------------
    def pf_ThreadFun_IncommingEve(self):
        self.s_rxq_thread_active = True
        while True == self.s_rxq_thread_active:
            UtilAna.gf_Sleep(0.005)
            while True:
                rxSocId, rxEveId, rxEveData = self.s_srv_obj.gf_GetEvents()
                if None == rxSocId:
                    break
                while True:
                    if rxSocId < self.s_soc_max:
                        break
                    else:
                        self.pf_AddSocParam()
 
                if 'DATA' == rxEveId:
                    self.s_soc_frame_obj[rxSocId].gf_GetFrame(rxSocId, rxEveData, self.pf_ExeCmds)

                elif 'STOP' == rxEveId:
                    self.pf_Debug(rxSocId, rxEveId)
                    self.s_soc_active[rxSocId] = False
                    self.s_soc_macid[rxSocId] = 0
                    self.s_soc_frame_obj[rxSocId].gf_Clear()
    
                elif "START" == rxEveId:
                    self.pf_Debug(rxSocId, rxEveId)
                    self.s_soc_active[rxSocId] = True
                    self.s_soc_macid[rxSocId] = 0
                    self.s_soc_frame_obj[rxSocId].gf_Clear()

                else:
                    self.pf_Debug(rxSocId, rxEveId)
                    self.s_srv_obj.gf_CloseClient( rxSocId )
        self.pf_ClearAllParam()
                    
    # ------------------------------------------------------------------------
    def gf_Start(self, i_host, i_port, i_child_max, i_inactivity_timeout):
        self.s_rxq_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_IncommingEve)
        self.s_srv_obj.gf_Start(i_host, i_port, i_child_max, i_inactivity_timeout)

    # ------------------------------------------------------------------------
    def gf_Stop(self):
        self.s_rxq_thread_active = False
        while True == self.s_rxq_thread.is_alive():
            UtilAna.gf_Sleep(1)
        self.s_rxq_thread = None
        self.s_srv_obj.gf_Stop()


# ============================================================================
class SrvUsrAppAna:
    def __init__(self, i_parent_obj, i_max_bufsize, i_debug_active):
        self.s_parent_obj = i_parent_obj
        self.s_cfg = self.s_parent_obj.s_cfg
        self.s_debug_active = i_debug_active
        self.s_max_bufsize = i_max_bufsize
        self.s_srv_obj = TcpServerAna_ParentSocHndl.ParentTcpServerSocHndlAna( \
                                                    'User_TcpServer', False)
        self.s_rxq_thread_active = False
        self.s_rxq_thread = None
        self.s_soc_max = 0
        self.s_soc_active = []
        self.s_soc_usrid = []
        self.s_soc_macids = []
        self.s_soc_frame_obj = []
        self.s_out_msg_buf = bytearray(self.s_max_bufsize)

    
    # ------------------------------------------------------------------------
    def pf_Debug(self, i_id, i_eve_id):
        if True == self.s_debug_active:
            s = 'USR_SOC_' + str(i_id) + '_' + i_eve_id
            UtilAna.gf_DebugLog( s )

    # ------------------------------------------------------------------------
    def pf_AddSocParam(self):
        self.s_soc_active.append(False)
        self.s_soc_usrid.append(0)
        self.s_soc_macids.append([])
        self.s_soc_frame_obj.append(RxDataFrameAna(self.s_max_bufsize))
        self.s_soc_max += 1


    # ------------------------------------------------------------------------
    def pf_ClearAllParam(self):
        for i in  range(0, self.s_soc_max, 1):
            self.s_soc_active.pop(0)
            self.s_soc_usrid.pop(0)
            self.s_soc_macids.pop(0)
            self.s_soc_frame_obj.pop(0)
        self.s_soc_max = 0
        
    # ------------------------------------------------------------------------
    def pf_FillHdrCrcAndTxd(self, i_soc_id, i_usr_id, i_type, i_len):
        i_len = i_len + 2
        if i_len < self.s_max_bufsize and 0 != i_soc_id and 0 != i_usr_id:
            self.s_out_msg_buf[0:2] = UtilAna.gf_FillUintToBinaryLi( i_len, 2 )
            self.s_out_msg_buf[2] = i_type
            self.s_out_msg_buf[3:5] = UtilAna.gf_FillUintToBinaryLi( i_usr_id, 2 )
            self.s_out_msg_buf[i_len-2:i_len] = [0]*2
            self.s_srv_obj.gf_SendOutMsg(i_soc_id, self.s_out_msg_buf[0:i_len])

    # ------------------------------------------------------------------------
    def pf_Txd_Y_Response(self, i_usr_id, i_soc_id, i_req_id, i_retStatus):
        if True == i_retStatus:
            self.s_out_msg_buf[5] = 1
        else:
            self.s_out_msg_buf[5] = 0
        self.pf_FillHdrCrcAndTxd(i_soc_id, i_usr_id, 128+i_req_id, 6)

    # ------------------------------------------------------------------------
    def pf_Txd_X_Response(self, i_usr_id, i_soc_id, i_req_id, i_usr_offset, i_retStatus, i_msg=None):
        if True == i_retStatus:
            self.s_out_msg_buf[5] = 1
        else:
            self.s_out_msg_buf[5] = 0
        self.s_out_msg_buf[6:8] = UtilAna.gf_FillUintToBinaryLi( i_usr_offset, 2 )
        ilen = 8
        if None != i_msg:
            imsglen = len(i_msg)
            self.s_out_msg_buf[8:8+imsglen] = i_msg[0:imsglen]
            ilen += imsglen
        self.pf_FillHdrCrcAndTxd(i_soc_id, i_usr_id, 128+i_req_id, ilen)

    # ------------------------------------------------------------------------
    def pf_GetUsrSocId(self, i_usr_id):
        for i in range(0, self.s_soc_max, 1):
            if True == self.s_soc_active[i]:
                if i_usr_id == self.s_soc_usrid[i]:
                    return i
        return self.s_soc_max

    # ------------------------------------------------------------------------
    def pf_Forward_DevToUser(self, i_usrids, i_dev_data):
        ilen = 5
        imsglen = len(i_dev_data)
        self.s_out_msg_buf[5:5+imsglen] = i_dev_data[0:imsglen]
        ilen += imsglen
        ulen = len(i_usrids)
        for i in range(0, ulen, 1):
            uid = i_usrids[i]
            usoc = self.pf_GetUsrSocId(uid)
            if usoc != self.s_soc_max:
                self.pf_FillHdrCrcAndTxd(usoc, uid, 128+120, ilen)

    # ------------------------------------------------------------------------
    def pf_ExeCmds(self, i_soc_id, i_data):
        # UtilAna.gf_DebugLog( i_data )
        rcvlen = len(i_data)
        inlen = UtilAna.gf_BinaryLiToInt(i_data[0:2], 2)
        intype = i_data[2]
        inUsrId = UtilAna.gf_BinaryLiToInt(i_data[3:5], 2)
        if 0 == inUsrId:
            self.s_srv_obj.gf_CloseClient(i_soc_id)
            return
        if inUsrId != self.s_soc_usrid[i_soc_id]:
            self.s_soc_usrid[i_soc_id] = inUsrId
            self.s_soc_macids[i_soc_id] = self.s_cfg.gf_GetUserIdToMacList(inUsrId)
            
        if rcvlen == inlen:
            if intype < 8:
                s = str(inUsrId) + '_' + str(intype) + '_REQ'
                self.pf_Debug(i_soc_id, s)
                if 1 == intype:       # request = keep alive, response send now
                    self.pf_Txd_Y_Response( inUsrId, i_soc_id, intype, True )
                
                elif 2 == intype:     # req = auth, response send now
                    self.pf_Txd_Y_Response( inUsrId, i_soc_id, intype, True )

                elif 3 == intype:     # req = save config and restart
                    self.pf_Txd_Y_Response( inUsrId, i_soc_id, intype, True )
                    self.s_cfg.gf_SaveCfg()
                    self.s_parent_obj.s_restart()

                elif 4 == intype:     # req = user and dev inactivity timeout
                    self.s_cfg.s_user_timeout = UtilAna.gf_BinaryLiToInt(i_data[5:7], 2)
                    self.s_cfg.s_device_timeout = UtilAna.gf_BinaryLiToInt(i_data[7:9], 2)
                    self.pf_Txd_Y_Response( inUsrId, i_soc_id, intype, True )
            
            elif intype < 120:
                inUsrOffset = UtilAna.gf_BinaryLiToInt(i_data[5:7], 2)
                s = str(inUsrId) + '_' + str(intype) + '_' + str(inUsrOffset) + '_REQ'
                self.pf_Debug(i_soc_id, s)
                if 8 == intype:     # req = set user id
                    inSetUsrId = UtilAna.gf_BinaryLiToInt(i_data[7:9], 2)
                    retSts = self.s_cfg.gf_SetUserId(inUsrOffset, inSetUsrId)
                    self.pf_Txd_X_Response(inUsrId, i_soc_id, intype, inUsrOffset, retSts)
                    
                elif 9 == intype:     # req = set user name
                    inSetUsrName = i_data[7:inlen-2].decode()
                    retSts = self.s_cfg.gf_SetUserName(inUsrOffset, inSetUsrName)
                    self.pf_Txd_X_Response(inUsrId, i_soc_id, intype, inUsrOffset, retSts)
                
                elif 10 == intype:     # req = set user passward
                    inSetUsrPass = i_data[7:inlen-2].decode()
                    retSts = self.s_cfg.gf_SetUserPassward(inUsrOffset, inSetUsrPass)
                    self.pf_Txd_X_Response(inUsrId, i_soc_id, intype, inUsrOffset, retSts)
                
                elif 11 == intype:     # req = set user type
                    inSetUsrType = i_data[7:inlen-2].decode()
                    retSts = self.s_cfg.gf_SetUserType(inUsrOffset, inSetUsrType)
                    self.pf_Txd_X_Response(inUsrId, i_soc_id, intype, inUsrOffset, retSts)
                
                elif 12 == intype:     # req = set user dev mac
                    inUsrOffset = UtilAna.gf_BinaryLiToInt(i_data[5:7], 2)
                    inSetUsrDevMac = UtilAna.gf_BinaryLiToInt(i_data[7:13], 6)
                    retSts = self.s_cfg.gf_SetUserMac(inUsrOffset, inSetUsrDevMac)
                    self.pf_Txd_X_Response(inUsrId, i_soc_id, intype, inUsrOffset, retSts)

            elif 120 == intype:     # req = forward message to device
                inLen = UtilAna.gf_BinaryLiToInt(i_data[5:7], 2)
                inDevMacId = UtilAna.gf_BinaryLiToInt(i_data[8:14], 6)
                if 1 != inUsrId:
                    m = self.s_soc_macids[i_soc_id]
                    for i in range(0, len(m), 1):
                        if inDevMacId == m[i]:
                            self.s_parent_obj.s_dev_obj.pf_Forward_UsrToDevie(inDevMacId, i_data[5:5+inLen])
                            break
                    return
                else:
                    self.s_parent_obj.s_dev_obj.pf_Forward_UsrToDevie(inDevMacId, i_data[5:5+inLen])
                    return


    # ------------------------------------------------------------------------
    def pf_ThreadFun_IncommingEve(self):
        self.s_rxq_thread_active = True
        while True == self.s_rxq_thread_active:
            UtilAna.gf_Sleep(0.025)
            while True:
                rxSocId, rxEveId, rxEveData = self.s_srv_obj.gf_GetEvents()
                if None == rxSocId:
                    break
                while True:
                    if rxSocId < self.s_soc_max:
                        break
                    else:
                        self.pf_AddSocParam()
 
                if 'DATA' == rxEveId:
                    # self.pf_Debug(rxSocId, rxEveId)
                    self.s_soc_frame_obj[rxSocId].gf_GetFrame(rxSocId, rxEveData, self.pf_ExeCmds)

                elif 'STOP' == rxEveId:
                    self.pf_Debug(rxSocId, rxEveId)
                    self.s_soc_active[rxSocId] = False
                    self.s_soc_usrid[rxSocId] = 0
    
                elif "START" == rxEveId:
                    self.pf_Debug(rxSocId, rxEveId)
                    self.s_soc_active[rxSocId] = True
                    self.s_soc_usrid[rxSocId] = 0

                else:
                    self.pf_Debug(rxSocId, rxEveId)
                    self.s_srv_obj.gf_CloseClient( rxSocId )
        self.pf_ClearAllParam()
                    
    # ------------------------------------------------------------------------
    def gf_Start(self, i_host, i_port, i_child_max, i_inactivity_timeout):
        self.s_rxq_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_IncommingEve)
        self.s_srv_obj.gf_Start(i_host, i_port, i_child_max, i_inactivity_timeout)

    # ------------------------------------------------------------------------
    def gf_Stop(self):
        self.s_rxq_thread_active = False
        while True == self.s_rxq_thread.is_alive():
            UtilAna.gf_Sleep(1)
        self.s_rxq_thread = None
        self.s_srv_obj.gf_Stop()

# ============================================================================
class ServerHndlAna:
    """
    """


    # ------------------------------------------------------------------------
    def __init__(self, i_restart, i_usr_debug_active, i_dev_debug_active):
        self.s_cfg = SrvEcoAppAna_CfgClass.AppConfigAna()
        self.s_usr_obj = SrvUsrAppAna(self, 4096, i_usr_debug_active)
        self.s_dev_obj = SrvDevAppAna(self, 4096, i_dev_debug_active)
        self.s_restart = i_restart

    # ------------------------------------------------------------------------
    def gf_Start(self):
        # cfg
        self.s_cfg.gf_LoadConfig()

        tusrcnt = self.s_cfg.s_user_max_cnt * 2
        if 0 == tusrcnt:
            tusrcnt = 2
        tdevcnt = self.s_cfg.s_device_max_cnt * 2
        if 0 == tdevcnt:
            tdevcnt = 2
       
        self.s_usr_obj.gf_Start(self.s_cfg.s_host,
                                self.s_cfg.s_user_port,
                                tusrcnt,
                                self.s_cfg.s_user_timeout )

        self.s_dev_obj.gf_Start(self.s_cfg.s_host,
                                self.s_cfg.s_device_port,
                                tdevcnt,
                                self.s_cfg.s_device_timeout )

    # ------------------------------------------------------------------------
    def gf_Stop(self):
        self.s_dev_obj.gf_Stop()
        self.s_usr_obj.gf_Stop()
        UtilAna.gf_Sleep(1)


# ============================================================================
# end of file
