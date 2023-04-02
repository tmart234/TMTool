import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

# Define the functions for the buttons' actions here
# ...

class TMToolGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TMTool GUI")
        self.setGeometry(100, 100, 800, 400)

        layout = QVBoxLayout()

        template_scripts_label = QLabel("Template Scripts:", self)
        template_scripts_label.setStyleSheet("color: #CCFFCC")
        model_scripts_label = QLabel("Model Scripts:", self)
        model_scripts_label.setStyleSheet("color: #CCE5FF")
        report_scripts_label = QLabel("Report Scripts:", self)
        report_scripts_label.setStyleSheet("color: #CCAAFF")

        template_layout = QVBoxLayout()
        template_layout.addWidget(template_scripts_label)
        template_layout.addWidget(self.create_button("Template -> XLSX", self.open_temp2xlsx))
        template_layout.addWidget(self.create_button("XLSX -> Template", self.open_xlsx2temp))
        template_layout.addWidget(self.create_button("Diff XLSX vs Template", self.open_diff))

        model_layout = QVBoxLayout()
        model_layout.addWidget(model_scripts_label)
        model_layout.addWidget(self.create_button("Set Model Metadata", self.open_metadata))
        model_layout.addWidget(self.create_button("Set Model Assets", self.open_assets))
        model_layout.addWidget(self.create_button("Convert to Threat Dragon", self.open_tmt2TD))

        report_layout = QVBoxLayout()
        report_layout.addWidget(report_scripts_label)
        report_layout.addWidget(self.create_button("Fix broken report hyperlinks", self.open_report_fix))
        report_layout.addWidget(self.create_button("Upload as Jira Issues", self.open_jira_upload))
        report_layout.addWidget(self.create_button("Upload to Confluence", self.upload_confluence))

        main_layout = QHBoxLayout()
        main_layout.addLayout(template_layout)
        main_layout.addLayout(model_layout)
        main_layout.addLayout(report_layout)

        layout.addLayout(main_layout)

        self.setLayout(layout)

    def create_button(self, text, function):
        button = QPushButton(text, self)
        button.clicked.connect(function)
        button.setStyleSheet("font-size: 14px; padding: 10px; background-color: #808080; color: #ffffff;")
        return button

    # Define the functions for the buttons' actions here
    # ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TMToolGUI()
    window.show()
    sys.exit(app.exec_())n__':
    main()
