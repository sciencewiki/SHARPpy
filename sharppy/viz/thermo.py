import numpy as np
from PySide import QtGui, QtCore
import sharppy.sharptab as tab
from sharppy.sharptab.constants import *
import datetime

## routine written by Kelton Halbert
## keltonhalbert@ou.edu

__all__ = ['backgroundText', 'plotText']

class backgroundText(QtGui.QFrame):
    '''
    Handles drawing the background frame.
    '''
    def __init__(self):
        super(backgroundText, self).__init__()
        self.initUI()

    def initUI(self):
        ## initialize fram variables such as size,
        ## padding, etc.
        self.setStyleSheet("QFrame {"
            "  background-color: rgb(0, 0, 0);"
            "  border-width: 1px;"
            "  border-style: solid;"
            "  border-color: #3399CC;}")
        self.label_font = QtGui.QFont('Helvetica', 10)
        self.label_metrics = QtGui.QFontMetrics( self.label_font )
        self.label_height = self.label_metrics.height()
        self.severe_font = QtGui.QFont('Helvetica', 12)
        self.severe_metrics = QtGui.QFontMetrics( self.severe_font )
        self.severe_height = self.severe_metrics.height()
        self.lpad = 0; self.rpad = 0
        self.tpad = 5; self.bpad = 0
        self.wid = self.size().width()
        self.hgt = self.size().height()
        self.tlx = self.rpad; self.tly = self.tpad
        self.brx = self.wid; self.bry = self.hgt
        self.plotBitMap = QtGui.QPixmap(self.width()-2, self.height()-2)
        self.plotBitMap.fill(QtCore.Qt.black)
        self.plotBackground()
    
    def draw_frame(self, qp):
        '''
        Draws the background frame and the text headers for indices.
        '''
        ## initialize a white pen with thickness 1 and a solid line
        pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.label_font)
        ## make the initial x value relative to the width of the frame
        x1 = self.brx / 8
        y1 = self.bry / 17
        ## draw the header for the indices
        rect0 = QtCore.QRect(x1*0, self.tpad, x1*2, self.label_height)
        rect1 = QtCore.QRect(x1*1, self.tpad, x1*2, self.label_height)
        rect2 = QtCore.QRect(x1*2, self.tpad, x1*2, self.label_height)
        rect3 = QtCore.QRect(x1*3, self.tpad, x1*2, self.label_height)
        rect4 = QtCore.QRect(x1*4, self.tpad, x1*2, self.label_height)
        rect5 = QtCore.QRect(x1*5, self.tpad, x1*2, self.label_height)
        rect6 = QtCore.QRect(x1*6, self.tpad, x1*2, self.label_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'PCL')
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'CAPE')
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'CINH')
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'LCL')
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'LI')
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'LFC')
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'EL')
        ## draw lines seperating the indices
        qp.drawLine( 0, y1+self.tpad-1, self.brx, y1+self.tpad-1 )
        qp.drawLine( 0, y1*5+self.tpad, self.brx, y1*5+self.tpad )
        qp.drawLine( 0, y1*13-self.tpad, x1*4.5, y1*13-self.tpad )
        qp.drawLine( x1*4.5, self.bry, x1*4.5, y1*10  )
        qp.drawLine( x1*4.5, y1*10, self.brx, y1*10  )
    
    def resizeEvent(self, e):
        '''
        Handles when the window gets resized.
        '''
        self.initUI()

    def plotBackground(self):
        '''
        Handles drawing the text background.
        '''
        ## initialize a QPainter objext
        qp = QtGui.QPainter()
        qp.begin(self.plotBitMap)
        qp.setRenderHint(qp.Antialiasing)
        qp.setRenderHint(qp.TextAntialiasing)
        ## draw the frame
        self.draw_frame(qp)
        qp.end()


class plotText(backgroundText):
    '''
    Handles plotting the indices in the frame.
    '''
    def __init__(self, prof):
        ## get the surfce based, most unstable, and mixed layer
        ## parcels to use for indices, as well as the sounding
        ## profile itself.
        self.sfcparcel = prof.sfcpcl
        self.mlparcel = prof.mlpcl
        self.fcstpcl = prof.fcstpcl
        self.muparcel = prof.mupcl
        self.prof = prof;
        
        
        ## either get or calculate the indices, round to the nearest int, and
        ## convert them to strings.
        ## K Index
        self.k_idx = tab.utils.INT2STR( prof.k_idx )
        ## precipitable water
        self.pwat = tab.utils.FLOAT2STR( prof.pwat, 2 )
        ## 0-3km agl lapse rate
        self.lapserate_3km = tab.utils.FLOAT2STR( prof.lapserate_3km, 1 )
        ## 3-6km agl lapse rate
        self.lapserate_3_6km = tab.utils.FLOAT2STR( prof.lapserate_3_6km, 1 )
        ## 850-500mb lapse rate
        self.lapserate_850_500 = tab.utils.FLOAT2STR( prof.lapserate_850_500, 1 )
        ## 700-500mb lapse rate
        self.lapserate_700_500 = tab.utils.FLOAT2STR( prof.lapserate_700_500, 1 )
        ## convective temperature
        self.convT = tab.utils.INT2STR( prof.convT )
        ## sounding forecast surface temperature
        self.maxT = tab.utils.INT2STR( prof.maxT )
        #fzl = str(int(self.sfcparcel.hght0c))
        ## 100mb mean mixing ratio
        self.mean_mixr = tab.utils.FLOAT2STR( prof.mean_mixr, 1 )
        ## 150mb mean rh
        self.low_rh = tab.utils.INT2STR( prof.low_rh )
        self.mid_rh = tab.utils.INT2STR( prof.mid_rh )
        ## calculate the totals totals index
        self.totals_totals = tab.utils.INT2STR( prof.totals_totals )
        
        super(plotText, self).__init__()

    def resizeEvent(self, e):
        '''
        Handles when the window is resized.
        '''
        super(plotText, self).resizeEvent(e)
        self.plotData()
    
    def paintEvent(self, e):
        super(plotText, self).paintEvent(e)
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawPixmap(1, 1, self.plotBitMap)
        qp.end()

    def plotData(self):
        '''
        Handles the drawing of the text on the frame.
        '''
        ## initialize a QPainter object
        qp = QtGui.QPainter()
        qp.begin(self.plotBitMap)
        qp.setRenderHint(qp.Antialiasing)
        qp.setRenderHint(qp.TextAntialiasing)
        ## draw the indices
        self.drawConvectiveIndices(qp)
        self.drawIndices(qp)
        self.drawSevere(qp)
        qp.end()
    
    def drawSevere(self, qp):
        '''
        This handles the severe indices, such as STP, sig hail, etc.
        ---------
        qp: QtGui.QPainter object
        '''
        ## initialize a pen to draw with.
        pen = QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.severe_font)
        ## needs to be coded.
        x1 = self.brx / 10
        y1 = self.bry / 17
        ship = tab.utils.FLOAT2STR( self.prof.ship, 1 )
        stp_fixed = tab.utils.FLOAT2STR( self.prof.stp_fixed, 1 )
        stp_cin = tab.utils.FLOAT2STR( self.prof.stp_cin, 1 )
        right_scp = tab.utils.FLOAT2STR( self.prof.right_scp, 1 )
        left_scp = tab.utils.FLOAT2STR( self.prof.left_scp, 1 )
        rect0 = QtCore.QRect(x1*6, y1*10.00+(self.tpad), x1*8, self.severe_height)
        rect1 = QtCore.QRect(x1*6, y1*11.25+(self.tpad), x1*8, self.severe_height)
        rect2 = QtCore.QRect(x1*6, y1*12.50+(self.tpad), x1*8, self.severe_height)
        rect3 = QtCore.QRect(x1*6, y1*13.75+(self.tpad), x1*8, self.severe_height)
        rect4 = QtCore.QRect(x1*6, y1*15.00+(self.tpad), x1*8, self.severe_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'Supercell = ' + right_scp)
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'Left Supercell = ' + left_scp)
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'STP (cin) = ' + stp_cin)
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'STP (fix) = ' + stp_fixed)
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'Sig Hail = ' + ship)
    
    def drawIndices(self, qp):
        '''
        Draw the non-parcel indices.
        --------
        qp: QtGui.QPainter object
        '''
        ## initialize a white pen with width 2 as a solid line
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.label_font)
        ## make the initial x point relatice to the width of the frame.
        x1 = self.brx / 10
        y1 = self.bry / 17
        rpad = 5
        tpad = 5

        ## Now we have all the data we could ever want. Time to start drawing
        ## them on the frame.
        ## This starts with the left column.
        
        rect0 = QtCore.QRect(rpad, y1*5+self.tpad*2, x1*4, self.label_height)
        rect1 = QtCore.QRect(rpad, y1*6+self.tpad*2, x1*4, self.label_height)
        rect2 = QtCore.QRect(rpad, y1*7+self.tpad*2, x1*4, self.label_height)
        rect3 = QtCore.QRect(rpad, y1*8+self.tpad*2, x1*4, self.label_height)
        rect4 = QtCore.QRect(rpad, y1*13, x1*8, self.label_height)
        rect5 = QtCore.QRect(rpad, y1*14, x1*8, self.label_height)
        rect6 = QtCore.QRect(rpad, y1*15, x1*8, self.label_height)
        rect7 = QtCore.QRect(rpad, y1*16, x1*8, self.label_height+self.tpad)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'PW = ' + self.pwat + 'in')
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'MeanW = ' + self.mean_mixr + 'g/kg')
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'LowRH = ' + self.low_rh + '%')
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'MidRH = ' + self.mid_rh + '%')
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'Sfc-3km AGL LR = ' + self.lapserate_3km + ' C/km')
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, '3-6km AGL LR = ' + self.lapserate_3_6km + ' C/km')
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, '850-500mb LR = ' + self.lapserate_850_500 + ' C/km')
        qp.drawText(rect7, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, '700-500mb LR = ' + self.lapserate_700_500 + ' C/km')
    ## middle-left column
        rect0 = QtCore.QRect(x1*3.5, y1*5+self.tpad*2, x1*4, self.label_height)
        rect1 = QtCore.QRect(x1*3.5, y1*6+self.tpad*2, x1*4, self.label_height)
        rect2 = QtCore.QRect(x1*3.5, y1*7+self.tpad*2, x1*4, self.label_height)
        rect3 = QtCore.QRect(x1*3.5, y1*8+self.tpad*2, x1*4, self.label_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'K = ' + self.k_idx)
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'TT = ' + self.totals_totals)
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'ConvT = ' + self.convT + 'F')
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft, 'maxT = ' + self.maxT + 'F')
    ## middle-right column
    #qp.drawText((x1*15), 70, 60, 20,
    #        QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft,
    #        'FZL = ' + fzl)

    
    def drawConvectiveIndices(self, qp):
        '''
        This handles the drawing of the parcel indices.
        --------
        qp: QtGui.QPainter object
        '''
        ## initialize a white pen with thickness 2 and a solid line
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.label_font)
        ## make the initial x pixel coordinate relative to the frame
        ## width.
        x1 = self.brx / 8
        y1 = self.bry / 17
        ## get the indices rounded to the nearest int, conver to strings
        ## Start with the surface based parcel.
        sfc_bplus = tab.utils.INT2STR( self.sfcparcel.bplus )
        sfc_bminus = tab.utils.INT2STR( self.sfcparcel.bminus )
        sfc_lclhght = tab.utils.INT2STR( self.sfcparcel.lclhght )
        sfc_limax = tab.utils.INT2STR( self.sfcparcel.li5 )
        sfc_lfchght = tab.utils.INT2STR( self.sfcparcel.lfchght )
        sfc_elhght = tab.utils.INT2STR( self.sfcparcel.elhght )
        ## get the forecast surface parvel
        fcst_bplus = tab.utils.INT2STR( self.fcstpcl.bplus )
        fcst_bminus = tab.utils.INT2STR( self.fcstpcl.bminus )
        fcst_lclhght = tab.utils.INT2STR( self.fcstpcl.lclhght )
        fcst_limax = tab.utils.INT2STR( self.fcstpcl.li5 )
        fcst_lfchght = tab.utils.INT2STR( self.fcstpcl.lfchght )
        fcst_elhght = tab.utils.INT2STR( self.fcstpcl.elhght )
        ## Now get the mixed layer parcel indices
        ml_bplus = tab.utils.INT2STR( self.mlparcel.bplus )
        ml_bminus = tab.utils.INT2STR( self.mlparcel.bminus )
        ml_lclhght = tab.utils.INT2STR( self.mlparcel.lclhght )
        ml_limax = tab.utils.INT2STR( self.mlparcel.li5 )
        ## check and see if the lfc is there
        ml_lfchght = tab.utils.INT2STR( self.mlparcel.lfchght )
        ml_elhght = tab.utils.INT2STR( self.mlparcel.elhght )
        ## get the most unstable parcel indices
        mu_bplus = tab.utils.INT2STR( self.muparcel.bplus )
        mu_bminus = tab.utils.INT2STR( self.muparcel.bminus )
        mu_lclhght = tab.utils.INT2STR( self.muparcel.lclhght )
        mu_limax = tab.utils.INT2STR( self.muparcel.li5 )
        ## make sure the lfc is there
        mu_lfchght = tab.utils.INT2STR( self.muparcel.lfchght )
        mu_elhght = tab.utils.INT2STR( self.muparcel.elhght )

        ## Now that we have all the data, time to plot the text in their
        ## respective columns.

        ## Start by plotting the surface parcel
        rect0 = QtCore.QRect(x1*0, y1+self.tpad, x1*2, self.label_height)
        rect1 = QtCore.QRect(x1*1, y1+self.tpad, x1*2, self.label_height)
        rect2 = QtCore.QRect(x1*2, y1+self.tpad, x1*2, self.label_height)
        rect3 = QtCore.QRect(x1*3, y1+self.tpad, x1*2, self.label_height)
        rect4 = QtCore.QRect(x1*4, y1+self.tpad, x1*2, self.label_height)
        rect5 = QtCore.QRect(x1*5, y1+self.tpad, x1*2, self.label_height)
        rect6 = QtCore.QRect(x1*6, y1+self.tpad, x1*2, self.label_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'SFC')
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, sfc_bplus)
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, sfc_bminus)
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, sfc_lclhght)
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, sfc_limax)
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, sfc_lfchght)
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, sfc_elhght)
        ## plot forcast surface parcel
        rect0 = QtCore.QRect(x1*0, y1*2+self.tpad, x1*2, self.label_height)
        rect1 = QtCore.QRect(x1*1, y1*2+self.tpad, x1*2, self.label_height)
        rect2 = QtCore.QRect(x1*2, y1*2+self.tpad, x1*2, self.label_height)
        rect3 = QtCore.QRect(x1*3, y1*2+self.tpad, x1*2, self.label_height)
        rect4 = QtCore.QRect(x1*4, y1*2+self.tpad, x1*2, self.label_height)
        rect5 = QtCore.QRect(x1*5, y1*2+self.tpad, x1*2, self.label_height)
        rect6 = QtCore.QRect(x1*6, y1*2+self.tpad, x1*2, self.label_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'FCST')
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, fcst_bplus)
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, fcst_bminus)
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, fcst_lclhght)
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, fcst_limax)
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, fcst_lfchght)
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, fcst_elhght)
        ## plot ML Parcel
        rect0 = QtCore.QRect(x1*0, y1*3+self.tpad, x1*2, self.label_height)
        rect1 = QtCore.QRect(x1*1, y1*3+self.tpad, x1*2, self.label_height)
        rect2 = QtCore.QRect(x1*2, y1*3+self.tpad, x1*2, self.label_height)
        rect3 = QtCore.QRect(x1*3, y1*3+self.tpad, x1*2, self.label_height)
        rect4 = QtCore.QRect(x1*4, y1*3+self.tpad, x1*2, self.label_height)
        rect5 = QtCore.QRect(x1*5, y1*3+self.tpad, x1*2, self.label_height)
        rect6 = QtCore.QRect(x1*6, y1*3+self.tpad, x1*2, self.label_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'ML')
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, ml_bplus)
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, ml_bminus)
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, ml_lclhght)
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, ml_limax)
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, ml_lfchght)
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, ml_elhght)
        ## plot MU parcel
        rect0 = QtCore.QRect(x1*0, y1*4+self.tpad, x1*2, self.label_height)
        rect1 = QtCore.QRect(x1*1, y1*4+self.tpad, x1*2, self.label_height)
        rect2 = QtCore.QRect(x1*2, y1*4+self.tpad, x1*2, self.label_height)
        rect3 = QtCore.QRect(x1*3, y1*4+self.tpad, x1*2, self.label_height)
        rect4 = QtCore.QRect(x1*4, y1*4+self.tpad, x1*2, self.label_height)
        rect5 = QtCore.QRect(x1*5, y1*4+self.tpad, x1*2, self.label_height)
        rect6 = QtCore.QRect(x1*6, y1*4+self.tpad, x1*2, self.label_height)
        qp.drawText(rect0, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, 'MU')
        qp.drawText(rect1, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, mu_bplus)
        qp.drawText(rect2, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, mu_bminus)
        qp.drawText(rect3, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, mu_lclhght)
        qp.drawText(rect4, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, mu_limax)
        qp.drawText(rect5, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, mu_lfchght)
        qp.drawText(rect6, QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter, mu_elhght)