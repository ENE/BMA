import random
import time
import wx

from PyNeuro.PyNeuro import PyNeuro

class ScoreBar(wx.Window):
    def __init__(self, parent, value=0):
        wx.Window.__init__(self, parent, style=wx.SIMPLE_BORDER)
        self.value = value
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, event):
        margin = 2
        border = 1
        dc = wx.PaintDC(self)
        w, h = self.GetSize()
        #print(w,h)
        score = self.value
        color = self.map_value_to_color(score)
        dc.SetBrush(wx.Brush(color))
        w_rect = int(score * (w - (2*margin+2*border)) / 100)
        h_rect = h - (2*margin+2*border)
        dc.DrawRectangle(margin, margin, w_rect, h_rect)

    def OnSize(self, event):
        self.Refresh()

    def map_value_to_color(self, value):
        score = min(100, max(0, value))
        color = None
        if score < 50:
            color = wx.Colour(255, int(255 * score / 50), 0)
        else:
            color = wx.Colour(255 - int(255 * (score - 50) / 50), 255, 0)
        return color
    
    def update_score(self, value):
        self.value = value
        self.Refresh()

class ScoreBarPanel(wx.Panel):
    def __init__(self, parent=None):        
        wx.Panel.__init__(self, parent)
        self.bmaFrame = parent
        self.InitVars()
        self.InitUI()
        self.RunTimers() 

    def InitVars(self):
        self._prefix = 'Força da piscada'
        self._blinkForce = 100  # percent
        self._lastFrac = self._blinkForce    
        self._intervalForDecrease = 50  # milliseconds
        self._theLockGap = 400
        self._breakScoreFrom = 0.15
        self._maximumIsLocked = True  # because on tests we starts with score
        self._maximumTimestamp = self._get_timestamp_in_ms()
        self._forZeroNow = False

    def InitUI(self):  # for testing it starts at 100
        self._print_force()
        self._do_eye_status_icon()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.score_bar = ScoreBar(self, value=self._blinkForce)
        sizer.Add(self.score_bar, 1, wx.EXPAND)
        self.SetSizer(sizer)     
 
    def RunTimers(self):
        self.timer_decrease = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer_decrease, self.timer_decrease)
        self.timer_decrease.Start(self._intervalForDecrease)

    def PutScore(self, percentage): 
        self._maximumIsLocked = True
        self._maximumTimestamp = self._get_timestamp_in_ms()
        self._lastFrac = percentage
        self._forZeroNow = False
        self._do_new_score(percentage)
        self._do_eye_status_icon()
        self.bmaFrame.WriteStatus_LastBlinkForce(percentage)  
  
    def _get_timestamp_in_ms(self):
        return int(time.perf_counter()*1000)

    def _do_new_score(self, number):
        self.score_bar.update_score(number)  #TODO percent from 255 values
        self._blinkForce = number
        self._print_force()

    def _do_eye_status_icon(self):
        if self._maximumIsLocked:
            self.bmaFrame.SetEyeStatusIcon(blinking=True)
        else:
            self.bmaFrame.SetEyeStatusIcon(blinking=False)

    def _print_force(self):
        title = self._prefix + ': ' + str(self._blinkForce)
        return self.bmaFrame.SetTitle(title)
  
    def _on_timer_decrease(self, event):
        self._do_eye_status_icon()
        timestamp = self._get_timestamp_in_ms()
        gapOfNow = timestamp - self._maximumTimestamp
        if gapOfNow > self._theLockGap:
            if not self._forZeroNow:
                self._maximumIsLocked = False            
                score = self.score_bar.value
                frac = int(score * self._breakScoreFrom)  #TODO from an interval calc
                self._do_new_score(score - frac)
                #self._do_eye_status_icon()
                if self._lastFrac <= score:
                    self._forZeroNow = not self._forZeroNow
                self._lastFrac = frac
            else:
                if not self._maximumIsLocked:
                    self._do_new_score(0)
                    #self._do_eye_status_icon()      
        #print("gap = %4d %s" % (gapOfNow, self._maximumIsLocked))

class SingleScoreFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)
        self.InitUI()

    def InitUI(self):
        self.scorePanel = ScoreBarPanel(self)
        self.SetSize(320, 70)

class SingleScoreFrameOSC(SingleScoreFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

    def InitVars(self):
        super().InitVars()
        self._intervalForPush = 800  # milliseconds

    def RunTimers(self):
        super().RunTimers()

        self.timer_push = wx.Timer(self)  
        self.Bind(wx.EVT_TIMER, self._on_timer_push, self.timer_push)
        self.timer_push.Start(self._intervalForPush)

    def _on_timer_push(self, event):
        timestamp = self._get_timestamp_in_ms()
        number = 0
        self._maximumIsLocked = False  # is used?
        if not self._forZeroNow:
            number = int(random.uniform(0, 100))
            self._maximumTimestamp = timestamp
            self._maximumIsLocked = True
            #print(self._maximumIsLocked)
        self._forZeroNow = not self._forZeroNow
        self._do_new_score(number)
  
    def _on_timer_decrease(self, event):
        timestamp = self._get_timestamp_in_ms()
        gapOfNow = timestamp - self._maximumTimestamp
        if gapOfNow > self._theLockGap:
            if not self._forZeroNow:
                self._maximumIsLocked = False            
                score = self.score_bar.value
                frac = int(score * self._breakScoreFrom)  #TODO from an interval calc
                self._do_new_score(score - frac)      
        #print("gap = %4d %s" % (gapOfNow, self._maximumIsLocked))

class StatusFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent,size=(320, 90),
        # Impedir redimensionar e impedir maximizar
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        # Sobrepor janela mas manter uma barra de títulos com Fechar:
        self.SetWindowStyleFlag(wx.STAY_ON_TOP | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)
        ''' debug: (before, with self.__current_status=0)
        InitUI | __current_status = 0
        OnSize | __current_status = 1
        OnSize | __current_status = 2  *
         Timer | __current_status = 3  ...  '''
        self._current_status = 2  # começa "visualmente" desconectado, igual a 4
        self._current_status = 4  # finalmente! TODO?

        # TODO Segmentation fault no fechamento do início vazio
        # TODO deixar mesmo com a piscada força=100 no início?

        self.InitUI()

        #print("InitUI | currentStatus =", self._current_status)
        self.WriteStatus()
       
    def InitUI(self):
        self.Center()
        self.scorePanel = ScoreBarPanel(self)
        self.statusbar = self.CreateStatusBar(style=wx.SB_FLAT)
        self.statusbar.SetBackgroundColour(wx.WHITE)
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([10,-1,70])
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        #print("OnSize | currentStatus =", self.__current_status)
        self.WriteStatus()

    def DrawIcon(self, path_icon):
        rect = self.statusbar.GetFieldRect(0)
        #print("h = %d  w = %d" % (rect.height, rect.width))
        bmp = wx.Bitmap(path_icon)
        image = bmp.ConvertToImage()
        image = image.Rescale(rect.height-4, rect.height-4)
        bmp = wx.Bitmap(image)
        dc = wx.ClientDC(self.statusbar)
        dc.DrawBitmap(bmp, rect.x+2, rect.y+2, True)
        #self.statusbar.Refresh()

    def WriteStatus_LastBlinkForce(self, percentage):
        str_lastForce = "Da última: %d" % (percentage)
        self.statusbar.SetStatusText(str_lastForce, 2)

    def WriteStatus(self, status=None):
        status_now = PyNeuro.status_def_at[self._current_status]
        if status:
            status = PyNeuro.status_def[status]
            self._current_status = status.index
            status_now = status
        self.DrawIcon(status_now.icon)  # status bar
        self.statusbar.SetStatusText(status_now.description, 1)    

    def SetIcon(self, path_icon):
        icon = wx.Icon(path_icon, wx.BITMAP_TYPE_ICO)
        return super().SetIcon(icon)

    def SetEyeStatusIcon(self, blinking=False):
        path_icon = "icons/olho-aberto.ico"
        if blinking:
            path_icon = "icons/olho-fechado.ico"
        self.SetIcon(path_icon)

class StatusFrameOSC(StatusFrame):
    def __init__(self, title):
        super().__init__(title)
        self.RunTimers()

    def OnTimer(self, event):
        #print("Timer | currentStatus =", self._current_status)
        self.WriteStatus()

    def RunTimers(self):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(2000)  # 2 seconds

    def WriteStatus(self):  # rotates the status by timer
        super().WriteStatus()
        if self._current_status == 0: # connected, see above
            self.WriteStatus_LastBlinkForce(int(random.uniform(0, 100)))
        else:
            self.WriteStatus_LastBlinkForce(0)  # only in testing 
        self._current_status = (self._current_status + 1) % 5

class BmaSingleMeter(StatusFrame):
    def __init__(self):
        StatusFrame.__init__(self)
        self.Start_EEG()

    def Start_EEG(self):
        self.TGSP = PyNeuro()
        self.TGSP.set_blinkStrength_callback(self.OnBlinkStrength)
        self.TGSP.set_status_callback(self.OnStatusChange)
        # TODO dentro do PyNeuro, os callbacks de print() ou logger
        # TODO estudar como detalhar o "error" genérico do parser
        self.TGSP.connect()
        self.TGSP.start()

    def OnBlinkStrength(self, value):  # 0-255
        percentage = int( (100*value) / 255 )  # 0-100
        self.scorePanel.PutScore(percentage)
    
    def OnStatusChange(self):
        self.WriteStatus(self.TGSP.status) # needs lock?

def test_single_meter():
    app = wx.App()
    frame = BmaSingleMeter()
    frame.Show()
    app.MainLoop()

def test_status_things():
    app = wx.App()
    frame = StatusFrame("Barra de status")
    #frame = StatusFrameOSC("Barra de status (OSC)")
    frame.Show()
    app.MainLoop()

def test_score_things():
    app = wx.App()
    #frame = SingleScoreFrameOSC()
    frame = SingleScoreFrame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    #test_status_things()
    #test_score_things()
    test_single_meter()