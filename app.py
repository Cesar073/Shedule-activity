import pyautogui as pa
import keyboard
from time import sleep
from datetime import datetime as dt
from datetime import timedelta
import threading

TEXT_MENU = '''            
"S" para salir (exit-salir).

1. Crear nuevo evento.
2. Evitar la suspensión.
    2.1. Activar
    2.2. Desactivar
3. Activar la Automatización.
4. Desactivar la Automatización.
5. Editar evento.
'''

class AutomaticActions:
    def __init__(self):
        self.main_bucle = True
        self.susp_activate = False
        self.list_clics = []
        self.counter_clics = 0
        self.close = False
        # seconds
        self.check_times = 30
        
        self.print_menu()

    def avoid_suspension(self):
        while self.susp_activate:
            pa.moveTo(x=500, y=600)
            sleep(5)
            pa.moveTo(x=550, y=550)
            sleep(55)
    
    def check_bucle(self):
        while self.main_bucle:
            min = 3600
            clic_counter = 0

            for clics in self.list_clics:
                clic_counter += 1

                clics["counter"] -= self.check_times
                
                if clics["activate"] == True:
                    if min > clics["counter"]:
                        min = clics["counter"]
                    if clics["counter"] <= 0:
                        pa.click(clics["x"], clics["y"])
                        clics["activate"] = False
                        print("Se ejectuó un evento")
                        continue
                        # if min > self.check_times * 2:
                        #     self.check_times = 1
                
                if min < 30:
                    self.check_times = 1
                else:
                    self.check_times = 30
                print(f"Al evento en la pos: {clic_counter} le faltan: {clics['counter']} segundos.")
            sleep(self.check_times)

    def get_data(self):
        # print(f"El tamaño de su pantalla es: {pa.size()}")
        # print("Tenga en cuenta que la pantalla ")
        hora = input("Una vez que presiones Enter, tendrás 3 segundos para\ncolocar el mouse en la posición que desees hacer clic:")
        for i in range(3, 0, -1):
            print(i)
            sleep(1)

        pos = pa.position()
        print(f"x: {pos.x} - y: {pos.y}")

        while hora != "s" or hora != "S":
            hora = input("""S para salir.
            Escribe la hora y minuto en que quieras iniciarlo separado por un punto.
            Por ejemplo si quisiéramos ejecutarlo a las 18:25:00 sería así: 18.25
            Ingrese la hora: """)
            if hora.upper() == "S":
                break
            moment = dt.now()
            try:
                moment = moment.replace(hour=int(hora[:2]), minute=int(hora[3:]), second=0)
            except Exception:
                print("La hora ingresada no tiene el formato correcto.")
                continue

            if moment < dt.now():
                moment = moment + timedelta(days=1)
                print("Aviso!, se pasó para mañana porque el horario colocado ya ocurrió en el día de hoy.")

            diff = moment - dt.now()
            self.list_clics.append({"counter": diff.total_seconds(), "x": pos.x, "y": pos.y, "activate": True})
            print(f"Agregado")
            break

    def check_cancelar(self, time):
        start = dt.now()
        start = start.replace(microsecond=0)
        finish = start + timedelta(seconds=time)
        while True:
            if keyboard.is_pressed('esc'):
                self.close = False
                print("Se canceló el cierre.")
                break
            if finish < dt.now():
                break

    def print_menu(self):
        """
        Aquí ejecutamos el bucle que pide todos los datos y genera todos los hilos necesarios.
        """

        greeting = True
        action = ""
        show_back_menu = False

        while True:
            text = ""

            if greeting:
                text = "AUTOMATIZAR CLICS:\n"
                greeting = False
            
            if show_back_menu:
                text += '"M" para cancelar la actividad y volver al menú ppal.'

            text += TEXT_MENU
            print(text)

            action = input("Elija una acción: ").upper()
            
            if action == "S":
                threading.Thread(target=self.check_cancelar, args=(3,)).start()
                self.close = True
                print("El programa se cerrará en 3 segundos, presione Esc para Cancelar.")
                for i in range(3, 0, -1):
                    if self.close == False:
                        break
                    print(i)
                    sleep(1)
            
            if action == "1":
                threading.Thread(target=self.check_bucle).start()
            elif action == "2":
                threading.Thread(target=self.check_bucle).start()
            elif action == "2.1":
                threading.Thread(target=self.check_bucle).start()
            elif action == "2.2":
                threading.Thread(target=self.check_bucle).start()
            elif action == "3":
                threading.Thread(target=self.check_bucle).start()
            elif action == "4":
                threading.Thread(target=self.check_bucle).start()
            elif action == "5":
                threading.Thread(target=self.check_bucle).start()

            if self.close == True:
                break






hacer_clic = AutomaticActions()


