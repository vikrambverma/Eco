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
try:
    import UsrEcoAppAna_CfgFile as c_cfg
except Exception:
    pass

gv_DfltHost = '164.52.212.8'
# gv_DfltHost = '127.0.0.1'
gv_DfltPort = 30000
gv_DfltDeviceMacs = []
gv_DfltSelfUserId = 2
gv_DfltInactivityTimeout = 60

# ============================================================================
class AppConfigAna:
    """
    """
    
    
    # ------------------------------------------------------------------------
    def __init__(self):
        self.s_host = gv_DfltHost
        self.s_port = gv_DfltPort
        self.s_self_userid = gv_DfltSelfUserId
        self.s_inactivity_timeout = gv_DfltInactivityTimeout
        self.s_self_dev_max = 0
        self.s_self_dev_macs = []

    # ------------------------------------------------------------------------
    def pf_AppendSelfDevMac(self, i_mac_id):
            self.s_self_dev_macs.append( i_mac_id )
            self.s_self_dev_max = self.s_self_dev_max + 1


    # ------------------------------------------------------------------------
    def pf_IsSelfDeviceMacIdPresent(self, i_mac_id):
        if 0 != i_mac_id:
            if 0 != self.s_self_dev_max:
                for i in range( 0, self.s_self_dev_max, 1):
                    if i_mac_id == self.s_self_dev_macs[i]:
                        return i
        return self.s_self_dev_max


    # ------------------------------------------------------------------------
    def pf_AddNewSelfDevMac(self, i_mac_id):
        if 0 != i_mac_id:
            i = self.pf_IsSelfDeviceMacIdPresent( i_mac_id )
            if i == self.s_self_dev_max:
                self.pf_AppendSelfDevMac( i_mac_id )


    # ------------------------------------------------------------------------
    def pf_UpdateSelfMacs(self, i_macs):
        l = len(i_macs)
        for i in range(0, l, 1):
            self.pf_AddNewSelfDevMac( i_macs[i] )
    

    # ------------------------------------------------------------------------
    def gf_LoadConfig(self):
        save_req = False
        try:
            self.s_host = c_cfg.gv_Host
            self.s_port = c_cfg.gv_Port
            self.s_inactivity_timeout = c_cfg.gv_InactivityTimeout
            self.s_self_userid = c_cfg.gv_SelfUserId
            if gv_DfltSelfUserId != self.s_self_userid:
                self.s_self_userid = gv_DfltSelfUserId
                save_req = True
        except Exception:
            self.s_host = gv_DfltHost
            self.s_port = gv_DfltPort
            self.s_inactivity_timeout = gv_DfltInactivityTimeout
            self.s_self_userid = gv_DfltSelfUserId
            save_req = True
        try:
            m = c_cfg.gv_SelfDeviceMacs
            if len(m) > 0:
                self.pf_UpdateSelfMacs( m )
            else:
                self.pf_UpdateSelfMacs( gv_DfltDeviceMacs )
                save_req = True
        except Exception:
            self.pf_UpdateSelfMacs( gv_DfltDeviceMacs )
            save_req = True
        if True == save_req:
            self.gf_SaveConfig()


    # ------------------------------------------------------------------------
    def gf_SaveConfig(self):
        fh = open("UsrEcoAppAna_CfgFile.py","w+")

        s = "gv_Host = '" + str(self.s_host) + "'\n"
        fh.write( s )

        s = "gv_Port = " + str(self.s_port) + "\n"
        fh.write( s )

        s = "gv_InactivityTimeout = " + str(self.s_inactivity_timeout) + "\n"
        fh.write( s )

        s = "gv_SelfUserId = " + str(self.s_self_userid) + "\n"
        fh.write( s )

        s = "gv_SelfDeviceMacs = " + str(self.s_self_dev_macs) + "\n"
        fh.write( s )

        fh.close()

# ============================================================================
# end of file

