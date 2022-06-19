import random


class TileLayoutGenerator:
    
    # tileSizes: array of 4 tuples with the tile width / heights, and the number of each that is the limit (how many tiles you have). Units used are grid squares (eg with 300mm grid squares 2x3 = 600x900)
    # 4th of the 4 tuple is a priority ordering for choosing which tile to use
    # so for the ones we are getting, we have:
    # 14 x (3,2)  - 900x600
    # 14 x (2,2) - 600x600
    # 14 x (2,1)  - 600x290
    # 9 x   (1,1)   - 290x290
    def __init__(self,tileSizes,constraints):
        self.tileSizes=tileSizes
        self.constraints=constraints
        
    def numSlabs(self):
        retVal=0
        for c in self.tileSizes:
            retVal+=c[2]
        return retVal
        
        
    #spaceArray: array defining the space - this is an NxM array, top first (can import this from an excel table)
    def generateRandomLayout(self,spaceArray,maxLineLength):
        layoutList=list()
        tilesLeft=[]
        for c in self.tileSizes:
            tilesLeft.append(c[2])
        # fill algorithm:
        # choose a tile from what is left (use random weighted by number of tiles left)
        # orient the tile randomly v or h
        # Choose a point in the top most line to put a tile in
        # or maybe just drop it in from the top 
        #  put in the tile if: 
        #       a)it fits
        #       b) no rules broken: four corners rule, possibly a rule about big tiles going off the top edge if small tiles are still left, possibly a rule about putting 290s next to 600s?
        #       c) doesn't make any holes below it
        # else dump tile and repeat
        # aiming to get: even distribution up/down of big/small, and also even distrib across
        # stop when: a)whole layout is full, or b)no tiles left
        # this should generate a layout with all cuts at the bottom,left and right
        # output = list of tuples: each one being:(tileType,tileWidth,tileHeight,tileX,tileY)
        finished=False
        numTiles=0
        # minimum line with a gap in it
        minLine=0
        allowOverlap=False
        for c in tilesLeft:
            numTiles=numTiles+c
        while finished==False:
            # first find the list of empty places
            possibleSpaces=[]
            for x in range(0,len(spaceArray[minLine])):
                if spaceArray[minLine][x]==-1:
                    possibleSpaces.append(x)
            if len(possibleSpaces)==0:
                minLine+=1
                if minLine>=len(spaceArray):
                    finished=True
            else:
                random.shuffle(possibleSpaces)
                # now find a tile to put in
                # if we are on line 0, then put in anything at random to lay an edge course
                if minLine==0:
                    randomSample=random.randrange(0,numTiles)
                    curTile=0
                    for c in tilesLeft:
                        randomSample-=c
                        if randomSample>=0:
                            curTile=curTile+1
                    #print "tilesLeft:",tilesLeft
                    # we've got a tile of type c
                    orientation=random.randrange(0,2)
                    if self.tryFitTile(possibleSpaces,spaceArray,layoutList,minLine,curTile,orientation,numTiles,allowOverlap,maxLineLength)!=-1:
                        tilesLeft[curTile]=tilesLeft[curTile]-1
                        numTiles-=1
                else:
                    #print "tilesLeft:",tilesLeft
                    # on lower courses try big tiles first, try wide way round first
                    fittedTile=False
                    
                    priorities={}
                    for index,tileInfo in enumerate(self.tileSizes):
                        priority=tileInfo[3]
                        if priority in priorities:
                            priorities[priority].append(index)
                        else:
                            priorities[priority]=[index]
                    priorityNums=priorities.keys()
                    priorityNums.sort()
                    tileTryOrder=[]
                    for c in priorityNums:
                        random.shuffle(priorities[c])
                        tileTryOrder.extend(priorities[c])
                    #print "try order:",tileTryOrder
                    
                    #make a list of tile types sorted by priority and random otherwise                    
                    for curTile in tileTryOrder:
                        for orientation in range(0,2):
                            if fittedTile==False and tilesLeft[curTile]>0:
                                if self.tryFitTile(possibleSpaces,spaceArray,layoutList,minLine,curTile,orientation,numTiles,allowOverlap,maxLineLength)!=-1:                
                                    tilesLeft[curTile]=tilesLeft[curTile]-1
                                    numTiles-=1
                                    fittedTile=True
                    if not fittedTile:
                        if allowOverlap==True:
                            finished=True
                        elif self.constraints['bottomOverlap']==True:
                            allowOverlap=True
                        else:
                            finished=True
                if numTiles==0:
                    finished=True
#        for line in spaceArray:
#            for tileVal in line:
#                print "%3d"%tileVal,
#            print ""
#        print minLine
        return layoutList
        
    def tryFitTile(self,possibleSpaces,spaceArray,layoutList,minLine,curTile,orientation,numTiles,allowOverlap,maxLineLength):
        if orientation==0:
            tileWidth = self.tileSizes[curTile][0]
            tileHeight = self.tileSizes[curTile][1]
        else:
            tileHeight = self.tileSizes[curTile][0]
            tileWidth = self.tileSizes[curTile][1]
        # now try to fit it in all possible places on the bottom line in random order
        foundPos=-1
        for x in possibleSpaces:
            if foundPos==-1 and x+tileWidth<=len(spaceArray[minLine]):
                tileFits=True
                for c in range(0,tileWidth):
                    for d in range(0,tileHeight):
                        if minLine+d<len(spaceArray):
                            if spaceArray[minLine+d][x+c]!=-1:
                                tileFits=False
                        elif allowOverlap==False:
                            tileFits=False
                # check that it isn't going to create 4 corners together - ie. that there aren't two corners above either of our top corners
                if self.constraints['crossConstraint']==True:
                    if tileFits==True and minLine!=0:
                        if self.isBottomLeftCorner(spaceArray,x,minLine-1) and self.isBottomRightCorner(spaceArray,x-1,minLine-1):
                            tileFits=False
                        elif self.isBottomRightCorner(spaceArray,x+tileWidth-1,minLine-1) and self.isBottomLeftCorner(spaceArray,x+tileWidth,minLine-1):
                            tileFits=False
                #TODO:check that this isn't going to make a greater than maximum length line
                # 
                if self.upLineLengthToLeft(spaceArray,x,minLine-1) + tileHeight>self.constraints['maxLenUp']:
                    tileFits=False
                if self.upLineLengthToLeft(spaceArray,x+tileWidth,minLine-1) + tileHeight>self.constraints['maxLenUp']:
                    tileFits=False
                if self.leftLineLengthAbove(spaceArray,x-1,minLine) + tileWidth +self.rightLineLengthAbove(spaceArray,x+tileWidth,minLine) >self.constraints['maxLenAcross']:
                    tileFits=False
                if tileFits==True:
                    foundPos=x
# output = list of tuples: each one being:(tileType,tileWidth,tileHeight,tileX,tileY)
        if foundPos!=-1:
            layoutList.append((curTile,tileWidth,tileHeight,foundPos,minLine))
            for x in range(foundPos,foundPos+tileWidth):
                for y in range(minLine,min(len(spaceArray),minLine+tileHeight)):
                    spaceArray[y][x]=(100*(curTile+1))+numTiles
        return foundPos
        
    # a point is a bottom left corner if 
    #   a)the space below it isn't the same block
    #   b)the space to the left of it is a different block
    #   
    #   nb. corners in walls don't count - only corners where the other thing is a block
    #
    #
    def isBottomLeftCorner(self,spaceArray,x,y):
        if x<=0:
            return False
        if y<0:
            return False
        if y>=len(spaceArray)-1:
            return False
        thisPoint=spaceArray[y][x]
        belowSpace=spaceArray[y+1][x]
        leftSpace=spaceArray[y][x-1]
        if thisPoint==belowSpace:
            return False
        if thisPoint==leftSpace:
            return False
        if thisPoint<100 :
            return False
        #print "bottomLeftCorner %d:%d"%(x,y)
        return True        
    # a point is a bottom left corner if 
    #   a)the space below it isn't the same block
    #   b)the space to the right of it is a different block
    #   
    #   nb. corners in walls or undefined space (-1)  don't count - only corners where the other thing is a block
    #
    #
    def isBottomRightCorner(self,spaceArray,x,y):
        if y<0:
            return False
        if y>=len(spaceArray)-1:
            return False
        if x>=len(spaceArray[y])-1:
            return False
        thisPoint=spaceArray[y][x]
        belowSpace=spaceArray[y+1][x]
        rightSpace=spaceArray[y][x+1]
        if thisPoint==belowSpace:
            return False
        if thisPoint==rightSpace:
            return False
        if thisPoint<100 :
            return False
        #print "bottomRightCorner %d:%d"%(x,y)
        return True
        
    # length of line that goes to left side of x (across x,x-1) from Y  
    def upLineLengthToLeft(self,spaceArray,x,y):
        lineCount=0
        curY=y
        if x==0 or x>=len(spaceArray[0]):
            return 0
        while curY>=0:
            # boundaries  are okay to be next to - don't count as a line
            if spaceArray[curY][x]!=spaceArray[curY][x-1] and spaceArray[curY][x-1]!=0 and spaceArray[curY][x]!=0:
                lineCount=lineCount+1
                curY=curY-1
            else:
                break
#        print "upLineLength at x=%d, y=%d - %d"%(x,y,lineCount)
        return lineCount
        
    # length of leftward line that goes to top side of y (across y,y-1) from x  
    def leftLineLengthAbove(self,spaceArray,x,y):
        if y==0:
            return 0
        lineCount=0
        while x>=0:
            # boundaries  are okay to be next to - don't count as a line
            if spaceArray[y][x]!=spaceArray[y-1][x] and spaceArray[y-1][x]!=0 and spaceArray[y][x]!=0:
                lineCount=lineCount+1
                x=x-1
            else:
                break
        return lineCount
    
    # length of rightward line that goes to top side of y (across y,y-1) from x  
    def rightLineLengthAbove(self,spaceArray,x,y):
        if y==0:
            return 0
        lineCount=0
        while x<len(spaceArray[y]):
            # boundaries  are okay to be next to - don't count as a line
            if spaceArray[y][x]!=spaceArray[y-1][x] and spaceArray[y-1][x]!=0 and spaceArray[y][x]!=0:
                lineCount=lineCount+1
                x=x+1
            else:
                break
        return lineCount
