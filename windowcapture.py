import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:
    #weidt and height of window to grab
    w = 0
    h = 0
    hwnd = None
    cropped_y = 0
    cropped_x = 0

    #constructor
    def __init__(self, window_name):
        #self.hwnd =  win32gui.GetWindowRect(hwnd)
        #self.hwnd = win32gui.FindWindow(None, 'DaRealFashGordon · DLive - Brave')
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('window not found: {}'.format(window_name))

        window_rect =  win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        

        #this is going to vary on the window sized.
        #capturing the whole browser and scanning for text reduced frame rate from 20fps to .02fps
        #screen shot and use paint to box the area of the subs to find frame_pixel_ H & W
        #image 1909x1111px
        #we want bottom right 440 x 157
        #1450 by 1000 ish
        frame_pixel_h = 750
        frame_pixel_w = 1500
        #box is about 460x260
        self.w = 460
        self.h = 260
        #self.w = self.w - (frame_pixel_h)
        #self.h = self.h - (frame_pixel_w)
        self.cropped_x = frame_pixel_w
        self.cropped_y = frame_pixel_h



    def get_screenshot(self):
    
        # get window img data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        dataBitMap.SaveBitmapFile(cDC, 'current.jpg')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        #free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        #drops alpha channel or cv.mathTemplate will throw error
        #img = img[..., :3]
        #this is for match template in openCV
        #brings down FPS

        img = np.ascontiguousarray(img)

        return img


    #this finds windows name
    @staticmethod
    def list_windows_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    
    #end window name find
