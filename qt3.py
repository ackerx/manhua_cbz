import os
import zipfile
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QMessageBox

class FolderZipper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件夹打包工具')
        self.setGeometry(100, 100, 400, 300)

        self.root_label = QLabel('根目录:')
        self.root_line = QLineEdit()
        self.root_button = QPushButton('选择根目录')
        self.root_button.clicked.connect(self.selectRootDir)

        self.output_label = QLabel('输出目录:')
        self.output_line = QLineEdit()
        self.output_button = QPushButton('选择输出目录')
        self.output_button.clicked.connect(self.selectOutputDir)

        self.start_button = QPushButton('开始处理')
        self.start_button.clicked.connect(self.startProcessing)

        self.log_label = QLabel('日志:')
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.root_label)
        vbox.addWidget(self.root_line)
        vbox.addWidget(self.root_button)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_line)
        vbox.addWidget(self.output_button)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.log_label)
        vbox.addWidget(self.log_text)

        self.setLayout(vbox)

    def selectRootDir(self):
        root_dir = QFileDialog.getExistingDirectory(self, '选择根目录')
        self.root_line.setText(root_dir)

    def selectOutputDir(self):
        output_dir = QFileDialog.getExistingDirectory(self, '选择输出目录')
        self.output_line.setText(output_dir)

    def listFolders(self, root_dir):
        folders = []
        for root, dirs, files in os.walk(root_dir):
            for dir in dirs:
                folders.append(os.path.join(root, dir))
        return folders

    def createCBZ(self, folders, output_dir):
        for folder in folders:
            folder_name = os.path.basename(folder)
            output_path = os.path.join(output_dir, f"{folder_name}.zip")
            zip_path = os.path.join(output_dir, f"{folder_name}.cbz")

            with zipfile.ZipFile(output_path, 'w') as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, folder))

            os.rename(output_path, zip_path)
            log_message = f"生成文件: {zip_path}\n"
            self.log_text.append(log_message)

        QMessageBox.information(self, '生成完成', '文件夹打包完成！')

    def startProcessing(self):
        root_dir = self.root_line.text()
        output_dir = self.output_line.text()
        if root_dir and output_dir:
            folders = self.listFolders(root_dir)
            self.createCBZ(folders, output_dir)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderZipper()
    ex.show()
    sys.exit(app.exec_())