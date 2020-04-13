import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s')


class Taller(object):
    def __init__(self, start=0):
        self.condicionMangasMAX = threading.Condition()
        self.condicionMangasMIN = threading.Condition()
        self.mangas = 0
        self.cuerpos = 0
        self.prenda = 0

    def incrementarManga(self):
        with self.condicionMangasMAX:
            if self.mangas >= 10:
                logging.debug("No hay espacio para mangas")
                self.condicionMangasMAX.wait()
            else:
                self.mangas += 1
                logging.debug("Manga creada, mangas=%s", self.mangas)
        with self.condicionMangasMIN:
            if self.mangas >= 2:
                logging.debug("Existen suficientes mangas")
                self.condicionMangasMIN.notify()

    def decrementarManga(self):
        with self.condicionMangasMIN:
            while not self.mangas >= 2:
                logging.debug("Esperando mangas")
                self.condicionMangasMIN.wait()
            self.mangas -= 2
            logging.debug("Mangas tomadas, mangas=%s", self.mangas)
        with self.condicionMangasMAX:
            logging.debug("Hay espacio para mangas")
            self.condicionMangasMAX.notify()

    def getMangas(self):
        return (self.mangas)

    def getCuerpos(self):
        return (self.cuerpos)


    def incrementarCuerpo(self):
        # verificar que la cesta de cuerpos no esté llena
        with self.condicionMangasMAX:
                if self.cuerpos >= 5 :
                    logging.debug("NO hay espacio en la canasta de cuerpos")
                    self.condicionMangasMAX.wait()
                else:
                    self.cuerpos += 1
                    logging.debug("Cuerpo creado, cuerpo = %s", self.cuerpos)
        # notificar que hay cuerpos disponibles
        with self.condicionMangasMIN:
            logging.debug("Hay suficientes cuerpos disponibles")
            self.condicionMangasMIN.notify()


    def incrementarPrenda(self):
         with self.condicionMangasMIN:
             while self.cuerpos == 0:
                logging.debug("Esperando cuerpos")
                self.condicionMangasMIN.wait()
             self.prenda += 1
             self.cuerpos -= 1
             logging.debug("Prenda creada, prenda = %s", self.prenda)


def crearManga(Taller):
    while (Taller.getMangas() <= 10):
        Taller.incrementarManga()
        time.sleep(3)


def crearCuerpo(Taller):
    while (taller.getMangas() >= 0):
        # incrementarCuerpo (antes de decrementar
        # manga se debe validar que haya cupo en
        # la canasta de cuerpos)
        Taller.decrementarManga()
        Taller.incrementarCuerpo()
        time.sleep(3)


def ensamblaPrenda(Taller):
    while (taller.getCuerpos() >= 0):
        Taller.incrementarPrenda()
        logging.debug('Ensamblando todo')
        time.sleep(3)


taller = Taller()
Lupita = threading.Thread(name='Lupita(mangas)', target=crearManga, args=(taller,))
Sofia = threading.Thread(name='Sofía(cuerpos)', target=crearCuerpo, args=(taller,))
Maria = threading.Thread(name='Maria(prenda)', target=ensamblaPrenda, args=(taller,))
Lupita.start()
Sofia.start()
Maria.start()

Lupita.join()
Sofia.join()
Maria.join()

