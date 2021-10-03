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
import ConvtFileXToYAna

XFileName = [ 
    "./i/DevEcoAppAna_CfgClass.py",
    "./i/DevEcoAppAna_CfgFile.py",
    "./i/DevEcoAppAna_Logic.py",
    "./i/DevEcoAppAna_Main.py",
    "./i/TcpClientAna_ChildSocHndl.py",
    "./i/TcpClientAna_ParentSocHndl.py",
    "./i/UtilAna.py"
            ]

YFileName = [ 
    "./o/DevEcoAppAna_CfgClass.py",
    "./o/DevEcoAppAna_CfgFile.py",
    "./o/DevEcoAppAna_Logic.py",
    "./o/DevEcoAppAna_Main.py",
    "./o/TcpClientAna_ChildSocHndl.py",
    "./o/TcpClientAna_ParentSocHndl.py",
    "./o/UtilAna.py"
            ]

ConvtFileXToYAna.gf_ConverXToYFileApp(XFileName, YFileName)
ConvtFileXToYAna.gf_ConverXToYFileApp(YFileName, XFileName)

# ============================================================================
# end of file

