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
    "./i/UsrEcoAppAna_CfgClass.py",
    "./i/UsrEcoAppAna_CfgFile.py",
    "./i/UsrEcoAppAna_Logic.py",
    "./i/UsrEcoAppAna_Main.py",
    "./i/TcpClientAna_ChildSocHndl.py",
    "./i/TcpClientAna_ParentSocHndl.py",
    "./i/UtilAna.py",
    "./i/UserOneCfgAna.py"
            ]

YFileName = [ 
    "./o/UsrEcoAppAna_CfgClass.py",
    "./o/UsrEcoAppAna_CfgFile.py",
    "./o/UsrEcoAppAna_Logic.py",
    "./o/UsrEcoAppAna_Main.py",
    "./o/TcpClientAna_ChildSocHndl.py",
    "./o/TcpClientAna_ParentSocHndl.py",
    "./o/UtilAna.py",
    "./o/UserOneCfgAna.py"
            ]

#ConvtFileXToYAna.gf_ConverXToYFileApp(XFileName, YFileName)
ConvtFileXToYAna.gf_ConverXToYFileApp(YFileName, XFileName)

# ============================================================================
# end of file

