# ============================================================================
"""

Owner Name    : Vikramsingh
Company Name  : ANA Software Limited
Owner Address : SP-106, Silver Palace Apartment, Shobhagpura, Udaipur,
              : Rajasthan, India, Pin Code - 313001
Created Date  : 02-Oct-2021
Licence       : MIT

"""

# ----------------------------------------------------------------------------
import UtilAna

# ============================================================================
def pf_GetXToY( i_val ):
    tmp = 0
    k = 0

    k = i_val & 0x80
    if ( 0 != k ):
        tmp |= 0x01

    k = i_val & 0x40
    if ( 0 != k ):
        tmp |= 0x02

    k = i_val & 0x20
    if ( 0 != k ):
        tmp |= 0x04

    k = i_val & 0x10
    if ( 0 != k ):
        tmp |= 0x08

    k = i_val & 0x08
    if ( 0 != k ):
        tmp |= 0x10

    k = i_val & 0x04
    if ( 0 != k ):
        tmp |= 0x20

    k = i_val & 0x02
    if ( 0 != k ):
        tmp |= 0x40

    k = i_val & 0x01
    if ( 0 != k ):
        tmp |= 0x80

    return tmp
    

# ============================================================================
def pf_ConvFileXToY( i_in_fname, i_out_fname ):
    sts = False
    cnt = 0
    fdata = None
    tmp = bytearray(256)
    offset = 0
    t = 0
    j = 0

    infh = UtilAna.gf_FileAna_Open( i_in_fname )
    outfh = UtilAna.gf_FileAna_Open( i_out_fname )
    if (None != infh):
        if (None != outfh):
            offset = 0
            while True:
                sts, cnt, fdata = UtilAna.gf_FileAna_Read( infh, offset, 256 )
                if ( False != sts ):
                    if ( 0 != cnt ):
                        for j in range(0, cnt, 1):
                            t = pf_GetXToY( fdata[j] )
                            tmp[j:j+1] = UtilAna.gf_FillUintToBinaryLi(t,1)
                        sts = UtilAna.gf_FileAna_Write( outfh, offset, tmp[0:cnt] )
                        if ( True == sts ):
                            offset += cnt
                        else:
                            # out file write fails, conversion failed
                            break
                    else:
                        # end of file, break while, conversion success
                        break
                else:
                    # file read fails, break while, conversion failed
                    break
            # while over
        else:
            # do nothing, file open fails, conversion failed
            pass
    else:
        # donthing, file open fails, conversion failed
        pass
    
    msg = ""
    if ( True == sts ):
        msg += "[ SUCCESS ] :"
    else:
        msg += "[  FAILS  ] :"
    msg += i_in_fname + " ---> " + i_out_fname
    UtilAna.gf_DebugLog( msg )

    UtilAna.gf_FileAna_Close( infh )
    UtilAna.gf_FileAna_Close( outfh )

# ============================================================================
def gf_ConverXToYFileApp( i_infile_name, i_outfile_name ):
    cnt1 = len( i_infile_name )
    cnt2 = len( i_outfile_name )
    if ( 0 != cnt1 ) and ( cnt1 == cnt2 ):
        for i in range(0, cnt1, 1):
            pf_ConvFileXToY( i_infile_name[i], i_outfile_name[i] )
    else:
        UtilAna.gf_DebugLog( " File conversion FAILED, inputs are not good. " )

# ============================================================================
# end of file

