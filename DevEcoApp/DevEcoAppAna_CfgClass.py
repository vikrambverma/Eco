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
try:
    import DevEcoAppAna_CfgFile as c_cfg
except Exception:
    pass

gv_DfltHost = '165.22.216.99'
# gv_DfltHost = '127.0.0.1'
gv_DfltPortNum = 40000
gv_DfltInactivityTimeout = 10
gv_DfltDeviceMacs = [1,2]

# ============================================================================
class AppConfigAna:
    """
    """
    
    
    # ------------------------------------------------------------------------
    def __init__(self):
        self.s_host = gv_DfltHost
        self.s_port = gv_DfltPortNum
        self.s_inactivity_timeout = gv_DfltInactivityTimeout
        self.s_dev_max = 0
        self.s_dev_macs = []


    # ------------------------------------------------------------------------
    def pf_AppendDevMac(self, i_mac_id):
            self.s_dev_macs.append( i_mac_id )
            self.s_dev_max = self.s_dev_max + 1


    # ------------------------------------------------------------------------
    def pf_IsDeviceMacIdPresent(self, i_mac_id):
        if 0 != i_mac_id:
            if 0 != self.s_dev_max:
                for i in range(0, self.s_dev_max, 1):
                    if i_mac_id == self.s_dev_macs[i]:
                        return i
        return self.s_dev_max


    # ------------------------------------------------------------------------
    def pf_AddNewDevMac(self, i_mac_id):
        if 0 != i_mac_id:
            i = self.pf_IsDeviceMacIdPresent( i_mac_id )
            if i == self.s_dev_max:
                self.pf_AppendDevMac( i_mac_id )


    # ------------------------------------------------------------------------
    def pf_UpdateMacs(self, i_macs):
        lt = len(i_macs)
        for i in range(0, lt, 1):
            self.pf_AddNewDevMac( i_macs[i] )
    

    # ------------------------------------------------------------------------
    def gf_LoadConfig(self):
        save_req = False
        try:
            self.s_host = c_cfg.gv_Host
            self.s_port = c_cfg.gv_PortNum
            self.s_inactivity_timeout = c_cfg.gv_InactivityTimeout
        except Exception:
            self.s_host = gv_DfltHost
            self.s_port = gv_DfltPortNum
            self.s_inactivity_timeout = gv_DfltInactivityTimeout
            save_req = True
        try:
            m = c_cfg.gv_DeviceMacs
            if len(m) > 0:
                self.pf_UpdateMacs( m )
            else:
                self.pf_UpdateMacs( gv_DfltDeviceMacs )
                save_req = True
        except Exception:
            self.pf_UpdateMacs( gv_DfltDeviceMacs )
            save_req = True
        if True == save_req:
            self.gf_SaveConfig()


    # ------------------------------------------------------------------------
    def gf_SaveConfig(self):
        try:
            fh = open("DevEcoAppAna_CfgFile.py","w+")

            s = "gv_Host = '" + str(self.s_host) + str("'\n")
            fh.write( s )
            UtilAna.gf_DebugLog( s )

            s = "gv_PortNum = " + str(self.s_port) + str("\n")
            fh.write( s )
            UtilAna.gf_DebugLog( s )

            s = "gv_InactivityTimeout = " + str(self.s_inactivity_timeout) + str("\n")
            fh.write( s )
            UtilAna.gf_DebugLog( s )

            s = "gv_DeviceMacs = " + str(self.s_dev_macs) + str("\n")
            fh.write( s )
            UtilAna.gf_DebugLog( s )

            fh.close()
            UtilAna.gf_DebugLog("[SAVE OK] : DevEcoAppAna_CfgFile.py")
        except Exception:
            UtilAna.gf_DebugLog("[SAVE FAILED] : DevEcoAppAna_CfgFile.py")


# =============================================================================
# end of file

