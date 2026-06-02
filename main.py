import pygame
import pyautogui
import time, math

# --- CONFIGURACIÓN ---
DEADZONE = 0.15      # Ignorar movimientos muy leves para evitar el "drift" del mando
SENSITIVITY = 15     # Velocidad del ratón (píxeles por iteración)

def distance(a, b):
    return math.sqrt(abs((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))

def main():
    # Inicializar Pygame y el subsistema de joysticks
    pygame.init()
    pygame.joystick.init()

    # Comprobar si hay algún mando conectado
    if pygame.joystick.get_count() == 0:
        print("No se ha detectado ningún mando conectado. Por favor, conecta uno y vuelve a intentarlo.")
        return

    # Usar el primer mando detectado
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Mando conectado: {joystick.get_name()}")
    print("Mueve el joystick izquierdo para controlar el ratón. Presiona el botón principal (A/X) para hacer clic.")
    print("Presiona Ctrl+C en la consola para salir.")

    width, height = pyautogui.size()

    prevButton = False

    lastPos = (0,0)

    try:
        while True:
            # Es obligatorio llamar a pump() o procesar los eventos para que los valores se actualicen
            pygame.event.pump() 

            # Leer los ejes del joystick izquierdo
            # Normalmente: Eje 0 = Horizontal (Izquierda/Derecha), Eje 1 = Vertical (Arriba/Abajo)
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)

            # Leer el botón (El índice 0 suele ser el botón principal)
            button_click = joystick.get_button(0)
            button2_click = joystick.get_button(1)
        

            # Aplicar la zona muerta (Deadzone)
            if abs(axis_x) < DEADZONE: 
                axis_x = 0
            if abs(axis_y) < DEADZONE: 
                axis_y = 0

            # Mover el ratón si hay entrada del joystick
            if axis_x != 0 or axis_y != 0:
                pos = (axis_x * 200, axis_y * 200)
                if(distance(pos, lastPos) > 10):
                    pyautogui.moveTo(width / 2 + axis_x * 200, height / 2 + axis_y * 200)
                
                lastPos = pos

            # Hacer clic si se presiona el botón
            if button_click and not prevButton:
                pyautogui.mouseDown()
            if not button_click and prevButton:
                pyautogui.mouseUp()

            prevButton = button_click

            if button2_click:
                pyautogui.click(977, 496)
                time.sleep(0.25)

            # Pequeña pausa para no sobrecargar el procesador (CPU al 100%)
            #time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    finally:
        # Limpiar y cerrar Pygame correctamente
        pygame.quit()

if __name__ == "__main__":
    main()