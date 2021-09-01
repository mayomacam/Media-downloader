#from logging import exception
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os, time
import requests
import json
from pytube import YouTube, Playlist
#from pytube.cli import on_progress
import re
import urllib.request

headers = {
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'}

exceptions = {}

class windows(QWidget):
    def __init__(self, parent):
        super(windows, self).__init__(parent=parent)
        self.parent = parent
        self.name = ''
        self.type_data = ''
        self.sort_data = ''
        self.website_data = ''
        self.input = ''
        self.input2 = ''
        self.count = 0
        self.input20 = ''

        # website choose
        self.websitelabel = QLabel("Website")

        self.website = QComboBox()
        # self.website.setStyleSheet("max-width: 250px;")
        self.website.addItems(
            ['choose website', 'youtube', 'reddit', 'gfycat', 'imgur'])
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

        # type of sort
        self.sortlabel = QLabel("Sort")
        self.sortlabel.hide()

        self.sorty = QComboBox()
        self.sorty.currentIndexChanged[str].connect(self.text_changed3)
        self.sorty.hide()

        self.layoutsort = QHBoxLayout()
        # self.layouttype.setContentsMargins(0, 0, 0, 0)
        self.layoutsort.addWidget(self.sortlabel)
        self.layoutsort.addWidget(self.sorty)

        # website link
        self.linklabel = QLabel()
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
        self.controlLayout.addLayout(self.layoutsort)
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
        if self.type_data != 'subreddit' or self.type_data != 'playlist':
            self.outputlabel.show()
            self.outputlabel1.show()
            self.output.show()
        else:
            self.button.show()

    def outputname(self):
        print("output name")
        self.button.show()
        #self.progressBar.show()

    def edited(self, a):
        #print('editied')
        self.input = a
        #print(self.input)

    def edited2(self, a):
        # print('editied')
        self.input2 = a
        # print(self.input2)

    def text_changed(self, i):
        self.website_data = i
        print(self.website_data)
        if len(self.website_data) != 0:
            if self.website_data == 'youtube':
                self.type.addItems(['choose type', 'video', 'playlist'])
            elif self.website_data == 'reddit':
                self.type.addItems(
                    ['choose type', 'image', 'video', 'subreddit'])
            elif self.website_data == 'gfycat':
                self.type.addItems(['choose type', 'video'])
            elif self.website_data == 'imgur':
                self.type.addItems(['choose type', 'video', 'image'])
        if self.website.currentIndex() != 0:
            self.type.show()
            self.typelabel.show()
            # print(self.type.)

    def text_changed2(self, i):
        self.type_data = i
        print(self.type_data)
        """if self.count == 1:
            #if self.type.currentIndex() != 0:
            self.linklabel.show()
            self.value.show()"""
        normal_type = ['video', 'image', 'playlist']
        if self.type_data in normal_type:
            self.linklabel.setText('Paste link: ')
            self.linklabel.show()
            self.value.show()
        if self.type_data == 'subreddit':
            self.linklabel.setText('Enter subreddit name: ')
            self.sortlabel.show()
            self.sorty.addItems(['choose sort', 'top', 'hot'])
            self.sorty.show()
        self.count = self.count + 1
    
    def text_changed3(self, i):
        self.sort_data = i
        if self.sorty.currentIndex() != 0:
            self.linklabel.show()
            self.value.show()


    def gfycat(self, url):
        gfycat_response = requests.get(url, headers=headers)
        # print(gfycat_response.text)
        data = gfycat_response.text
        data = re.findall(r"[\w:\/.-]*mp4", data)[0]
        return data

    def refresh(self):
        self.folderlabel.hide()
        self.folderlabel1.hide()
        self.location.hide()
        self.outputlabel.hide()
        self.outputlabel1.hide()
        self.output.hide()
        self.button.hide()
        self.type.hide()
        self.typelabel.hide()
        self.linklabel.hide()
        self.value.hide()
        self.sorty.hide()
        self.sortlabel.hide()
        self.count = 0
        self.website.setCurrentIndex(0)
        self.type.clear()
        self.sorty.clear()
        #self.progressBar.hide()
        #self.value.setText = ''
        self.input = ''

    def Handle_Progress(self, blocknum, blocksize, totalsize):

        # calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
        #else:
        #    self.progressBar.hide()
    
    #def youtube_progress(self, stream, chunk, remain):
        #remaining = (100 * (self.filesize - remain)) / self.filesize
        #self.progressBar.setValue(remaining)
            #QApplication.processEvents()
        #self.progressBar.hide()
    
    def request_reddit(self, i):
        response = requests.get(i, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            next_page = response_json['data']['after']
            posts = response_json['data']['children']
            for post in posts:
                self.progressBar.show()
                # Identify post download url and source.
                source = post['data']['domain']
                media_url = post['data']['url']
                filename = post['data']['title']
                #download_media(media_url, filename.replace('/', '_'), source, 'downloads/'+sub_reddit)
                try:
                    img_url = media_url
                    file_name = filename.replace('/', '_')
                    file_path = self.name+ '/'+ self.input
                    if not os.path.exists(file_path):
                        print('???', file_path, '????????')
                        os.makedirs(file_path)
                    
                    if source == 'gfycat.com':
                        #gfycat_name = img_url.split('/')[-1]
                        img_url = self.gfycat(img_url)
                        if img_url:
                            file_suffix = os.path.splitext(img_url)[1]
                            filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                            if os.path.exists(filename):
                                print("File {0} already exists".format(filename))
                                return False
                            print('\nDownloading gfycat', img_url)
                            urllib.request.urlretrieve(img_url, filename, self.Handle_Progress)
                    elif source == 'i.imgur.com':
                        img_url = img_url.replace('.gifv', '.mp4')
                        file_suffix = os.path.splitext(img_url)[1]
                        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                        if os.path.exists(filename):
                                print("File {0} already exists".format(filename))
                                return False
                        print('\nDownloading imgur', img_url)
                        urllib.request.urlretrieve(img_url, filename, self.Handle_Progress)
                    elif source == 'i.redd.it':
                        file_suffix = os.path.splitext(img_url)[1]
                        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
                        if os.path.exists(filename):
                                print("File {0} already exists".format(filename))
                                return False
                        print('\nDownloading imgur', img_url)
                        urllib.request.urlretrieve(img_url, filename, self.Handle_Progress)
                    else:
                        exceptions[source] = img_url

                except IOError as e:
                    print('??????', e)
                except Exception as e:
                    print('?? ?', e)

            if next_page is not None:
                print("\nHeading over to next page ... ")
                url = i+'&after='+next_page
                self.request_reddit(url)
            else:
                print(response)

    def Download(self):
        print("start downloading")
        if self.type_data == 'video':
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
                        #response = YouTube(self.input, on_progress_callback=self.youtube_progress)
                        response = YouTube(self.input)
                        self.filesize = response.filesize
                        response.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=save_loc)
                        print(response)
                    except:
                        continue

            if self.website_data == 'reddit':
                if self.input[-1:] == '/':
                    self.input = self.input[:-1]
                url = self.input + '.json'
                response = requests.get(url=url, headers=headers)
                video_link = json.loads(response.text)[0]["data"]["children"][0]["data"]["media"]["reddit_video"]["scrubber_media_url"]
                # checking link where it belongs...
                if 'redd' in video_link:
                    d = urllib.request.urlretrieve(
                        video_link, save_loc, self.Handle_Progress)
                elif 'imgur' in video_link:
                    video_link = video_link.replace('.gifv', '.mp4')
                    d = urllib.request.urlretrieve(
                        video_link, save_loc, self.Handle_Progress)
                elif 'gfycat' in video_link:
                    video_link = self.gfycat(video_link)
                    d = urllib.request.urlretrieve(
                        video_link, save_loc, self.Handle_Progress)

            if self.website_data == 'gfycat':
                video_link = self.gfycat(video_link)
                d = urllib.request.urlretrieve(video_link, save_loc, self.Handle_Progress)
            
        if self.type_data == 'image':
            print("image")

        if self.type_data == 'subreddit':
            print('subreddit')
            if self.sorty == 'top':
                url = 'https://www.reddit.com/r/{0}/top.json?sort=top&t=all'.format(self.input)
            else:
                url = 'https://www.reddit.com/r/{0}.json?'.format(self.input)
            
            response = self.request_reddit(url)

        if self.type_data == 'playlist':
            print('playlist')
            playlist = Playlist(self.input)   
            DOWNLOAD_DIR = self.name
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")    
            print(len(playlist.video_urls))    
            for url in playlist.video_urls:
                print(url)
                try:
                    response = YouTube(url)
                    self.filesize = response.filesize
                    response.streams.filter(type='video',progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                    response.download(DOWNLOAD_DIR)
                    print(response)
                except:
                    response = YouTube(url)
                    self.filesize = response.filesize
                    response.streams.filter(type='video',progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(DOWNLOAD_DIR)
                    print(response)
            """for video in playlist.videos:
                print('downloading : {} with url : {}'.format(video.title, video.watch_url))
                video.streams.\
                    filter(type='video', progressive=True, file_extension='mp4').\
                    order_by('resolution').\
                    desc().\
                    first().\
                    download(DOWNLOAD_DIR)"""
        self.refresh()


class UIManager(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        # including Window class
        self.viewer = windows(parent=self)
        self.setCentralWidget(self.viewer)
        self.resize(640, 480)
        self.setWindowTitle('Reddit-downloader')
        if 'nt' in os.name:
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
