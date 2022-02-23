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
from datetime import datetime
import time
import threading
import socket
import os

# ============================================================================
def gf_UsrEcoAppFileNameStr(i_mm, i_ft="", i_path="."):
    dt = datetime.now()
    s = dt.strftime(i_path + "/%d_%m_%Y")
    try:
        os.mkdir( s )
    except Exception:
        None
    s = s + "/" + i_ft + dt.strftime("%d_%m_%Y_%H_") + str(i_mm) + ".txt"
    return s

# ============================================================================
def gf_GetDataTimeStemp():
    dt = datetime.now()
    return round( dt.timestamp(), 2)

# ============================================================================
def gf_GetDataTimeStr():
    dt = datetime.now()
    s = dt.strftime("%d-%m-%Y %H:%M:%S.%f : ")
    return s

# ============================================================================
def gf_GetDataStr( i_type = '-' ):
    s = ""
    dt = datetime.now()
    if '_' == i_type:
        s = dt.strftime("%d_%m_%Y")
    elif '\\' == i_type:
        s = dt.strftime("%d\%m\%Y")
    elif '/' == i_type:
        s = dt.strftime("%d/%m/%Y")
    else:
        s = dt.strftime("%d-%m-%Y")
    return s

# ============================================================================
def gf_GetNowMinutes():
    dt = datetime.now()
    return dt.minute

# ============================================================================
def gf_GetTimeStr( i_type = ':' ):
    s = ""
    dt = datetime.now()
    if '_' == i_type:
        s = dt.strftime("%H_%M_%S")
    if '-' == i_type:
        s = dt.strftime("%H-%M-%S")
    else:
        s = dt.strftime("%H:%M:%S")
    return s

# ============================================================================
def gf_DebugLog(i_msg):
    s = gf_GetDataTimeStr() + i_msg
    try:
        print( s )
    except Exception:
        pass

        
# ============================================================================
def gf_Sleep(i_seconds):
#    gf_DebugLog('sleep start')
    time.sleep(i_seconds)
#    gf_DebugLog('sleep end')

# ============================================================================
def gf_AppStartMsg(i_app_name):
    s = '..... ' + i_app_name + ' [ START ] .....'
    gf_DebugLog(s)

# ============================================================================
def gf_AppStopMsg(i_app_name):
    s = '..... ' + i_app_name + ' [ STOP ] .....'
    gf_DebugLog(s)


# ============================================================================
def gf_SocHostMsg(i_msg, i_host, i_port, i_max, i_timeout):
    s = i_msg + ": (" + i_host + ", " + str(i_port) + "), " + str(i_max) + ", " + str(i_timeout)
    gf_DebugLog(s)

# ============================================================================
def gf_BinaryLiToInt(i_data_value , i_data_len):
    j = 0
    k = i_data_len - 1
    for i in range(0, i_data_len, 1):
        j = j * 256
        j = j + i_data_value[(k - i)]
    return j


# ============================================================================
def gf_BinaryBiToInt(i_data_value , i_data_len):
    j = 0
    for i in range(0, i_data_len, 1):
        j = (j*256) + i_data_value[i]
    return j


# ============================================================================
def gf_FillUintToBinaryLi(i_data_value , i_data_len):
    m = [0]*i_data_len
    i = 0

    while i < i_data_len:
        m[i] = i_data_value % 256
        i_data_value = i_data_value // 256
        i = i + 1
    return m


# ============================================================================
def pf_ExitKeyMonitorThreadFun():
    gf_DebugLog( "Exit key monitor thread [ START ]" )
    while True:
        v = input("")
        # s = f"input = {v}"
        # gfDebug( s )
        if "0" == v:
            break
    gf_DebugLog( "Exit key monitor thread [ STOP ]" )


# ============================================================================
def gf_StartExitKeyMonitorig():
    th = gf_StartThreadAna(pf_ExitKeyMonitorThreadFun)
    return th


# ============================================================================
def gf_StartThreadAna( i_thread_fun):
    try:
        th = threading.Thread(target=i_thread_fun)
        th.start()
        return th
    except Exception:
        return None

# ============================================================================
def gf_ChkRange1ToMax(i_dvalue, i_dvmax):
    if i_dvalue > 0:
        if (i_dvalue-1) < i_dvmax:
            return True
    return False


# ============================================================================
def gf_GetStrToBytes(i_dstr):
    m = bytearray(i_dstr, 'utf-8')
    return m


# ============================================================================
def gf_GetBytesToStr(i_bytes):
    m = i_bytes.decode()
    return m


# ============================================================================
# TCP/IP Socket Functions
# ============================================================================
def gf_CloseSocketAna(i_sock):
    if None != i_sock:
        try:
            i_sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            try:
                i_sock.close()
                return True
            except Exception:
                return False
        try:
            i_sock.close()
            return True
        except Exception:
            return False
    return True


# ============================================================================
def gf_ConnectSocketAna(i_host, i_port):
    try:
        sc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sc.connect((i_host, i_port))
        return sc
    except Exception:
        return None


# ============================================================================
def gf_AcceptSocketAna(i_srv_sock):
    try:
        (sc, adr) = i_srv_sock.accept()
        return sc
    except Exception:
        return None


# ============================================================================
def gf_SetListenSocketAna(i_host, i_port, i_listen_sock_count):
    try:
        srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srvsock.bind((i_host, i_port))
        srvsock.listen(i_listen_sock_count)
        return srvsock
    except Exception:
        gf_CloseSocketAna(srvsock)
        return None


# ============================================================================
def gf_TxdSocketAna(i_sock, i_out_msg):
    if None != i_sock:
        m = bytes(i_out_msg)
        try:
            i_sock.send( m )
            return True
        except Exception:
            return False
    return False


# ============================================================================
def gf_RxdSocketAna(i_sock):
    if None != i_sock:
        try:
            d = i_sock.recv(4096)
            if len(d) > 0:
                return d
        except Exception:
            pass
    return None


# ============================================================================
# File Functions
# ============================================================================
def gf_FileAna_Open( i_file_name, i_mode ):
    try:
        f = open( i_file_name, i_mode )
        return f
    except Exception:
        gf_DebugLog( "File open fails : " + i_file_name )
        return None

# ============================================================================
def gf_FileAna_Close( i_file_hndl ):
    try:
        i_file_hndl.close()
    except Exception:
        gf_DebugLog( "File close fails." )
        None

# ============================================================================
def gf_FileAna_FileLength( i_file_name ):
    flen = 0
    try:
        flen = os.path.getsize( i_file_name )
    except Exception:
        flen = 0
    return flen

# ============================================================================
def gf_FileAna_Write( i_file_hndl, i_wr_offset, i_wr_data ):
    retStatus = False
    try:
        if None != i_wr_offset:
            i_file_hndl.seek( i_wr_offset )
        i_file_hndl.write( i_wr_data )
        retStatus = True
    except Exception:
        retStatus = False
    return retStatus

# ============================================================================
def gf_FileAna_Read( i_file_hndl, i_rd_offset, i_rd_cnt ):
    retSts = False
    rdcnt = 0
    rddata = []
    try:
        i_file_hndl.seek( i_rd_offset )
        rddata = i_file_hndl.read( i_rd_cnt )
        rdcnt = len( rddata )
        retSts = True
    except Exception:
        rdcnt = 0
        rddata = None
        retSts = False
    return ( retSts, rdcnt, rddata )

# ============================================================================
def gf_Get_HexStrToInt( i_str, i_bytes = None ):
    v = 0
    c = 0

    m = bytearray(i_str, 'utf-8')
    ln = len(m)

    if None != i_bytes:
        if i_bytes != ln:
            return v

    for i in range(0, ln, 1):
        c = m[i]
        v = v * 16
        if (c > 47) and (c < 58):
            v = v + c - 48
        elif (c > 64) and (c < 71):
            v = v + c + 10 - 65
        elif (c > 96) and (c < 103):
            v = v + c + 10 - 97
        else:
            v = 0
            break
    return v

# ============================================================================
def gf_Get_IntToHexStr( i_val, i_bytes = None ):
    m = ['0', '1', '2', '3','4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    s = ""
    t = 1
    if None == i_bytes:
        i_bytes = 1
   
    for i in range(0, i_bytes, 1):
        t = t * 16
        
    i_val = i_val % t
    for i in range(0, i_bytes, 1):
        k = t / 16
        v = int(i_val / k)
        i_val = i_val % k
        t = k
        s = s + m[v]
    return s

# ---------------------------------------------------------------------------
def pf_Get_StrToInt( i_str ):
    rsts = True
    v = 0
    m = bytearray(i_str, 'utf-8')
    
    for i in range(0, len(m), 1):
        t = m[i]
        if t < 58:
            if t > 47:
                t = t - 48
                v = v * 10 + t
            else:
                rsts = False
        else:
            rsts = False
    
    if False == rsts:
        v = 0
    return v

# ============================================================================
# end of file
