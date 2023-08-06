# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main-window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

from ..widgets import ControlToolButton
from  . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(340, 500)
        MainWindow.setWindowTitle(u"Eternal Radio Player")
        icon = QIcon()
        icon.addFile(u":/icons/eternal-radio-player.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_window_layout = QVBoxLayout(self.centralwidget)
        self.main_window_layout.setSpacing(0)
        self.main_window_layout.setObjectName(u"main_window_layout")
        self.main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QStackedWidget(self.centralwidget)
        self.main_widget.setObjectName(u"main_widget")
        self.recent_songs_page = QWidget()
        self.recent_songs_page.setObjectName(u"recent_songs_page")
        self.recent_songs_page_layout = QVBoxLayout(self.recent_songs_page)
        self.recent_songs_page_layout.setSpacing(0)
        self.recent_songs_page_layout.setObjectName(u"recent_songs_page_layout")
        self.recent_songs_page_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_songs = QScrollArea(self.recent_songs_page)
        self.recent_songs.setObjectName(u"recent_songs")
        self.recent_songs.setFrameShape(QFrame.NoFrame)
        self.recent_songs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.recent_songs.setWidgetResizable(True)
        self.recent_songs_container = QWidget()
        self.recent_songs_container.setObjectName(u"recent_songs_container")
        self.recent_songs_container.setGeometry(QRect(0, 0, 323, 478))
        self.recent_songs.setWidget(self.recent_songs_container)

        self.recent_songs_page_layout.addWidget(self.recent_songs)

        self.main_widget.addWidget(self.recent_songs_page)
        self.console_page = QWidget()
        self.console_page.setObjectName(u"console_page")
        self.console_page_layout = QVBoxLayout(self.console_page)
        self.console_page_layout.setSpacing(8)
        self.console_page_layout.setObjectName(u"console_page_layout")
        self.console_page_layout.setContentsMargins(8, 8, 8, 8)
        self.console = QPlainTextEdit(self.console_page)
        self.console.setObjectName(u"console")
        self.console.setReadOnly(True)
        self.console.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.console.setMaximumBlockCount(1000)

        self.console_page_layout.addWidget(self.console)

        self.console_back_button = QPushButton(self.console_page)
        self.console_back_button.setObjectName(u"console_back_button")
        self.console_back_button.setText(u"Back")

        self.console_page_layout.addWidget(self.console_back_button, 0, Qt.AlignRight)

        self.main_widget.addWidget(self.console_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.settings_page_layout = QVBoxLayout(self.settings_page)
        self.settings_page_layout.setSpacing(0)
        self.settings_page_layout.setObjectName(u"settings_page_layout")
        self.settings_page_layout.setContentsMargins(0, 0, 0, 0)
        self.settings = QScrollArea(self.settings_page)
        self.settings.setObjectName(u"settings")
        self.settings.setFrameShape(QFrame.NoFrame)
        self.settings.setWidgetResizable(True)
        self.settings_container = QWidget()
        self.settings_container.setObjectName(u"settings_container")
        self.settings_container.setGeometry(QRect(0, 0, 340, 478))
        self.settings_layout = QVBoxLayout(self.settings_container)
        self.settings_layout.setSpacing(8)
        self.settings_layout.setObjectName(u"settings_layout")
        self.settings_layout.setContentsMargins(8, 8, 8, 8)
        self.settings_group = QGroupBox(self.settings_container)
        self.settings_group.setObjectName(u"settings_group")
        self.settings_group.setTitle(u"Settings")
        self.settings_group_layout = QGridLayout(self.settings_group)
        self.settings_group_layout.setSpacing(8)
        self.settings_group_layout.setObjectName(u"settings_group_layout")
        self.settings_group_layout.setContentsMargins(8, 8, 8, 8)
        self.connection_timeout_label = QLabel(self.settings_group)
        self.connection_timeout_label.setObjectName(u"connection_timeout_label")
        self.connection_timeout_label.setText(u"Connection timeout:")

        self.settings_group_layout.addWidget(self.connection_timeout_label, 0, 0, 1, 1)

        self.recent_songs_update_time_label = QLabel(self.settings_group)
        self.recent_songs_update_time_label.setObjectName(u"recent_songs_update_time_label")
        self.recent_songs_update_time_label.setText(u"Recent songs update time:")

        self.settings_group_layout.addWidget(self.recent_songs_update_time_label, 1, 0, 1, 1)

        self.connection_timeout_input = QDoubleSpinBox(self.settings_group)
        self.connection_timeout_input.setObjectName(u"connection_timeout_input")
        self.connection_timeout_input.setDecimals(1)
        self.connection_timeout_input.setMinimum(1.000000000000000)
        self.connection_timeout_input.setMaximum(60.000000000000000)

        self.settings_group_layout.addWidget(self.connection_timeout_input, 0, 1, 1, 1)

        self.recent_songs_update_time_input = QDoubleSpinBox(self.settings_group)
        self.recent_songs_update_time_input.setObjectName(u"recent_songs_update_time_input")
        self.recent_songs_update_time_input.setDecimals(1)
        self.recent_songs_update_time_input.setMinimum(10.000000000000000)
        self.recent_songs_update_time_input.setMaximum(300.000000000000000)

        self.settings_group_layout.addWidget(self.recent_songs_update_time_input, 1, 1, 1, 1)


        self.settings_layout.addWidget(self.settings_group)

        self.system_info_group = QGroupBox(self.settings_container)
        self.system_info_group.setObjectName(u"system_info_group")
        self.system_info_group.setTitle(u"System Information")
        self.system_info_group_layout = QVBoxLayout(self.system_info_group)
        self.system_info_group_layout.setSpacing(8)
        self.system_info_group_layout.setObjectName(u"system_info_group_layout")
        self.system_info_group_layout.setContentsMargins(8, 8, 8, 8)
        self.system_info = QPlainTextEdit(self.system_info_group)
        self.system_info.setObjectName(u"system_info")
        self.system_info.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.system_info.setReadOnly(True)
        self.system_info.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.system_info_group_layout.addWidget(self.system_info)


        self.settings_layout.addWidget(self.system_info_group)

        self.credits_group = QGroupBox(self.settings_container)
        self.credits_group.setObjectName(u"credits_group")
        self.verticalLayout = QVBoxLayout(self.credits_group)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.credits = QPlainTextEdit(self.credits_group)
        self.credits.setObjectName(u"credits")
        self.credits.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.credits.setReadOnly(True)
        self.credits.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.credits)


        self.settings_layout.addWidget(self.credits_group)

        self.settings_navigation = QFrame(self.settings_container)
        self.settings_navigation.setObjectName(u"settings_navigation")
        self.settings_navigation.setFrameShape(QFrame.NoFrame)
        self.settings_navigation_layout = QHBoxLayout(self.settings_navigation)
        self.settings_navigation_layout.setSpacing(8)
        self.settings_navigation_layout.setObjectName(u"settings_navigation_layout")
        self.settings_navigation_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_save_button = QPushButton(self.settings_navigation)
        self.settings_save_button.setObjectName(u"settings_save_button")
        self.settings_save_button.setText(u"Save")

        self.settings_navigation_layout.addWidget(self.settings_save_button)

        self.settings_back_button = QPushButton(self.settings_navigation)
        self.settings_back_button.setObjectName(u"settings_back_button")
        self.settings_back_button.setText(u"Back")

        self.settings_navigation_layout.addWidget(self.settings_back_button)


        self.settings_layout.addWidget(self.settings_navigation, 0, Qt.AlignRight)

        self.settings.setWidget(self.settings_container)

        self.settings_page_layout.addWidget(self.settings)

        self.main_widget.addWidget(self.settings_page)

        self.main_window_layout.addWidget(self.main_widget)

        self.controls_widget = QFrame(self.centralwidget)
        self.controls_widget.setObjectName(u"controls_widget")
        self.controls_widget.setFrameShape(QFrame.NoFrame)
        self.controls_layout = QHBoxLayout(self.controls_widget)
        self.controls_layout.setSpacing(0)
        self.controls_layout.setObjectName(u"controls_layout")
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.play_button = ControlToolButton(self.controls_widget)
        self.play_button.setObjectName(u"play_button")
#if QT_CONFIG(tooltip)
        self.play_button.setToolTip(u"Play")
#endif // QT_CONFIG(tooltip)
        icon1 = QIcon()
        icon1.addFile(u":/icons/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon1)
        self.play_button.setCheckable(True)

        self.controls_layout.addWidget(self.play_button)

        self.volume_button = ControlToolButton(self.controls_widget)
        self.volume_button.setObjectName(u"volume_button")
#if QT_CONFIG(tooltip)
        self.volume_button.setToolTip(u"Mute")
#endif // QT_CONFIG(tooltip)
        icon2 = QIcon()
        icon2.addFile(u":/icons/volume-normal.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.volume_button.setIcon(icon2)
        self.volume_button.setCheckable(True)

        self.controls_layout.addWidget(self.volume_button)

        self.volume_slider = QSlider(self.controls_widget)
        self.volume_slider.setObjectName(u"volume_slider")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_slider.sizePolicy().hasHeightForWidth())
        self.volume_slider.setSizePolicy(sizePolicy)
#if QT_CONFIG(tooltip)
        self.volume_slider.setToolTip(u"Volume")
#endif // QT_CONFIG(tooltip)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(5)
        self.volume_slider.setValue(100)
        self.volume_slider.setOrientation(Qt.Horizontal)

        self.controls_layout.addWidget(self.volume_slider)

        self.controls_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.controls_layout.addItem(self.controls_spacer)

        self.output_device_button = ControlToolButton(self.controls_widget)
        self.output_device_button.setObjectName(u"output_device_button")
#if QT_CONFIG(tooltip)
        self.output_device_button.setToolTip(u"Select Output Device")
#endif // QT_CONFIG(tooltip)
        icon3 = QIcon()
        icon3.addFile(u":/icons/output-device.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.output_device_button.setIcon(icon3)

        self.controls_layout.addWidget(self.output_device_button)

        self.console_button = ControlToolButton(self.controls_widget)
        self.console_button.setObjectName(u"console_button")
#if QT_CONFIG(tooltip)
        self.console_button.setToolTip(u"View Console")
#endif // QT_CONFIG(tooltip)
        icon4 = QIcon()
        icon4.addFile(u":/icons/console.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.console_button.setIcon(icon4)

        self.controls_layout.addWidget(self.console_button)

        self.settings_button = ControlToolButton(self.controls_widget)
        self.settings_button.setObjectName(u"settings_button")
#if QT_CONFIG(tooltip)
        self.settings_button.setToolTip(u"Settings")
#endif // QT_CONFIG(tooltip)
        icon5 = QIcon()
        icon5.addFile(u":/icons/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settings_button.setIcon(icon5)

        self.controls_layout.addWidget(self.settings_button)


        self.main_window_layout.addWidget(self.controls_widget, 0, Qt.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.main_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.credits_group.setTitle(QCoreApplication.translate("MainWindow", u"Credits", None))
        pass
    # retranslateUi

