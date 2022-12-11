from tkinter import *
import json
from tkinter import messagebox as MessageBox
from copy import copy
import time


#CREACION DE LA INTERFAZ PRINCIPAL
inicio = Tk()
inicio.config(bg="black")
inicio.title("Inicio de sesión")
inicio.resizable(False, False)
#inicio.geometry("1920x1080")
fondoMontaña = PhotoImage( file = "Proyecto.png")
canvas = Canvas(inicio, width = 1366, height = 768)
canvas.create_image(0,0, image = fondoMontaña, anchor = "nw")
canvas.config(bg = "#C8C0BF")
canvas.pack()

#DEFINICION DE LA CALSE ARISTA CON SU CONSTRUCTOR
class Carretera():

    def __init__(self, origen, destino, peso, coordenadas):
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.coordenadas = coordenadas
        self.estado = False
        self.herramientas = []

    def obtenerOrigen(self):
        return self.origen

    def obtenerDestino(self):
        return self.destino

    def obtenerPeso(self):
        return self.peso

    def obtenerCoordenadas(self):
        return self.coordenadas

    def ponerOrigen(self, origen):
        self.origen = origen

    def ponerDestino(self, destino):
        self.destino = destino

    def ponerPeso(self, peso):
        self.peso = peso

    def obtenerBloqueado(self):
        return self.estado

    def ponerBloqueado(self, valor):
        self.estado = valor

class Cueva():

    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.listaAdyacentes = []
        self.salientes = 0
        self.entrantes = 0

    def ponerSalientes(self, salientes):
        self.salientes = salientes

    def ponerEntrantes(self, entrantes):
        self.entrantes = entrantes

    def obtenerSalientes(self):
        return self.salientes

    def obtenerEntrantes(self):
        return self.entrantes

    def obtenerNombre(self):
        return self.nombre

    def ponerNombre(self, nombre):
        self.nombre = nombre

    def obtenerListaAdyacentes(self):
        return self.listaAdyacentes

    def ponerListaAdyacentes(self, ListaAdyacentes):
        self.ListaAdyacentes = ListaAdyacentes

    def obtenerX(self):
        return self.x

    def obtenerY(self):
        return self.y


class Grafo():

    def __init__(self):
        self.listaCuevas = []
        self.listaCarreteras = []
        self.listaVisitados = []
        self.coordenadasLista = []

    def ingresarCueva(self, dato, x, y):
        if self.verificarCueva(dato) == None:
            self.listaCuevas.append(Cueva(dato, x, y))

    def obtenerListaCuevas(self):
        return self.listaCuevas

    def obtenerListaCarreteras(self):
        return self.listaCarreteras

    def verificarCueva(self, nombre):
        for cueva in self.listaCuevas:
            if cueva.obtenerNombre() == nombre:
                return cueva
        return None

    def ingresarCarretera(self, origen, destino, peso, coordenadas):
        if self.verificarCarretera(origen, destino) == None:
            if self.verificarCarretera(origen) != None and self.verificarCueva(destino) != None:
                self.listaCarreteras.append(Carretera(origen, destino, peso, coordenadas))

    def añadirCarretera(self, origen, destino, peso, coordenadas):
        self.listaCarreteras.append(Carretera(origen, destino, peso, coordenadas))

    def verificarCarretera(self, origen, destino):
        for carretera in self.listaCarreteras:
            if carretera.obtenerOrigen() == origen and carretera.obtenerDestino() == destino:
                return carretera
        return None

    def coordenadas(self, datos):
        self.coordenadasLista.append(datos)

grafo = Grafo()
datos_json = open("montana2.json")
datos = json.load(datos_json)
global diccionarioCuevas
diccionarioCuevas = {}
global diccionarioDestinos
diccionarioDestinos = {}
diccionarioPesos = {}

for cueva in datos.get("montana"):
    grafo.ingresarCueva(cueva.get("nombre"), cueva.get("x"), cueva.get("y"))
    grafo.coordenadas([cueva.get("x"),cueva.get("y")])
    diccionarioCuevas[cueva.get("nombre")] = [cueva.get("x"), cueva.get("y")]
    diccionarioDestinos[cueva.get("nombre")] = []
    diccionarioPesos[cueva.get("nombre")] = []
    for carretera in cueva.get("aristas"):
        grafo.añadirCarretera(cueva.get("nombre"),carretera.get("nombreD"),carretera.get("costo"),
                                  carretera.get("coordenadasD"))
        diccionarioDestinos[cueva.get("nombre")].append(carretera.get("nombreD"))
        diccionarioPesos[cueva.get("nombre")].append(carretera.get("costo"))
cuevaImagen = PhotoImage(file = ("Webp.net-resizeimage.png"))



def Canvas():
    cuevas = grafo.obtenerListaCuevas()
    for cueva in cuevas:
        x = cueva.obtenerX()
        y = cueva.obtenerY()
        botonCueva = Button(image = cuevaImagen, width = 50, height = 50, bg = "lightgray", bd = 0, borderwidth = 0)
        botonCueva.place(x = x, y = y, anchor = "center")
        nombreCueva = cueva.obtenerNombre()
        nombre = Label(text = nombreCueva, bg = "#B47637")
        nombre.place(x = x, y = y, anchor = "s")

print (diccionarioCuevas)
print(diccionarioDestinos)
print(diccionarioPesos)

def cuevaNueva():
    ventana = Toplevel(width=700, height=320, bg="#F9F2E2")
    ventana.title("Viajes")
    ventana.resizable(False, False)

    nombreCuevaLabel = Label(ventana, text="Nombre de la cueva:", font=("normal", 15, "bold"), fg="#D4AF37",
                         bg="#1D1F27")
    nombreCuevaLabel.place(x=20, y=20)

    XLabel = Label(ventana, text="Posición en X:", font=("normal", 15, "bold"), fg="#D4AF37",
                             bg="#1D1F27")
    XLabel.place(x=20, y=70)

    YLabel = Label(ventana, text="Posición en Y:", font=("normal", 15, "bold"), fg="#D4AF37",
                   bg="#1D1F27")
    YLabel.place(x=20, y=120)

    conexionLabel = Label(ventana, text="Conectar con:", font=("normal", 15, "bold"), fg="#D4AF37",
                   bg="#1D1F27")
    conexionLabel.place(x=20, y=170)

    pesoLabel = Label(ventana, text="Peso de esa conexión:", font=("normal", 15, "bold"), fg="#D4AF37",
                          bg="#1D1F27")
    pesoLabel.place(x=20, y=220)

    nombreEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    nombreEntry.place(x=420, y=20)

    XEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    XEntry.place(x=420, y=70)

    YEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    YEntry.place(x=420, y=120)

    conexionEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    conexionEntry.place(x=420, y=170)

    pesoEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    pesoEntry.place(x=420, y=220)

    def ok():
        grafo.ingresarCueva(str(nombreEntry.get()), int(XEntry.get()), int(YEntry.get()))
        grafo.coordenadas([int(XEntry.get()), int(YEntry.get())])
        grafo.añadirCarretera(str(nombreEntry.get()), str(conexionEntry.get()), int(pesoEntry.get()), diccionarioCuevas[str(conexionEntry.get())])
        diccionarioCuevas[str(nombreEntry.get())] = [int(XEntry.get()), int(YEntry.get())]
        diccionarioDestinos[str(nombreEntry.get())] = [str(conexionEntry.get())]
        diccionarioPesos[str(nombreEntry.get())] = [pesoEntry.get()]
        Canvas()
        CanvasLinea()
        CanvasId()
        actualizarListaAdyacentes()
        actualizarDiccionarios()
        ventana.destroy()

    boton_ok = Button(ventana, text="OK", font=("normal", 12, "bold"), fg="#D4AF37",
                              bg="#1D1F27", command=ok)
    boton_ok.place(x=350, y=270, anchor = "c")

def CanvasLinea():
    actualizarListaAdyacentes()
    for i in grafo.listaCuevas:
        xOrigen = i.x
        yOrigen = i.y
        for k in i.listaAdyacentes:
            destino = k.destino
            for j in grafo.listaCuevas:
                if j.nombre == destino:
                    xDestino = j.x
                    yDestino = j.y
            if k.obtenerBloqueado() == False:
                canvas.create_line(xOrigen, yOrigen, xDestino, yDestino, width=14, fill="#1D1F27")
            elif k.obtenerBloqueado() == True:
                canvas.create_line(xOrigen, yOrigen, xDestino, yDestino, width=14, fill="red")
    # for i in diccionarioDestinos.items():
    #     nombre = i[0]
    #     origen = diccionarioCuevas[nombre]
    #     xOrigen = origen[0]
    #     yOrigen = origen[1]
    #     for k in diccionarioDestinos[nombre]:
    #         xDestino = diccionarioCuevas[k][0]
    #         yDestino = diccionarioCuevas[k][1]
    #         canvas.create_line(xOrigen, yOrigen, xDestino, yDestino, width=14, fill="#1D1F27")

def CanvasId():
    actualizarListaAdyacentes()
    actualizarDiccionarios()
    for i in diccionarioDestinos:
        peso = 0
        xOrigen = diccionarioCuevas[i][0]
        yOrigen = diccionarioCuevas[i][1]
        for j in diccionarioDestinos[i]:
            destino = diccionarioCuevas[j]
            xDestino = destino[0]
            yDestino = destino[1]
            canvas.create_text((xOrigen + xDestino) / 2, (yOrigen + yDestino) / 2, text=diccionarioPesos[i][peso],
                               fill="#D4AF37", font=("normal", 12, "bold"))
            peso = peso + 1

def esPozo():
    listaPozos = []
    for i in diccionarioDestinos:
        if diccionarioDestinos[i] == []:
            listaPozos.append(i)
            print(i)
    if len(listaPozos) > 0:
        MessageBox.showinfo("Pozos", "Las cuevas de " + str(listaPozos) + " son pozos")
    else:
        MessageBox.showinfo("Pozos", "No se han encontrado pozos")

def gradoVertices():
    actualizarListaAdyacentes()
    actualizarDiccionarios()
    entrantes = 0
    salientes = 0
    diccionarioGrados = {}
    for i in diccionarioDestinos:
        salientes = len(diccionarioDestinos[i])

        for k in diccionarioDestinos.values():
            for j in k:
                if j == i:
                    entrantes = entrantes + 1

        diccionarioGrados[i] = []
        diccionarioGrados[i].append(salientes)
        diccionarioGrados[i].append(entrantes)

        print("De la cueva", i, "salen ", salientes, "y entran ", entrantes, "vertices" )
        entrantes = 0
    print(diccionarioGrados)
    ventana = Toplevel(width=800, height=320, bg="darkgray")
    ventana.title("Viajes")
    ventana.resizable(False, False)

    texto = Text(ventana)
    texto.pack()
    texto.config(width=40, height=30, font=("Normal", 12),
                 padx=15, pady=15)
    texto.insert(END, "Nombre, grado saliente, grado entrante")
    texto.insert(END, "\n")
    for i in diccionarioGrados:
        texto.insert(END, i)
        texto.insert(END, ", ")
        texto.insert(END, diccionarioGrados[i][0])
        texto.insert(END, ", ")
        texto.insert(END, diccionarioGrados[i][1])
        texto.insert(END, "\n")
    return diccionarioGrados

def bloquear():
    ventana = Toplevel(width=700, height=320, bg="#F9F2E2")
    ventana.title("Bloquear o desbloquear")
    ventana.resizable(False, False)

    nombreOrigen = Label(ventana, text="Origen de la arista", font=("normal", 15, "bold"), fg="#D4AF37",
                             bg="#1D1F27")
    nombreOrigen.place(x=20, y=20)

    nombreDestino = Label(ventana, text="Destino de la arista", font=("normal", 15, "bold"), fg="#D4AF37",
                   bg="#1D1F27")
    nombreDestino.place(x=20, y=70)

    origenEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    origenEntry.place(x=420, y=20)

    destinoEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    destinoEntry.place(x=420, y=70)

    def bloquear():
        origen = origenEntry.get()
        destino = destinoEntry.get()

        for i in grafo.listaCarreteras:
            if i.obtenerOrigen() == origen:
                if i.obtenerDestino() == destino:
                    i.ponerBloqueado(True)
                    print("La arista que empieza en", i.obtenerOrigen(), "y termina en ", i.obtenerDestino(), "esta: ", i.obtenerBloqueado(), "costo: ", i.obtenerPeso())
                    actualizarListaAdyacentes()

    def desbloquear():
        origen = origenEntry.get()
        destino = destinoEntry.get()

        for i in grafo.listaCarreteras:
            if i.obtenerOrigen() == origen:
                if i.obtenerDestino() == destino:
                    i.ponerBloqueado(False)
                    print("La arista que empieza en", i.obtenerOrigen(), "y termina en ", i.obtenerDestino(), "esta: ", i.obtenerBloqueado(), "costo: ", i.obtenerPeso())
                    actualizarListaAdyacentes()

    botonBloquear = Button(ventana, text = "BLOQUEAR", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=bloquear)
    botonBloquear.place(x = 20, y = 120)

    botonDesbloquear = Button(ventana, text="DESBLOQUEAR", font=("normal", 12, "bold"), fg="#D4AF37",
                                bg = "#1D1F27", command = desbloquear)
    botonDesbloquear.place(x = 420, y = 120)

def actualizarListaAdyacentes():

    for cueva in grafo.listaCuevas:
        cueva.listaAdyacentes = []
        for carretera in grafo.listaCarreteras:
            if cueva.obtenerNombre() == carretera.obtenerOrigen():
                cueva.listaAdyacentes.append(carretera)
    # for cueva in grafo.listaCuevas:
    #     for i in cueva.obtenerListaAdyacentes():
    #         print("---------------------------------------------------")
    #         print(cueva.obtenerNombre())
    #         print(i.obtenerOrigen(), i.obtenerDestino(), i.obtenerPeso())
    #         print("---------------------------------------------------")

def invertir():
    ventana = Toplevel(width=700, height=320, bg="#F9F2E2")
    ventana.title("Bloquear o desbloquear")
    ventana.resizable(False, False)

    nombreOrigen = Label(ventana, text="Origen de la arista", font=("normal", 15, "bold"), fg="#D4AF37",
                         bg="#1D1F27")
    nombreOrigen.place(x=20, y=20)

    nombreDestino = Label(ventana, text="Destino de la arista", font=("normal", 15, "bold"), fg="#D4AF37",
                          bg="#1D1F27")
    nombreDestino.place(x=20, y=70)

    origenEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    origenEntry.place(x=420, y=20)

    destinoEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    destinoEntry.place(x=420, y=70)

    def procesar():
        origen = origenEntry.get()
        destino = destinoEntry.get()

        for i in grafo.listaCarreteras:
            if i.obtenerOrigen() == origen:
                if i.obtenerDestino() == destino:
                    i.destino = origen
                    i.origen = destino

        actualizarListaAdyacentes()
        actualizarDiccionarios()
        ventana.destroy()
        for cueva in grafo.listaCuevas:
            for k in cueva.obtenerListaAdyacentes():
                if k.obtenerOrigen() == origen:
                    if k.obtenerDestino() == destino:
                        k.destino = origen
                        k.origen = destino
            for cueva in grafo.listaCuevas:
                for k in cueva.obtenerListaAdyacentes():
                    print(k.obtenerOrigen(), k.obtenerDestino(), k.obtenerPeso())

    botonConfirmar = Button(ventana, text="INVERTIR", font=("normal", 12, "bold"), fg="#D4AF37",
                               bg="#1D1F27", command=procesar)
    botonConfirmar.place(x=20, y=120)

# for cueva in grafo.listaCuevas:
#     for i in cueva.obtenerListaAdyacentes():
#          print(cueva.obtenerNombre())
#          print(i.obtenerOrigen(), i.obtenerDestino(), i.obtenerPeso())
#          print("---------------------------------------------------")
#-----------------------------------------------------PROFUNIDAD-------------------------------------------------------
def invocarProfundidad():
    ventana = Toplevel(width=700, height=320, bg="darkgray")
    ventana.title("Recorrido en profundidad")
    ventana.resizable(False, False)

    nombreOrigen = Label(ventana, text="Origen de la arista", font=("normal", 15, "bold"), fg="#D4AF37",
                         bg="#1D1F27")
    nombreOrigen.place(x=20, y=20)

    origenEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    origenEntry.place(x=420, y=20)

    def empezar():

        origenProfundidad = origenEntry.get()
        recorridoProfundidad(origenProfundidad)
        ventana.destroy()

    botonConfirmar = Button(ventana, text="EMPEZAR", font=("normal", 12, "bold"), fg="#D4AF37",
                            bg="#1D1F27", command=empezar)
    botonConfirmar.place(x=20, y=120)


def recorridoProfundidad(origen):
    actualizarListaAdyacentes()
    for cueva in grafo.listaCuevas:
        if cueva.obtenerNombre() == origen and origen not in grafo.listaVisitados:
            grafo.listaVisitados.append(origen)
            proximo = cueva.obtenerListaAdyacentes()
            for k in proximo:
                if k.obtenerBloqueado() == False:
                    recorridoProfundidad(k.obtenerDestino())
    print(grafo.listaVisitados)
    return grafo.listaVisitados


#-----------------------------------------------------------------------------------------------------------------------

def invocarAnchura():
    ventana = Toplevel(width=700, height=320, bg="darkgray")
    ventana.title("Recorrido en anchura")
    ventana.resizable(False, False)

    nombreOrigen = Label(ventana, text="Origen de la arista", font=("normal", 15, "bold"), fg="#D4AF37",
                         bg="#1D1F27")
    nombreOrigen.place(x=20, y=20)

    origenEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    origenEntry.place(x=420, y=20)

    def empezar():

        origenAnchura = origenEntry.get()
        recorridoAnchura(origenAnchura)
        ventana.destroy()

    botonConfirmar = Button(ventana, text="EMPEZAR", font=("normal", 12, "bold"), fg="#D4AF37",
                            bg="#1D1F27", command=empezar)
    botonConfirmar.place(x=20, y=120)

def recorridoAnchura(dato):
    actualizarListaAdyacentes()
    print(dato)
    visitados = []
    pila = []
    imprimir = []
    vertices = []
    arista = []
    pila.append(dato)
    visitados.append(dato)

    for vertice in grafo.listaCuevas:
        vertices.append(vertice.obtenerNombre())

    if dato in vertices:
        while pila:
            x = pila[-1]
            imprimir.append(x)
            pila.remove(pila[-1])

            vertice = traerVertice(x)
            for key in vertice.obtenerListaAdyacentes():
                for a in grafo.listaCuevas:
                    if a.obtenerNombre() == key.obtenerDestino():
                        if a.obtenerNombre() not in visitados:
                            visitados.append(a.obtenerNombre())
                            pila.append(a.obtenerNombre())
                            arista.append(key)

        print("Recorrido en Anchura")
        print("Visitados:", visitados)
    else:
        print("No existe")
    global graficoAnchura
    graficoAnchura = visitados
    inaccesibles = []
    todos = []
    for i in grafo.listaCuevas:
        todos.append(i.obtenerNombre())

    for k in todos:
        if k not in visitados:
            inaccesibles.append(k)
    print(inaccesibles)
    if len(inaccesibles) >= 1:
        MessageBox.showerror("INCREIBLE MI PANA", "No se puede acceder a los nodos " + str(inaccesibles))
    return arista

#---------------------------------------------------------------------------------------------------------------------
def llamarDijkstra():
    ventana = Toplevel(width=700, height=320, bg="#F9F2E2")
    ventana.title("Recorrido Dijkstra")
    ventana.resizable(False, False)

    nombreOrigen = Label(ventana, text="Cueva origen", font=("normal", 15, "bold"), fg="#D4AF37",
                         bg="#1D1F27")
    nombreOrigen.place(x=20, y=20)

    nombreDestino = Label(ventana, text="Cueva destino", font=("normal", 15, "bold"), fg="#D4AF37",
                          bg="#1D1F27")
    nombreDestino.place(x=20, y=70)

    origenEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    origenEntry.place(x=420, y=20)

    destinoEntry = Entry(ventana, width=17, fg="black", font=("normal", 15, "bold"), relief="flat")
    destinoEntry.place(x=420, y=70)

    def caminoMasCorto():
        origen = origenEntry.get()
        destino = destinoEntry.get()
        VerticesAux = []
        VerticesD = []
        caminos = dijkstra(origen, VerticesAux)
        cont = 0
        for i in caminos:
            print("La distancia mínima a: " + grafo.listaCuevas[cont].nombre + " es " + str(i))
            cont = cont + 1

        rutas(VerticesD, VerticesAux, destino, origen)
        print("El camino más corto de: " + origen + " a " + destino + " es: ")
        print(VerticesD)
        ventana.destroy()
        global caminoDijkstra
        caminoDijkstra = VerticesD
        return VerticesD


    botonConfirmar = Button(ventana, text="EMPEZAR", font=("normal", 12, "bold"), fg="#D4AF37",
                            bg="#1D1F27", command=caminoMasCorto)
    botonConfirmar.place(x=20, y=120)



def rutas(VerticesD, VerticesAux, destino, origen):
    verticeDestino = traerVertice(destino)
    indice = grafo.listaCuevas.index(verticeDestino)
    if VerticesAux[indice] is None:
        print("No hay camino entre: ", (origen, destino))
        MessageBox.showerror("ERROR CAMARADA", "No hay camino entre" + origen + "y " + destino)
        return
    aux = destino
    while aux != origen:
        verticeDestino = traerVertice(aux)
        indice = grafo.listaCuevas.index(verticeDestino)
        VerticesD.insert(0, aux)
        aux = VerticesAux[indice]
    VerticesD.insert(0, aux)


def dijkstra(origen, VerticesAux):
    actualizarListaAdyacentes()
    marcados = []  # la lista de los que ya hemos visitado
    caminos = []  # la lista final
    # iniciar los valores en infinito
    for v in grafo.listaCuevas:
        caminos.append(float("inf"))
        marcados.append(False)
        VerticesAux.append(None)    #se añade un None a VerticesAux
        if v.obtenerNombre() == origen:
            caminos[grafo.listaCuevas.index(v)] = 0
            VerticesAux[grafo.listaCuevas.index(v)] = v.obtenerNombre()
    while not todosMarcados(marcados):
        aux = menorNoMarcado(caminos, marcados)  # obtuve el menor no marcado
        if aux is None:
            break
        indice = grafo.listaCuevas.index(aux)  # indice del menor no marcado
        marcados[indice] = True  # marco como visitado
        valorActual = caminos[indice]
        for vAdya in aux.obtenerListaAdyacentes():
            indiceNuevo = grafo.listaCuevas.index(traerVertice(vAdya.obtenerDestino()))
            arista = verificararista(aux.obtenerNombre(), vAdya.obtenerDestino())
            if arista != None:
                if caminos[indiceNuevo] > valorActual + arista.obtenerPeso():
                    caminos[indiceNuevo] = valorActual + arista.obtenerPeso()
                    VerticesAux[indiceNuevo] = grafo.listaCuevas[indice].obtenerNombre()

    return caminos

def menorNoMarcado(caminos, marcados):
    verticeMenor = None
    caminosAux = sorted(caminos)
    copiacaminos = copy(caminos)
    bandera = True
    contador = 0
    while bandera:
        menor = caminosAux[contador]
        if marcados[copiacaminos.index(menor)] == False:
            verticeMenor = grafo.listaCuevas[copiacaminos.index(menor)]
            bandera = False
        else:
            copiacaminos[copiacaminos.index(menor)] = "x"
            contador = contador + 1
    return verticeMenor

def todosMarcados(marcados):
    for j in marcados:
        if j is False:
            return False
    return True


def verificararista(a, b):
    for arista in grafo.listaCarreteras:
        if arista.obtenerBloqueado() == False:
            if arista.obtenerOrigen() == a and arista.obtenerDestino() == b:
                return arista
    return None

def traerVertice(dato):
    for vertice in grafo.listaCuevas:
        if vertice.obtenerNombre() == dato:
            return vertice
    return None

#----------------------------------------------------------------------------------------------------------------------

def actualizarDiccionarios():
    for cueva in grafo.listaCuevas:
        diccionarioCuevas[cueva.obtenerNombre()] = []
        diccionarioDestinos[cueva.obtenerNombre()] = []
        diccionarioPesos[cueva.obtenerNombre()] = []
        diccionarioCuevas[cueva.obtenerNombre()].append(cueva.x)
        diccionarioCuevas[cueva.obtenerNombre()].append(cueva.y)
        for arista in cueva.listaAdyacentes:
            diccionarioDestinos[cueva.obtenerNombre()].append(arista.obtenerDestino())
            diccionarioPesos[cueva.obtenerNombre()].append(arista.obtenerPeso())

    print(diccionarioDestinos)

def fuertementeConexo():
    actualizarListaAdyacentes()
    actualizarDiccionarios()
    entrantes = 0
    salientes = 0
    diccionarioGrados = {}
    for i in diccionarioDestinos:
        salientes = len(diccionarioDestinos[i])

        for k in diccionarioDestinos.values():
            for j in k:
                if j == i:
                    entrantes = entrantes + 1

        diccionarioGrados[i] = []
        diccionarioGrados[i].append(salientes)
        diccionarioGrados[i].append(entrantes)
        entrantes = 0
    resultado = 0
    print(diccionarioGrados)
    for i in diccionarioGrados.values():
        if i[0] == 0 or i[1] == 0:
            resultado = 1
        else:
            resultado = 2

    if resultado == 1:
        MessageBox.showerror("NEGATIVO PAISANO", "El grafo no es fuertemente conexo")
    else:
        MessageBox.showinfo("POSITIVO PAI", "El grafo es fuertemente conexo")

def listaRecorrerProfundidad():
    lista = grafo.listaVisitados
    if len(lista) < 1:
        MessageBox.showerror("MUY MAL BRO", "Primero se debe hacer un recorrido en profundidad")
    print(lista)
    contador = 0
    for i in lista:
        origen = i
        destino = lista[contador + 1]
        for j in grafo.listaCuevas:
            if j.nombre == origen:
                xOrigen = j.x
                yOrigen = j.y
            if j.nombre == destino:
                xDestino = j.x
                yDestino = j.y
        print(i)
        canvas.create_line(xOrigen, yOrigen, xDestino, yDestino, width=14, fill="red")
        canvas.create_oval(xOrigen, yOrigen, xOrigen+50, yOrigen+50, fill="red")
        canvas.update()
        time.sleep(2.00)
        contador = contador + 1

    grafo.listaVisitados = []

def listaRecorrerAnchura():

    if len(graficoAnchura) < 1:
        MessageBox.showerror("MUY MAL BRO", "Primero se debe hacer un recorrido en anchura")

    contador = 0
    for i in graficoAnchura:
        origen = i
        for j in grafo.listaCuevas:
            if j.nombre == origen:
                xOrigen = j.x
                yOrigen = j.y

        print(i)
        canvas.create_oval(xOrigen-50, yOrigen-50, xOrigen+50, yOrigen+50, fill="gold")
        canvas.update()
        time.sleep(2.00)
        contador = contador + 1

def listaRecorrerDijkstra():
    if len(caminoDijkstra) < 1:
        MessageBox.showerror("MUY MAL BRO", "Primero se debe hacer un recorrido de Dijkstra")
    print(caminoDijkstra)
    contador = 0
    for i in caminoDijkstra:
        origen = i
        destino = caminoDijkstra[contador + 1]
        for j in grafo.listaCuevas:
            if j.nombre == origen:
                xOrigen = j.x
                yOrigen = j.y
            if j.nombre == destino:
                xDestino = j.x
                yDestino = j.y
        print(i)
        canvas.create_line(xOrigen, yOrigen, xDestino, yDestino, width=14, fill="red")
        canvas.update()
        time.sleep(2.00)
        contador = contador + 1

    grafo.listaVisitados = []

def cargar():
    canvas.delete("all")
    canvas.update()
    Canvas()
    CanvasLinea()
    CanvasId()

    canvas.update()

botonGraficar = Button(canvas, text = "GRAFICAR / REFRESCAR", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=cargar)
botonGraficar.place(x = 50, y = 50)

botonCrear = Button(canvas, text="CREAR UNA CUEVA", font=("normal", 12, "bold"), fg="#D4AF37", bg="#1D1F27",
                    command = cuevaNueva)
botonCrear.place(x=50, y=100)

botonPozos = Button(canvas, text = "AVERIGUAR POZOS", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=esPozo)
botonPozos.place(x = 50, y = 150)

botonGrados = Button(canvas, text = "GRADOS DE LOS VERTICES", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=gradoVertices)
botonGrados.place(x = 50, y = 200)

botonBloquear = Button(canvas, text = "BLOQUEAR / DESBLOQUEAR", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=bloquear)
botonBloquear.place(x = 50, y = 250)

botonInvertir = Button(canvas, text = "INVERTIR UN CAMINO", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=invertir)
botonInvertir.place(x = 50, y = 300)

botonProfundidad = Button(canvas, text = "RECORRER EN PROFUNDIDAD", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=invocarProfundidad)
botonProfundidad.place(x = 50, y = 350)

botonAnchura = Button(canvas, text = "RECORRER EN ANCHURA", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=invocarAnchura)
botonAnchura.place(x = 50, y = 400)

botonConexo = Button(canvas, text = "FUERTEMENTE CONEXO", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=fuertementeConexo)
botonConexo.place(x = 50, y = 450)

botonDijkstra = Button(canvas, text = "RECORRIDO DIJKSTRA", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=llamarDijkstra)
botonDijkstra.place(x = 50, y = 500)

botonDijkstra = Button(canvas, text = "RECORRIDO PROFUNDIDAD GRAFICO", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=listaRecorrerProfundidad)
botonDijkstra.place(x = 50, y = 550)

botonDijkstra = Button(canvas, text = "RECORRIDO ANCHURA GRAFICO", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=listaRecorrerAnchura)
botonDijkstra.place(x = 50, y = 600)

botonDijkstra = Button(canvas, text = "RECORRIDO DIJKSTRA GRAFICO", font=("normal", 12, "bold"), fg="#D4AF37",
                                 bg="#1D1F27", command=listaRecorrerDijkstra)
botonDijkstra.place(x = 50, y = 650)

inicio.mainloop()