"""Modulo base do robo de corrida"""
from time import sleep, time
from typing import Self
from desvio import Desvio
from estado import Estado
from comm import *
from sensor_distancia import *
from camera import *
from alinhamento import *
from gyro import *
from exceptions import *
from controller import Controller
import constantes as c


class Robo:
    """Classe base do robo de corrida"""

    __slots__ = ['state', 'comm', 'camera', 'distance_sensor',
                 'gyro', 'controller', '_compiled', '_debug_mode']

    @staticmethod
    def build_instance() -> Self:
        return Robo(SerialArduino(), IMU(), RaspCamera(), SensorDistancia())

    def __init__(self,
                 arduino: Serial,
                 camera: Camera,
                 sensor_distancia: SensorDistancia,
                 gyro: Gyro):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""

        self.estado: Estado = Estado.PARADO
        self.arduino: Serial = arduino
        self.camera: Camera = camera
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.gyro: Gyro = gyro
        self._compiled = False
        self._debug_mode = False

    def compile(self, use_ml: bool = False) -> Self:
        '''
            Método responsável por observar se o objeto robô possui o estado de hardware apropriado para o funcionamento. 
            Os possíveis estados são:


            Além disso, o método também é responsável por compilar o alinhamento do robô.
            Para mais detalhes, ler code report.
        '''

        self._compiled = True
        observers = {
            'camera': self.camera,
            'sensor_distancia': self.sensor_distancia,
            'gyro': self.gyro,
        }
        self.controller = Controller('ml' if use_ml else 'standard', observers)
        return self

    def corrida(self) -> None:
        '''Método base da corrida do robo'''
        if not self._compiled:
            raise RobotCompileException('Robô não compilado')
        while True:
            self.estado = self.controller.proximo_estado()
            self.discovery.write_state(self.estado, self._debug_mode)
            sleep(0.1)
