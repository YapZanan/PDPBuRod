from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)


#ambil waktu sekarang pakai library datetime
        sekarang = QDate.currentDate()
        tanggalsekarang = sekarang.toString('ddd dd MMMM yyyy')
        waktusekarang = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(tanggalsekarang)
        self.Time_Label.setText(waktusekarang)
        self.image = None

    @pyqtSlot()
    def startVideo(self, kamera):
        if len(kamera) == 1:
        	self.capture = cv2.VideoCapture(int(kamera))
        else:
        	self.capture = cv2.VideoCapture(kamera)
        self.timer = QTimer(self)  # Create Timer

        # import gambar belajar
        direktori = 'Belajar' #import folder belajar
        if not os.path.exists(direktori):
            os.mkdir(direktori) #buat direktori kalau misalkan gaada


        images = []
        self.nama = [] #buat array kosong yang nanti bakalan dipakai buat masukin nama
        self.encode_list = [] #naruh semua hasil encoding wajah di sini
        self.TimeList1 = [] #buat naruh waktu
        data = os.listdir(direktori) #naruh semua direktori di variabel 'direktori

        #proses gambar dari folder belajar
        for kelas in data:  #perulangan buat ambil gambar dari os
            loadgambar = cv2.imread(f'{direktori}/{kelas}') #masukin gambar ke dalam loadgambar
            images.append(loadgambar)
            self.nama.append(os.path.splitext(kelas)[0])  #ngambil nama kelas 0 dari sebuah file (sebelum titik)

        # ngasih encoding ke gambar yang ada di folder
        for gambar in images: #perulangan buat masukin image dari belajar
            gambar = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB) #ubah color space gambar ke RGB
            kotak = face_recognition.face_locations(gambar)
            encoding = face_recognition.face_encodings(gambar, kotak)[0] #pakai fungsi dari library face recogni
            self.encode_list.append(encoding)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

        print(len(encoding))

    def face_rec_(self, sementara, diketahui, nama):



#fungsi buat presensi di pyqt
        def presensi(name):
            if self.Hadir.isChecked():
                self.Hadir.setEnabled(False)
                with open('Daftar_Hadir.csv', 'a') as f:
                        if (name != 'Tidak terdaftar'):
                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                f.writelines(f'\n{name},{date_time_string},Presensi')
                                self.Hadir.setChecked(False)
                                self.NameLabel.setText(name)
                                self.StatusLabel.setText('Anda sudah melakukan absensi!')
                                self.MinLabel.setText('')
                                self.Time1 = datetime.datetime.now()
                                self.Hadir.setEnabled(True)



        lokasiwajah = face_recognition.face_locations(sementara) #nyari tau posisi wajah pakai fungsi dari libary 'face_recognition'
        encoding = face_recognition.face_encodings(sementara, lokasiwajah) # pakai fungsi dari library face recognition buat encoding, sekalian ngasih lokasi wajah

#komparasi wajah kamera dan belajar
        for encodeFace, faceLoc in zip(encoding, lokasiwajah):
            sama = face_recognition.compare_faces(diketahui, encodeFace, tolerance=0.50)
            faceDis = face_recognition.face_distance(diketahui, encodeFace)
            name = "Tidak terdaftar"
            indekssama = np.argmin(faceDis)

            if sama[indekssama]:
                name = nama[indekssama]
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(sementara, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(sementara, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(sementara, name, (x1 + 6, y2 - 6), font, 0.5, (255, 255, 255), 1)
            presensi(name)
        return sementara

#fungsi buat print ke csv
    def ElapseList(self,name):
        with open('Daftar_Hadir.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Presensi':
                            if row[0] == name:
                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)

#ambil setiap frame dari video yang diterima
    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.nama, 1)

#nampilin opencv ke pyqt
    def displayImage(self, image, encode_list, class_names, window=1):
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
