import wx
import wx.grid 

class MaterialsListEditor(wx.Frame):
    def __init__(self,parent,id,callback):
        wx.Frame.__init__(self, parent, id, 'Materials List Editor')
        self.callback=callback
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = wx.grid.Grid(panel)
        self.grid.CreateGrid(10,4)
        self.grid.SetColLabelValue(0,"Width")
        self.grid.SetColLabelValue(1,"Height")
        self.grid.SetColLabelValue(2,"Count")
        self.grid.SetColLabelValue(3,"Priority")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE,self.OnCellChange)
        self.Bind(wx.EVT_CLOSE,self.OnClose)

    def OnClose(self,event):
        self.callback.OnMaterialsEditorClosed()
        event.Skip()

    def OnCellChange(self,event):
        self.OnChange()
        event.Skip()
        
    def LoadMaterialsListFromArray(self,infoBoxes):
        self.grid.ClearGrid()
        for y,row in enumerate(infoBoxes):
            for x,value in enumerate(row):
                self.grid.SetCellValue(y,x,str(value))
        self.Refresh()
        
    def GetMaterialsListArray(self):
        retVal=[]
        for c in range(0,self.grid.GetNumberRows()):
            try:                
                value = (int(self.grid.GetCellValue(c,0)),int(self.grid.GetCellValue(c,1)),int(self.grid.GetCellValue(c,2)),int(self.grid.GetCellValue(c,3)))
                retVal.append(value)
            except Exception as e:
                continue
        return retVal

    def OnChange(self):
        if self.callback!=0:
            boxes=self.GetMaterialsListArray()
            self.callback.OnMaterialsListChange(boxes)

        
#class MyApp(wx.App):

#    def OnMaterialsListChange(self, boxes):
#        print"layoutchange"
#        print boxes
        
#    def OnInfoEditorClosed(self):
#        print "editorClose"
   # wxWindows calls this method to initialize the application
#    def OnInit(self):#

#        # Create an instance of our customized Frame class
#        frame = MaterialsListEditor(None, -1,self)
#        frame.Show(True)       
#        # Tell wxWindows that this is our main window
#        self.SetTopWindow(frame)
#        frame.LoadMaterialsListesFromArray([("Manhole",7,.7333,1.5,2)])
        
        
        # Return a success flag
#        return True

#app = MyApp(0)     # Create an instance of the application class
#app.MainLoop()     # Tell it to start processing events
#exit(0)
