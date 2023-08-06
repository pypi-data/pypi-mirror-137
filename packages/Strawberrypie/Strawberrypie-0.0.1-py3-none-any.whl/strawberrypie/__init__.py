import tkinter as tk
from tkinter import ttk 
from PIL import Image , ImageTk


class Pie:
	def __init__(self, master,bar,title="PIE",geo='600x600',headless=True,bg="#000",exit_key = "e",fg="#fff"):
		self.master = master
		self.bar = bar
		master.title(title)
		master['bg'] = bg
		master.overrideredirect(headless)
		master.geometry(geo)
		self.bg = bg
		self.fg = fg
		if headless :
			master.bind('<Button-1>', self.set_position)
			self.master.bind(f'<{exit_key}>',lambda x :self.master.destroy())
		
	def set_position(self,event): 
	        xwin = self.bar.winfo_x()
	        ywin = self.bar.winfo_y()
	        startx = event.x_root
	        starty = event.y_root
	        ywin = ywin - starty
	        xwin = xwin - startx
	        def drag(event): 
	            self.master.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')    

	        self.bar.bind('<B1-Motion>', drag)

	def statbar(self,full = False):
		window_handel = tk.Frame(self.master, bg ='red',relief= 'flat')
		window_handel.place(relx = 0.935 , rely =0 , relheight=0.042 , relwidth= 0.065)
		closebtn = Btn(window_handel , text = "X", bg = "#8f0621" , fg = "black",command = lambda : self.master.destroy())
		closebtn.place(relx = 0 , rely =0 , relheight=1 , relwidth= 1)
		color_ch({"enter":"#f7365d","leave":"#8f0621","actbg" :"#f7365d",'actfg' :'#fff'},closebtn)
		if full == False :
			window_handel.place(relx = 0.78 , rely =0 , relheight=0.05 , relwidth= 0.22)
			closebtn.place(relx = 0.66 , rely =0 , relheight=1 , relwidth= 0.35)
			minibtn = Btn(window_handel , text = "-", bg = self.bg , fg = self.fg,command = self.end_fullscreen)
			minibtn.place(relx = 0 , rely =0 , relheight=1 , relwidth= 0.33)		
			scalebtn = Btn(window_handel , text = "S",  bg = self.bg , fg = self.fg,command = self.toggle_fullscreen)
			scalebtn.place(relx = 0.33 , rely =0 , relheight=1 , relwidth= 0.33)
        
	def toggle_fullscreen(self,event=None):
		self.master.overrideredirect(False)
		self.master.attributes("-fullscreen", True)
		return "break"
		
	def end_fullscreen(self,event=None):
		self.master.attributes("-fullscreen", False)
		self.master.overrideredirect(True)
		return "break"

def simg(image):

	return ImageTk.PhotoImage(Image.open(image))

def color_ch(colors,element):
	
	element.bind('<Enter>' , lambda e : element.config(bg = colors['enter']))
	element.bind('<Leave>' , lambda e : element.config(bg = colors['leave']))
	element.config(activebackground = colors['actbg'])
	element.config(activeforeground = colors["actfg"])

class Tfield(ttk.Entry):
	
	defaults = dict(font=["Futura" ,14],width = 25)
	def __init__(self, *args, **kwargs):
		kwargs = dict(self.defaults, **kwargs)
		super().__init__(*args, **kwargs)
		self.pop = tk.Menu(self ,tearoff =0 )
		self.pop.add_command(label = "Cut		", command = self.Cut)
		self.pop.add_command(label = "Copy		", command = self.Copy)
		self.pop.add_command(label = "Paste		", command = self.Paste)
		self.bind('<Button-3>' , self.pop2)

	def pop2(self, e):
		try:
			self.pop.tk_popup(e.x_root , e.y_root , 0)
		finally :
			self.pop.grab_release()
	def Copy(self):
		self.event_generate("<<Copy>>")
	def Paste(self):
		self.event_generate("<<Paste>>")
	def Cut(self):
		self.event_generate("<<Cut>>")

class Tline(tk.Label):
  
    defaults = dict(font=["Futura" ,14 ],relief ="flat",
                    fg="#fff", bg="#000")

    def __init__(self, *args, **kwargs):
        kwargs = dict(self.defaults, **kwargs)
        super().__init__(*args, **kwargs)

class Btn(tk.Button):
    
    defaults = dict(font=["Futura" ,14  ],relief ="flat",height = 2 ,width = 10,
                    fg="#000", bg="#fff",activebackground="#fff",activeforeground="#000" 
					,bd=0)

    def __init__(self, *args, **kwargs):
        kwargs = dict(self.defaults, **kwargs)
        super().__init__(*args, **kwargs)


def Center_root(master , geometry ='600x600'):
	width ,height = geometry.split("x")
	screen_w,screen_h = master.winfo_screenwidth() ,master.winfo_screenheight()
	x_coordinate , y_coordinate = (screen_w/2) - (int(width)/2) ,(screen_h/2) - (int(height)/2)
	master.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")

class intro:
	"""this should be used at the start of the of programe"""
	def __init__(self,img,text="Just a moment", font = ("calibri", 17) , done = 10 ,geo =(350 ,350)):
		root = tk.Tk()
		pie(root,bar = root)
		Center_root(root ,geo)
		bgimg = simg(img)
		mother = tk.Label(root ,text =text ,
			fg = "white", image = bgimg ,compound='center' ,font = font)
		mother.pack(fill = tk.BOTH , expand = True)
		root.after(done * 1000,root.destroy)
		root.mainloop()
 