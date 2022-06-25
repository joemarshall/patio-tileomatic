
import functools

import wx

class PatioShapeEditor(wx.Frame):
    def __init__(self,parent,id,callback):
        wx.Frame.__init__(self, parent, id, 'Patio Shape Editor')
        self.callback=0
        self.grid=0
        self.patioLayout=[]
        self.patioButtons=[]
        self.panel = wx.Panel ( self, -1 )
        vBox = wx.BoxSizer(wx.VERTICAL)
        hBox=wx.BoxSizer(wx.HORIZONTAL)
        self.widthControl=wx.SpinCtrl(self.panel)
        self.heightControl=wx.SpinCtrl(self.panel)
        hBox.Add(wx.StaticText(self.panel,-1,"Width",style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT),1,flag=wx.CENTRE)
        hBox.Add(self.widthControl,1)
        hBox.Add(wx.StaticText(self.panel,-1,"Height",style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT),1,flag=wx.CENTRE)
        hBox.Add(self.heightControl,1)
        vBox.Add(hBox,0,flag=wx.EXPAND)
        self.vBox=vBox
        self.panel.SetSizerAndFit ( vBox )
        self.SetGridSize(10,10)
        self.widthControl.Bind(wx.EVT_SPIN,self.OnWidthChange)
        self.heightControl.Bind(wx.EVT_SPIN,self.OnHeightChange)
        groundLayout=\
            [\
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],\
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],\
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,77,-1,-1,0],\
            ]
        self.LoadLayoutFromArray(groundLayout)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.callback=callback
        
    def OnClose(self,event):
        self.callback.OnPatioEditorClosed()
        event.Skip()
        
    def OnWidthChange(self,event):
        self.SetGridSize(self.widthControl.GetValue(),self.heightControl.GetValue())
        
    def OnHeightChange(self,event):
        self.SetGridSize(self.widthControl.GetValue(),self.heightControl.GetValue())    


    def OnGridButtonClicked(self,x,y,event):
        if self.patioLayout[y][x]==0:
            self.patioLayout[y][x]=-1
            self.patioButtons[y][x].SetBackgroundColour(wx.Colour(255,255,255,255))
        else:
            self.patioLayout[y][x]=0
            self.patioButtons[y][x].SetBackgroundColour(wx.Colour(0,0,0,255))
        self.OnChange()
            

    def LoadLayoutFromArray(self,patioLayoutArray):
        self.patioLayout=patioLayoutArray
        for line in self.patioLayout:
            for idx in range(0,len(line)):
                if line[idx]!=0:
                    line[idx]=-1
        if len(self.patioLayout)>0:
            self.SetGridSize(len(self.patioLayout[0]),len(self.patioLayout))
            
    def SetGridSize(self,w,h):
        if self.grid!=0:
            self.grid.Clear(True)
            self.vBox.Remove(self.grid)
            self.grid=0
        self.grid=wx.GridSizer(int(w),int(h),0)
        oldPatioLayout=self.patioLayout
        self.patioLayout=[]
        self.patioButtons=[]
        for y in range(0,h):
            self.patioLayout.append([])
            self.patioButtons.append([])            
            for x in range(0,w):
                checkBox=wx.Button(self.panel,-1,"")
                self.grid.Add(checkBox,flag=wx.EXPAND)
                curValue=-1
                if y<len(oldPatioLayout) and x<len(oldPatioLayout[y]):
                    curValue=oldPatioLayout[y][x]
                if curValue==0:
                    checkBox.SetBackgroundColour(wx.Colour(0,0,0,255))
                else:
                    checkBox.SetBackgroundColour(wx.Colour(255,255,255,255))
                checkBox.Bind(wx.EVT_BUTTON,functools.partial(self.OnGridButtonClicked,x,y))
                self.patioLayout[y].append(curValue)
                self.patioButtons[y].append(checkBox)
        self.vBox.Add(self.grid,1,flag=wx.EXPAND)
        self.patioSize=(w,h)
        self.heightControl.SetValue(h)
        self.widthControl.SetValue(w)
        self.panel.Layout (  )
        self.OnChange()

    def OnChange(self):
        if self.callback!=0:
            self.callback.OnPatioShapeChange(self.patioLayout)
