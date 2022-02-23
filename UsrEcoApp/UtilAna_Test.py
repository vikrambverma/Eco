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

macstr = "FFFFFFFFFFFF"
v = 0

v = UtilAna.gf_Get_HexStrToInt(macstr,12)
if 281474976710655 != v:
    print("[FAIL] : " + "HEXStr = " + macstr + " --> Int = " + str(v) )
else:
    print("[PASS] : " + "HEXStr = " + macstr + " --> Int = " + str(v) )

macstr = UtilAna.gf_Get_IntToHexStr(v,12)
if "FFFFFFFFFFFF" != macstr:
    print("[FAIL] : " + "Int = " + str(v) + " --> HexStr = " + macstr )
else:
    print("[PASS] : " + "Int = " + str(v) + " --> HexStr = " + macstr )
    
macstr = "000000000001"
v = 0
v = UtilAna.gf_Get_HexStrToInt(macstr,12)
if 1 != v:
    print("[FAIL] : " + "HEXStr = " + macstr + " --> Int = " + str(v) )
else:
    print("[PASS] : " + "HEXStr = " + macstr + " --> Int = " + str(v) )

macstr = UtilAna.gf_Get_IntToHexStr(v,12)
if "000000000001" != macstr:
    print("[FAIL] : " + "Int = " + str(v) + " --> HexStr = " + macstr )
else:
    print("[PASS] : " + "Int = " + str(v) + " --> HexStr = " + macstr )

macstr = "FEDCBA987654"
v = 0
v = UtilAna.gf_Get_HexStrToInt(macstr,12)
if 280223976814164 != v:
    print("[FAIL] : " + "HEXStr = " + macstr + " --> Int = " + str(v) )
else:
    print("[PASS] : " + "HEXStr = " + macstr + " --> Int = " + str(v) )

macstr = UtilAna.gf_Get_IntToHexStr(v,12)
if "FEDCBA987654" != macstr:
    print("[FAIL] : " + "Int = " + str(v) + " --> HexStr = " + macstr )
else:
    print("[PASS] : " + "Int = " + str(v) + " --> HexStr = " + macstr )

# ============================================================================
# end of file

