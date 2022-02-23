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
import importlib
try:
    import GuiCfgFile
except Exception:
    pass

# ============================================================================
class CfgUserAppAna:
    """
    """
    
    
    # ------------------------------------------------------------------------
    def __init__(self):
        self.s_User_DeviceMaxAllowed = 16
        self.s_UserSelfId = 2
        
        self.s_FileSave_MaxDurationMin = 15
        self.s_FileData_SecMaxAllowed = self.s_FileSave_MaxDurationMin * 60
        self.s_Device_SamplePerSec = 1024
        self.s_Device_MaxFileDataSize = self.s_Device_SamplePerSec * self.s_FileData_SecMaxAllowed
 
        self.s_Cfg_Change = False
        
        self.s_Customer_Name = "MAPS Technologies"
        self.s_Customer_Site = "Officers Campus Extension, Jaipur"

        self.s_User_LoginId = 'user'
        self.s_User_LoginPwd = 'userpwd'
        self.s_User_Name = "user-1"

        self.s_Admin_LoginId = 'admin'
        self.s_Admin_LoginPwd = 'adminpwd'
        self.s_Admin_Name = "admin-1"

        self.s_RemoteHost_IP = '165.22.216.99'
        self.s_RemoteHost_Port = 0
        self.gf_SetRemoteHostPort(30000)
        self.s_RemoteHost_InactivitySec = 0
        self.gf_SetRemoteHostInactivitySec(60)

        self.s_Device_LiveDataSec = 0
        self.gf_SetDeviceLiveDataSec(10)
        self.s_Device_HDFilePath = "./.."
        self.s_Device_HDWindowSec = 0
        self.gf_SetDeviceHDWindowSec(10)
        self.s_Device_HDWStep1 = 0
        self.gf_SetDeviceHDWStep1(2)
        self.s_Device_HDWStep2 = 0
        self.gf_SetDeviceHDWStep1(5)
        
        self.s_Device_MacIds = [i+1 for i in range(0, self.s_User_DeviceMaxAllowed, 1) ]
        self.s_Device_Names = ['CH-'+str(i+1) for i in range(0, self.s_User_DeviceMaxAllowed, 1) ]
        self.s_Device_LDVEnableds = [0 for i in range(0, self.s_User_DeviceMaxAllowed, 1) ]
        self.s_Device_EventCounts = [0 for i in range(0, self.s_User_DeviceMaxAllowed, 1) ]
        self.s_Device_LastEventTimes = [0 for i in range(0, self.s_User_DeviceMaxAllowed, 1) ]
        self.s_Device_LastEventRates = [0 for i in range(0, self.s_User_DeviceMaxAllowed, 1)  ]
        self.s_Device_StaSmplCnts = [10 for i in range(0, self.s_User_DeviceMaxAllowed, 1)  ]
        self.s_Device_StaPattnCnts = [3 for i in range(0, self.s_User_DeviceMaxAllowed, 1)  ]
        self.s_Device_StaLtaRatios = [3 for i in range(0, self.s_User_DeviceMaxAllowed, 1)  ]

        self.s_Device_LiveData = [[0 for j in range(self.s_Device_MaxFileDataSize)] for i in range(self.s_User_DeviceMaxAllowed)]
        
        self.gf_LoadCfg(True)

    # ---------------------------------------------------------------------------
    def gf_SetCustomerName(self, i_name):
        if i_name != self.s_Customer_Name:
            self.s_Customer_Name = i_name
            self.s_Cfg_Change = True

    # ---------------------------------------------------------------------------
    def gf_SetCustomerSite(self, i_site):
        if i_site != self.s_Customer_Site:
            self.s_Customer_Site = i_site
            self.s_Cfg_Change = True

    # ---------------------------------------------------------------------------
    def gf_SetUserName(self, i_name):
        if i_name != self.s_User_Name:
            self.s_User_Name = i_name
            self.s_Cfg_Change = True

    def gf_SetUserLoginId(self, i_loginid):
        if i_loginid != self.s_User_LoginId:
            self.s_User_LoginId = i_loginid
            self.s_Cfg_Change = True

    def gf_SetUserLoginPwd(self, i_loginpwd):
        if i_loginpwd != self.s_User_LoginPwd:
            self.s_User_LoginPwd = i_loginpwd
            self.s_Cfg_Change = True

    # ---------------------------------------------------------------------------
    def gf_SetAdminName(self, i_name):
        if i_name != self.s_Admin_Name:
            self.s_Admin_Name = i_name
            self.s_Cfg_Change = True

    def gf_SetAdminLoginId(self, i_loginid):
        if i_loginid != self.s_Admin_LoginId:
            self.s_Admin_LoginId = i_loginid
            self.s_Cfg_Change = True

    def gf_SetAdminLoginPwd(self, i_loginpwd):
        if i_loginpwd != self.s_Admin_LoginPwd:
            self.s_Admin_LoginPwd = i_loginpwd
            self.s_Cfg_Change = True

    # ---------------------------------------------------------------------------
    def gf_SetRemoteHostIp(self, i_ip):
        if i_ip != self.s_RemoteHost_IP:
            self.s_RemoteHost_IP = i_ip
            self.s_Cfg_Change = True

    def gf_SetRemoteHostPort(self, i_port):
        if i_port != self.s_RemoteHost_Port:
            if i_port < 0 or i_port > 65535:
                i_port = 30000
            self.s_RemoteHost_Port = i_port
            self.s_Cfg_Change = True

    def gf_SetRemoteHostInactivitySec(self, i_sec):
        if i_sec != self.s_RemoteHost_InactivitySec:
            if i_sec < 1 or i_sec > 900:
                i_sec = 60
            self.s_RemoteHost_InactivitySec = i_sec
            self.s_Cfg_Change = True

    # ---------------------------------------------------------------------------
    def gf_SetDeviceLiveDataSec(self, i_sec):
        if i_sec != self.s_Device_LiveDataSec:
            if i_sec < 2 or i_sec > 25:
                i_sec = 2
            self.s_Device_LiveDataSec = i_sec
            self.s_Cfg_Change = True

    def gf_SetDeviceHDFilePath(self, i_fhpath):
        if i_fhpath != self.s_Device_HDFilePath:
            self.s_Device_HDFilePath = i_fhpath
            self.s_Cfg_Change = True

    def gf_SetDeviceHDWindowSec(self, i_sec):
        if i_sec != self.s_Device_HDWindowSec:
            if i_sec < 5 or i_sec > 25:
                i_sec = 5
            self.s_Device_HDWindowSec = i_sec
            self.s_Cfg_Change = True
    def gf_SetDeviceHDWStep1(self, i_sec):
        if i_sec != self.s_Device_HDWStep1:
            if i_sec < 1 or i_sec > 25:
                i_sec = 1
            self.s_Device_HDWStep1 = i_sec
            self.s_Cfg_Change = True
    def gf_SetDeviceHDWStep2(self, i_sec):
        if i_sec != self.s_Device_HDWStep2:
            if i_sec < 1 or i_sec > 25:
                i_sec = 2
            self.s_Device_HDWStep2 = i_sec
            self.s_Cfg_Change = True

    def gf_SetDeviceMacId(self, i_id, i_mac):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_mac != self.s_Device_MacIds[i_id]:
                if i_mac < 0 or i_mac > 281474976710655:
                    i_mac = 0
                self.s_Device_MacIds[i_id] = i_mac
                self.s_Cfg_Change = True

    def gf_SetDeviceName(self, i_id, i_name):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_name != self.s_Device_Names[i_id]:
                self.s_Device_Names[i_id] = i_name
                self.s_Cfg_Change = True

    def gf_SetDeviceLDVEnabled(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v != self.s_Device_LDVEnableds[i_id]:
                if i_v < 0 or i_v > 1:
                    i_v = 0
                self.s_Device_LDVEnableds[i_id] = i_v
                self.s_Cfg_Change = True

    def gf_SetDeviceEventCount(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v != self.s_Device_EventCounts[i_id]:
                self.s_Device_EventCounts[i_id] = i_v
                self.s_Cfg_Change = True

    def gf_SetDeviceLastEventTime(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v != self.s_Device_LastEventTimes[i_id]:
                self.s_Device_LastEventTimes[i_id] = i_v
                self.s_Cfg_Change = True

    def gf_SetDeviceLastEventRate(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v != self.s_Device_LastEventRates[i_id]:
                self.s_Device_LastEventRates[i_id] = i_v
                self.s_Cfg_Change = True

    def gf_SetDeviceStaSmplCnt(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v < 1 or i_v > 1000:
                i_v = 10
            i_v = int( (self.s_Device_SamplePerSec*i_v) / 1000) + 1
            if i_v != self.s_Device_StaSmplCnts[i_id]:
                self.s_Device_StaSmplCnts[i_id] = i_v
                self.s_Cfg_Change = True

    def gf_GetDeviceStaSmplCnt(self, i_id):
        v = 10
        if i_id < self.s_User_DeviceMaxAllowed:
            v = self.s_Device_StaSmplCnts[i_id]
            v = int((v*1000)/self.s_Device_SamplePerSec)
        return v

    def gf_SetDeviceStaPattnCnt(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v != self.s_Device_StaPattnCnts[i_id]:
                if i_v < 1 or i_v > 20:
                    i_v = 3
                self.s_Device_StaPattnCnts[i_id] = i_v
                self.s_Cfg_Change = True

    def gf_SetDeviceStaLtaRatio(self, i_id, i_v):
        if i_id < self.s_User_DeviceMaxAllowed:
            if i_v != self.s_Device_StaLtaRatios[i_id]:
                if i_v < 1 or i_v > 100:
                    i_v = 5
                self.s_Device_StaLtaRatios[i_id] = i_v
                self.s_Cfg_Change = True

    # ---------------------------------------------------------------------------
    def gf_LoadCfg(self, i_sts=False):
        fb = False
        try:
            importlib.reload(GuiCfgFile)
        except Exception:
            fb = True
        
        if False == fb:
            try:
                if True == GuiCfgFile.s_Cfg_Change:
    
                    try:
                        self.s_Customer_Name = GuiCfgFile.s_Customer_Name
                    except Exception:
                        fb = True
                    try:
                        self.s_Customer_Site = GuiCfgFile.s_Customer_Site
                    except Exception:
                        fb = True
    

                    try:
                        self.s_User_LoginId = GuiCfgFile.s_User_LoginId
                    except Exception:
                        fb = True
                    try:
                        self.s_User_LoginPwd = GuiCfgFile.s_User_LoginPwd
                    except Exception:
                        fb = True
                    try:
                        self.s_User_Name = GuiCfgFile.s_User_Name
                    except Exception:
                        fb = True
    

                    try:
                        self.s_Admin_LoginId = GuiCfgFile.s_Admin_LoginId
                    except Exception:
                        fb = True
                    try:
                        self.s_Admin_LoginPwd = GuiCfgFile.s_Admin_LoginPwd
                    except Exception:
                        fb = True
                    try:
                        self.s_Admin_Name = GuiCfgFile.s_Admin_Name
                    except Exception:
                        fb = True
    


                    try:
                        self.s_RemoteHost_IP = GuiCfgFile.s_RemoteHost_IP
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetRemoteHostPort( GuiCfgFile.s_RemoteHost_Port )
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetRemoteHostInactivitySec( GuiCfgFile.s_RemoteHost_InactivitySec )
                    except Exception:
                        fb = True



                    try:
                        self.gf_SetDeviceShortAvgCfg_SampleCnt( GuiCfgFile.s_Device_ShortAvgCfg_SampleCnt )
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetDeviceShortAvgCfg_ContEventCnt( GuiCfgFile.s_Device_ShortAvgCfg_ContEventCnt )
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetDeviceShortAvgCfg_RatioForEvent( GuiCfgFile.s_Device_ShortAvgCfg_RatioForEvent )
                    except Exception:
                        fb = True



                    try:
                        self.gf_SetDeviceLiveDataSec( GuiCfgFile.s_Device_LiveDataSec )
                    except Exception:
                        fb = True
    
                    try:
                        self.s_Device_HDFilePath = GuiCfgFile.s_Device_HDFilePath
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetDeviceHDWindowSec( GuiCfgFile.s_Device_HDWindowSec )
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetDeviceHDWStep1( GuiCfgFile.s_Device_HDWStep1 )
                    except Exception:
                        fb = True
                    try:
                        self.gf_SetDeviceHDWStep2( GuiCfgFile.s_Device_HDWStep2 )
                    except Exception:
                        fb = True

                    try:
                        for i in range(0, len(GuiCfgFile.s_Device_MacIds), 1):
                            self.gf_SetDeviceMacId( i, GuiCfgFile.s_Device_MacIds[i] )
                            self.gf_SetDeviceName(i, GuiCfgFile.s_Device_Names[i] )
                            self.gf_SetDeviceLDVEnabled(i, GuiCfgFile.s_Device_LDVEnableds[i] )
                            self.s_Device_StaSmplCnts[i] = GuiCfgFile.s_Device_StaSmplCnts[i]
                            self.gf_SetDeviceStaPattnCnt(i, GuiCfgFile.s_Device_StaPattnCnts[i] )
                            self.gf_SetDeviceStaLtaRatio(i, GuiCfgFile.s_Device_StaLtaRatios[i] )
                            if True == i_sts:
                                self.gf_SetDeviceEventCount(i, GuiCfgFile.s_Device_EventCounts[i] )
                                self.gf_SetDeviceLastEventTime(i, GuiCfgFile.s_Device_LastEventTimes[i] )
                                self.gf_SetDeviceLastEventRate(i, GuiCfgFile.s_Device_LastEventRates[i] )
                    except Exception:
                        fb = True
    
            except Exception:
                fb = True
                
        self.s_Cfg_Change = False
        if True == fb:
            self.s_Cfg_Change = True
        self.gf_SaveCfg()
    
    # ---------------------------------------------------------------------------
    def gf_SaveCfg(self):
        if True == self.s_Cfg_Change:
            fh = open("GuiCfgFile.py","w+")
            
            s = "s_Customer_Name = '" + str( self.s_Customer_Name ) + "'\n"
            fh.write( s )
            s = "s_Customer_Site = '" + str( self.s_Customer_Site ) + "'\n"
            fh.write( s )
            
            s = "s_User_LoginId = '" + str( self.s_User_LoginId ) + "'\n"
            fh.write( s )
            s = "s_User_LoginPwd = '" + str( self.s_User_LoginPwd ) + "'\n"
            fh.write( s )
            s = "s_User_Name = '" + str( self.s_User_Name ) + "'\n"
            fh.write( s )
    
            s = "s_Admin_LoginId = '" + str( self.s_Admin_LoginId ) + "'\n"
            fh.write( s )
            s = "s_Admin_LoginPwd = '" + str( self.s_Admin_LoginPwd ) + "'\n"
            fh.write( s )
            s = "s_Admin_Name = '" + str( self.s_Admin_Name ) + "'\n"
            fh.write( s )
    
        
            s = "s_RemoteHost_IP = '" + str( self.s_RemoteHost_IP ) + "'\n"
            fh.write( s )
            s = "s_RemoteHost_Port = " + str( self.s_RemoteHost_Port ) + "\n"
            fh.write( s )
            s = "s_RemoteHost_InactivitySec = " + str( self.s_RemoteHost_InactivitySec ) + "\n"
            fh.write( s )


            s = "s_Device_LiveDataSec = " + str( self.s_Device_LiveDataSec ) + "\n"
            fh.write( s )
            s = "s_Device_HDFilePath = '" + str( self.s_Device_HDFilePath ) + "'\n"
            fh.write( s )
            s = "s_Device_HDWindowSec = " + str( self.s_Device_HDWindowSec ) + "\n"
            fh.write( s )
            s = "s_Device_HDWStep1 = " + str( self.s_Device_HDWStep1 ) + "\n"
            fh.write( s )
            s = "s_Device_HDWStep2 = " + str( self.s_Device_HDWStep2 ) + "\n"
            fh.write( s )
        
            s = "s_Device_MacIds = " + str( self.s_Device_MacIds ) + "\n"
            fh.write( s )
            s = "s_Device_Names = " + str( self.s_Device_Names ) + "\n"
            fh.write( s )
            s = "s_Device_EventCounts = " + str( self.s_Device_EventCounts ) + "\n"
            fh.write( s )
            s = "s_Device_LastEventTimes = " + str( self.s_Device_LastEventTimes ) + "\n"
            fh.write( s )
            s = "s_Device_LastEventRates = " + str( self.s_Device_LastEventRates ) + "\n"
            fh.write( s )
            s = "s_Device_LDVEnableds = " + str( self.s_Device_LDVEnableds ) + "\n"
            fh.write( s )
            s = "s_Device_StaSmplCnts = " + str( self.s_Device_StaSmplCnts ) + "\n"
            fh.write( s )
            s = "s_Device_StaPattnCnts = " + str( self.s_Device_StaPattnCnts ) + "\n"
            fh.write( s )
            s = "s_Device_StaLtaRatios = " + str( self.s_Device_StaLtaRatios ) + "\n"
            fh.write( s )
            
            s = "s_Cfg_Change = " + str( self.s_Cfg_Change ) + "\n"
            fh.write( s )
      
            fh.close()
            
            self.s_Cfg_Change = False
        
# m = CfgUserAppAna()
# m.gf_LoadCfg()
      
# ============================================================================
# end of file
