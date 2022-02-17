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
import UsrEcoAppAna_CfgClass
import TcpClientAna_ParentSocHndl

import importlib
import numpy as np
import matplotlib.pyplot as plt
try:
    import UserOneCfgAna
except  Exception:
    pass

gv_DfltSec = 10
gv_Dflt1SecDSize = 1000
gv_DfltDSize = (gv_Dflt1SecDSize * gv_DfltSec)
gv_DfltXAxis = np.linspace(0, gv_DfltSec, gv_DfltDSize)
gv_ClrTbl = ['red', 'green', 'blue', 'orange', 'black']

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
class UsrAppAna:
    def __init__(self, i_max_bufsize, i_debug_active):
        self.s_cfg = UsrEcoAppAna_CfgClass.AppConfigAna()
        self.s_debug_active = i_debug_active
        self.s_max_bufsize = i_max_bufsize
        self.s_clt_obj = TcpClientAna_ParentSocHndl.ParentTcpClientSocHndlAna(\
                                            'Device_TcpClient', False)
        self.s_rxq_thread_active = False
        self.s_rxq_thread = None
        self.s_usr_state = 0
        self.s_usr_tmr = 0
        self.s_soc_frame_obj = RxDataFrameAna(self.s_max_bufsize)
        self.s_out_msg_buf = bytearray(self.s_max_bufsize)
        self.s_app_thread_active = False
        self.s_app_thread = None
        self.s_ticks = 0

        self.s_dev_max = 0
        self.s_dev_macs = []
        self.s_dev_wave_data = []
        
        self.s_fig = plt.figure()
        gs = self.s_fig.add_gridspec(8, hspace=0)
        self.s_axs = gs.subplots(sharex=True, sharey=True)
        self.s_fig.suptitle('Eco Device Graph')
        for ax in self.s_axs:
            ax.label_outer()
    
    # ------------------------------------------------------------------------
    def pf_Debug(self, i_id, i_eve_id):
        if True == self.s_debug_active:
            s = 'USER_SOC_' + str(i_id) + '_' + i_eve_id
            UtilAna.gf_DebugLog( s )

    # ------------------------------------------------------------------------
    def pf_IsDevMacPresent(self, i_mac):
        if 0 != i_mac:
            if 0 != self.s_dev_max:
                for i in range(0, self.s_dev_max, 1):
                    if i_mac == self.s_dev_macs[i]:
                        return i
        return self.s_dev_max

    # ------------------------------------------------------------------------
    def pf_AddMac(self, i_mac):
        if 0 != i_mac:
            i = self.pf_IsDevMacPresent( i_mac )
            if i == self.s_dev_max:
                self.s_dev_macs.append( i_mac )
                self.s_dev_wave_data.append( [0]*gv_DfltDSize )
                self.s_dev_max += 1

    # ------------------------------------------------------------------------
    def pf_updatewavedata(self, i_bufid, i_start, i_end, i_data):
        j = 0
        for i in range(i_start, i_end, 1):
            self.s_dev_wave_data[i_bufid][i] = i_data[j]
            j += 1

    # ------------------------------------------------------------------------
    def pf_SaveDeviceWaveData(self, i_bufid, i_data):
        sk = gv_DfltDSize-gv_Dflt1SecDSize
        ek = gv_DfltDSize
        self.pf_updatewavedata(i_bufid, sk, ek, i_data )

    # ------------------------------------------------------------------------
    def pf_ShiftDeviceWaveData(self):
        sk = gv_DfltDSize-gv_Dflt1SecDSize
        for i in range(0, self.s_dev_max, 1):
            self.pf_updatewavedata(i, 0, sk, self.s_dev_wave_data[i][gv_Dflt1SecDSize:])
            m = [0]*gv_Dflt1SecDSize
            self.pf_SaveDeviceWaveData( i, m )

    def gf_ShowDeviceData(self):
        # show graph here
        for i in range(0, self.s_dev_max, 1):
            c = gv_ClrTbl[i%5]
            self.s_axs[i].clear()
            self.s_axs[i].plot(gv_DfltXAxis, self.s_dev_wave_data[i], c)
            self.s_axs[i].set_ylabel(str(self.s_dev_macs[i]), rotation=0, labelpad=40)
        if 0 == self.s_dev_max:
            self.s_axs[0].clear()
            self.s_axs[0].plot(gv_DfltXAxis, gv_DfltXAxis)
        self.s_fig.canvas.draw()
        self.s_fig.canvas.flush_events()
                
        # shift data by one second and fill zero
        self.pf_ShiftDeviceWaveData()


    # ------------------------------------------------------------------------
    def pf_SendUserCmd(self, i_len, i_cmd_type):
        i_len += 2
        self.s_out_msg_buf[0:2] = UtilAna.gf_FillUintToBinaryLi(i_len, 2)
        self.s_out_msg_buf[2] = i_cmd_type
        self.s_out_msg_buf[3:5] = UtilAna.gf_FillUintToBinaryLi( self.s_cfg.s_self_userid, 2 )
        self.s_out_msg_buf[i_len-2:i_len] = [0]*2
        self.s_clt_obj.gf_SendOutMsg( 1, self.s_out_msg_buf[0:i_len] )

    # ------------------------------------------------------------------------
    def pf_SendAuthFrame(self):
        self.pf_SendUserCmd( 5, 2 )
    
    def pf_SendKeepAliveCmd(self):
        self.pf_SendUserCmd( 5, 1 )

    def pf_SendSaveCfgCmd(self):
        self.pf_SendUserCmd( 5, 3 )

    # ------------------------------------------------------------------------
    def pf_SendSetUserIdCmd(self, i_offset):
        # id
        self.s_out_msg_buf[5:7] = UtilAna.gf_FillUintToBinaryLi( i_offset, 2 )
        self.s_out_msg_buf[7:9] = UtilAna.gf_FillUintToBinaryLi( i_offset+1, 2 )
        self.pf_SendUserCmd( 9, 8 )

    def pf_SendSetUserNameCmd(self, i_offset, i_name):
        # name
        self.s_out_msg_buf[5:7] = UtilAna.gf_FillUintToBinaryLi( i_offset, 2 )
        l = len( i_name )
        self.s_out_msg_buf[7:7+l] = UtilAna.gf_GetStrToBytes( i_name )
        self.pf_SendUserCmd( 7+l, 9 )

    def pf_SendSetUserPasswardCmd(self, i_offset, i_passward):
        # password
        self.s_out_msg_buf[5:7] = UtilAna.gf_FillUintToBinaryLi( i_offset, 2 )
        l = len( i_passward )
        self.s_out_msg_buf[7:7+l] = UtilAna.gf_GetStrToBytes( i_passward )
        self.pf_SendUserCmd( 7+l, 10 )
        
    def pf_SendSetUserTypeCmd(self, i_offset, i_usrtype):
        # type
        self.s_out_msg_buf[5:7] = UtilAna.gf_FillUintToBinaryLi( i_offset, 2 )
        l = len( i_usrtype )
        self.s_out_msg_buf[7:7+l] = UtilAna.gf_GetStrToBytes( i_usrtype )
        self.pf_SendUserCmd( 7+l, 11 )
        
    def pf_SendSetUserMacListCmd(self, i_offset, i_macs):
        # user device macs
        ml = len( i_macs )
        for i in range(0, ml, 1):
            self.s_out_msg_buf[5:7] = UtilAna.gf_FillUintToBinaryLi( i_offset, 2 )
            t = i_macs[i]
            self.s_out_msg_buf[7:13] = UtilAna.gf_FillUintToBinaryLi( t, 6 )
            self.pf_SendUserCmd( 13, 12 )

    def pf_SendSetTimeoutsCmd(self, i_usr_soc_timeout, i_dev_soc_timeout):
        # user, device timeouts
        self.s_out_msg_buf[5:7] = UtilAna.gf_FillUintToBinaryLi( i_usr_soc_timeout, 2 )
        self.s_out_msg_buf[7:9] = UtilAna.gf_FillUintToBinaryLi( i_dev_soc_timeout, 2 )
        self.pf_SendUserCmd( 9, 4 )

   # ------------------------------------------------------------------------
    def pf_ChkUsrOneCfgChange(self):
        if 1 != self.s_cfg.s_self_userid:
            return
        importlib.reload(UserOneCfgAna)
        try:
            m_chnge = UserOneCfgAna.gv_Master_CfgChanged
        except Exception:
            return
        if True != m_chnge:
            return
        try:
            m_usrt = UserOneCfgAna.gv_Master_UserTimeout
            m_devt = UserOneCfgAna.gv_Master_DeviceTimeout
            m_names = UserOneCfgAna.gv_Master_UserNames
            m_passwords = UserOneCfgAna.gv_Master_UserPasswords
            m_types = UserOneCfgAna.gv_Master_UserTypes
            m_devlist = UserOneCfgAna.gv_Master_UserDevMacs
        except Exception:
            return
        
        l = len(m_names)
        for i in range(0, l , 1):
            self.pf_SendSetUserIdCmd( i )
            self.pf_SendSetUserNameCmd( i, m_names[i] )
            self.pf_SendSetUserPasswardCmd( i, m_passwords[i] )
            self.pf_SendSetUserTypeCmd( i, m_types[i] )
            self.pf_SendSetUserMacListCmd( i , m_devlist[i] )
            s = str(i+1) + "_" + str(m_names[i]) + "_" + str(m_passwords[i]) + "_" + str(m_types[i]) + "_" + str(m_devlist[i]) + "\n"
            print(s)
        self.pf_SendSetTimeoutsCmd(m_usrt, m_devt)
        self.pf_SendSaveCfgCmd()
        m_chnge = False

        fh = open("UserOneCfgAna.py","w+")
        s = "gv_Master_CfgChanged = " + str(m_chnge) + "\n"
        fh.write(s)

        s = "gv_Master_DeviceTimeout = " + str(m_devt) + "\n"
        fh.write(s)

        s = "gv_Master_UserTimeout = " + str(m_usrt) + "\n"
        fh.write(s)

        s = "gv_Master_UserNames = " + str(m_names) + "\n"
        fh.write(s)

        s = "gv_Master_UserPasswords = " + str(m_passwords) + "\n"
        fh.write(s)

        s = "gv_Master_UserTypes = " + str(m_types) + "\n"
        fh.write(s)

        s = "gv_Master_UserDevMacs = " + str(m_devlist) + "\n"
        fh.write(s)

        fh.close()

    # ------------------------------------------------------------------------
    def gf_ExeDevEveData(self, i_rcvlen, i_rcv_data):
        inlen = UtilAna.gf_BinaryLiToInt(i_rcv_data[5:7], 2)
        intype = i_rcv_data[7]
        inmac = UtilAna.gf_BinaryLiToInt(i_rcv_data[8:14], 6)
        if inlen == (i_rcvlen - 7):
            if 8 == intype:      # data frame
                if 2063 == inlen:
                    t = self.pf_IsDevMacPresent(inmac)
                    if t == self.s_dev_max:
                        self.pf_AddMac( inmac )
                        s = "DevData_MAC_" + str(inmac)
                        UtilAna.gf_DebugLog( s )
                    # save data in device data
                    m = [0] * 1000
                    k = 18
                    for i in range(0,1000,1):
                        m[i] = UtilAna.gf_BinaryLiToInt(i_rcv_data[k:k+2],2)
                        m[i] = m[i] * 5.12/65536 - 2.56
                        k += 2
                    self.pf_SaveDeviceWaveData(t, m)
            elif 9 == intype:    # device info
                if 11 == inlen:
                    s = "DevInfo_MAC_" + str(inmac)
                    UtilAna.gf_DebugLog(s)


    # ------------------------------------------------------------------------
    def pf_ExeCmds(self, i_soc_id, i_rcv_data):
        rcvlen = len(i_rcv_data)
        inlen = UtilAna.gf_BinaryLiToInt(i_rcv_data[0:2], 2)
        inid = UtilAna.gf_BinaryLiToInt(i_rcv_data[3:5], 2)
        intype = i_rcv_data[2]
        if inid == self.s_cfg.s_self_userid:
            if rcvlen == inlen:
                if 128+1 == intype:       # keep alive response
                    self.s_usr_tmr = 0
                    # UtilAna.gf_DebugLog( "User keep alive OK" )
                elif 128+2 == intype:     # auth resopnse
                    self.s_usr_state = 4
                    self.s_usr_tmr = 0
                    UtilAna.gf_DebugLog( "User auth OK" )
                elif 128+120 == intype:      # device data frame
                    self.gf_ExeDevEveData( inlen, i_rcv_data )
                    # ECO back test for device
                    # i_rcv_data[2] = 120
                    # self.s_clt_obj.gf_SendOutMsg(1,i_rcv_data)

    # ------------------------------------------------------------------------
    def pf_ThreadFun_IncommingEve(self):
        self.s_rxq_thread_active = True
        while True == self.s_rxq_thread_active:
            UtilAna.gf_Sleep(0.5)
            while True:
                rxSocId, rxEveId, rxEveData = self.s_clt_obj.gf_GetEvents()
                if None == rxSocId or 0 == rxSocId:
                    break
                if 1 != rxSocId:
                    self.s_clt_obj.gf_Close(rxSocId)
                else:
                    if 'DATA' == rxEveId:
#                        self.pf_Debug(1, rxEveId)
                        self.s_soc_frame_obj.gf_GetFrame(1, rxEveData, self.pf_ExeCmds)
    
                    elif 'STOP' == rxEveId:
                        self.pf_Debug(1, rxEveId)
                        self.s_usr_state = 0
                        self.s_usr_tmr = 0
                        self.s_soc_frame_obj.gf_Clear()
        
                    elif "START" == rxEveId:
                        self.pf_Debug(1, rxEveId)
                        self.s_usr_state = 2
                        self.s_usr_tmr = 0
                        self.s_soc_frame_obj.gf_Clear()
    
                    else:
                        self.pf_Debug(1, rxEveId)
                        self.s_clt_obj.gf_Close(1)
                    
    # ------------------------------------------------------------------------
    def pf_ThreadFun_App(self):
        self.s_app_thread_active = True
        while True == self.s_app_thread_active:
            UtilAna.gf_Sleep(0.990)
            self.s_ticks += 1
            if 0 == self.s_usr_state:
                self.s_usr_tmr += 1
                if self.s_usr_tmr > 5:
                    self.s_clt_obj.gf_ConnectReq(1)
                    self.s_usr_state = 1
            elif 1 == self.s_usr_state:
                pass
            elif 2 == self.s_usr_state:
                self.pf_SendAuthFrame()
                self.s_usr_state = 3
            elif 3 == self.s_usr_state:
                pass
            elif 4 == self.s_usr_state:
                self.pf_ChkUsrOneCfgChange()
                self.s_usr_state = 5
                self.s_usr_tmr = 0
            else:
                t = self.s_ticks % 15
                if 0 == t:
                    self.pf_ChkUsrOneCfgChange()
                self.s_usr_tmr = self.s_usr_tmr + 1
                if self.s_usr_tmr > (self.s_cfg.s_inactivity_timeout-5):
                    self.pf_SendKeepAliveCmd()
                elif self.s_usr_tmr > self.s_cfg.s_inactivity_timeout:
                    self.s_clt_obj.gf_CloseClient( 1 )
                    self.s_usr_state = 1

    # ------------------------------------------------------------------------
    def gf_Start(self):
        self.s_cfg.gf_LoadConfig()
        self.s_rxq_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_IncommingEve)
        self.s_app_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_App)
        ih = self.s_cfg.s_host
        ip = self.s_cfg.s_port
        it = self.s_cfg.s_inactivity_timeout
        self.s_clt_obj.gf_Start(ih, ip, 1, it, 15)


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

# ============================================================================
# end of file
