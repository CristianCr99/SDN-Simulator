from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
miNombre = StringVar()
# Damos un titulo a la interfaz
root.title("Interface")

# Dejamos redimensionar la ventana (ancho, alto):
root.resizable(True,True)                   # Por defecto estan a True

# Ponemos una imagen de icono
root.iconbitmap('little_cat.ico')

# Damos un ancho y alto a nuestra ventana:
root.geometry('1280x720')

# Importante: Cuando este hecho el programa cambiar la extension .py por .pyw

miFrame = Frame(root)
miFrame.pack(fill='both', expand='True')      # De esta forma unimo el frame a la interfaz (y los parámetros que
                                                  # le pasamos permite que se redimensione a la vez que la interfaz)
miFrame.config(bg='white')

# Vamos a trabajar con label

# Texto (fijo):
#miLabel = Label(miFrame, text='Hola mundo', fg='blue', font=('Comic Sans MS',18))
#miLabel.place(x=100,y=200) # Ancho y alto (hacia abajo)

# Imagen:
imagen = PhotoImage(file='../gatito.png')
Label(miFrame,image=imagen).place(x=100, y=400)

# Wigets entry para introducir texto (to_do lo visto para los labels vale para los Entry):
cuadroTexto = Entry(miFrame, textvariable=miNombre) # Podemos poner que pertenezca a root o a miFrame (textvariable=miNombre asocia la variable a este cuadro)
cuadroTexto.grid(row=0,column=1, sticky='w', padx=5, pady=5) # Fila y columna son los parametros pra hubicarlo como si de una cuadrícula se tratara.
nombreLabel = Label(miFrame, text='Nombre:')
nombreLabel.grid(row=0,column=0, sticky='w', padx=5, pady=5) # w es la cordenada este, para situarlos [egados a la izquierda

contrasenia = Entry(miFrame)
contrasenia.grid(row=1,column=1, sticky='w', padx=5, pady=5)
contrasenia.config(show='*')
contrasenialabel = Label(miFrame, text='Contraseña:')
contrasenialabel.grid(row=1,column=0, sticky='w', padx=5, pady=5)

# Nota: el pading es el espacio de un wiets hacia los bordes del elemento en el que está implementado

# Vamos a trabajar con los Wigets botons y text:

comentarios = Label(miFrame, text='Comentarios:')
comentarios.grid(row=2,column=0, sticky='nw', padx=5, pady=5)
textoComentario = Text(miFrame, width=40, height=5)
textoComentario.grid(row=2,column=1, padx=5, pady=5)
# Creamos un scrollbar y le decimos que pertenece al text:

scrollVer = Scrollbar(miFrame, command=textoComentario.yview)
scrollVer.grid(row=2, column=2, sticky='nsew')
textoComentario.config(yscrollcommand=scrollVer.set) # esto es para que el scroll indique la posicion a medida que escribimos

# Botonoes:

def codigoBoton():
    print(miNombre.get())

boton = Button(root, text='Boton', command=codigoBoton)
boton.pack()

# Vamos a ver botones de radio:
varOpcion = IntVar()
def imprimir():
    if varOpcion.get()==1:
        eti.config(text='Has elegido Masculino')
    else:
        eti.config(text='Has elegido Femenino')

etiq = Label(root, text='Género:')
etiq.pack()
botonRadio = Radiobutton(root, text="Masculino", variable=varOpcion, command=imprimir, value=1)
botonRadio.pack()
botonRadio2 = Radiobutton(root, text="Femenino", variable=varOpcion, command=imprimir ,value=2)
botonRadio2.pack()

eti = Label(root)
eti.pack()

eti2 = Label(miFrame)
eti2.config(text='Elige Destinos')
eti2.grid(row=3,column=0, sticky='w', padx=5, pady=5)

playa = IntVar()
montania= IntVar()
tueismo= IntVar()

def opcionesViaje():
    opcionEscogida = ''
    if playa.get() == 1:
        opcionEscogida += 'playa'
    if montania.get() == 1:
        opcionEscogida += ' montania'
    if tueismo.get() == 1:
        opcionEscogida += ' turismo'
    textoFinal.config(text='Opcion escogida: ' + opcionEscogida)

textoFinal = Label(miFrame)
textoFinal.grid(row=6,column=1, sticky='w', padx=5, pady=5)

botonchek = Checkbutton(miFrame, text='Playa', variable= playa,onvalue=1, offvalue=0 ,command= opcionesViaje)
botonchek.grid(row=3,column=1, sticky='w', padx=5, pady=5)
botonchek2 = Checkbutton(miFrame, text='Montaña', variable=montania,onvalue=1, offvalue=0 ,command= opcionesViaje)
botonchek2.grid(row=4,column=1, sticky='w', padx=5, pady=5)
botonchek3 = Checkbutton(miFrame, text='Turismo', variable=tueismo,onvalue=1, offvalue=0 ,command= opcionesViaje)
botonchek3.grid(row=5,column=1, sticky='w', padx=5, pady=5)

# Crear un menu:

barraMenu = Menu(root)
root.config(menu=barraMenu)

Elemento1 = Menu(barraMenu, tearoff=0)
Elemento2 = Menu(barraMenu, tearoff=0)
Elemento3 = Menu(barraMenu, tearoff=0)
Elemento4 = Menu(barraMenu, tearoff=0)

barraMenu.add_cascade(label= 'Archivo', menu=Elemento1)
barraMenu.add_cascade(label= 'Preferencias', menu=Elemento2)
barraMenu.add_cascade(label= 'Configuracion', menu=Elemento3)
barraMenu.add_cascade(label= 'Guargar', menu=Elemento4)


# Ventanas emergentes:

def ventanaEmer():
    messagebox.showinfo('Informacion del programa', 'Esta ventana es solo informativa')
def avisoLicencia():
    messagebox.showwarning('Informacion de la licencia del programa', 'copyright (©)')
def avisoSalir():
    #valor = messagebox.askquestion('Salir', 'Desea salir de la aplicación?')
    valor = messagebox.askokcancel('Salir', 'Desea salir de la aplicación?')
    if valor==True:
        root.destroy()
    # Hay mas tipos de ventanas emer.

# Ventanas emergentes de archivos
def abreFichero():
    fichero = filedialog.askopenfilename(title='Abrir', initialdir='./', filetypes=(('Ficheros .txt', '*.txt'), (('Cualquier Fichero', '*.*'))))
    print(fichero)

#Button(miFrame, text='Abrir Fichero', command=abreFichero).grid(row=7,column=0, sticky='w', padx=5, pady=5)

# Asi se aniaden subapartados:
Elemento1.add_command(label='Nuevo')
Elemento1.add_command(label='Cargar', command=abreFichero)
Elemento1.add_command(label='Informacion', command=ventanaEmer)
Elemento1.add_command(label='Licencia', command=avisoLicencia)
Elemento1.add_separator()
Elemento1.add_command(label='Salir', command=avisoSalir)


root.mainloop()