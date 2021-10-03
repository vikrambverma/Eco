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
    "./i/SrvEcoAppAna_CfgClass.py",
    "./i/SrvEcoAppAna_CfgFile.py",
    "./i/SrvEcoAppAna_Logic.py",
    "./i/DevEcoAppAna_Main.py",
    "./i/TcpServerAna_ChildSocHndl.py",
    "./i/TcpServerAna_ParentSocHndl.py",
    "./i/UtilAna.py"
            ]

YFileName = [ 
    "./o/SrvEcoAppAna_CfgClass.py",
    "./o/SrvEcoAppAna_CfgFile.py",
    "./o/SrvEcoAppAna_Logic.py",
    "./o/DevEcoAppAna_Main.py",
    "./o/TcpServerAna_ChildSocHndl.py",
    "./o/TcpServerAna_ParentSocHndl.py",
    "./o/UtilAna.py"
            ]

ConvtFileXToYAna.gf_ConverXToYFileApp(XFileName, YFileName)
ConvtFileXToYAna.gf_ConverXToYFileApp(YFileName, XFileName)

# ============================================================================
# end of file

