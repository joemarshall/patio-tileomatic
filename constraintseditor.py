import wx
import wx.grid 

class ConstraintsEditor(wx.Frame):
    def __init__(self,parent,id,callback):
        wx.Frame.__init__(self, parent, id, 'Layout Constraints')
        self.callback=callback
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        vBox = wx.BoxSizer(wx.VERTICAL )
#        hBox1=wx.BoxSizer(wx.HORIZONTAL)
#        hBox2=wx.BoxSizer(wx.HORIZONTAL)
        self.maxLenControlUp=wx.SpinCtrl(self.panel)
        self.maxLenControlAcross=wx.SpinCtrl(self.panel)
        self.crossConstraintCheck=wx.CheckBox(self.panel,-1,"Don't allow 4 corners to meet")
        self.allowOverlapCheck=wx.CheckBox(self.panel,-1,"Allow overlap at bottom")
        vBox.Add(wx.StaticText(self.panel,-1,"Maximum border length across",),0)
        vBox.Add(self.maxLenControlAcross,0)
        vBox.Add(wx.StaticText(self.panel,-1,"Maximum border length up/down"),0)
        vBox.Add(self.maxLenControlUp,0)
        vBox.Add(self.crossConstraintCheck,0)
        vBox.Add(self.allowOverlapCheck,0)

        self.panel.SetSizer(vBox)
        self.maxLenControlAcross.Bind(wx.EVT_SPINCTRL,self.OnControlChange)
        self.maxLenControlUp.Bind(wx.EVT_SPINCTRL,self.OnControlChange)
        self.crossConstraintCheck.Bind(wx.EVT_CHECKBOX,self.OnControlChange)
        self.allowOverlapCheck.Bind(wx.EVT_CHECKBOX,self.OnControlChange)
        self.Bind(wx.EVT_CLOSE,self.OnClose)

    def OnClose(self,event):
        self.callback.OnConstraintsEditorClosed()
        event.Skip()

    def OnControlChange(self,event):
        self.OnChange()
        event.Skip()
        
    def LoadConstraintsFromArray(self,constraints):
        self.maxLenControlUp.SetValue(constraints['maxLenUp'])
        self.maxLenControlAcross.SetValue(constraints['maxLenAcross'])
        self.crossConstraintCheck.SetValue(constraints['crossConstraint'])
        self.allowOverlapCheck.SetValue(constraints['bottomOverlap'])
        self.Refresh()
        
    def GetConstraintsArray(self):
        retVal={}
        retVal['maxLenUp']=self.maxLenControlUp.GetValue()
        retVal['maxLenAcross']=self.maxLenControlAcross.GetValue()
        retVal['crossConstraint']=self.crossConstraintCheck.GetValue()
        retVal['bottomOverlap']=self.allowOverlapCheck.GetValue()
        return retVal

    def OnChange(self):
        if self.callback!=0:
            constraints=self.GetConstraintsArray()
            self.callback.OnConstraintsChange(constraints)

        
#class MyApp(wx.App):

#    def OnInfoBoxChange(self, boxes):
#        print"layoutchange"
#        print boxes
        
#    def OnInfoEditorClosed(self):
#        print "editorClose"
   # wxWindows calls this method to initialize the application
#    def OnInit(self):#

#        # Create an instance of our customized Frame class
#        frame = InfoBoxEditor(None, -1,self)
#        frame.Show(True)       
#        # Tell wxWindows that this is our main window)
#        self.SetTopWindow(frame)
#        frame.LoadInfoBoxesFromArray([("Manhole",7,.7333,1.5,2)])
        
        
        # Return a success flag
#        return True

#app = MyApp(0)     # Create an instance of the application class
#app.MainLoop()     # Tell it to start processing events
#exit(0)
