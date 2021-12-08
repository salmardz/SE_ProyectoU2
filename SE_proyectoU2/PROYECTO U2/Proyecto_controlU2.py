##uso de modulo pyserial
import serial as s
import numpy as n
import sys


from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "controlproyectoi.ui"  # Nombre del archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.arduino = None
        self.btn_conexion.clicked.connect(self.conexion)

        self.SegundoPlano = QtCore.QTimer()
        self.SegundoPlano.timeout.connect(self.accion)

        self.btn_control.clicked.connect(self.control)

        self.valorSensor1 = -1
        self.valorSensor2 = -1
        self.valorSensor3 = -1


    def control(self):
        self.valorSensor1 /= 100
        self.valorSensor2 /= 100
        self.valorSensor3 /= 100

        T = [0.6, 0.2, 0.2],[0.3, 0.4, 0.3], [0.1, 0.4, 0.5]

        P_inicial = [float(self.valorSensor1), float(self.valorSensor2), float(self.valorSensor3)]

        matriz_T = n.array(T)
        matriz_P0 = n.array(P_inicial)

        estadoDeseado = int(self.tx_P0.text())

        estadoActual = matriz_P0
        for i in range(estadoDeseado-1):
            estadoActual = estadoActual.dot(matriz_T)


        estadoActual=str(estadoActual).replace('[','').replace(']','')
        estadoActual=str(estadoActual).replace(' ',',').replace(' ',',')
        self.arduino.write(str(estadoActual).encode())
        # Aplicar cadenas de markov
        # respuesta = ....

        # supongamos ....
       # if self.valorSensor1 + self.valorSensor2 + self.valorSensor3 > 1.5:
        #    self.arduino.write("1".encode())
        #else:
         #   self.arduino.write("0".encode())
        #P_inicial = self.valorSensor1 + self.valorSensor2 + self.valorSensor3
        if self.valorSensor1 + self.valorSensor2 + self.valorSensor3 >1.2:
            self.arduino.write("1".encode())
        elif self.valorSensor1 + self.valorSensor2 + self.valorSensor3 == 1:
            self.arduino.write("2".encode())
        elif self.valorSensor1 + self.valorSensor2 + self.valorSensor3 < 0.8:
            self.arduino.write("3".encode())
        else:
            self.arduino.write("0".encode())

    def accion(self):

        while self.arduino.inWaiting():
            valor = self.arduino.readline().decode()

            valor = valor.replace("\n", "")
            valor = valor.replace("\r", "")

            auxiliar = ""

            if valor[0] == 'I':
                if valor[len(valor) - 1] == 'F':

                    # slicing
                    index = valor.find("R")
                    valor1 = valor[1:index]

                    auxiliar += " Sensor1: " + valor1
                    self.valorSensor1 = float(valor1)

                    valorNuevo = valor[index + 1:]

                    index = valorNuevo.find("R")
                    valor2 = valorNuevo[0:index]

                    auxiliar += " Sensor2: " + valor2
                    self.valorSensor2 = float(valor2)

                    valor3 = valorNuevo[index + 1:len(valorNuevo) - 1]

                    auxiliar += " Sensor3: " + valor3
                    self.valorSensor3 = float(valor3)

            self.datosSensor.addItem(auxiliar)

            self.datosSensor.setCurrentRow(self.datosSensor.count() - 1)

    def conexion(self):
        v = self.btn_conexion.text()
        if v == "CONECTAR":
            self.btn_conexion.setText("DESCONECTAR")

            if self.arduino == None:
                com = "COM" + self.txt_com.text()
                self.arduino = s.Serial(com, baudrate=9600, timeout=1000)

                self.txt_estado.setText("INICIALIZADO")

                self.SegundoPlano.start(100)

            elif not self.arduino.isOpen():
                self.arduino.open()
                self.txt_estado.setText("REESTABLECIDO")

                self.SegundoPlano.start(100)
        else:
            self.btn_conexion.setText("CONECTAR")

            self.arduino.close()
            self.txt_estado.setText("CERRADO")

            self.SegundoPlano.stop()

    def mensaje(self, msj):
        m = QtWidgets.QMessageBox()
        m.setText(msj)
        m.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
