# Import only the modules for LCD communication
import qrcode
from turing_smart_screen_python.library.lcd.lcd_comm import Orientation
from turing_smart_screen_python.library.lcd.lcd_comm_rev_a import LcdCommRevA
from turing_smart_screen_python.library.lcd.lcd_comm_rev_b import LcdCommRevB
from PIL import Image
import time
import serial
from sys import argv
import subprocess
import win32com.client



QR_display_width = 320
QR_display_height = 480
VENDOR_ID = 0x1A86  # Замените на свой Vendor ID
PRODUCT_ID = 0x5722  # Замените на свой Product ID



def get_usb_device_instance_id(vendor_id, product_id):
    """
    функция определяет какое конкретно устройство у нас висит на COM порту
    """
    cmd = "wmic path Win32_USBControllerDevice get Dependent, Antecedent"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    my_device = []
    for line in result.stdout.splitlines():
        if "USB\\VID_{:04X}&PID_{:04X}".format(vendor_id, product_id) in line:
            device_id = line.split("USB\\")[-1]
            my_device.append(device_id.strip())
    return my_device


def found_com_port(vendor_id, product_id) -> str:
    """
    функция перебирает COM порты и ищет подходящие устройства
    возвращает строку с именем COM порта
    """
    wmi = win32com.client.GetObject("winmgmts:")
    for serial in wmi.InstancesOf("Win32_SerialPort"):
        dev_id = serial.PNPDeviceID
        expected_line = "VID_{:04X}&PID_{:04X}".format(vendor_id, product_id)
        if expected_line in dev_id:
            print(serial.PNPDeviceID, serial.DeviceID, serial.Name, serial.Description)
            return serial.DeviceID


def check_com_port(port):
    """
    проверяем есть у нас что-то на com порту или нет
    """
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


def output_content_on_minidisplay(pict, text, display_on: bool = True):
    """
    функция поиска дисплея вывода изображения на него
    и выключения дисплея
    """
    COM_PORT = found_com_port(VENDOR_ID, PRODUCT_ID)
    if check_com_port(COM_PORT):
        image = qr_image(i_text=pict)
        my_device = get_usb_device_instance_id(VENDOR_ID, PRODUCT_ID)
        if my_device[0].find('2017-2-25') >= 0:
            lcd_comm = LcdCommRevB(com_port=COM_PORT,
                                   display_width=320,
                                   display_height=480)
        else:
            lcd_comm = LcdCommRevA(com_port=COM_PORT,
                                   display_width=320,
                                   display_height=480)
        if display_on:
            show_qr(lcd=lcd_comm, image=image, qr_text=text)
        else:
            show_qr(lcd=lcd_comm, image=None)

def main():
    qr_pict = 'https://yandex.ru/video/preview/11469769755445690591'
    qr_text = "для оплаты по СБП\nсканируйте QR код"
    output_content_on_minidisplay(qr_pict, qr_text)

if __name__ == '__main__':
    main()