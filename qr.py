# Import only the modules for LCD communication
import qrcode
from library.lcd.lcd_comm import Orientation
from library.lcd.lcd_comm_rev_b import LcdCommRevB
import time
import serial


COM_PORT = "COM13"
QR_display_width = 320
QR_display_height = 480


def check_com_port(port):
    """
    проверяем есть у нас что-то на com13 или нет
    """
    try:
        ser = serial.Serial(port)
        ser.close()
        return True
    except serial.SerialException:
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


def show_qr(image: object, qr_text: str = 'nothing'):
    """
    функция вывода qr кода на экран 3.5
    :param image: объект картинка, который будем показывать на минидисплее
    :param qr_text: текст который просто будм выводить на экранчике
    :return:
    """

    lcd_comm = LcdCommRevB(com_port=COM_PORT,
                           display_width=320,
                           display_height=480)
    if image:
        lcd_comm.Reset()
        lcd_comm.InitializeComm()
        lcd_comm.SetBrightness(level=25)
        lcd_comm.SetOrientation(orientation=Orientation.REVERSE_PORTRAIT)
        lcd_comm.DisplayPILImage(image, x=0, y=0)
        lcd_comm.DisplayText(qr_text, 0, 400, background_color=(255, 255, 255))
    else:
        lcd_comm.SetBrightness(0)


def main():
    url = 'https://yandex.ru/video/preview/11469769755445690591'
    qr_text = "для оплаты по СБП\nсканируйте QR код"

    if check_com_port(COM_PORT):
        image = qr_image(i_text=url)
        show_qr(image=image, qr_text=qr_text)

    # тут у нас выключение дисплея
    time.sleep(100)
    show_qr(image=None)

if __name__ == '__main__':
    main()