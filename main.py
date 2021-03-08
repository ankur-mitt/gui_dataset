import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtWidgets import (QApplication, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QGridLayout, QFileDialog, QPushButton)


class TopBar(QFrame):
    def __init__(self):
        super().__init__()

        # components creation
        image = QLabel()
        image.setPixmap(QPixmap('resources/images/main_logo.png').scaledToHeight(75))  # maintain aspect ratio

        heading = QLabel('GUI to manipulate (add augmentation) and update dataset')
        heading_font = QFont()
        heading_font.setPixelSize(28)
        heading.setFont(heading_font)

        # adding to layout using grid with alignment
        layout = QGridLayout()
        layout.addWidget(image, 0, 0, 1, 1, Qt.AlignCenter)  # 10% space for image
        layout.addWidget(heading, 0, 1, 1, 9, Qt.AlignCenter)  # 90% space for heading

        # load the layout on app
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class PreviewResults(QWidget):
    def __init__(self, image_paths: list):
        super().__init__()

        # create child components
        heading = QLabel('Preview Results')
        heading.setFont(QFont().setPixelSize(20))
        heading.setAlignment(Qt.AlignCenter)

        # issue: QScrollArea not getting activated
        preview_images_container = QScrollArea()
        preview_images_container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        preview_images_container.setWidgetResizable(True)
        # layout to be added to scroll area
        preview_images_layout = QGridLayout()

        preview_image_dimension = 100
        row, col, col_count = 0, 0, 4
        for img_path in image_paths:
            img_label = QLabel()
            img_label.setPixmap(QPixmap(img_path).scaledToWidth(preview_image_dimension))
            preview_images_layout.addWidget(img_label, row, col, 1, 1, Qt.AlignJustify)
            # go to next row and column
            col = int(col + 1)
            row = int(row + int(col / col_count))
            col = int(col - int(col / col_count) * col_count)

        images_widget = QWidget()
        images_widget.setLayout(preview_images_layout)
        preview_images_container.setWidget(images_widget)

        # layout for 'self'
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
        # possible solution: using QtModel and QtStateMachine
        self.image_files_list = user_input  # todo

    def __init__(self):
        super().__init__()

        # issue: state management and component update
        # possible solution: using QtModel and QtStateMachine
        # component state
        self.image_files_list = []      # will be populated later by user
        self.handle_choose_images()     # to be removed later only for testing purpose as state is not getting updated

        # create components
        manipulation_options = QPushButton('Choose images')
        manipulation_options.clicked.connect(self.handle_choose_images)
        manipulation_options.setFixedWidth(500)  # to be removed later

        self.preview_results = PreviewResults(self.image_files_list)

        # add to layout
        layout = QHBoxLayout()
        layout.addWidget(manipulation_options)
        layout.addWidget(self.preview_results)

        # load the layout on the app
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
    main_window.setWindowTitle('Manipulate (add augmentation) and Update Dataset')
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    change_dataset_gui()
