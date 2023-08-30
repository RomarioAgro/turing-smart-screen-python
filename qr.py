# Import only the modules for LCD communication
import qrcode
from library.lcd.lcd_comm import Orientation
from library.lcd.lcd_comm_rev_b import LcdCommRevB
from PIL import Image
import time
import serial
from sys import argv

COM_PORT = "COM13"
QR_display_width = 320
QR_display_height = 480


def check_com_port(port):
    """
    проверяем есть у нас что-то на com13 или нет
    """
    # a = api.lookup(api.TYPE_APPLE_SERIAL, '2017-2-25')
    if port:
        try:
            ser = serial.Serial(port)
            ser.close()
            return True
        except serial.SerialException:
            return False
    return False

def qr_image(i_text: str = 'https://yandex.ru/video/preview/11469769755445690591'):
    """
    получаем объект изображение qr-кода
    """
    qr = qrcode.QRCode()
    qr.add_data(i_text)
    qr.make()
    image = qr.make_image()
    image = image.resize((QR_display_width, QR_display_width))
    return image


def show_qr(lcd: object, image: object, qr_text: str = ''):
    """
    функция вывода qr кода на экран 3.5
    : param image: объект картинка, который будем показывать на минидисплее
    : param qr_text: текст который просто будем выводить на экранчике
    : return:
    """

    if image:
        lcd.Reset()
        lcd.InitializeComm()
        lcd.SetBrightness(level=25)
        lcd.SetOrientation(orientation=Orientation.REVERSE_PORTRAIT)
        lcd.DisplayText(qr_text, 0, 330, background_color=(255, 255, 255))
        lcd.DisplayPILImage(image, x=0, y=0)

    else:
        bg = Image.new('RGB', (320, 480), (255, 255, 255))
        lcd.DisplayPILImage(bg)
        lcd.SetBrightness(0)


def main():
    qr_pict = 'https://yandex.ru/video/preview/11469769755445690591'
    qr_text = "для оплаты по СБП\nсканируйте QR код"
    # if argv[1] and argv[2]:
    #     qr_pict = argv[1]
    #     qr_text = argv[2]
    lcd_comm = None
    # COM_PORT = None
    if check_com_port(COM_PORT):
        image = qr_image(i_text=qr_pict)
        lcd_comm = LcdCommRevB(com_port=COM_PORT,
                               display_width=320,
                               display_height=480)
        # lcd_comm = LcdCommRevA(com_port=COM_PORT,
        #                        display_width=320,
        #                        display_height=480)

        show_qr(lcd=lcd_comm, image=image, qr_text=qr_text)

        # тут у нас выключение дисплея
    time.sleep(20)
    show_qr(lcd=lcd_comm, image=None)

if __name__ == '__main__':
    main()