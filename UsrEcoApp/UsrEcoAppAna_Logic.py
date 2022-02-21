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
import TcpClientAna_ParentSocHndl

import importlib
try:
    import UserOneCfgAna
except  Exception:
    pass

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
    def __init__(self, i_cfg, i_max_bufsize, i_debug_active):
        self.s_cfgNew = i_cfg
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

        self.s_dev_max = self.s_cfgNew.s_User_DeviceMaxAllowed
        self.s_dev_secdata_rcvs = [False for i in range(self.s_dev_max)]
        self.s_dev_longavgs = [0 for i in range(self.s_dev_max)]
        self.s_dev_shrtavgs = [0 for i in range(self.s_dev_max)]
        self.s_dev_shrtsmpls = [0 for i in range(self.s_dev_max)]
        self.s_dev_shrtconts = [0 for i in range(self.s_dev_max)]
        self.s_dev_idl_tmr = 0
        
        self.s_file_mm = self.pf_FileNameMm()
        self.s_datafile_hndl = None
        self.s_eventfile_hndl = None
        self.pf_OpenFileMm()

    # ------------------------------------------------------------------------
    def pf_Debug(self, i_id, i_eve_id):
        if True == self.s_debug_active:
            s = 'USER_SOC_' + str(i_id) + '_' + i_eve_id
            UtilAna.gf_DebugLog( s )

    # ------------------------------------------------------------------------
    def pf_PreareFileName(self, i_str):
        mm = UtilAna.gf_GetNowMinutes()
        mt = mm % self.s_cfgNew.s_FileSave_MaxDurationMin
        mm = mm - mt
        return mm

    # ------------------------------------------------------------------------
    def pf_FileNameMm(self):
        mm = UtilAna.gf_GetNowMinutes()
        mt = mm % self.s_cfgNew.s_FileSave_MaxDurationMin
        mm = mm - mt
        return mm

    # ------------------------------------------------------------------------
    def pf_OpenFileMm(self):
        if self.s_datafile_hndl == None:
            s = UtilAna.gf_UsrEcoAppFileNameStr(self.s_file_mm, "DATA_", self.s_cfgNew.s_Device_HDFilePath)
            print(("Open File : " + s))
            self.s_datafile_hndl = UtilAna.gf_FileAna_Open( s, "w+" )
        
        if self.s_eventfile_hndl == None:
            s = UtilAna.gf_UsrEcoAppFileNameStr(self.s_file_mm, "EVENT_", self.s_cfgNew.s_Device_HDFilePath)
            print(("Open File : " + s))
            self.s_eventfile_hndl = UtilAna.gf_FileAna_Open( s, "w+" )

    # ------------------------------------------------------------------------
    def pf_CloseFileMm(self):
        if self.s_datafile_hndl != None:
            UtilAna.gf_FileAna_Close( self.s_datafile_hndl )
            self.s_datafile_hndl = None

        if self.s_eventfile_hndl != None:
            UtilAna.gf_FileAna_Close( self.s_eventfile_hndl )
            self.s_eventfile_hndl = None

    # ------------------------------------------------------------------------
    def pf_ChkFileMm(self):
        mm = self.pf_FileNameMm()
        if mm != self.s_file_mm:
            self.pf_CloseFileMm()
            self.s_file_mm = mm
        self.pf_OpenFileMm()
    
    def pf_SaveEventFile(self, i_did, i_ecnt):
        self.pf_ChkFileMm()
        if None != self.s_eventfile_hndl:
            ms = str(self.s_cfgNew.s_Device_MacIds[i_did])
            mn = str(self.s_cfgNew.s_Device_Names[i_did])
            dd = UtilAna.gf_GetDataStr()
            dt = UtilAna.gf_GetTimeStr()
            s = ms + "," + mn + "," + dd  + "," + dt + "," + str(i_ecnt) + "\n"
            UtilAna.gf_FileAna_Write(self.s_eventfile_hndl, None, s)

    def pf_SaveDataFile(self, i_did, m):
        self.pf_ChkFileMm()
        if None != self.s_datafile_hndl:
            pass
            # ms = str(self.s_cfgNew.s_Device_MacIds[i_did])
            # mn = str(self.s_cfgNew.s_Device_Names[i_did])
            # dd = UtilAna.gf_GetDataStr()
            # dt = UtilAna.gf_GetTimeStr()
            # s = ms + "," + mn + "," + dd  + "," + dt + "," + str(m) + "\n"
            # UtilAna.gf_FileAna_Write(self.s_datafile_hndl, None, s)

    # ------------------------------------------------------------------------
    def pf_IsDevMacPresent(self, i_mac):
        if 0 != i_mac:
            if 0 != self.s_dev_max:
                for i in range(0, self.s_dev_max, 1):
                    if i_mac == self.s_cfgNew.s_Device_MacIds[i]:
                        return i
        return self.s_dev_max

    # ------------------------------------------------------------------------
    def pf_updateWaveData(self, i_bufid, i_data):
        bf = self.s_cfgNew.s_Device_LiveData
        ds1 = self.s_cfgNew.s_Device_SamplePerSec
        ddm = self.s_cfgNew.s_Device_MaxFileDataSize
        bf[i_bufid][ddm-ds1:ddm] = i_data[0:ds1]
        bf[i_bufid][0:ddm-ds1] = bf[i_bufid][ds1:ddm]

    # ------------------------------------------------------------------------
    def pf_RxdSaveDeviceWaveData(self, i_bufid, i_data):
        self.s_dev_secdata_rcvs[i_bufid] = True
        self.pf_updateWaveData(i_bufid, i_data)

    # ------------------------------------------------------------------------
    def pf_IdleSaveDeviceWaveData(self):
        self.s_dev_idl_tmr = self.s_dev_idl_tmr + 1
        if self.s_dev_idl_tmr > 2:
            self.s_dev_idl_tmr = 0
            self.pf_ChkFileMm()
            m = [0]*self.s_cfgNew.s_Device_SamplePerSec
            for i in range(0, self.s_dev_max, 1):
                if True != self.s_dev_secdata_rcvs[i]:
                    self.s_dev_longavgs[i] = 0
                    self.pf_updateWaveData(i,m)
                else:
                    self.s_dev_secdata_rcvs[i] = False

    # ------------------------------------------------------------------------
    def gf_GetLiveGuiNSecData(self, i_sec, i_devcnt, i_mac, i_data, i_eve_cnts, i_eve_rates):
        f = False
        ds1 = self.s_cfgNew.s_Device_SamplePerSec
        ddm = self.s_cfgNew.s_Device_MaxFileDataSize
        s = ddm - (i_sec+1)*ds1
        e = ddm - (1)*ds1
        m = [0]*(e-s)
        for i in range(0, i_devcnt, 1):
            f = False
            for j in range(0, self.s_dev_max, 1):
                if i_mac[i] == self.s_cfgNew.s_Device_MacIds[j]:
                    i_data[i][0:e-s] = self.s_cfgNew.s_Device_LiveData[j][s:e]
                    i_eve_cnts[i] = self.s_cfgNew.s_Device_EventCounts[j]
                    i_eve_rates[i] = self.s_cfgNew.s_Device_LastEventRates[j]
                    f = True
                    break
            if False == f:
                i_data[i][0:e-s] = m[0:e-s]
                i_eve_cnts[i] = 0
                i_eve_rates[i] = 0
                
        
    # ------------------------------------------------------------------------
    def pf_SendUserCmd(self, i_len, i_cmd_type):
        i_len += 2
        self.s_out_msg_buf[0:2] = UtilAna.gf_FillUintToBinaryLi(i_len, 2)
        self.s_out_msg_buf[2] = i_cmd_type
        self.s_out_msg_buf[3:5] = UtilAna.gf_FillUintToBinaryLi( self.s_cfgNew.s_UserSelfId, 2 )
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
        if 1 != self.s_cfgNew.s_UserSelfId:
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
    def gf_EventFoundLogic(self, i_did, i_ds1, i_rcv_data):
        m = [0] * i_ds1
        k = 18

        lta_l = self.s_dev_longavgs[i_did]
        lta_n = lta_l
        
        sta_lav = self.s_dev_shrtavgs[i_did]
        sta_lscnt = self.s_dev_shrtsmpls[i_did]
        sta_lcesa = self.s_dev_shrtconts[i_did]
 
        dev_eve_cnts = self.s_cfgNew.s_Device_EventCounts[i_did]
        dev_eve_times = self.s_cfgNew.s_Device_LastEventTimes[i_did]
        dev_eve_rates = self.s_cfgNew.s_Device_LastEventRates[i_did]
        
        sta_cvc = self.s_cfgNew.s_Device_StaSmplCnts[i_did]
        sta_efra = self.s_cfgNew.s_Device_StaLtaRatios[i_did]
        sta_efcc = self.s_cfgNew.s_Device_StaPattnCnts[i_did]
        eve_found = False
        
        for i in range(0, i_ds1, 1):
            z = UtilAna.gf_BinaryLiToInt( i_rcv_data[k:k+2],2 )
            z = round( (((z * 5.12)/65536) - 2.56), 5)
            m[i] = z
            lta_n = lta_n + abs(z)
            sta_lav = sta_lav + abs(z)
            sta_lscnt = sta_lscnt + 1
            if sta_lscnt >= sta_cvc:
                sta_lscnt = 0
                sta_lav = round((sta_lav/(sta_cvc+1)), 5)
                if 0 == lta_l:
                    lta_l = sta_lav
                    z = 1
                else:
                    z = sta_lav / lta_l
                if z > sta_efra:
                    sta_lcesa = sta_lcesa + 1
                    if sta_lcesa == sta_efcc:
                        eve_found = True
                        dev_eve_cnts = dev_eve_cnts + 1
                        tms = UtilAna.gf_GetDataTimeStemp()
                        tmd = tms - dev_eve_times
                        if 0 == tmd:
                            tmd = 1
                        dev_eve_rates = round( (3600/tmd), 3)
                        dev_eve_times = tms
                        self.pf_SaveEventFile(i_did, dev_eve_cnts)
                else:
                    sta_lcesa = 0
            k += 2
        
        lta_l = round( (lta_n/(i_ds1+1)), 5)
        self.s_dev_longavgs[i_did] = lta_l
        
        self.s_dev_shrtavgs[i_did] = sta_lav
        self.s_dev_shrtsmpls[i_did] = sta_lscnt
        self.s_dev_shrtconts[i_did] = sta_lcesa
        
        self.s_cfgNew.s_Device_EventCounts[i_did] = dev_eve_cnts
        self.s_cfgNew.s_Device_LastEventTimes[i_did] = dev_eve_times
        self.s_cfgNew.s_Device_LastEventRates[i_did] = dev_eve_rates
        self.pf_RxdSaveDeviceWaveData(i_did, m)
        self.pf_SaveDataFile(i_did, m)
        if True == eve_found:
            self.s_cfgNew.s_Cfg_Change = True
            self.s_cfgNew.gf_SaveCfg()
        
    # ------------------------------------------------------------------------
    def gf_ExeDevEveData(self, i_rcvlen, i_rcv_data):
        ds1 = self.s_cfgNew.s_Device_SamplePerSec
        inlen = UtilAna.gf_BinaryLiToInt(i_rcv_data[5:7], 2)
        intype = i_rcv_data[7]
        inmac = UtilAna.gf_BinaryLiToInt(i_rcv_data[8:14], 6)
        if inlen == (i_rcvlen - 7):
            if 8 == intype:      # data frame
                if ((ds1*2)+15) == inlen:
                    t = self.pf_IsDevMacPresent(inmac)
                    if t == self.s_dev_max:
                        s = "DevData_MAC_" + str(inmac) + " : Not Configured"
                        UtilAna.gf_DebugLog( s )
                        return
                    # save data in device data
                    self.gf_EventFoundLogic(t, ds1, i_rcv_data)
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
        if inid == self.s_cfgNew.s_UserSelfId:
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
            self.pf_IdleSaveDeviceWaveData()
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
                if self.s_usr_tmr > (self.s_cfgNew.s_RemoteHost_InactivitySec-5):
                    self.pf_SendKeepAliveCmd()
                elif self.s_usr_tmr > self.s_cfgNew.s_RemoteHost_InactivitySec:
                    self.s_clt_obj.gf_CloseClient( 1 )
                    self.s_usr_state = 1

    # ------------------------------------------------------------------------
    def gf_Start(self):
        self.s_rxq_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_IncommingEve)
        self.s_app_thread = UtilAna.gf_StartThreadAna(self.pf_ThreadFun_App)
        ih = self.s_cfgNew.s_RemoteHost_IP
        ip = self.s_cfgNew.s_RemoteHost_Port
        it = self.s_cfgNew.s_RemoteHost_InactivitySec
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
        self.pf_CloseFileMm()

# ============================================================================
# end of file
