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
def gf_GetDataTimeStr():
    dt = datetime.now()
    s = dt.strftime("%d-%m-%Y %H:%M:%S.%f : ")
    return s


# ============================================================================
def gf_DebugLog(i_msg):
    s = gf_GetDataTimeStr() + i_msg
    print( s )

        
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
def gf_FileAna_Open( i_file_name ):
    try:
        f = open( i_file_name, 'r+b')
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
# end of file

