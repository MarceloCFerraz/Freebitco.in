# Bot para automatizar cliques no botão ROLL do freebitco.in
# TODO:
# descobrir como fazer para alternar para a janela do programa

import ctypes
import pyautogui as gui
import time
import winsound
from PIL import ImageGrab
import pytesseract as tesseract
import cv2
import ctypes
import numpy as nm
from pytesseract import Output


tesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def imgtorgb(img):
    rgb = cv2.cvtColor(nm.array(img), cv2.COLOR_BGR2RGB)
    return rgb


def imgtogray(img):
    gray = cv2.cvtColor(nm.array(img), cv2.COLOR_BGR2GRAY)
    return gray


def PrintTela(x1, y1, x2, y2):
    # ImageGrab-To capture the screen image in a loop.
    # Bbox used to capture a specific area.
    return (ImageGrab.grab(bbox=(x1, y1, x2, y2)))


def LimiarizacaoOtsu(gray):
    limiar, img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("- Limiar Gaussiano: {}".format(limiar))
    # cv2.imshow("Limiarizacao Simples", limiar)
    # cv2.waitKey()

    return img


def AcharBotao(botao, x, y):
    achou = False

    gui.click(x/2, 12)
    time.sleep(0.5)
    gui.press("end")

    rodadas = 0

    while not achou:
        rodadas += 1
        print("Rodada atual: {}".format(rodadas))

        img = PrintTela(317, 89, 1565, 1027)
        gray = imgtogray(img)

        limiar = LimiarizacaoOtsu(gray)
        invert_limiar = 255 - limiar

        # img_copia = invert_limiar.copy()

        resultados = tesseract.image_to_data(invert_limiar, output_type=Output.DICT)
        print(resultados)

        for i in range(0, len(resultados["text"])):
            confiabilidade = int(float(resultados["conf"][i]))
            x = resultados["left"][i]
            y = resultados["top"][i]
            w = resultados["width"][i]
            h = resultados["height"][i]
            texto = resultados["text"][i]

            if confiabilidade > 20:
                cv2.rectangle(invert_limiar,
                              (x, y),
                              (x+w, y+h),
                              (0,0,0),
                              1)
                # cv2.rectangle(invert_limiar,
                #               (x, y),
                #               (x+w, y+h),
                #               (255,255,255),
                #               1)

            if botao.upper() in texto.upper():
                # print("{0}\n{1}\n{2}".format(texto, text, resultados["text"][i+1]))
                achou = True

                print("{0} - {1} ({2}, {3}, {4}, {5})".format(resultados["text"][i],
                                                              confiabilidade,
                                                              x,
                                                              y,
                                                              x+w,
                                                              y+h)
                      )
                gui.click(x+(w/2), y+(h/2)+438)

    # cv2.imshow("resultado final", invert_limiar)
    # cv2.waitKey()


def primeira_chamada():
    print("-----------------------------------------------------------------------------------")
    print("| Atenção! Abra a aplicação do FreeBitco.in dentro de 30 segundos e certifique-se |")
    print("| de mantê-la aberta e em foco antes do clique (tanto no início quanto no final   |")
    print("| do timer. ESTA APLICAÇÃO NÃO ABRIRÁ NADA AUTOMATICAMENTE PARA VOCÊ!             |")
    print("-----------------------------------------------------------------------------------")


def contagem(tempo):
    # transforma os minutos recebidos em segundos
    tempo = tempo * 60

    while tempo > 0:
        if tempo <= 10:
            # emite som de alerta com contagem regressiva de 10 segundos
            winsound.Beep(900, 100)
        print("Tempo restante: {0}s\r".format(tempo))
        tempo -= 1
        time.sleep(1)


if __name__ == '__main__':
    # A cada comando do gui há uma espera de 1 segundo;
    # Levar o ponteiro do mouse para o canto superior esquerdo da tela gera uma exceção na aplicação
    gui.PAUSE = 1
    gui.FAILSAFE = True

    user32 = ctypes.windll.user32

    # A primeira chamada manda uma mensagem específica explicativa e aciona uma contagem de 30 segundos.
    # por tal motivo ela está fora do loop principal
    primeira_chamada()
    contagem(0.05)

    # loop infinito para que o bot nunca pare
    while 1:
        # descobre a resolução do monitor principal. Para o segundo monitor, passar 78 e 79 como parametros.
        x = user32.GetSystemMetrics(0)
        y = user32.GetSystemMetrics(1)
        # calcular a posição do botão no centro da tela
        # x_botao = x * 0.50
        # y_botao = y * 0.75
        # print(gui.locateOnWindow('button.png'))

        print("Resolução da tela: {0:n} x {1:n}".format(x, y))
        # print("O botão localiza-se em {0:n} x {1:n}\n".format(x_botao, y_botao))

        AcharBotao("ROLL", x, y)

        contagem(60.05)
        # chama a função de contagem regressiva passando 60 minutos + 9 segundos de margem de segurança
        
