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
import UsrEcoAppAna_Logic
import UsrEcoAppAna_GUILogic
import UserEcoAppAna_NewCfgFile

# import signal

# gv_RestartApp = False
# gv_ExitApp = False
# ============================================================================
# def RestartReq():
#     global gv_RestartApp
#     gv_RestartApp = True

# def ExitMyApp(signnum, frame):
#     global gv_ExitApp
#     gv_ExitApp = True

# ============================================================================
def AppAna_Main(i_app_name):
    # global gv_ExitApp
    # global gv_RestartApp
    
    UtilAna.gf_AppStartMsg(i_app_name)
    
    s_cfg = UserEcoAppAna_NewCfgFile.CfgUserAppAna()
    
    s_usr_hndl = UsrEcoAppAna_Logic.UsrAppAna(s_cfg, 4096, True)
    s_usr_hndl.gf_Start()
    
    s_gui = UsrEcoAppAna_GUILogic.UsrEcoAppGui(s_usr_hndl.gf_GetLiveGuiNSecData, s_cfg)
    s_gui.gf_GuiStart()

    # signal.signal(signal.SIGINT, ExitMyApp)
    # while False == gv_ExitApp:
    UtilAna.gf_Sleep(1)

    s_usr_hndl.gf_Stop()

    UtilAna.gf_AppStopMsg(i_app_name)


# ============================================================================
def main() -> None:

    # 0 = never terminate, other then terminate after x count
    exit_cnt = 1
    while exit_cnt < 2:
        AppAna_Main("USER_ECO_APP_GUI (V1.0)")
        if 0 != exit_cnt:
            exit_cnt = exit_cnt + 1

# ============================================================================
if __name__ == '__main__':
    main()

# ============================================================================
# end of file

