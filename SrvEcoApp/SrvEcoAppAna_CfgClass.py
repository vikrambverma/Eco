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
import importlib
try:
    import SrvEcoAppAna_CfgFile as cfg
except Exception:
    pass

# gv_DfltHost = '127.0.0.1'
gv_DfltHost = '164.52.212.8'
gv_DlftUserPort = 30000
gv_DfltUserTimout = 900
gv_DfltDevicePort = 40000
gv_DlftDeviceTimout = 11

gv_DfltUserName = 'admin'
gv_DfltUserPassword = 'admin@1234'
gv_DfltUserId = 1 # dont change this
gv_DfltUserType = 'admin' # dont change this
gv_DfltUserDeviceMacs = []

# ============================================================================
class AppConfigAna:
    def __init__(self):
        self.s_host = gv_DfltHost
        
        self.s_device_port = gv_DfltDevicePort
        self.s_device_timeout = gv_DlftDeviceTimout
        self.s_device_max_cnt = 0
        self.s_device_macs = []

        self.s_user_port = gv_DlftUserPort
        self.s_user_timeout = gv_DfltUserTimout
        self.s_user_max_cnt = 0
        self.s_user_ids = []
        self.s_user_names = []
        self.s_user_passwords = []
        self.s_user_types = []
        self.s_user_dev_max = []
        self.s_user_dev_macs = []

    # ------------------------------------------------------------------------
    def pf_ClearAllUsrAllInfo(self):
        for i in range(0, len(self.s_user_ids), 1):
            self.s_user_ids.pop(0)
        for i in range(0, len(self.s_user_names), 1):
            self.s_user_names.pop(0)
        for i in range(0, len(self.s_user_passwords), 1):
            self.s_user_passwords.pop(0)
        for i in range(0, len(self.s_user_types), 1):
            self.s_user_types.pop(0)
        for i in range(0, len(self.s_user_dev_max), 1):
            self.s_user_dev_max.pop(0)
        for i in range(0, len(self.s_user_dev_macs), 1):
            self.s_user_dev_macs.pop(0)
        for i in range(0, len(self.s_device_macs), 1):
            self.s_device_macs.pop(0)
        self.s_device_max_cnt = 0
        self.s_user_max_cnt = 0

    # ------------------------------------------------------------------------
    def gf_GetUserId(self, i_usr_offset):
        if i_usr_offset < self.s_user_max_cnt:
            return self.s_user_ids[i_usr_offset]
        else:
            return 0
    def gf_GetUserName(self, i_usr_offset):
        if i_usr_offset < self.s_user_max_cnt:
            return self.s_user_names[i_usr_offset]
        else:
            return ""
    def gf_GetUserPassward(self, i_usr_offset):
        if i_usr_offset < self.s_user_max_cnt:
            return self.s_user_passwords[i_usr_offset]
        else:
            return ""
    def gf_GetUserType(self, i_usr_offset):
        if i_usr_offset < self.s_user_max_cnt:
            return self.s_user_types[i_usr_offset]
        else:
            return ""


    # ------------------------------------------------------------------------
    def pf_IsUserIdPresent(self, i_usr_id):
        for i in range(0, self.s_user_max_cnt, 1):
            if i_usr_id == self.s_user_ids[i]:
                return i
        return self.s_user_max_cnt
        

    # ------------------------------------------------------------------------
    def pf_AddUserId(self, i_usr_id):
        if 0 != i_usr_id:
            if self.s_user_max_cnt != self.pf_IsUserIdPresent( i_usr_id ):
                return False
            self.s_user_ids.append(i_usr_id)
            self.s_user_names.append("")
            self.s_user_passwords.append("")
            self.s_user_types.append("")
            self.s_user_dev_max.append(0)
            self.s_user_dev_macs.append([])
            self.s_user_max_cnt += 1
            return True
        return False

    # ------------------------------------------------------------------------
    def gf_SetUserId(self, i_usr_offset, i_usr_id):
        if 0 != i_usr_id:
            if 0 == i_usr_offset:
                self.pf_ClearAllUsrAllInfo()
            return self.pf_AddUserId(i_usr_id)
        return False
        

    def gf_SetUserName(self, i_usr_offset, i_usr_name):
        if i_usr_offset < self.s_user_max_cnt:
            if gv_DfltUserId == self.s_user_ids[i_usr_offset]:
                i_usr_name = gv_DfltUserName
            self.s_user_names[i_usr_offset] = i_usr_name
            return True
        return False

    def gf_SetUserPassward(self, i_usr_offset, i_usr_passward):
        if i_usr_offset < self.s_user_max_cnt:
            # if gv_DfltUserId == self.s_user_ids[i_usr_offset]:
            #     i_usr_passward = gv_DfltUserName
            self.s_user_passwords[i_usr_offset] = i_usr_passward
            return True
        return False

    def gf_SetUserType(self, i_usr_offset, i_usr_type):
        if i_usr_offset < self.s_user_max_cnt:
            if gv_DfltUserId == self.s_user_ids[i_usr_offset]:
                i_usr_type = gv_DfltUserType
            self.s_user_types[i_usr_offset] = i_usr_type
            return True
        return False

    def gf_SetUserMac(self, i_usr_offset, i_mac):
        if i_usr_offset < self.s_user_max_cnt:
            maccnt = self.s_user_dev_max[i_usr_offset] 
            for i in range(0, maccnt, 1):
                if i_mac == self.s_user_dev_macs[i_usr_offset][i]:
                    return False
            self.s_user_dev_macs[i_usr_offset].append(i_mac)
            self.s_user_dev_max[i_usr_offset] += 1
            for i in range(0, self.s_device_max_cnt, 1):
                if i_mac == self.s_device_macs[i]:
                    return True
            self.s_device_macs.append(i_mac)
            self.s_device_max_cnt += 1
            return True
        return False

    # ------------------------------------------------------------------------
    def pf_SetUserAllInfo(self, i_offset, i_usr_id, i_usr_name,
                          i_usr_passward, i_usr_type, i_macs):
        self.gf_SetUserId(i_offset, i_usr_id)
        self.gf_SetUserName(i_offset, i_usr_name)
        self.gf_SetUserPassward(i_offset, i_usr_passward)
        self.gf_SetUserType(i_offset, i_usr_type)
        maccnt = len(i_macs)
        for i in range(0, maccnt, 1):
            self.gf_SetUserMac(i_offset, i_macs[i] )
    
    # ------------------------------------------------------------------------
    def pf_SetDfltUser(self):
        self.pf_SetUserAllInfo(0,
                               gv_DfltUserId,
                               gv_DfltUserName,
                               gv_DfltUserPassword,
                               gv_DfltUserType,
                               gv_DfltUserDeviceMacs)

    # ------------------------------------------------------------------------
    def gf_LoadConfig(self):
        self.pf_ClearAllUsrAllInfo()
        try:
            importlib.reload(cfg)
        except Exception:
            pass
        save_req = False
        try:
            self.s_host = cfg.gv_Host
            self.s_user_port = cfg.gv_UserPort
            self.s_user_timeout = cfg.gv_UserTimeout
            self.s_device_port = cfg.gv_DevicePort
            self.s_device_timeout = cfg.gv_DeviceTimeout
        except Exception:
            self.s_host = gv_DfltHost
            self.s_user_port = gv_DlftUserPort
            self.s_user_timeout = gv_DfltUserTimout
            self.s_device_port = gv_DfltDevicePort
            self.s_device_timeout = gv_DlftDeviceTimout
            save_req = True
        try:
            u = cfg.gv_UserIds
            n = cfg.gv_UserNames
            p = cfg.gv_UserPasswords
            t = cfg.gv_UserTypes
            d = cfg.gv_UserDeviceMacs
            if len(u) == len(n) == len(p) == len(t):
                for i in range( 0, len(u) ):
                    self.pf_SetUserAllInfo(i, u[i], n[i], p[i], u[i], d[i])
                if self.s_user_dev_max == self.pf_IsUserIdPresent( gv_DfltUserId ):
                    self.pf_SetDfltUser()
                    save_req = True
            else:
                self.pf_SetDfltUser()
                save_req = True
        except Exception:
            self.pf_SetDfltUser()
            save_req = True
        if True == save_req:
            self.gf_SaveCfg()
    
    # ------------------------------------------------------------------------
    def pf_SaveFileCfg(self, fh):
        s = "gv_Host = '" + self.s_host + str("'\n")
        fh.write( s )

        s = 'gv_UserPort = ' + str(self.s_user_port) + str('\n')
        fh.write( s )

        s = 'gv_UserTimeout = ' + str(self.s_user_timeout) + str('\n')
        fh.write( s )

        s = 'gv_DevicePort = ' + str(self.s_device_port) + str('\n')
        fh.write( s )

        s = 'gv_DeviceTimeout = ' + str(self.s_device_timeout) + str('\n')
        fh.write( s )

        s = 'gv_UserIds = ' + str(self.s_user_ids) + str('\n')
        fh.write( s )

        s = 'gv_UserNames = ' + str(self.s_user_names) + str('\n')
        fh.write( s )

        s = 'gv_UserPasswords = ' + str(self.s_user_passwords) + str('\n')
        fh.write( s )

        s = 'gv_UserTypes = ' + str(self.s_user_types) + str('\n')
        fh.write( s )

        s = 'gv_UserDeviceMacs = ' + str(self.s_user_dev_macs) + str('\n')
        fh.write( s )

    # ------------------------------------------------------------------------
    def gf_SaveCfg(self):
        fh = open("SrvEcoAppAna_CfgFile.py","w+")
        self.pf_SaveFileCfg( fh )
        fh.close()
        
    # ------------------------------------------------------------------------
    def gf_GetMacIdToUserIdList(self, i_mac_id):
        m = []
        for i in range(0, self.s_user_max_cnt, 1):
            j = self.s_user_dev_max[i]
            for k in range(0, j, 1):
                if i_mac_id == self.s_user_dev_macs[i][k]:
                    m.append(i+1)
                    break
        return m

    # ------------------------------------------------------------------------
    def gf_GetUserIdToMacList(self, i_usr_id):
        m = []
        if True == UtilAna.gf_ChkRange1ToMax(i_usr_id, self.s_user_max_cnt):
            m = self.s_user_dev_macs[i_usr_id-1]
        return m

# ============================================================================
# end of file

