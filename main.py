import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QGridLayout, QFileDialog, QPushButton)


def debug(element):
    element.setStyleSheet('background-color: black;')


class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.resize(1000, 75)

        # components creation
        image = QLabel()
        image.setPixmap(QPixmap('resources/images/main_logo.png').scaled(68, 75))
        image.setFixedWidth(90)
        image.setAlignment(Qt.AlignCenter)

        heading = QLabel(text='<font size=30>GUI to manipulate and update dataset</font>')
        heading.setAlignment(Qt.AlignCenter)

        # adding to layout
        layout = QHBoxLayout()
        layout.addWidget(image)
        layout.addWidget(heading)

        # load the layout on app
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class PreviewResults(QWidget):
    def __init__(self, image_paths: list):
        super().__init__()

        preview_image_dimension = 90

        heading = QLabel(text='<font size=20>Preview Results</font>')
        heading.setAlignment(Qt.AlignCenter)
        preview_images_container = QScrollArea()
        preview_images_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        preview_images_container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        preview_images_layout = QGridLayout()
        preview_images_layout.setContentsMargins(0, 0, 0, 0)
        row, col, col_count = 0, 0, 5
        for img_path in image_paths:
            img_label = QLabel()
            img_label.setPixmap(QPixmap(img_path).scaledToHeight(preview_image_dimension))
            img_label.setFixedSize(preview_image_dimension, preview_image_dimension)
            preview_images_layout.addWidget(img_label, row, col)
            col += 1
            row += int(col / col_count)
            col %= col_count

        preview_images_container.setLayout(preview_images_layout)

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(preview_images_container)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class MainContainer(QFrame):
    @Slot()
    def handle_choose_images(self):
        user_input = QFileDialog.getOpenFileNames(self, 'Choose Images', '', 'Image Files (*.png *.jpeg *.jpg)')[0]
        # issue: state management and component update
        # possible solution: using QtModel
        self.image_files_list = user_input  # todo

    def __init__(self):
        super().__init__()
        self.resize(1000, 550)

        # issue: state management and component update
        # possible solution: using QtModel
        self.image_files_list = []  # will be populated later by user

        # create components
        self.manipulation_options = QPushButton('Choose images')
        self.manipulation_options.setFixedWidth(500)  # to be removed later
        self.manipulation_options.clicked.connect(self.handle_choose_images)
        self.preview_results = PreviewResults(self.image_files_list)

        # todo
        # add to layout
        layout = QHBoxLayout()
        layout.addWidget(self.manipulation_options)
        layout.addWidget(self.preview_results)
        # todo

        # load the layout on the app
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # load all the components
        top_bar = TopBar()
        main_container = MainContainer()

        # add all the components in layout
        layout = QVBoxLayout()
        layout.addWidget(top_bar)
        layout.addWidget(main_container)

        # load the layout on app
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


# GUI to manipulate and update dataset
def change_dataset_gui():
    app = QApplication([])

    # main GUI window
    main_window = MainWindow()
    main_window.resize(1000, 625)
    main_window.setWindowIcon(QIcon('resources/images/app_icon.ico'))
    main_window.setWindowTitle('Manipulate and Update Dataset')
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    change_dataset_gui()
