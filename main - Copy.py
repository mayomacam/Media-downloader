from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import requests
import json
from pytube import YouTube
import re
import urllib.request

headers = {
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'}


class windows(QWidget):
    def __init__(self, parent):
        super(windows, self).__init__(parent=parent)
        self.parent = parent
        self.name = ''
        self.type_data = ''
        self.website_data = ''
        self.input = ''
        self.count = 0
        self.input20 = ''

        # website choose
        self.websitelabel = QLabel("Website")

        self.website = QComboBox()
        # self.website.setStyleSheet("max-width: 250px;")
        self.website.addItems(['choose website','youtube', 'reddit', 'gfycat', 'imgur'])
        self.website.currentIndexChanged[str].connect(self.text_changed)

        self.layoutwebsite = QHBoxLayout()
        # self.layoutwebsite.setContentsMargins(0, 0, 0, 0)
        self.layoutwebsite.addWidget(self.websitelabel)
        self.layoutwebsite.addWidget(self.website)
        # self.layoutwebsite.setAlignment(Qt.AlignLeft)
        # self.layoutwebsite.setSpacing(100)

        # type of data
        self.typelabel = QLabel("Type")
        self.typelabel.hide()

        self.type = QComboBox()
        #self.type.addItems(['image', 'video', 'playlist'])
        self.type.currentIndexChanged[str].connect(self.text_changed2)
        self.type.hide()

        self.layouttype = QHBoxLayout()
        # self.layouttype.setContentsMargins(0, 0, 0, 0)
        self.layouttype.addWidget(self.typelabel)
        self.layouttype.addWidget(self.type)
        # self.layouttype.setAlignment(Qt.AlignLeft)

        # website link
        self.linklabel = QLabel("Paste link:")
        self.linklabel.hide()

        self.value = QLineEdit()
        self.value.textEdited.connect(self.edited)
        self.value.returnPressed.connect(self.requestURL)
        self.value.hide()
        # self.value.setStyleSheet("max-width: 100%;")

        self.layoutlink = QVBoxLayout()
        # self.layoutlink.setContentsMargins(0, 0, 0, 70)
        self.layoutlink.addWidget(self.linklabel)
        self.layoutlink.addWidget(self.value)

        # output save
        self.outputlabel = QLabel("Enter filename for saveing:")
        self.outputlabel.hide()
        self.outputlabel1 = QLabel("(default: download.(file-ext)*")
        self.outputlabel1.hide()

        self.output = QLineEdit()
        self.output.textEdited.connect(self.edited2)
        self.output.returnPressed.connect(self.outputname)
        self.output.hide()

        self.layoutoutput = QVBoxLayout()
        # self.layoutoutput.setContentsMargins(0, 0, 0, 0)
        self.layoutoutput.addWidget(self.outputlabel)
        self.layoutoutput.addWidget(self.outputlabel1)
        self.layoutoutput.addWidget(self.output)

        # save location
        self.folderlabel = QLabel("Choose location:")
        self.folderlabel.hide()
        self.folderlabel1 = QLabel("(Defult: from where it's running*)")
        self.folderlabel1.hide()

        self.location = QPushButton()
        self.location.clicked.connect(self.folderlocation)
        self.location.setText("Choose location")
        self.location.hide()

        self.layoutfolder = QVBoxLayout()
        # self.layouttype.setContentsMargins(0, 0, 0, 0)
        self.layoutfolder.addWidget(self.folderlabel)
        self.layoutfolder.addWidget(self.folderlabel1)
        self.layoutfolder.addWidget(self.location)

        self.progressBar = QProgressBar(self)
        self.progressBar.hide()

        self.button = QPushButton('Download', self)
        self.button.clicked.connect(self.Download)
        self.button.hide()

        """self.controlLayout = QGridLayout()
        self.controlLayout.addLayout(self.layoutlink, 2,0)
        self.controlLayout.addLayout(self.layoutwebsite,0,0)
        self.controlLayout.addLayout(self.layouttype,1,0)
        self.controlLayout.addWidget(self.location,3,1)
        self.controlLayout.addWidget(self.output,3,0)
        self.controlLayout.addWidget(self.button, 4,1)
        self.controlLayout.addWidget(self.progressBar,5,0)
        # self.controlLayout.setContentsMargins()
        self.setLayout(self.controlLayout)"""

        self.controlLayout = QVBoxLayout()
        self.controlLayout.addLayout(self.layoutwebsite)
        self.controlLayout.addLayout(self.layouttype)
        self.controlLayout.addLayout(self.layoutlink)
        self.controlLayout.addLayout(self.layoutfolder)
        self.controlLayout.addLayout(self.layoutoutput)
        self.controlLayout.addWidget(self.button)
        self.controlLayout.addWidget(self.progressBar)
        # self.controlLayout.setContentsMargins()
        self.setLayout(self.controlLayout)

    def requestURL(self):
        print("input url")
        print(self.input)
        self.folderlabel.show()
        self.folderlabel1.show()
        self.location.show()

    def folderlocation(self):
        self.name = QFileDialog().getExistingDirectory(self, 'Open File', '')
        print(self.name)
        self.output.setText(self.name)
        self.outputlabel.show()
        self.outputlabel.show()
        self.output.show()

    def outputname(self):
        print("output name")
        self.button.show()


    def edited(self, a):
        print('editied')
        self.input = a
        print(self.input)

    def edited2(self, a):
        #print('editied')
        self.input2 = a
        #print(self.input2)

    def text_changed(self, i):
        self.website_data = i
        print(self.website_data)
        if self.website_data == 'youtube':
            self.type.addItems(['choose type','video', 'playlist'])
        elif self.website_data == 'reddit':
            self.type.addItems(['choose type','image','video', 'subreddit'])
        elif self.website_data == 'gfycat':
            self.type.addItems(['choose type','video', 'gif'])
        elif self.website_data == 'imgur':
            self.type.addItems(['choose type','video', 'image'])
        if self.website.currentIndex() != 0:
            self.type.show()
            self.typelabel.show()

    def text_changed2(self, i):
        self.type_data = i
        print(self.type_data)
        if self.count == 1:
            if self.type.currentIndex() != 0:
                self.linklabel.show()
                self.value.show()
        self.count = self.count + 1

    def gfycat(self, url):
        gfycat_response = requests.get(url, headers=headers)
        # print(gfycat_response.text)
        data = gfycat_response.text
        data = re.findall(r"[\w:\/.-]*mp4", data)[0]
        return data
    
    def refresh(self):
        """d = self.children()
        e = reversed(d)

        for g in e:
            g.deleteLater()
        
        self.viewer = windows(parent=self.parent)
        #self.setCentralWidget(self.viewer)"""
        self.folderlabel.hide()
        self.folderlabel1.hide()
        self.location.hide()
        self.outputlabel.hide()
        self.outputlabel.hide()
        self.output.hide()
        self.button.hide()
        self.type.hide()
        self.typelabel.hide()
        self.linklabel.hide()
        self.value.hide()
        self.count =0
        self.website.setCurrentIndex(0)
        self.type.setCurrentIndex(0)
        self.value.setText = ''

    def Handle_Progress(self, blocknum, blocksize, totalsize):

        # calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
        else:
            self.progressBar.hide()

    def Download(self):
        print(self.input2)
        print("start downloading")
        self.progressBar.show()
        if len(self.input2) == 0:
            save_loc = 'download.mp4'
        else:
            if '.mp4' in self.input2:
                save_loc = self.input2
            else:
                save_loc = self.input2+'download.mp4'
    
        if self.website_data == 'youtube':
            while(True):
                try:
                    response = YouTube(self.input).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first().download(filename=save_loc)
                    print(response)
                    break
                except:
                    continue
        
        if self.website_data == 'reddit':
            if self.input[-1:] == '/':
                self.input = self.input[:-1]
            url = self.input + '.json'
            response = requests.get(url=url, headers=headers)
            if self.type_data == 'image':
                image_link = json.loads(response.text)[0]["data"]["children"][0]["data"]["url"]
                #if image_link[-4:] == '.gifv':
                    
            elif self.type_data == 'video':
                video_link = json.loads(response.text)[0]["data"]["children"][0]["data"]["media"]["reddit_video"]["scrubber_media_url"]
                # checking link where it belongs...
                if 'redd' in video_link:
                    d = urllib.request.urlretrieve(video_link, save_loc, self.Handle_Progress)
                    self.progressBar.hide()
                elif 'imgur' in video_link:
                    video_link = video_link.replace('.gifv','.mp4')
                    d = urllib.request.urlretrieve(video_link, save_loc, self.Handle_Progress)
                    self.progressBar.hide()
                elif 'gfycat' in video_link:
                    video_link = self.gfycat(video_link)
                    d = urllib.request.urlretrieve(video_link, save_loc, self.Handle_Progress)
                    self.progressBar.hide()
                """
                if 'redd' in video_link:
                    d = requests.get(video_link, self.Handle_Progress).content
                elif 'imgur' in video_link:
                    d = requests.get(video_link, self.Handle_Progress).content
                elif 'gfycat' in video_link:
                    video_link = self.gfycat(video_link)
                    d = requests.get(video_link, self.Handle_Progress).content
                if len(self.input2) == 0:
                    with open('download.mp4', 'wb') as file:
                        file.write(d)
                else:
                    if '.mp4' in self.input2:
                        with open(self.input2, 'wb') as file:
                            file.write(d)
                    else:
                        with open(self.input2+'download.mp4', 'wb') as file:
                            file.write(d)"""
        
        if self.website_data == 'gfycat':
            video_link = self.gfycat(video_link)
            d = urllib.request.urlretrieve(video_link, save_loc, self.Handle_Progress)
        
        self.refresh()




class UIManager(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # including Window class
        self.viewer = windows(parent=self)
        self.setCentralWidget(self.viewer)
        self.resize(480, 320)
        self.setWindowTitle('Reddit-downloader')
        if 'windows' in os.name:
            self.setWindowIcon(QIcon('icons/download.png'))
        elif 'mac' in os.name:
            self.setWindowIcon(QIcon('icons/download-mac-os.png'))
        else:
            self.setWindowIcon(QIcon('icons/download-linux.png'))

        # exit
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+X')
        exit_act.triggered.connect(self.close)

        # Create menubar
        menu_bar = self.menuBar()
        # For MacOS users, places menu bar in main window
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        menu_bar.addAction(exit_act)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(style_sheet)
    app.setStyle("Fusion")
    window = UIManager()
    window.show()
    sys.exit(app.exec_())
