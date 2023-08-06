from threading import Thread
import time
import tkinter as tk
from tkinter import ttk, font
from time import sleep
from PIL import Image, ImageTk, ImageOps
from pathlib import Path
import math
import qrcode
import sys
import platform
import ctypes
from typing import Type
import _tkinter

class GUI():

    global_master = None
    master = None
    font_name = None

    def __init__(self):
        def mainloopThread():
            GUI.global_master = tk.Tk()
            families = {'HYQiHei', '汉仪旗黑 50S', '汉仪旗黑', 'HYQiHei 50S'}
            for family in families:
                if family in font.families():
                    self.font_name = family
                    # print("found font:" + family)
                    break
            else:
                self.font_name = self.load_font(Path(__file__).parent/"HYQiHei_50S.ttf")
                # print("loaded font:" + family)

            families = {'Segment7'}
            for family in families:
                if family in font.families():
                    self.font_digit_name = family
                    # print("found font:" + family)
                    break
            else:
                self.font_digit_name = self.load_font(Path(__file__).parent/"Segment7-4Gml.otf")
                # print("loaded font:" + family)
            
            style = ttk.Style(GUI.global_master)
            style.configure('.', font=(self.font_name, 11))
            GUI.global_master.geometry('240x320')
            GUI.global_master.resizable(0, 0)
            # GUI.global_master.iconify()
            # GUI.global_master.update()
            # GUI.global_master.deiconify()
            if platform.system() != "Darwin":
                GUI.global_master.mainloop()
            else:
                print("Mac OS can only run UI on the main thread. Use gui.update() to update GUI")
        
        if GUI.thd is not None:
            raise Exception("Can only create single GUI instance!")
            return
        if platform.system() != "Darwin":
            GUI.thd = Thread(target=mainloopThread)   # gui thread
            GUI.thd.daemon = True  # background thread will exit if main thread exits
            GUI.thd.start()  # start tk loop
        else:
            GUI.thd = mainloopThread
            GUI.thd()
        while GUI.global_master is None:
            sleep(0.01)
        self.master = GUI.global_master
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill='both', expand=1)

        self.canvas = tk.Canvas(self.frame, bd=0, highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        

        def check_alive():
            self.master.after(500, check_alive)
        check_alive()

    def update(self):
        if platform.system() == "Darwin":
            while True:
                self.master.willdispatch()
                if self.master.dooneevent(_tkinter.DONT_WAIT+_tkinter.ALL_EVENTS) == 0:
                    break

    def load_font(self, path):
        import os
        from contextlib import redirect_stderr
        from fontTools import ttLib


        def font_name(font_path):
            font = ttLib.TTFont(font_path, ignoreDecompileErrors=True)
            with redirect_stderr(None):
                names = font['name'].names
            families = set()
            for x in names:
                if x.nameID == 1 or x.nameID == 16:
                    try:
                        families.add(x.toUnicode())
                    except UnicodeDecodeError:
                        families.add(x.string.decode(errors='ignore'))
            # print("font_name:" + str(families))
            return families

        families = font_name(path)
        tk_font_families = font.families()
        for family in families:
            if family in tk_font_families:
                return family
        import shutil
        if platform.system() == "Linux":
            Path.mkdir(Path.home()/".fonts", exist_ok=True)
            shutil.copy(path, Path.home()/".fonts")
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif platform.system() == "Windows":
            import ctypes
            import os
            import shutil

            from ctypes import wintypes

            try:
                import winreg
            except ImportError:
                import _winreg as winreg

            user32 = ctypes.WinDLL('user32', use_last_error=True)
            gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

            FONTS_REG_PATH = r'Software\Microsoft\Windows NT\CurrentVersion\Fonts'

            HWND_BROADCAST = 0xFFFF
            SMTO_ABORTIFHUNG = 0x0002
            WM_FONTCHANGE = 0x001D
            GFRI_DESCRIPTION = 1
            GFRI_ISTRUETYPE = 3

            if not hasattr(wintypes, 'LPDWORD'):
                wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

            user32.SendMessageTimeoutW.restype = wintypes.LPVOID
            user32.SendMessageTimeoutW.argtypes = (
                wintypes.HWND,   # hWnd
                wintypes.UINT,   # Msg
                wintypes.LPVOID, # wParam
                wintypes.LPVOID, # lParam
                wintypes.UINT,   # fuFlags
                wintypes.UINT,   # uTimeout
                wintypes.LPVOID  # lpdwResult
            )

            gdi32.AddFontResourceW.argtypes = (
                wintypes.LPCWSTR,) # lpszFilename

            # http://www.undocprint.org/winspool/getfontresourceinfo
            gdi32.GetFontResourceInfoW.argtypes = (
                wintypes.LPCWSTR, # lpszFilename
                wintypes.LPDWORD, # cbBuffer
                wintypes.LPVOID,  # lpBuffer
                wintypes.DWORD)   # dwQueryType


            def install_font(src_path):
                # copy the font to the Windows Fonts folder
                dst_path = os.path.join(
                    os.environ['USERPROFILE'], 'AppData\Local\Microsoft\Windows\Fonts', os.path.basename(src_path)
                )
                shutil.copy(src_path, dst_path)

                # load the font in the current session
                if not gdi32.AddFontResourceW(dst_path):
                    os.remove(dst_path)
                    raise WindowsError('AddFontResource failed to load "%s"' % src_path)

                # notify running programs
                user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, None)

                # store the fontname/filename in the registry
                filename = dst_path
                fontname = os.path.splitext(filename)[0]

                # try to get the font's real name
                cb = wintypes.DWORD()
                if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None, GFRI_DESCRIPTION):
                    buf = (ctypes.c_wchar * cb.value)()
                    if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf, GFRI_DESCRIPTION):
                        fontname = buf.value

                is_truetype = wintypes.BOOL()
                cb.value = ctypes.sizeof(is_truetype)
                gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), ctypes.byref(is_truetype), GFRI_ISTRUETYPE)

                if is_truetype:
                    fontname += ' (TrueType)'

                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, FONTS_REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)
            
            install_font(path)
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif platform.system() == "Darwin":
            Path.mkdir(Path.home() / "Library" / "Fonts", exist_ok=True)
            shutil.copy(path, Path.home() / "Library" / "Fonts")
            time.sleep(0.5)
            os.execl(sys.executable, sys.executable, *sys.argv)


    def on_key_click(self, event, onclick):
        self.master.bind(event, lambda event: onclick())

    def on_a_click(self, onclick):
        self.master.bind('a', lambda event: onclick())

    def on_b_click(self, onclick):
        self.master.bind('b', lambda event: onclick())

    def on_mouse_move(self, onmove):
        self.master.bind('<Motion>', lambda event: onmove(event.x, event.y))

    cache_images = {}

    class CanvasBase(object):
        ids = None
        parent = None

        def __init__(self, parent):
            self.ids = []
            self.parent = parent

        def preprocess_init(self, arg_last, kw_map, kw_last, kw_ex_last):
            self.arg = arg_last
            self.kw_map = kw_map
            self.kw = kw_last
            self.kw_ex = kw_ex_last

            self.arg_current = {}
            self.kw_current = {}
            self.kw_ex_current = {}

        def preprocess_current(self, kw):
            self.arg_current = {}
            for key in self.arg.keys():
                if key in kw: self.arg_current[key] = kw.pop(key)

            if 'anchor' in self.arg_current: self.arg_current['anchor'] = self.convert_anchor(self.arg_current['anchor'])

            self.kw_current = {}
            for key in self.kw_map.keys():
                if key in kw:
                    self.kw_current[self.kw_map[key]] = kw.pop(key)
            for key in self.kw.keys():
                if key in kw:
                    self.kw_current[key] = kw.pop(key)
            
            if 'fill' in self.kw_current: self.kw_current['fill'] = self.rgb2hex(self.kw_current['fill'])
            if 'outline' in self.kw_current: self.kw_current['outline'] = self.rgb2hex(self.kw_current['outline'])
            if 'anchor' in self.kw_current: self.kw_current['anchor'] = self.convert_anchor(self.kw_current['anchor'])


            self.kw_ex_current = {}
            for key in self.kw_ex.keys():
                if key in kw: self.kw_ex_current[key] = kw.pop(key)
            
            if 'color' in self.kw_ex_current: self.kw_ex_current['color'] = self.rgb2hex(self.kw_ex_current['color'])



            self.kw_current.update(kw)

        def preprocess_color(self):
            if 'color' in self.kw_ex_current:
                if 'outline' not in self.kw_current:
                    self.kw_current['outline'] = self.kw_ex_current['color']
                if self.kw['fill'] != '' and 'fill' not in self.kw_current:
                    self.kw_current['fill'] = self.kw_ex_current['color']

        def preprocess_last(self):
            self.arg.update(self.arg_current)
            self.kw.update(self.kw_current)
            self.kw_ex.update(self.kw_ex_current)

        def postprocess_onclick(self):
            if 'onclick' in self.kw_ex_current:
                for id in self.ids:
                    self.parent.canvas.tag_bind(id, '<Button-1>', lambda event: self.kw_ex['onclick']())

        def remove(self):
            for id in self.ids:
                self.parent.cache_images.pop(id, None)
                self.parent.canvas.delete(id)
        
        def rgb2hex(self, color):
            if isinstance(color, tuple):
                return "#%02x%02x%02x" % color
            return color

        def convert_anchor(self, anchor):
            converter = {
                'top_left':'nw', 'top':'n', 'top_right':'ne',
                'left':'w', 'right':'e',
                'bottom_left':'sw', 'bottom':'s', 'bottom_right':'se'}
            if anchor in converter:
                return converter[anchor]
            else:
                return anchor
            

    class CanvasText(CanvasBase):

        def preprocess(self, kw):
            self.preprocess_current(kw)
            font = (self.kw_current.pop('font_family', self.kw['font'][0]), self.kw_current.pop('font_size', self.kw['font'][1]))
            if font != self.kw['font']:                
                if 'font' not in self.kw_current:
                    self.kw_current['font'] = font

            self.preprocess_last()


        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x':0, 'y':0},
                {'font_size':'font_size', 'origin':'anchor', 'color':'fill', 'font_family':'font_family'},
                {'font': (self.parent.font_name, 14), 'anchor':'nw', 'fill':'black'},
                {'onclick':None})

            self.preprocess(kw)
            self.ids.append(self.parent.canvas.create_text(self.arg['x'], self.arg['y'], **self.kw))
            self.postprocess_onclick()      
        
        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                self.parent.canvas.coords(self.ids[0], self.arg['x'], self.arg['y'])
            if self.kw_current:
                self.parent.canvas.itemconfigure(self.ids[0], **self.kw_current)
            self.postprocess_onclick() 
  
    def draw_text(self, **kw):
        return GUI.CanvasText(self, **kw)

    def draw_digit(self, **kw):
        if 'font_family' not in kw:
            kw['font_family'] = self.font_digit_name
        return GUI.CanvasText(self, **kw)


    class CanvasImage(CanvasBase):
        def preprocess(self, kw):
            self.preprocess_current(kw)
            image = None
            if 'image_raw' in self.kw_current:
                self.kw_ex_current['image_raw'] = image = self.kw_current.pop('image_raw')
            elif 'w' in self.kw_ex_current or 'h' in self.kw_ex_current:
                image = self.kw_ex['image_raw']
            
            if image is not None:
                if isinstance(image, str):
                    image = Image.open(image)
                self.kw_ex.update(self.kw_ex_current)
                w, h = (self.kw_ex['w'], self.kw_ex['h'])
                if w is not None or h is not None:
                    target_size = (4096 if w is None else w, 4096 if h is None else h)
                    image = ImageOps.contain(image, target_size)
                self.kw_current['image'] = ImageTk.PhotoImage(image)
            self.preprocess_last()

        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x':0, 'y':0},
                {'origin':'anchor', 'image':'image_raw'},
                {'anchor':'nw', 'image':None},
                {'onclick':None, 'w':None, 'h':None, 'image_raw':None})

            self.preprocess(kw)
            self.ids.append(self.parent.canvas.create_image(self.arg['x'], self.arg['y'], **self.kw))
            self.parent.cache_images[self.ids[0]] = self.kw_current['image']
            self.postprocess_onclick()

        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                self.parent.canvas.coords(self.ids[0], self.arg['x'], self.arg['y'])
            if self.kw_current:
                self.parent.canvas.itemconfigure(self.ids[0], **self.kw_current)
                if 'image' in self.kw_current:
                    self.parent.cache_images[self.ids[0]] = self.kw['image']
            self.postprocess_onclick()

    def draw_image(self, **kw):
        return GUI.CanvasImage(self, **kw)
    

    
    class CanvasLine(CanvasBase):

        def preprocess(self, kw):
            self.preprocess_current(kw)
            self.preprocess_last()

        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x0':0, 'y0':0, 'x1':240, 'y1':320},
                {'color':'fill'},
                {'fill':'black'},
                {'onclick':None})

            self.preprocess(kw)
            self.ids.append(self.parent.canvas.create_line(self.arg['x0'], self.arg['y0'], self.arg['x1'], self.arg['y1'], **self.kw))
            self.postprocess_onclick()

        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                self.parent.canvas.coords(self.ids[0], self.arg['x0'], self.arg['y0'], self.arg['x1'], self.arg['y1'])
            if self.kw_current:
                self.parent.canvas.itemconfigure(self.ids[0], **self.kw_current)
            self.postprocess_onclick()

    def draw_line(self, **kw):
        return GUI.CanvasLine(self, **kw)

    class CanvasCircle(CanvasBase):
        def preprocess(self, kw):
            self.preprocess_current(kw)
            self.preprocess_color()
            self.preprocess_last()

        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x':120, 'y':160, 'r':50},
                {},
                {'fill':'', 'outline':'black'},
                {'onclick':None, 'color':'black'})

            self.preprocess(kw)
            x, y, r = (self.arg['x'], self.arg['y'], self.arg['r'])
            self.ids.append(self.parent.canvas.create_oval(x-r, y-r, x+r, y+r, **self.kw))
            self.postprocess_onclick()
        
        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                x, y, r = (self.arg['x'], self.arg['y'], self.arg['r'])
                self.parent.canvas.coords(self.ids[0], x-r, y-r, x+r, y+r)
            if self.kw_current:
                self.parent.canvas.itemconfigure(self.ids[0], **self.kw_current)
            self.postprocess_onclick()

    def draw_circle(self, **kw):
        return GUI.CanvasCircle(self, **kw)

    def fill_circle(self, **kw):
        kw['fill'] = kw.get('fill', kw.get('color', 'black'))
        return GUI.CanvasCircle(self, **kw)

    def draw_point(self, x, y, **kw):
        kw['fill'] = kw.get('fill', kw.get('color', 'black'))
        kw['r'] = kw.get('r', 0)
        return GUI.CanvasCircle(self, **kw)


    class CanvasRect(CanvasBase):
        def preprocess(self, kw):
            self.preprocess_current(kw)
            self.preprocess_color()
            self.preprocess_last()

        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x':0, 'y':0, 'w':40, 'h':20},
                {},
                {'fill':'', 'outline':'black'},
                {'onclick':None, 'color':'black'})

            self.preprocess(kw)
            x, y, w, h = (self.arg['x'], self.arg['y'], self.arg['w'], self.arg['h'])
            self.ids.append(self.parent.canvas.create_rectangle(x, y, x+w, y+h, **self.kw))
            self.postprocess_onclick()
        
        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                x, y, w, h = (self.arg['x'], self.arg['y'], self.arg['w'], self.arg['h'])
                self.parent.canvas.coords(self.ids[0], x, y, x+w, y+h)
            if self.kw_current:
                self.parent.canvas.itemconfigure(self.ids[0], **self.kw_current)
            self.postprocess_onclick()


    def draw_rect(self, **kw):
        return GUI.CanvasRect(self, **kw)

    def fill_rect(self, **kw):
        kw['fill'] = kw.get('fill', kw.get('color', 'black'))
        return GUI.CanvasRect(self, **kw)

    
    class CanvasClock(CanvasBase):
        def preprocess(self, kw):

            self.preprocess_current(kw)
            if 'color' in self.kw_ex_current:
                if 'outline' not in self.kw_current:
                    self.kw_current['outline'] = self.kw_ex_current['color']
            
            if 'style' in self.kw_ex_current:
                if self.kw_ex_current['style'] == 'customize':
                    pass
                elif self.kw_ex_current['style'] == 'dark':
                    self.kw_current['outline'] = 'white'
                    if self.kw['fill'] != '' or 'fill' in self.kw_current:
                        self.kw_current['fill'] = 'black'
                else:
                    self.kw_current['outline'] = 'black'
                    if self.kw['fill'] != '' or 'fill' in self.kw_current:
                        self.kw_current['fill'] = 'white'

            self.preprocess_last()

        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x':120, 'y':160, 'r':100, 'h':11, 'm':40, 's':20},
                {},
                {'fill':'', 'outline':'black'},
                {'onclick':None, 'color':'black', 'style':'customize'})

            self.preprocess(kw)
            x, y, r, h, m, s = (self.arg['x'], self.arg['y'], self.arg['r'], self.arg['h'], self.arg['m'], self.arg['s'])
            
            self.ids.append(self.parent.canvas.create_oval(x-r, y-r, x+r, y+r, width=r//12, outline=self.kw['outline'], fill=self.kw['fill']))
            self.ids.append(self.parent.canvas.create_oval(x-r//24,y-r//24,x+r//24,y+r//24, outline=self.kw['outline'], fill=self.kw['outline']))
            r1=r # dial lines for one minute 
            r2=r//1.42 # for hour numbers  after the lines 
            rs=r//1.2 # length of second needle 
            rm=r//1.3 # length of minute needle
            rh=r//1.8 # lenght of hour needle

            in_degree = 0
            in_degree_s=int(s)*6 # local second 
            in_degree_m=int(m)*6 # local minutes  
            in_degree_h=(int(h)*30)%360 # 12 hour format 

            h=iter(['12','1','2','3','4','5','6','7','8','9','10','11'])

            for i in range(0,60):
                in_radian = math.radians(in_degree)
                if(i%5==0): 
                    ratio=0.85 # Long marks ( lines )
                    t1=x+r2*math.sin(in_radian) # coordinate to add text ( hour numbers )
                    t2=y-r2*math.cos(in_radian) # coordinate to add text ( hour numbers )
                    self.ids.append(self.parent.canvas.create_text(t1,t2,fill=self.kw['outline'],font=(self.parent.font_name, int(r//6)),text=next(h))) # number added
                    marksWidth = 2
                else:
                    ratio=0.9 # small marks ( lines )
                    marksWidth = 1
                
                x1=x+ratio*r1*math.sin(in_radian)
                y1=y-ratio*r1*math.cos(in_radian)
                x2=x+r1*math.sin(in_radian)
                y2=y-r1*math.cos(in_radian)
                self.ids.append(self.parent.canvas.create_line(x1,y1,x2,y2,fill=self.kw['outline'],width=marksWidth)) # draw the line for segment
                in_degree=in_degree+6 # increment for next segment
                # End of Marking on the dial with hour numbers 
                # Initialize the second needle based on local seconds value  
            
            in_radian = math.radians(in_degree_s) 
            x2=x+rs*math.sin(in_radian)
            y2=y-rs*math.cos(in_radian)
            self.ids.append(self.parent.canvas.create_line(x,y,x2,y2,fill=self.kw['outline'],width=r/40)) # draw the second needle

            in_radian = math.radians(in_degree_m)
            x2=x+rm*math.sin(in_radian)
            y2=y-rm*math.cos(in_radian) 
            self.ids.append(self.parent.canvas.create_line(x,y,x2,y2,width=r/40,fill=self.kw['outline']))

            in_degree_h=in_degree_h+(in_degree_m*0.0833333)          
            in_radian = math.radians(in_degree_h)
            x2=x+rh*math.sin(in_radian)
            y2=y-rh*math.cos(in_radian)
            self.ids.append(self.parent.canvas.create_line(x,y,x2,y2,width=r/40+r/40,fill=self.kw['outline']))
            
            self.postprocess_onclick()
        
        def config(self, **kw):

            self.preprocess(kw)

            if self.arg_current:
                x, y, r, h, m, s = (self.arg['x'], self.arg['y'], self.arg['r'], self.arg['h'], self.arg['m'], self.arg['s'])

                in_degree_s=int(s)*6 # local second 
                in_degree_m=int(m)*6 # local minutes  
                in_degree_h=(int(h)*30)%360 # 12 hour format 

                rs=r//1.2 # length of second needle 
                rm=r//1.3 # length of minute needle
                rh=r//1.8 # lenght of hour needle

                if 'x' in self.arg_current or 'y' in self.arg_current or 'r' in self.arg_current:
                    self.parent.canvas.coords(self.ids[0], x-r, y-r, x+r, y+r)
                    self.parent.canvas.itemconfigure(self.ids[0], width=r//12)

                    self.parent.canvas.coords(self.ids[1], x-r//24,y-r//24,x+r//24,y+r//24)
            
                    r1=r # dial lines for one minute 
                    r2=r//1.42 # for hour numbers  after the lines 

                    in_degree = 0
                    h=iter(['12','1','2','3','4','5','6','7','8','9','10','11'])
                    j = 2

                    for i in range(0,60):
                        in_radian = math.radians(in_degree)
                        if(i%5==0): 
                            ratio=0.85 # Long marks ( lines )
                            t1=x+r2*math.sin(in_radian) # coordinate to add text ( hour numbers )
                            t2=y-r2*math.cos(in_radian) # coordinate to add text ( hour numbers )
                            self.parent.canvas.coords(self.ids[j], t1,t2)
                            self.parent.canvas.itemconfigure(self.ids[j], font=(self.parent.font_name, int(r//6)))
                            j += 1
                        else:
                            ratio=0.9 # small marks ( lines )
                        
                        x1=x+ratio*r1*math.sin(in_radian)
                        y1=y-ratio*r1*math.cos(in_radian)
                        x2=x+r1*math.sin(in_radian)
                        y2=y-r1*math.cos(in_radian)

                        self.parent.canvas.coords(self.ids[j], x1,y1,x2,y2)
                        j += 1
                        in_degree=in_degree+6 # increment for next segment
                    
                    self.parent.canvas.itemconfigure(self.ids[-3], width=r/40)
                    self.parent.canvas.itemconfigure(self.ids[-2], width=r/40)
                    self.parent.canvas.itemconfigure(self.ids[-1], width=r/40+r/40)

                in_radian = math.radians(in_degree_s) 
                x2=x+rs*math.sin(in_radian)
                y2=y-rs*math.cos(in_radian)
                self.parent.canvas.coords(self.ids[-3], x, y, x2, y2)
                

                in_radian = math.radians(in_degree_m)
                x2=x+rm*math.sin(in_radian)
                y2=y-rm*math.cos(in_radian) 
                self.parent.canvas.coords(self.ids[-2], x, y, x2, y2)

                in_degree_h=in_degree_h+(in_degree_m*0.0833333)          
                in_radian = math.radians(in_degree_h)
                x2=x+rh*math.sin(in_radian)
                y2=y-rh*math.cos(in_radian)
                self.parent.canvas.coords(self.ids[-1], x, y, x2, y2)
                
            if self.kw_current:
                for i, id in enumerate(self.ids):
                    if i == 0:
                        self.parent.canvas.itemconfigure(id, outline=self.kw['outline'], fill=self.kw['fill'])
                    elif i == 1:
                        self.parent.canvas.itemconfigure(id, outline=self.kw['outline'], fill=self.kw['outline'])
                    else:
                        self.parent.canvas.itemconfigure(id, fill=self.kw['outline'])

            self.postprocess_onclick()


    def draw_clock(self, **kw):
        return GUI.CanvasClock(self, **kw)

    def fill_clock(self, **kw):
        kw['fill'] = kw.get('fill', 'white')
        return GUI.CanvasClock(self, **kw)



    class CanvasRoundRect(CanvasBase):
        def preprocess(self, kw):
            self.preprocess_current(kw)
            self.preprocess_color()
            self.preprocess_last()

        def __init__(self, parent, **kw):
            super().__init__(parent)

            self.preprocess_init(
                {'x':0, 'y':0, 'w':40, 'h':20, 'r':8},
                {},
                {'fill':'', 'outline':'black'},
                {'onclick':None, 'color':'black'})

            self.preprocess(kw)
            x, y, w, h, r = (self.arg['x'], self.arg['y'], self.arg['w'], self.arg['h'], self.arg['r'])
            r = min((w/2, h/2, r))

            kw_temp = self.kw.copy()
            if kw_temp['fill'] != '':
                kw_temp['outline'] = kw_temp['fill']
                kw_temp['state'] = 'normal'
            else:
                kw_temp['state'] = 'hidden'
            points=[
                x+r, y+r, x+r, y, x+w-r, y, x+w-r, y+r, x+w, y+r, x+w, y+h-r,
                x+w-r, y+h-r, x+w-r, y+h ,x+r, y+h, x+r, y+h-r, x, y+h-r, x, y+r, 
            ]
            self.ids.append(self.parent.canvas.create_polygon(points, **kw_temp))
            self.ids.append(self.parent.canvas.create_arc(x,   y,   x+2*r,   y+2*r,   **kw_temp, start= 90, extent=90, style="pieslice"))
            self.ids.append(self.parent.canvas.create_arc(x+w-2*r, y+h-2*r, x+w, y+h, **kw_temp, start=270, extent=90, style="pieslice"))
            self.ids.append(self.parent.canvas.create_arc(x+w-2*r, y,   x+w, y+2*r,   **kw_temp, start=  0, extent=90, style="pieslice"))
            self.ids.append(self.parent.canvas.create_arc(x,   y+h-2*r, x+2*r,   y+h, **kw_temp, start=180, extent=90, style="pieslice"))

            self.ids.append(self.parent.canvas.create_arc(x,   y,   x+2*r,   y+2*r,   start= 90, extent=90, style="arc", **self.kw))
            self.ids.append(self.parent.canvas.create_arc(x+w-2*r, y+h-2*r, x+w, y+h, start=270, extent=90, style="arc", **self.kw))
            self.ids.append(self.parent.canvas.create_arc(x+w-2*r, y,   x+w, y+2*r,   start=  0, extent=90, style="arc", **self.kw))
            self.ids.append(self.parent.canvas.create_arc(x,   y+h-2*r, x+2*r,   y+h, start=180, extent=90, style="arc", **self.kw))
            
            kw_temp = self.kw.copy()
            kw_temp['fill'] = kw_temp.pop('outline')
            self.ids.append(self.parent.canvas.create_line(x+r, y,   x+w-r, y    , **kw_temp))
            self.ids.append(self.parent.canvas.create_line(x+r, y+h, x+w-r, y+h  , **kw_temp))
            self.ids.append(self.parent.canvas.create_line(x,   y+r, x,     y+h-r, **kw_temp))
            self.ids.append(self.parent.canvas.create_line(x+w, y+r, x+w,   y+h-r, **kw_temp))

            self.postprocess_onclick()
        
        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                x, y, w, h, r = (self.arg['x'], self.arg['y'], self.arg['w'], self.arg['h'], self.arg['r'])
                r = min((w/2, h/2, r))
                points=(
                x+r, y+r, x+r, y, x+w-r, y, x+w-r, y+r, x+w, y+r, x+w, y+h-r,
                x+w-r, y+h-r, x+w-r, y+h ,x+r, y+h, x+r, y+h-r, x, y+h-r, x, y+r, 
                )
                self.parent.canvas.coords(self.ids[0], *points)
                self.parent.canvas.coords(self.ids[1], x,   y,   x+2*r,   y+2*r)
                self.parent.canvas.coords(self.ids[2], x+w-2*r, y+h-2*r, x+w, y+h)
                self.parent.canvas.coords(self.ids[3], x+w-2*r, y,   x+w, y+2*r)
                self.parent.canvas.coords(self.ids[4], x,   y+h-2*r, x+2*r,   y+h)

                self.parent.canvas.coords(self.ids[5], x,   y,   x+2*r,   y+2*r)
                self.parent.canvas.coords(self.ids[6], x+w-2*r, y+h-2*r, x+w, y+h)
                self.parent.canvas.coords(self.ids[7], x+w-2*r, y,   x+w, y+2*r)
                self.parent.canvas.coords(self.ids[8], x,   y+h-2*r, x+2*r,   y+h)

                self.parent.canvas.coords(self.ids[9], x+r, y,   x+w-r, y    )
                self.parent.canvas.coords(self.ids[10], x+r, y+h, x+w-r, y+h  )
                self.parent.canvas.coords(self.ids[11], x,   y+r, x,     y+h-r)
                self.parent.canvas.coords(self.ids[12], x+w, y+r, x+w,   y+h-r)

            if self.kw_current:
                kw_temp = self.kw.copy()
                if kw_temp['fill'] != '':
                    kw_temp['outline'] = kw_temp['fill']
                    kw_temp['state'] = 'normal'
                else:
                    kw_temp['state'] = 'hidden'
                for i in range(0, 5):
                    self.parent.canvas.itemconfigure(self.ids[i], **kw_temp)
                
                for i in range(5, 9):
                    self.parent.canvas.itemconfigure(self.ids[i], **self.kw)
                
                kw_temp = self.kw.copy()
                kw_temp['fill'] = kw_temp.pop('outline')
                for i in range(9, 13):
                    self.parent.canvas.itemconfigure(self.ids[i], **kw_temp)

            self.postprocess_onclick()

    def draw_round_rect(self, **kw):
        return GUI.CanvasRoundRect(self, **kw)

    def fill_round_rect(self, **kw):
        kw['fill'] = kw.get('fill', kw.get('color', 'black'))
        return GUI.CanvasRoundRect(self, **kw)


    class CanvasQRCode(CanvasImage):
        def __init__(self, parent, **kw):
            self.text = kw.pop('text', '')
            img = qrcode.make(self.text)
            img = img.resize(img.size)
            super().__init__(parent, image=img, **kw)
        
        def config(self, **kw):
            self.text = kw.pop('text', '')
            img = qrcode.make(self.text)
            img = img.resize(img.size)
            super().config(image=img, **kw)


    def draw_qr_code(self, **kw):
        return GUI.CanvasQRCode(self, **kw)


    class WidgetButton(CanvasBase):
        button : ttk.Button = None
        def preprocess(self, kw):
            self.preprocess_current(kw)
            if 'anchor' in self.kw_current:
                anchor = self.kw_current.pop('anchor')
                if 'anchor' not in self.arg_current:
                    self.arg_current['anchor'] = anchor
            self.preprocess_last()

        def __init__(self, parent, **kw):
            self.parent = parent
            
            self.preprocess_init(
                {'x':0, 'y':0, 'w':100, 'h':30, 'anchor':'nw'},
                {'origin':'anchor', 'onclick':'command'},
                {'style':'TButton', 'text':'button'},
                {})

            self.preprocess(kw)
            self.button = ttk.Button(self.parent.canvas, **self.kw)
            self.button.place(x=self.arg['x'], y=self.arg['y'], width=self.arg['w'], height=self.arg['h'], anchor=self.arg['anchor'])
        def remove(self):
            self.button.place_forget()
            self.button.destroy()
        def config(self, **kw):
            self.preprocess(kw)
            if self.arg_current:
                self.button.place(x=self.arg['x'], y=self.arg['y'], width=self.arg['w'], height=self.arg['h'], anchor=self.arg['anchor'])
            if self.kw_current:
                self.button.configure(**self.kw_current)

            
    def add_button(self, **kw):
        return GUI.WidgetButton(self, **kw)
    
    def start_loop(self, callback):
        def loop():
            try:
                while True:
                    callback()
            finally:
                pass
        loop_thread = Thread(target=loop)
        loop_thread.daemon = True
        loop_thread.start()
        return loop_thread
    
    def stop_loop(self, thread):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
        while thread.is_alive():
            time.sleep(0.01)


GUI.thd = None