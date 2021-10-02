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

XFileName = [ "./in/T1.txt", "./in/T2.txt" ]
YFileName = [ "./out/T1.txt", "./out/T2.txt" ]

ConvtFileXToYAna.gf_ConverXToYFileApp(XFileName, YFileName)
ConvtFileXToYAna.gf_ConverXToYFileApp(YFileName, XFileName)

# ============================================================================
# end of file

