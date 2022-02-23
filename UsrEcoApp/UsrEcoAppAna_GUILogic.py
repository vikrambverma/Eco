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
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import UtilAna

gv_MyColor = ['red', 'green', 'blue', 'orange', 'black']
# ---------------------------------------------------------------------------
def pf_GuiLibAdd_Label_TxtVar(i_owner, i_a, i_xs, i_ys, i_xw, i_yh):
    txt_var_obj = tk.StringVar(i_owner)
    txt_var_obj.set("")
    lbl_obj = tk.Label(master=i_owner, anchor=i_a, textvariable=txt_var_obj)
    lbl_obj.place(relx=i_xs, rely=i_ys, relwidth=i_xw, relheight=i_yh)
    return txt_var_obj, lbl_obj

# ---------------------------------------------------------------------------
def pf_GuiLibAdd_Label_FixTxt(i_owner, i_a, i_xs, i_ys, i_xw, i_yh, i_txt):
    lbl_obj = tk.Label(master=i_owner, anchor=i_a, text=i_txt)
    lbl_obj.place(relx=i_xs, rely=i_ys, relwidth=i_xw, relheight=i_yh)
    return lbl_obj
    
# ---------------------------------------------------------------------------
def pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw, i_yh):
    txt_var_obj = tk.StringVar(i_owner)
    txt_var_obj.set("")
    entry_obj = tk.Entry(master=i_owner, textvariable=txt_var_obj)
    entry_obj.place(relx=i_xs, rely=i_ys, relwidth=i_xw, relheight=i_yh)
    return txt_var_obj, entry_obj

# ---------------------------------------------------------------------------
def pf_GuiLibAdd_LabelEntry_TxtVarOne(i_owner, i_xs, i_ys, i_xw1, i_yh, i_xw2, i_txt):
    lObj = pf_GuiLibAdd_Label_FixTxt(i_owner, 'e', i_xs, i_ys, i_xw1, i_yh, i_txt)
    i_xs = i_xs + i_xw1
    v1Obj, e1Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw2, i_yh)
    return v1Obj, e1Obj, lObj

def pf_GuiLibAdd_LabelEntry_TxtVarTwo(i_owner, i_xs, i_ys, i_xw1, i_yh, i_xw2, i_xw3, i_txt):
    lObj = pf_GuiLibAdd_Label_FixTxt(i_owner, 'e', i_xs, i_ys, i_xw1, i_yh, i_txt)
    i_xs = i_xs + i_xw1
    v1Obj, e1Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw2, i_yh)
    i_xs = i_xs + i_xw2
    v2Obj, e2Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw3, i_yh)
    return v1Obj, v2Obj, e1Obj, e2Obj, lObj

def pf_GuiLibAdd_LabelEntry_TxtVarThree(i_owner, i_xs, i_ys, i_xw1, i_yh, i_xw2, i_xw3, i_xw4, i_txt):
    lObj = pf_GuiLibAdd_Label_FixTxt(i_owner, 'e', i_xs, i_ys, i_xw1, i_yh, i_txt)
    i_xs = i_xs + i_xw1
    v1Obj, e1Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw2, i_yh)
    i_xs = i_xs + i_xw2
    v2Obj, e2Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw3, i_yh)
    i_xs = i_xs + i_xw3
    v3Obj, e3Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw4, i_yh)
    return v1Obj, v2Obj, v3Obj, e1Obj, e2Obj, e3Obj, lObj

def pf_GuiLibAdd_LabelEntry_TxtVarSix(i_owner, i_xs, i_ys, i_xw1, i_yh, i_xw2, i_xw3, i_xw4, i_xw5, i_xw6, i_xw7, i_txt):
    lObj = pf_GuiLibAdd_Label_FixTxt(i_owner, 'e', i_xs, i_ys, i_xw1, i_yh, i_txt)
    i_xs = i_xs + i_xw1
    v1Obj, e1Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw2, i_yh)
    i_xs = i_xs + i_xw2
    v2Obj, e2Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw3, i_yh)
    i_xs = i_xs + i_xw3
    v3Obj, e3Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw4, i_yh)
    i_xs = i_xs + i_xw4
    v4Obj, e4Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw5, i_yh)
    i_xs = i_xs + i_xw5
    v5Obj, e5Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw6, i_yh)
    i_xs = i_xs + i_xw6
    v6Obj, e6Obj = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs, i_ys, i_xw7, i_yh)
    return v1Obj, v2Obj, v3Obj, v4Obj, v5Obj, v6Obj, e1Obj, e2Obj, e3Obj, e4Obj, e5Obj, e6Obj, lObj

# ---------------------------------------------------------------------------
def pf_AddLoginEntry(i_owner, i_xs, i_ys, i_xw, i_yh, i_txt):
    pf_GuiLibAdd_Label_FixTxt(i_owner, 'e', i_xs, i_ys, i_xw, i_yh, i_txt+"  LoginId :")
    vloginId, eloginId = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs+i_xw, i_ys, i_xw, i_yh)
    i_ys = i_ys + i_yh + 0.01 
    pf_GuiLibAdd_Label_FixTxt(i_owner, 'e', i_xs, i_ys, i_xw, i_yh, i_txt+" Password :")
    vloginPwd, eloginPwd = pf_GuiLibAdd_Entry_TxtVar(i_owner, i_xs+i_xw, i_ys, i_xw, i_yh)
    return vloginId, eloginId, vloginPwd, eloginPwd

# ---------------------------------------------------------------------------
def pf_GuiLibAdd_Frame(i_owner, i_xs, i_ys, i_xw, i_yh, i_bgcolor):
    frame = None
    if None != i_bgcolor:
        frame = tk.Frame(i_owner, background=i_bgcolor)
    else:
        frame = tk.Frame(i_owner)
    frame.place(relx=i_xs, rely=i_ys, relwidth=i_xw, relheight=i_yh)
    return frame

# ---------------------------------------------------------------------------
def pf_GuiLibAdd_FigCanvsAxs(i_owner, i_xs, i_ys, i_xw, i_yh, i_bgcolor):
    fig = plt.Figure()
    # fig.patch.set_facecolor(i_bgcolor)
    axs = None
    canv = FigureCanvasTkAgg(fig, master=i_owner)
    # canv.get_tk_widget().configure(background=i_bgcolor)
    canv.get_tk_widget().place(relx=i_xs, rely=i_ys, relwidth=i_xw, relheight=i_yh)
    # canv._tkcanvas.config(bg=i_bgcolor)
    return fig, axs, canv

# ---------------------------------------------------------------------------
def pf_GetInegerEntryy( i_str ):
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

# ---------------------------------------------------------------------------
# Page_None : History Data View
class Page_None(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller
        
        self.s_vTitle, self.s_lTitle = pf_GuiLibAdd_Label_TxtVar(self, 'c', 0, 0, 1, 0.03)

    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        pass

    def pf_AfterStart(self):
        c = self.s_controller.s_Cfg
        self.s_vTitle.set('[ Idle ]   ' + c.s_Customer_Name + "   :   " + c.s_Customer_Site)

# ---------------------------------------------------------------------------
# Page_LDV : Live Data View
class Page_LDV(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller
        
        self.s_LiveDys = []
        self.s_LiveDx = []
        self.s_LiveEvents = []
        self.s_LiveLERates = []
        self.s_LiveDevMacs = []
        self.s_LiveDevNames = []

        self.s_LiveDSec = 0
        self.s_LiveDTSmplCount = 0
        self.s_LiveDeviceCount = 0
        self.s_LiveDSmplRate = 0
        
        self.s_Chnl_LVD_frame, self.s_Chnl_LVD_fig, self.s_Chnl_LVD_axs, self.s_Chnl_LVD_canv = self.pf_AddFigAxsCanv(0.00, 0.00, 0.87, 1.00, 'blue',  'white')
        self.s_Chnl_EVENTS_frame, self.s_Chnl_EVENTS_fig, self.s_Chnl_EVENTS_axs, self.s_Chnl_EVENTS_canv = self.pf_AddFigAxsCanv(0.87, 0.00, 0.06, 1.00, 'green', 'white')
        self.s_Chnl_LERATE_frame, self.s_Chnl_LERATE_fig, self.s_Chnl_LERATE_axs, self.s_Chnl_LERATE_canv = self.pf_AddFigAxsCanv(0.93, 0.00, 0.07, 1.00, 'black', 'white')
        
        self.s_execute_cnt = 0

    def pf_BeforeStop(self):
        self.s_controller.pf_StopCbk()
        
        while len(self.s_LiveDx) > 0:
            self.s_LiveDx.pop(0)
        while len(self.s_LiveEvents) > 0:
            self.s_LiveEvents.pop(0)
        while len(self.s_LiveLERates) > 0:
            self.s_LiveLERates.pop(0)
        while len(self.s_LiveDys) > 0:
            self.s_LiveDys.pop(0)
        while len(self.s_LiveDevMacs) > 0:
            self.s_LiveDevMacs.pop(0)
        while len(self.s_LiveDevNames) > 0:
            self.s_LiveDevNames.pop(0)

        self.s_LiveDeviceCount = 0
        self.s_LiveDSec = 0
        self.s_LiveDTSmplCount = 0

    def pf_BeforeStart(self):
        c = self.s_controller.s_Cfg
        self.s_LiveDeviceCount = 0
        for i in range(0, c.s_User_DeviceMaxAllowed, 1):
            if 1 == c.s_Device_LDVEnableds[i]:
                self.s_LiveDevMacs.append( c.s_Device_MacIds[i] )
                self.s_LiveDevNames.append( c.s_Device_Names[i] )
                self.s_LiveDeviceCount = self.s_LiveDeviceCount + 1
        if self.s_LiveDeviceCount < 1:
            self.s_LiveDevMacs.append( 0 )
            self.s_LiveDevNames.append( "Not Selected - 1" )
            self.s_LiveDeviceCount = self.s_LiveDeviceCount + 1
        if self.s_LiveDeviceCount < 2:
            self.s_LiveDevMacs.append( 0 )
            self.s_LiveDevNames.append( "Not Selected - 2" )
            self.s_LiveDeviceCount = self.s_LiveDeviceCount + 1

        self.s_LiveDSec = c.s_Device_LiveDataSec
        self.s_LiveDSmplRate = c.s_Device_SamplePerSec
        self.s_LiveDTSmplCount = self.s_LiveDSec * c.s_Device_SamplePerSec

        # self.pf_dbg()
        tstep = round(self.s_LiveDSec/self.s_LiveDTSmplCount, 5)
        for i in range(self.s_LiveDTSmplCount, 0, -1):
            tts = -round(tstep * i, 2)
            self.s_LiveDx.append(tts)
        for i in range(0, self.s_LiveDeviceCount, 1):
            self.s_LiveEvents.append(0)
            self.s_LiveLERates.append(0)
            self.s_LiveDys.append([0.0 for j in range(self.s_LiveDTSmplCount)])
        s = '[ Live Data ]   ' + c.s_Customer_Name + "   :   " + c.s_Customer_Site
        self.s_Chnl_LVD_axs = self.pf_InitFigAxs(self.s_Chnl_LVD_fig, 0.100, 0.09, 0.999, 0.95, s, self.s_LiveDx, self.s_LiveDys, self.s_LiveDevNames)
        self.s_Chnl_EVENTS_axs = self.pf_InitFigAxs(self.s_Chnl_EVENTS_fig, 0.010, 0.09, 0.99, 0.95, "Events", None, None, self.s_LiveEvents)
        self.s_Chnl_LERATE_axs = self.pf_InitFigAxs(self.s_Chnl_LERATE_fig, 0.010, 0.09, 0.80, 0.95, "Rate", None, None, self.s_LiveLERates)

    def pf_AfterStart(self):
        self.s_execute_cnt = 0
        self.s_controller.pf_StartCbk(900, self.pf_ShowLvd)
    
    def pf_AddFigAxsCanv(self, i_xs, i_ys, i_xw, i_yh, i_c1, i_c2):
        # frm = pf_GuiLibAdd_Frame(self, i_xs, i_ys, i_xw, i_yh, i_c1)
        fig, axs, canv = pf_GuiLibAdd_FigCanvsAxs(self, i_xs, i_ys, i_xw, i_yh, i_c2)
        return None, fig, axs, canv

    def pf_InitFigAxs(self, i_fig, i_xs, i_ys, i_xw, i_yh, i_str, i_gxv, i_gyv, i_gyl):
        i_fig.clf()
        i_fig.subplots_adjust(left=i_xs, bottom=i_ys, right=i_xw, top=i_yh, wspace=0.00, hspace=0.00)
        gs = i_fig.add_gridspec(self.s_LiveDeviceCount, hspace=0)
        axs = gs.subplots(sharex=True, sharey=True)
        i_fig.suptitle( i_str )
        i_fig.set_animated(True)
        for k in range(0, self.s_LiveDeviceCount, 1):
            if None != i_gxv:
                axs[k].label_outer()
            axs[k].spines["top"].set_visible(False)
            axs[k].spines["bottom"].set_visible(False)
        axs[0].spines["top"].set_visible(True)
        axs[k].spines["bottom"].set_visible(True)
        self.pf_update_fig(i_fig, axs, i_gxv, i_gyv, i_gyl)
        return axs

    def pf_update_fig(self, i_fig, i_axs, i_gxv, i_gyv, i_gyl):
        clrTbl = ['red', 'green', 'blue', 'orange', 'black']
        for k in range(0,self.s_LiveDeviceCount, 1):
            clr = clrTbl[k%5]
            i_axs[k].clear()
            i_axs[k].margins(x=0.00)
            if None != i_gxv:
                i_axs[k].set_ylim(-3,3)
                i_axs[k].plot(i_gxv, i_gyv[k], clr)
                i_axs[k].set_ylabel(i_gyl[k], rotation=0, labelpad=40)
                i_axs[k].set_xlabel( ("Date : " + UtilAna.gf_GetDataStr() + "             Time - " + UtilAna.gf_GetTimeStr() ), labelpad=10, loc="right")
                i_axs[k].grid()
            else:
                i_axs[k].get_xaxis().set_visible(False)
                i_axs[k].set_ylabel(i_gyl[k], rotation=0, labelpad=-60)
        i_fig.canvas.draw()
        i_fig.canvas.flush_events()
        
    def pf_ShowLvd(self):
        # UtilAna.gf_DebugLog("Draw Start")
        # c = self.s_controller.s_Cfg
        lf = self.s_controller.s_get_live_data_fun
        if None != lf:
            lf(self.s_LiveDSec, self.s_LiveDeviceCount, self.s_LiveDevMacs, self.s_LiveDys, self.s_LiveEvents, self.s_LiveLERates)
        self.pf_update_fig(self.s_Chnl_LVD_fig, self.s_Chnl_LVD_axs, self.s_LiveDx, self.s_LiveDys, self.s_LiveDevNames)
        self.pf_update_fig(self.s_Chnl_EVENTS_fig, self.s_Chnl_EVENTS_axs, None, None, self.s_LiveEvents)
        self.pf_update_fig(self.s_Chnl_LERATE_fig, self.s_Chnl_LERATE_axs, None, None, self.s_LiveLERates)
        # UtilAna.gf_DebugLog("Draw Stop")

# ---------------------------------------------------------------------------
# Page_HDV : History Data View
class Page_HDV(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller

        self.s_vTitle, self.s_lTitle = pf_GuiLibAdd_Label_TxtVar(self, 'c', 0.00, 0.00, 1.00, 0.03)
        self.s_vfh, self.s_lfh = pf_GuiLibAdd_Label_TxtVar(self, 'c', 0.00, 0.03, 1.00, 0.03)
        
        self.s_select_file_button = tk.Button(self, text="Select File", command=self.pf_SelectFilePressed)
        self.s_select_file_button.place(relx=0.40, rely=0.15, relwidth=0.09, relheight=0.04)
        self.s_view_file_data_button = tk.Button(self, text="View File Data", command=self.pf_ViewFileDataPressed)
        self.s_view_file_data_button.place(relx=0.50, rely=0.15, relwidth=0.09, relheight=0.04)
    
    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        c = self.s_controller.s_Cfg
        self.s_vTitle.set('[ History Data ]   ' + c.s_Customer_Name + "   :   " + c.s_Customer_Site)
        self.s_vfh.set("None")

    def pf_AfterStart(self):
        pass
    
    def pf_ViewFileDataPressed(self):
        self.s_vfh.set("None")

    def pf_SelectFilePressed(self):
        filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt')
            )
        filename = fd.askopenfilename(
            title='Select File',
            initialdir=self.s_controller.s_Cfg.s_Device_HDFilePath,
            filetypes=filetypes
            )
        if "" != filename or None == filename:
            self.s_vfh.set(filename)


# ---------------------------------------------------------------------------
# Page_USER_LOGIN : User Login
class Page_USER_LOGIN(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller

        self.s_vTitle, self.s_lTitle = pf_GuiLibAdd_Label_TxtVar(self, 'c', 0.00, 0.00, 1.00, 0.03)
        self.s_vLoginId, self.s_eLoginId, self.s_vLoginPwd, self.s_eLoginPwd =  pf_AddLoginEntry(self, 0.25, 0.05, 0.20, 0.03, 'User')

        self.s_submit_button = tk.Button(self, text="Submit", command=self.pf_SubmitPressed, underline=0)
        self.s_submit_button.place(relx=0.45, rely=0.15, relwidth=0.09, relheight=0.04)

    def pf_ClrLoginStr(self):
        self.s_vLoginPwd.set("")
        self.s_vLoginId.set("")
            
    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        c = self.s_controller.s_Cfg
        self.s_vTitle.set('[ User Login ]   ' + c.s_Customer_Name + "   :   " + c.s_Customer_Site)

    def pf_AfterStart(self):
        self.pf_ClrLoginStr()
        # self.s_entry_usrid.focus()

    def pf_SubmitPressed(self):
        if self.s_vLoginId.get() == self.s_controller.s_Cfg.s_User_LoginId:
            if self.s_vLoginPwd.get() == self.s_controller.s_Cfg.s_User_LoginPwd:
                if False == self.s_controller.s_UserLogInOk:
                    self.s_controller.s_UserLogInOk = True
                    self.s_controller.pf_ShowPage(Page_None)
                else:
                    self.s_controller.pf_ShowPage(Page_USER_SET)
            else:
                self.pf_ClrLoginStr()
        else:
            self.pf_ClrLoginStr()

# ---------------------------------------------------------------------------
# Page_USER_SET : Settings
class Page_USER_SET(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller

        tk.Label(self, text="User Settings").place(relx=0, rely=0, relwidth=1, relheight=0.03)
        
        rh = 0.03
        ry = 0.04
        self.s_usr_vloginid, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.20, ry, 0.20, rh, 0.30, 'User Login ID :')

        ry = ry + 0.04
        self.s_usr_vloginpwd, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.20, ry, 0.20, rh, 0.30, 'User Login Password :')

        ry = ry + 0.04
        self.s_save_button = tk.Button(self, text="Save", command=self.pf_SaveSubmit)
        self.s_save_button.place(relx=0.35, rely=ry, relwidth=0.09, relheight=rh)
        self.s_close_button = tk.Button(self, text="Close", command=lambda:self.s_controller.pf_ShowPage(Page_None) )
        self.s_close_button.place(relx=0.45, rely=ry, relwidth=0.09, relheight=rh)
        self.s_reload_button = tk.Button(self, text="ReLoad", command=self.pf_Update)
        self.s_reload_button.place(relx=0.55, rely=ry, relwidth=0.09, relheight=rh)
    
    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        pass

    def pf_AfterStart(self):
        self.pf_Update()

    def pf_Update(self):
        c = self.s_controller.s_Cfg
        c.gf_LoadCfg()
        
        self.s_usr_vloginid.set( c.s_User_LoginId )
        self.s_usr_vloginpwd.set( c.s_User_LoginPwd )
        
    def pf_SaveSubmit(self):
        c = self.s_controller.s_Cfg
        
        c.gf_SetUserLoginId( self.s_usr_vloginid.get() )
        c.gf_SetUserLoginPwd( self.s_usr_vloginpwd.get() )
            
        c.gf_SaveCfg()
        self.pf_Update()


# ---------------------------------------------------------------------------
# Page_ADMIN_LOGIN : User Login
class Page_ADMIN_LOGIN(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller

        self.s_vTitle, self.s_lTitle = pf_GuiLibAdd_Label_TxtVar(self, 'c', 0.00, 0.00, 1.00, 0.03)
      
        self.s_vLoginId, self.s_eLoginId, self.s_vLoginPwd, self.s_eLoginPwd =  pf_AddLoginEntry(self, 0.25, 0.05, 0.20, 0.03, 'Admin')

        self.s_submit_button = tk.Button(self, text="Submit", command=self.pf_SubmitPressed, underline=0)
        self.s_submit_button.place(relx=0.45, rely=0.15, relwidth=0.09, relheight=0.04)

    def pf_ClrLoginStr(self):
        self.s_vLoginPwd.set("")
        self.s_vLoginId.set("")
            
    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        c = self.s_controller.s_Cfg
        self.s_vTitle.set('[ Admin Login ]   ' + c.s_Customer_Name + "   :   " + c.s_Customer_Site)

    def pf_AfterStart(self):
        self.pf_ClrLoginStr()
        # self.s_entry_usrid.focus()

    def pf_SubmitPressed(self):
        if self.s_vLoginId.get() == self.s_controller.s_Cfg.s_Admin_LoginId:
            if self.s_vLoginPwd.get() == self.s_controller.s_Cfg.s_Admin_LoginPwd:
                self.s_controller.pf_ShowPage(Page_ADMIN_SET1)
            else:
                self.pf_ClrLoginStr()
        else:
            self.pf_ClrLoginStr()

# ---------------------------------------------------------------------------
# Page_ADMIN_SET1 : Settings
class Page_ADMIN_SET1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller
        tk.Label(self, text="Admin Settings - Page 1").place(relx=0, rely=0, relwidth=1, relheight=0.03)
        
        rh = 0.03
        ry = 0.04
        self.s_customer_name, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.05, ry, 0.20, rh, 0.60, 'Customer Name :')

        ry = ry + 0.04
        self.s_customer_site, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.05, ry, 0.20, rh, 0.60, 'Customer Site :')

        ry = ry + 0.04
        self.s_usr_name, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.05, ry, 0.20, rh, 0.60, 'User Name :')
        ry = ry + 0.04
        self.s_usr_loginid, self.s_usr_loginpwd, v3, v4, v5 = pf_GuiLibAdd_LabelEntry_TxtVarTwo(self, 0.05, ry, 0.20, rh, 0.30, 0.30, "User Login ( ID, Password ) :")

        ry = ry + 0.04
        self.s_admin_name, v2 , v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.05, ry, 0.20, rh, 0.60, 'Admin Name :')
        ry = ry + 0.04
        self.s_admin_loginid, self.s_admin_loginpwd,v3, v4, v5 = pf_GuiLibAdd_LabelEntry_TxtVarTwo(self, 0.05, ry, 0.20, rh, 0.30, 0.30, 'Admin Login ( ID, Password ) :')

        ry = ry + 0.04
        self.s_remotehost_ip, self.s_remotehost_port, self.s_remotehost_inactivesec, v4, v5, v6, v7 = pf_GuiLibAdd_LabelEntry_TxtVarThree(self, 0.05, ry, 0.20, rh, 0.20, 0.20, 0.20, 'Remote Host ( IP, Port, InactiveTime(s) ) :')

        ry = ry + 0.04
        self.s_dev_livedatasec, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.05, ry, 0.20, rh, 0.60, 'Live Data View(s) :')

        ry = ry + 0.04
        self.s_dev_hdfpath, v2, v3 = pf_GuiLibAdd_LabelEntry_TxtVarOne(self, 0.05, ry, 0.20, rh, 0.60, 'History Data File Path :')
        ry = ry + 0.04
        self.s_dev_hdwinsec, self.s_dev_hdstep1, self.s_dev_hdstep2, v4, v5, v6, v7 = pf_GuiLibAdd_LabelEntry_TxtVarThree(self, 0.05, ry, 0.20, rh, 0.20, 0.20, 0.20, "History Data View ( Window, Step1, Step2 ) :")

        ry = ry + 0.04
        self.s_save_button = tk.Button(self, text="Save", command=self.pf_SaveSubmit)
        self.s_save_button.place(relx=0.30, rely=ry, relwidth=0.09, relheight=rh)
        self.s_close_button = tk.Button(self, text="Close", command=lambda:self.s_controller.pf_ShowPage(Page_None) )
        self.s_close_button.place(relx=0.40, rely=ry, relwidth=0.09, relheight=rh)
        self.s_reload_button = tk.Button(self, text="ReLoad", command=self.pf_Update)
        self.s_reload_button.place(relx=0.50, rely=ry, relwidth=0.09, relheight=rh)
        self.s_next_button = tk.Button(self, text="Next", command=lambda:self.s_controller.pf_ShowPage(Page_ADMIN_SET2) )
        self.s_next_button.place(relx=0.60, rely=ry, relwidth=0.09, relheight=rh)
    
    def pf_AddEntry(self, irx, iry, irh, irw, istr):
        tk.Entry(self, textvariable=istr).place(relheight=irh, relwidth=irw, relx=irx, rely=iry)
        
    def pf_AddCfgLbl(self, irx, iry, irh, irw, itxt):
        lbl = tk.Label(self, anchor='e', text=itxt)
        lbl.place(relx=irx, rely=iry, relwidth=irw, relheight=irh)

    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        pass

    def pf_AfterStart(self):
        self.pf_Update()

    def pf_Update(self):
        c = self.s_controller.s_Cfg
        c.gf_LoadCfg()
        
        self.s_customer_name.set( c.s_Customer_Name )
        self.s_customer_site.set( c.s_Customer_Site )
        
        self.s_usr_name.set( c.s_User_Name )
        self.s_usr_loginid.set( c.s_User_LoginId )
        self.s_usr_loginpwd.set( c.s_User_LoginPwd )
        
        self.s_admin_name.set( c.s_Admin_Name )
        self.s_admin_loginid.set( c.s_Admin_LoginId )
        self.s_admin_loginpwd.set( c.s_Admin_LoginPwd )

        self.s_remotehost_ip.set( c.s_RemoteHost_IP )
        self.s_remotehost_port.set( str(c.s_RemoteHost_Port) )
        self.s_remotehost_inactivesec.set( str(c.s_RemoteHost_InactivitySec) )

        self.s_dev_livedatasec.set( str(c.s_Device_LiveDataSec) )
        self.s_dev_hdfpath.set( c.s_Device_HDFilePath )
        self.s_dev_hdwinsec.set( str(c.s_Device_HDWindowSec) )
        self.s_dev_hdstep1.set( str(c.s_Device_HDWStep1) )
        self.s_dev_hdstep2.set( str(c.s_Device_HDWStep2) )

    def pf_SaveSubmit(self):
        c = self.s_controller.s_Cfg

        c.gf_SetCustomerName( self.s_customer_name.get() )
        c.gf_SetCustomerSite( self.s_customer_site.get() )

        c.gf_SetUserName( self.s_usr_name.get() )
        c.gf_SetUserLoginId( self.s_usr_loginid.get() )
        c.gf_SetUserLoginPwd( self.s_usr_loginpwd.get() )

        c.gf_SetAdminName( self.s_admin_name.get() )
        c.gf_SetAdminLoginId( self.s_admin_loginid.get() )
        c.gf_SetAdminLoginPwd( self.s_admin_loginpwd.get() )
           
        c.gf_SetRemoteHostIp( self.s_remotehost_ip.get() )
        c.gf_SetRemoteHostPort( pf_GetInegerEntryy( self.s_remotehost_port.get() ) )
        c.gf_SetRemoteHostInactivitySec( pf_GetInegerEntryy( self.s_remotehost_inactivesec.get() ) )
        c.gf_SetDeviceLiveDataSec( pf_GetInegerEntryy( self.s_dev_livedatasec.get() ) )
        c.gf_SetDeviceHDFilePath( self.s_dev_hdfpath.get() )
        c.gf_SetDeviceHDWindowSec( pf_GetInegerEntryy( self.s_dev_hdwinsec.get() ) )
        c.gf_SetDeviceHDWStep1( pf_GetInegerEntryy( self.s_dev_hdstep1.get() ) )
        c.gf_SetDeviceHDWStep2( pf_GetInegerEntryy( self.s_dev_hdstep2.get() ) )

        c.gf_SaveCfg()
        self.pf_Update()
    
# ---------------------------------------------------------------------------
# Page_ADMIN_SET2 : Settings
class Page_ADMIN_SET2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.s_parent = parent;
        self.s_controller = controller
        tk.Label(self, text="Admin Settings - Page 2").place(relx=0, rely=0, relwidth=1, relheight=0.03)
        
        self.s_dev_mac = []
        self.s_dev_name = []
        self.s_dev_ldvenabled = []
        self.s_dev_stasmplcnt = []
        self.s_dev_stapattncnt = []
        self.s_dev_staltaratio = []

        rh = 0.03
        ry = 0.00

        for i in range(0, self.s_controller.s_Cfg.s_User_DeviceMaxAllowed):
            ry = ry + 0.04
            v1, v2, v3, v4, v5, v6, v7 = pf_GuiLibAdd_LabelEntry_TxtVarThree(self, 0.05, ry, 0.20, rh, 0.295, 0.295, 0.01, ("Device-" + str(i+1) + "( MACID , Name, LDVEnabled ) :") )
            v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13 = pf_GuiLibAdd_LabelEntry_TxtVarSix(self, 0.05, ry, 0.27, rh, 0.22, 0.22, 0.02, 0.04, 0.04, 0.04, ("Dev-" + str(i+1) + "( MACID , Name, LVDEnabled, STA(ms), Patt, Ratio ) :") )
            self.s_dev_mac.append(v1)
            self.s_dev_name.append(v2)
            self.s_dev_ldvenabled.append(v3)
            self.s_dev_stasmplcnt.append(v4)
            self.s_dev_stapattncnt.append(v5)
            self.s_dev_staltaratio.append(v6)
        
        ry = ry + 0.04
        self.s_save_button = tk.Button(self, text="Save", command=self.pf_SaveSubmit)
        self.s_save_button.place(relx=0.30, rely=ry, relwidth=0.09, relheight=rh)
        self.s_close_button = tk.Button(self, text="Close", command=lambda:self.s_controller.pf_ShowPage(Page_None) )
        self.s_close_button.place(relx=0.40, rely=ry, relwidth=0.09, relheight=rh)
        self.s_reload_button = tk.Button(self, text="ReLoad", command=self.pf_Update)
        self.s_reload_button.place(relx=0.50, rely=ry, relwidth=0.09, relheight=rh)
        self.s_back_button = tk.Button(self, text="Back", command=lambda:self.s_controller.pf_ShowPage(Page_ADMIN_SET1) )
        self.s_back_button.place(relx=0.60, rely=ry, relwidth=0.09, relheight=rh)
    
    def pf_BeforeStop(self):
        pass

    def pf_BeforeStart(self):
        pass

    def pf_AfterStart(self):
        self.pf_Update()

    def pf_Update(self):
        c = self.s_controller.s_Cfg
        c.gf_LoadCfg()
        
        for i in range(0, c.s_User_DeviceMaxAllowed):
            self.s_dev_mac[i].set( UtilAna.gf_Get_IntToHexStr(c.s_Device_MacIds[i], 12) )
            self.s_dev_name[i].set( c.s_Device_Names[i] )
            self.s_dev_ldvenabled[i].set( str(c.s_Device_LDVEnableds[i]) )
            self.s_dev_stasmplcnt[i].set( str(c.gf_GetDeviceStaSmplCnt(i)) )
            self.s_dev_stapattncnt[i].set( str(c.s_Device_StaPattnCnts[i]) )
            self.s_dev_staltaratio[i].set( str(c.s_Device_StaLtaRatios[i]) )

    def pf_SaveSubmit(self):
        c = self.s_controller.s_Cfg

        for i in range(0, self.s_controller.s_Cfg.s_User_DeviceMaxAllowed):
            c.gf_SetDeviceMacId( i, UtilAna.gf_Get_HexStrToInt( self.s_dev_mac[i].get(), 12 ) )
            c.gf_SetDeviceName( i, self.s_dev_name[i].get() )
            c.gf_SetDeviceLDVEnabled( i, pf_GetInegerEntryy( self.s_dev_ldvenabled[i].get() ) )
            c.gf_SetDeviceStaSmplCnt( i, pf_GetInegerEntryy( self.s_dev_stasmplcnt[i].get() ) )
            c.gf_SetDeviceStaPattnCnt( i, pf_GetInegerEntryy( self.s_dev_stapattncnt[i].get() ) )
            c.gf_SetDeviceStaLtaRatio( i, pf_GetInegerEntryy( self.s_dev_staltaratio[i].get() ) )

        c.gf_SaveCfg()
        self.pf_Update()

# ---------------------------------------------------------------------------
class UsrEcoAppGui():
    """
    """
    # ------------------------------------------------------------------------
    def __init__(self, i_livedatafun, i_cfg):
        self.s_get_live_data_fun = i_livedatafun
        self.s_root = tk.Tk()
        # self.s_root.iconbitmap(default="MapsLogo32x32.ico")
        self.s_root.title("GeoPhone Client Application : V1R0")
        # configuring size of the window 
        self.s_height = self.s_root.winfo_screenheight()
        self.s_width = self.s_root.winfo_screenwidth()
        self.s_root.geometry(str(self.s_height) + 'x' + str(self.s_width))
        style = ttk.Style()
        style.theme_use('clam')
        self.s_root.state( 'zoomed' )
        
        self.s_Cfg = i_cfg
        self.s_UserLogInOk = False
        
        self.s_container = tk.Frame(self.s_root)
        self.s_container.pack(side="top", fill="both", expand = True)
        self.s_container.grid_rowconfigure(0, weight=1)
        self.s_container.grid_columnconfigure(0, weight=1)
        
        self.s_ActivePage = None
        self.s_frames = {}
        for F in (Page_None, Page_LDV, Page_HDV,Page_USER_LOGIN, Page_USER_SET, Page_ADMIN_LOGIN, Page_ADMIN_SET1, Page_ADMIN_SET2):
            frame = F(self.s_container, self)
            self.s_frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.s_menubar = tk.Menu(self.s_root)
        self.pf_AddMenuDataView()
        self.pf_AddMenuSettingsView()
        self.s_root.config(menu=self.s_menubar, bg='white')
        self.s_cbk_active = False
        self.s_cbk_fun = None
        self.s_cbk_tmr = 0
        self.s_root_exit = False
        
    def pf_StartCbk(self, i_tmr, i_fun):
        self.s_cbk_fun = i_fun
        self.s_cbk_tmr = i_tmr
        self.s_cbk_active = True
    def pf_StopCbk(self):
        self.s_cbk_active = False
        self.s_cbk_tmr = 0
        self.s_cbk_fun = None

    def pf_CallAfterXxMs(self):
        t1 = 0
        t2 = 1
        if True == self.s_cbk_active:
            while t1 != t2:
                cbkf = self.s_cbk_fun
                t1 = self.s_cbk_tmr
                t2 = self.s_cbk_tmr
            if 0 != t1:
                if None != cbkf:
                    cbkf()
        else:
            t1 = 1000
        if t1 < 1 or t1 > 60000:
            t1 = 1000

        if False == self.s_root_exit:
            self.s_root.after(t1, self.pf_CallAfterXxMs)
        
    def pf_ShowPage(self, cont):
        t = False
        if True == self.s_UserLogInOk:
            t = True
        elif None == self.s_ActivePage:
            t = True
        if True == t:
            if self.s_ActivePage != self.s_frames[cont]:
                if None != self.s_ActivePage:
                    self.s_ActivePage.pf_BeforeStop()
                self.s_ActivePage = self.s_frames[cont]
                self.s_ActivePage.pf_BeforeStart()
                self.s_ActivePage.tkraise()
                self.s_ActivePage.pf_AfterStart()
            
    def pf_ExitGui(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.s_UserLogInOk = True
            self.pf_ShowPage(Page_None)
            if None != self.s_ActivePage:
                self.s_ActivePage.pf_BeforeStop()
            self.s_root_exit = True
            self.s_root.destroy()
        
    def gf_GuiStart(self):
        self.s_root.protocol("WM_DELETE_WINDOW", self.pf_ExitGui)
        self.pf_CallAfterXxMs()
        self.pf_ShowPage(Page_USER_LOGIN)
        self.s_root.mainloop()
        
    def pf_AddMenuDataView(self):
        self.s_menu_dataview = tk.Menu(self.s_menubar, tearoff=0)
        self.s_menu_dataview.add_command(label="LiveDataView", command=lambda:self.pf_ShowPage(Page_LDV) )
        self.s_menu_dataview.add_command(label="HistoryDataView", command=lambda:self.pf_ShowPage(Page_None) )
        self.s_menu_dataview.add_separator()
        self.s_menu_dataview.add_command(label="IdleView", command=lambda:self.pf_ShowPage(Page_None) )
        self.s_menu_dataview.add_separator()
        self.s_menu_dataview.add_command(label="Exit", command=lambda:self.pf_ExitGui() )
        self.s_menubar.add_cascade(label="DataView", underline=0, menu=self.s_menu_dataview)

    def pf_AddMenuSettingsView(self):
        self.s_menu_settingsview = tk.Menu(self.s_menubar, tearoff=0)
        self.s_menu_settingsview.add_command(label="User Settings", command=lambda:self.pf_ShowPage(Page_USER_LOGIN) )
        self.s_menu_settingsview.add_separator()
        self.s_menu_settingsview.add_command(label="Admin Settings", command=lambda:self.pf_ShowPage(Page_ADMIN_LOGIN) )
        self.s_menubar.add_cascade(label="Configuration", underline=0, menu=self.s_menu_settingsview)

# ============================================================================
# end of file
