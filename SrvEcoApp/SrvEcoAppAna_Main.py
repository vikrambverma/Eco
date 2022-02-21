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
import SrvEcoAppAna_Logic
import signal

gv_RestartApp = False
gv_ExitApp = False
# ============================================================================
def RestartReq():
    global gv_RestartApp
    gv_RestartApp = True

def ExitMyApp(signnum, frame):
    global gv_ExitApp
    gv_ExitApp = True

# ============================================================================
def AppAna_Main(i_app_name):
    global gv_ExitApp
    global gv_RestartApp
    
    UtilAna.gf_AppStartMsg(i_app_name)
    
    s_srvapp_hndl = SrvEcoAppAna_Logic.ServerHndlAna(RestartReq, True, True)
    s_srvapp_hndl.gf_Start()
    signal.signal(signal.SIGINT, ExitMyApp)

    while False == gv_ExitApp:
        UtilAna.gf_Sleep(1)
        if True == gv_RestartApp:
            gv_RestartApp = False
            UtilAna.gf_Sleep(5)
            s_srvapp_hndl.gf_Stop()
            UtilAna.gf_Sleep(5)
            s_srvapp_hndl.gf_Start()

    s_srvapp_hndl.gf_Stop()
     
    UtilAna.gf_AppStopMsg(i_app_name)


# ============================================================================
def main() -> None:

    # 0 = never terminate, other then terminate after x count
    exit_cnt = 1
    while exit_cnt < 2:
        AppAna_Main("ECO_SERVER_V1.0")
        if 0 != exit_cnt:
            exit_cnt = exit_cnt + 1

# ============================================================================
if __name__ == '__main__':
    main()

# ============================================================================
# end of file

