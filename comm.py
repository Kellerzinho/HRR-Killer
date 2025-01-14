"""Modulo base para implementacao de classes para a comunicacao serial"""
try:
    import RPi.GPIO as GPIO
except ImportError:
    print('GPIO not imported due to ImportError')
import serial

from abc import ABC, abstractmethod

from estado import Estado

PATH = './hrr/data/serial_teste/serial_teste.txt'


class Serialport(ABC):
    """Classe base para implementacao de classes para a comunicacao serial"""
    states = {
        "ANDAR": "0",
        "GIRAR_ESQUERDA": "1",
        "GIRAR_DIREITA": "2",
        "PARAR": "3",
        "SUBIR":  "6",
        "DESCER": "7"
    }


class SerialTeste(Serialport):
    """Classe herdada da classe SeriaBase e define uma porta serial fictícia
    por meio do arquivo de saida no path indicado"""

    def __init__(self):
        """Herda o __init__ da Serialport e define o local do arquivo destino"""
        self.output_path = PATH

    def escrever_estado(self, state):
        """Metodo que envia o estado atual para o arquivo destino,
        simulando uma comunicacao serial"""
        with open(self.output_path, 'a') as output:
            output.write(state + "\n")


class SerialArduino(Serialport):
    """Classe herdada da classe SeriaBase e define a porta serial que faz coneccao com a MyRIO"""

    def __init__(self):
        # Configuracoes da Rasp
        self.channel = 13  # porta utilizada
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

        # Configuracoes da MyRio
        porta = "/dev/ttyS0"  # nao e a porta AMA0**
        baudrate_arduino = 9600  # deve igualar a da myrio
        #porta serial que faz comunicacao com o Arduino
        self.serial_output = serial.Serial(porta, baudrate_arduino)
        print("Port serial setada")

    def obter_porta(self):
        return self.channel

    def escrever_estado(self, state):
        """Metodo que envia o estado atual para a myrio por meio de comunicacao serial"""
        self.serial_output.write(self.states[state])
        print(self.states[state] + "\n")

    def parar(self):
        self.serial_output.write("3")
        print("PARAR \n")


class Serial(ABC):

    @abstractmethod
    def write_state(self, state: Estado, debug=False):
        self.serial_output.write(state.value)
        if debug:
            print(state.value)

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_port(self):
        pass
