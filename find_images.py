import mss # type: ignore
import cv2
import numpy as np

def getMonitorRegion(number):
    with mss.mss() as sct:
        monitor_number = number
        try:
            mon = sct.monitors[monitor_number]
            region = (mon["left"], mon["top"], mon["width"], mon["height"])
            print(f"Região do monitor {number}: {region}")
            return mon
        except IndexError:
            print("Erro: Segundo monitor não encontrado.")
            return None


def locateImageOnNMonitor(image_path, monitor_to_look):
    mon = getMonitorRegion(monitor_to_look)
    if mon is None:
        print("Monitor não encontrado.")
        return None

    with mss.mss() as sct:
        # Captura a tela do segundo monitor
        sct_img = sct.grab(mon)
        screen = np.array(sct_img)
        
        # Converte para BGR para ser compatível com o OpenCV
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        
        # Carrega a imagem que queremos localizar
        needle_img = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # Define um limiar de confiança
        threshold = 0.6
        max_tries = 100
        tries = 0
        
        while tries < max_tries:
            result = cv2.matchTemplate(screen, needle_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                print(f"Imagem encontrada na posição: {max_loc} com confiança de {max_val}")
                # Converte a posição encontrada para coordenadas globais
                global_position = (max_loc[0] + mon["left"], max_loc[1] + mon["top"])
                print(f"Posição global: {global_position}")
                return global_position
            else:
                tries += 1
        print("Imagem não encontrada. {tries} tentativas. - monitor {monitor_to_look}")

def locateImage(imagepath):
    firstMonitor = locateImageOnNMonitor(imagepath, 1)
    if firstMonitor is not None:
        return firstMonitor
    else:
        secondMonitor = locateImageOnNMonitor(imagepath, 2)
        if secondMonitor is not None:
            return secondMonitor
        else:
            print("Imagem não encontrada em nenhum monitor.")
            return None
