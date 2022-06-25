import time
import sys
import wx
from tilelayoutgenerator import *
from patioshapeeditor import *
from infoboxeditor import *
from materialslisteditor import *
from constraintseditor import *
import pickle
#todo: patio shape/size editor
#todo: materials choice editor
#choice of line length maximums, 4 corner constraint, whether to allow cuts at end or not (for people laying patios with no border and not wanting to cut)
#todo: manhole cover outlines etc

class TileLayoutDisplay(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self, parent, id, 'Patio Tile-o-matic')
        
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_load = menu.Append(wx.ID_OPEN, "&Open\tO", "Open layout")
        m_save = menu.Append(wx.ID_SAVE, "&Save\tS", "Save layout")
        menu.AppendSeparator()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tQ", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnQuit, m_exit)
        self.Bind(wx.EVT_MENU, self.OnSave, m_save)
        self.Bind(wx.EVT_MENU, self.OnLoad, m_load)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        item=menu.Append(-1,"&Re-layout Slabs\tR","Find a tile layout to fit the current patio and materials")
        self.Bind(wx.EVT_MENU,self.OnRelayoutSlabs,item)
        menu.AppendSeparator()
        item=menu.Append(-1,"&Edit patio layout\tE","Edit the shape of the patio")
        self.Bind(wx.EVT_MENU,self.OnEditPatio,item)
        item=menu.Append(-1,"&Edit materials list\tM","Edit the list of slabs you have")
        self.Bind(wx.EVT_MENU,self.OnEditMaterials,item)
        item=menu.Append(-1,"&Edit layout constraints\tC","Set constraints on the layout of the slabs")
        self.Bind(wx.EVT_MENU,self.OnEditConstraints,item)
        item=menu.Append(-1,"&Edit information boxes\tI","Information boxes display the position of things like manhole covers on the patio layout")
        self.Bind(wx.EVT_MENU,self.OnEditInfo,item)
        menuBar.Append(menu, "&Edit")
        menu = wx.Menu()
        item=menu.AppendCheckItem(-1,"&Grey mode\tG","Show the tiles in grey without labels")
        self.Bind(wx.EVT_MENU,self.OnToggleGrey,item)
        self.mGreyMenuItem=item
        menu.AppendSeparator()
        item=menu.AppendCheckItem(-1,"&Fullscreen mode\tF","Make the tile layout fill the whole screen")
        self.Bind(wx.EVT_MENU,self.OnToggleFullscreen,item)
        self.mFullScreenMenuItem=item
        menuBar.Append(menu, "&View")
        menu = wx.Menu()
        item=menu.Append(-1,"&About","Show the about dialog")
        self.Bind(wx.EVT_MENU,self.OnAbout,item)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
        self.showInstructions=True
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.constraintArray={
        'maxLenUp':4,
        'maxLenAcross':6,
        'crossConstraint':True,
        'bottomOverlap':True
        }
        self.patioLayoutArray=0
        self.slabList=0
        self.fullscreen=False
        self.Bind(wx.EVT_KEY_DOWN,self.OnKey)
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.showSingleColour=False
        self.fileLabel=""
        self.informationBoxes=0
        self.shapeEditor=0
        self.infoEditor=0
        self.constraintEditor=0
        self.materialsEditor=0
        self.slabTypes=[(3,2,14,1),(2,2,14,1),(2,1,14,3),(1,1,9,4)]
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
            [0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],\
            ]
        self.setPatioLayout(groundLayout)
        self.setInformationBoxes([("Manhole",7,.7333,1.5,2)])
        try:
            self.loadLayout("default.slb")
            self.resetPatioLayout()
        except Exception as e:
            print("No default layout")

    def OnAbout(self,evt):
        dlg = wx.MessageDialog(self, 'Patio Tile-o-matic 1.0 (C)Joe Marshall 2011', 'About Tile Layout', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnEditPatio(self, evt):
        if self.shapeEditor!=0:
            self.shapeEditor.Raise()
        else:
            self.shapeEditor=PatioShapeEditor(None, -1,self)
            self.shapeEditor.LoadLayoutFromArray(self.patioLayoutArray)
            self.shapeEditor.Show(True)
            
    def OnEditConstraints(self, evt):
        if self.constraintEditor!=0:
            self.constraintEditor.Raise()
        else:
            self.constraintEditor=ConstraintsEditor(None, -1,self)
            self.constraintEditor.LoadConstraintsFromArray(self.constraintArray)
            self.constraintEditor.Show(True)
            
    def OnEditInfo(self, evt):
        if self.infoEditor!=0:
            self.infoEditor.Raise()
        else:
            self.infoEditor=InfoBoxEditor(None, -1,self)
            self.infoEditor.LoadInfoBoxesFromArray(self.informationBoxes)
            self.infoEditor.Show(True)

    def OnEditMaterials(self, evt):
        if self.materialsEditor!=0:
            self.materialsEditor.Raise()
        else:
            self.materialsEditor=MaterialsListEditor(None, -1,self)
            self.materialsEditor.LoadMaterialsListFromArray(self.slabTypes)
            self.materialsEditor.Show(True)
            
            
    def OnToggleGrey(self,evt):
        self.showSingleColour=not self.showSingleColour
        self.mGreyMenuItem.Check(self.showSingleColour)
        self.Refresh(False)

    def OnToggleFullscreen(self,evt):
        self.fullscreen=not self.fullscreen
        self.mFullScreenMenuItem.Check(self.fullscreen)
        self.ShowFullScreen(self.fullscreen)
        
    def OnRelayoutSlabs(self,evt):
        self.generateSlabLayout()
        
    def OnSize(self, evt):
        self.Refresh(False);

    def OnQuit(self, evt):
        sys.exit(0)

    def OnSave(self,evt):
        filename = time.strftime("slabs-%b%d-%H%M-%S")
        self.fileLabel=""
        filename=filename.lower()
        self.showInstructions=False
        self.showSingleColour=False
        self.savePNG(filename+".png")
        self.showSingleColour=True
        self.savePNG(filename+"grey.png")
        self.showSingleColour=False
        self.saveLayout(filename+".slb")
        self.fileLabel=filename
        self.showInstructions=True
        dlg = wx.MessageDialog(self, 'Saved to: \n\t%s.png (laying plan)\n\t%sgrey.png (grey version)\n\t%s.slb (slab layout) '%(filename,filename,filename), 'Saved tile layout', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        
        self.Refresh(False)

    def OnLoad(self,evt):
        dialog = wx.FileDialog ( self, "Open Slab Layout",wildcard="*.slb",style = wx.FD_OPEN )
        if dialog.ShowModal() == wx.ID_OK:
            self.loadLayout(dialog.GetPath())
            self.fileLabel=dialog.GetFilename()
        self.Refresh(False)

    def OnKey(self,event):
        if event.GetModifiers()!=0:
            event.Skip()            
        elif event.GetKeyCode() == 70: # F - fullscreen
            self.OnToggleFullscreen(0)
        elif event.GetKeyCode() == 82:#R - refresh
            self.OnRelayoutSlabs(0)
        elif event.GetKeyCode()==71: #G - grey
            self.OnToggleGrey(0)
        elif event.GetKeyCode()==69: #E -edit patio shape
            self.OnEditPatio(0)
        elif event.GetKeyCode()==67: #C -edit constraints
            self.OnEditConstraints(0)
        elif event.GetKeyCode()==73: #I - edit information boxes
            self.OnEditInfo(0)
        elif event.GetKeyCode()==77: #M - edit materials list
            self.OnEditMaterials(0)
        elif event.GetKeyCode() == 81: #Q
            self.OnQuit(0)
        elif event.GetKeyCode() == 83: # S save
            self.OnSave(0)
        elif event.GetKeyCode() == 79: # O open
            self.OnLoad(0)
        else:
            event.Skip()

    def OnInfoBoxChange(self, boxes):
        self.setInformationBoxes(boxes)
        self.saveLayout("default.slb")
        self.Refresh()
        
    def OnMaterialsEditorClosed(self):
        self.materialsEditor=0
            
    def OnMaterialsListChange(self, materials):
        self.slabTypes=materials
        self.resetPatioLayout()
        self.saveLayout("default.slb")
        self.Refresh()

    def OnConstraintsEditorClosed(self):
        self.constraintEditor=0
            
    def OnConstraintsChange(self, constraints):
        self.constraintArray=constraints
        self.resetPatioLayout()
        self.saveLayout("default.slb")
        self.Refresh()

        
    def OnInfoEditorClosed(self):
        self.infoEditor=0
            
    def OnPatioShapeChange(self, layout):
        #patio shape has been altered
        self.setPatioLayout(layout)
        self.resetPatioLayout()
        # save this to the default file
        self.saveLayout("default.slb")
        self.Refresh()
        
    def OnPatioEditorClosed(self):
        self.shapeEditor=0

            
    def setPatioLayout(self,layout):
        self.patioLayoutArray=layout
        
    def resetPatioLayout(self):
        for line in self.patioLayoutArray:
            for c in range(0,len(line)):
                if line[c]!=0:
                    line[c]=-1
        self.slabList=[]
        
    #list describing information things for the diagram - eg. manhole covers etc - as tuples (text,x,y,w,h)
    def setInformationBoxes(self,infoBoxes):
        self.informationBoxes=infoBoxes
        
    def setSlabList(self,slabList):
        self.slabList=slabList

    def OnPaint(self,event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        w,h=self.GetClientSize()
        self.drawToDC(dc,w,h)
            
    def drawToDC(self,dc,w,h):
        numSlabs=[]
        for c in self.slabTypes:
            numSlabs.append(0)
        origH=h
        origW=w
        if self.patioLayoutArray!=0 and len(self.patioLayoutArray)>0:
            patioHeight=len(self.patioLayoutArray)
            patioWidth=len(self.patioLayoutArray[0])
            dc.SetBrush(wx.Brush(wx.Colour(255,255,255,255)))
            dc.DrawRectangle(0,0,w,h)
            h=(h*9)/10
            if patioWidth *h > w * patioHeight:
                #shrink width
                h = w * patioHeight / patioWidth
            else:
                #shrink height
                w = h * patioWidth / patioHeight
            xPos=0
            yPos=0
            for y,lineList in enumerate(self.patioLayoutArray):
                for x,slabValue in enumerate(lineList):
                    tileType=-1
                    dc.SetPen(wx.TRANSPARENT_PEN)
                    if slabValue==-1:
                        dc.SetBrush(wx.Brush(wx.Colour(128,128,128,255)))
                    elif slabValue==0:
                        dc.SetBrush(wx.Brush(wx.Colour(0,0,0,255)))
                    else:
                        tileColours=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)]
                        tileType=int(slabValue/100)
                        tileType=tileType-1
                        if tileType>=0 and tileType<len(tileColours):
                            colour=tileColours[tileType]
                        else:
                            colour=tileColours[0]
                        if self.showSingleColour:
                            colour=(128,200,128)
                        
                        dc.SetBrush(wx.Brush(wx.Colour(colour[0],colour[1],colour[2],255)))
                    dc.DrawRectangle(int((x*w)/patioWidth),int((y*h)/patioHeight),int(((x+1)*w)/patioWidth) - int((x*w)/patioWidth),int(((y+1)*h)/patioHeight)-int((y*h)/patioHeight))
            # output = list of tuples: each one being:(tileType,tileWidth,tileHeight,tileX,tileY)
            if self.slabList!=0:
                for slab in self.slabList:
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    dc.SetPen(wx.BLACK_PEN)
                    slabX=slab[3]
                    slabY=slab[4]
                    slabW=slab[1]
                    slabH=slab[2]
                    slabType=slab[0]
                    dc.DrawRectangle(int((slabX*w)/patioWidth),int((slabY*h)/patioHeight),int(((slabX+slabW)*w)/patioWidth - (slabX*w)/patioWidth),int(((slabY+slabH)*h)/patioHeight-(slabY*h)/patioHeight))
                    numSlabs[slabType]+=1
                    if not self.showSingleColour:
                        label="%d"%(slabType+1)
                        dc.SetPen(wx.NullPen)
                        dc.SetFont(wx.Font(wx.Size(int(h/(patioHeight*4)),int(h/(patioHeight*3))),wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
                        labelSize=dc.GetTextExtent(label)
                        xPos= ((slabX*2+slabW)*w)/(patioWidth*2)
                        yPos= ((2*slabY+slabH)*h)/(patioHeight*2)
                        xPos-=labelSize[0]/2
                        yPos-=labelSize[1]/2
                        #print "%s %d %d"%(label,xPos,yPos)
                        dc.DrawText(label,int(xPos),int(yPos))
            dc.SetPen(wx.GREY_PEN)
            dc.SetFont(wx.Font(wx.Size(int(h/(patioHeight*4)),int(h/(patioHeight*3))),wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
            if len(self.fileLabel)>0:
                dc.DrawText("file: "+self.fileLabel,0,int(origH-h/(patioHeight*3)))
            if w<origW:
                dc.SetTextForeground(wx.Colour(0,0,0,255))
                dc.DrawText(" Materials List:",origW-75,int(h/2))
                for idx,c in enumerate(self.slabTypes):
                    textToDisplay=" %02d x Type %d : %dx%d Slab  "%(numSlabs[idx],idx+1,c[0],c[1])
                    (lineWidth,lineHeight)=dc.GetTextExtent(textToDisplay)
                    dc.DrawText(textToDisplay,origW-lineWidth, int(h/2 + (idx+1) * h/(patioHeight*3)) )
            if self.informationBoxes!=0:
                dc.SetPen(wx.BLACK_DASHED_PEN)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)

                for (text,adjustX,adjustY,adjustW,adjustH) in self.informationBoxes:
                    adjustX=(adjustX * w)/patioWidth
                    adjustY=(adjustY * h)/patioHeight
                    adjustW=(adjustW*w)/patioWidth
                    adjustH=(adjustH*h)/patioHeight
                    (tw,th)=dc.GetTextExtent(text)
                    dc.DrawRectangle(int(adjustX),int(adjustY),int(adjustW),int(adjustH))
                    dc.SetTextForeground(wx.Colour(255,255,255,255))
                    dc.DrawText(text,int(adjustX+adjustW/2-tw/2),int(adjustY+adjustH/2-th/2))
            if self.showInstructions==True:
                instructions=[
                    ("Q","Quit"),
                    ("S","Save layout"),
                    ("O","Open layout"),
                    ("F","Toggle fullscreen mode"),
                    ("G","Toggle grey mode"),
                    ("C","Edit layout constraints"),
                    ("I","Edit information boxes"),
                    ("M","Edit materials list"),
                    ("E","Edit patio shape"),
                    ("R","Re-layout slabs")
                    ]
                yPos=origH
                for line in instructions:
                    (lineWid,lineHeight)=dc.GetTextExtent(line[1]+" "+line[0])
                    yPos-=lineHeight
                    dc.SetTextForeground(wx.Colour(0,0,0,255))
                    dc.DrawText(line[1],origW-lineWid,yPos)
                    (lineWid,lineHeight)=dc.GetTextExtent(line[0])
                    dc.SetTextForeground(wx.Colour(255,0,0,255))
                    dc.DrawText(line[0],origW-lineWid,yPos)



                
    def savePNG(self,filename):
        print("Save png to %s"%filename)
        w,h=self.GetClientSize()
        bitmap=wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC()
        dc.SelectObject(bitmap)
        self.drawToDC(dc,w,h)
        dc.SelectObject(wx.NullBitmap)
        bitmap.SaveFile(filename,wx.BITMAP_TYPE_PNG)
        
    def saveLayout(self,filename):
        print("Save layout to %s"%filename)
        filehandler = open(filename, 'wb') 
        pickle.dump(self.patioLayoutArray, filehandler) 
        pickle.dump(self.slabList, filehandler) 
        pickle.dump(self.slabTypes, filehandler) 
        pickle.dump(self.informationBoxes, filehandler) 
        pickle.dump(self.constraintArray,filehandler)


    def loadLayout(self,filename):
        filehandler = open(filename, 'rb') 
        self.patioLayoutArray=pickle.load(filehandler) 
        self.slabList=pickle.load( filehandler) 
        self.slabTypes=pickle.load( filehandler) 
        self.informationBoxes=pickle.load( filehandler)
        self.constraintArray=pickle.load(filehandler)

    def generateSlabLayout(self):
        dlg=wx.ProgressDialog("Layout Slabs","",parent=self,style=wx.PD_CAN_ABORT)
        dlg.Pulse("")
        
        self.fileLabel=""
        tg = TileLayoutGenerator(self.slabTypes,self.constraintArray)

        layoutCount=0
        bUsedAll=False
        while not bUsedAll:
            # -1 = ground
            # 0 = blocked
            # anything else = tiled: tile number + 100 * tile
            self.resetPatioLayout()
            slabList = tg.generateRandomLayout(self.patioLayoutArray,999)
            bUsedAll=True
            for c in self.patioLayoutArray:
                for d in c:
                    if d==-1:
                        bUsedAll=False
            layoutCount=layoutCount+1
            if layoutCount%25==0:
                (cont,temp)=dlg.Pulse("Trying layouts: %d"%layoutCount)
                if cont==False:
                    break
            if layoutCount==10000:
                dlgMsg = wx.MessageDialog(self, 'Couldn\'t fit slabs to patio.\n\n\tCheck:\n\t1)You have a large enough quantity of slabs to fill the patio.\n\t2)Your edge length constraints are not set too low.\n\t3)You have enough small slabs to fit the shape of the patio edge.\n\nYou may want to make edges less jagged if they are not walls or other hard edges.', 'Layout Failed', wx.OK)
                dlgMsg.ShowModal()
                dlgMsg.Destroy()
                break
                

#            if len(slabList)==tg.numSlabs():
#                bUsedAll=True
        self.setSlabList(slabList)
        dlg.Destroy()
        self.Refresh(False)

    
class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = TileLayoutDisplay(None, -1)
        frame.Show(True)
        frame.Maximize(True)
        
        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        
        
        # Return a success flag
        return True

app = MyApp(0)     # Create an instance of the application class
app.MainLoop()     # Tell it to start processing events
exit(0)
