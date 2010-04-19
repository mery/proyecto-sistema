#!/usr/bin/env python
import os, glob, random, itertools, gconf
import sys, time
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    print ''
    sys.exit(1)

COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2



class Principal:
	def __init__(self):
		self.BACKGROUND_DIRS = ['/home/alumno/cambio-imagenes/imagenes']
		###############################################
		self.current_directory = 'imagenes/'
		
		###############################################
		
		#BACKGROUND_DIRS = ['/home/alumno/imagenes']
		self.EXTENSIONS = ['jpeg', 'jpg', 'png', 'svg']
		self.files = list(itertools.chain(*[[os.path.join(dirpath, name)
		for name in filenames]
		for dirpath, dirnames, filenames in
		itertools.chain(*[os.walk(os.path.expanduser(d))
		for d in self.BACKGROUND_DIRS])]))
		
		self.gladefile="cambio.glade"
		appdir = os.getcwd()
		self.PrjPath = appdir
		self.arbol = gtk.glade.XML(os.path.join(os.path.join(appdir,'glade'),self.gladefile),"VentanaPrincipal")
		self.arbold=self.arbol.get_widget("VentanaPrincipal")
		
		##########################################
		self.scrolled = self.arbol.get_widget("scrolled")

		eventos={"on_cam_ale_clicked":self.on_cam_ale_clicked,
			"on_selec_img_clicked":self.on_selec_img_clicked,
			"on_usar_clicked":self.on_usar_clicked,
			"on_salir_clicked":self.on_salir_clicked,
			"on_cam_direc_clicked":self.on_cam_direc_clicked,
			"on_ini_auto_clicked":self.on_ini_auto_clicked,
			"on_VentanaPrincipal_destroy": gtk.main_quit
		}
		
		self.fileIcon = self.get_icon(gtk.STOCK_FILE)
		self.dirIcon = self.get_icon(gtk.STOCK_OPEN)
		self.store = self.create_store()
		self.fill_store()
		self.visor_archivos = gtk.IconView(self.store)
		self.visor_archivos.set_selection_mode(gtk.SELECTION_MULTIPLE)
		
		self.visor_archivos.set_selection_mode(gtk.SELECTION_MULTIPLE)
		self.visor_archivos.set_text_column(COL_PATH)
		self.visor_archivos.set_pixbuf_column(COL_PIXBUF)
		
		self.visor_archivos.set_text_column(COL_PATH)
		self.visor_archivos.set_pixbuf_column(COL_PIXBUF)
		self.visor_archivos.connect("item-activated", self.on_item_activated)
		self.scrolled.add(self.visor_archivos)
		self.visor_archivos.grab_focus()
		
		self.arbol.signal_autoconnect(eventos)
		self.arbold.show_all()
	def on_cam_ale_clicked(self,widget):
		
		gconf.client_get_default().set_string('/desktop/gnome/background/picture_filename', random.choice(self.files))
		#print files
		
	def on_selec_img_clicked(self,widget):
		FileChoose=FileDialog(self.PrjPath,"Seleccionar Archivos","Imagenes",["*.png","*.gif","*.jpg","*.svg"])
		Result,FileName=FileChoose.run()
		if Result==1:
			gconf.client_get_default().set_string('/desktop/gnome/background/picture_filename', FileName)
		else:
			print "falso"
		
	def on_usar_clicked(self,widget):
		print""
		
	def on_salir_clicked(self,widget):
		gtk.main_quit
	
	def on_cam_direc_clicked(self,widget):
		FileChoose=FileDialog(self.PrjPath,"Seleccionar Directorio","Carpetas",[""])
		Result,FileName=FileChoose.run()
		if Result==1:
			try:
				self.BACKGROUND_DIRS = [FileName]
				self.files = list(itertools.chain(*[[os.path.join(dirpath, name)
				for name in filenames]
				for dirpath, dirnames, filenames in
				itertools.chain(*[os.walk(os.path.expanduser(d))
				for d in self.BACKGROUND_DIRS])]))
				self.current_directory=FileName
				self.fill_store()
			except:
				pass
		
	def on_ini_auto_clicked(self,widget):
		for x in range(0,16):
			if x%5==0:
				gconf.client_get_default().set_string('/desktop/gnome/background/picture_filename', random.choice(self.files))
			time.sleep(1)
	
	def create_store(self):
		store = gtk.ListStore(str, gtk.gdk.Pixbuf, bool)
		store.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
		return store
            
    
	def fill_store(self):
		self.store.clear()
		if self.current_directory == None:
			return
		for fl in os.listdir(self.current_directory):
			if not fl[0] == '.':
				if os.path.isdir(os.path.join(self.current_directory, fl)):
					print""
					#self.store.append([fl, self.dirIcon, True])
				else:
					self.store.append([fl, self.fileIcon, False])
					
	def get_icon(self, name):
		theme = gtk.icon_theme_get_default()
		return theme.load_icon(name, 48, 0)
	
	def on_item_activated(self, widget, item):
		print ""
		model = widget.get_model()
		path = model[item][COL_PATH]
		print path
		print self.BACKGROUND_DIRS[0] 
		gconf.client_get_default().set_string('/desktop/gnome/background/picture_filename',(str(self.BACKGROUND_DIRS[0])+'/'+path) )

class FileDialog:

    def __init__(self, currentpath='.',title='FileManager',name="aaaaaaa",pattern=["*.*"]):
		self.gladefile = "cambio.glade"
		self.CurPath=currentpath
		self.title = title
		self.filter = gtk.FileFilter()
		self.filter.set_name(name)
		for elem in pattern:
			self.filter.add_pattern(elem)
		
    def run(self):
		"""Esta funcion hace que podamos ver el dialogo"""	
        #cargamos el dialogo desde el archivo glade
		appdir = os.getcwd()
		self.arbol2 = gtk.glade.XML(os.path.join(os.path.join(appdir,'glade'),self.gladefile), "selectorimagen")
		#Obtenemos el directorio actual del widget
		self.dlg = self.arbol2.get_widget("selectorimagen")
		self.dlg.set_default_response(gtk.RESPONSE_OK)
		self.dlg.add_filter(self.filter)
		self.dlg.set_current_folder(self.CurPath)
		self.Result = self.dlg.run()
		filename_sel = self.dlg.get_filename()
		self.Filename=filename_sel
		self.dlg.destroy()
		return self.Result,self.Filename
if __name__ == "__main__":
	princi = Principal()
	gtk.main()
