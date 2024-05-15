import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QLineEdit, QTextEdit, QDateTimeEdit, QComboBox
from PyQt5.QtCore import QDateTime, Qt
from database import create_task, read_task, update_task, delete_task, list_tasks, recur_task

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Management App")

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.load_task)
        self.layout.addWidget(self.task_list)

        self.refresh_button = QPushButton("Refresh Tasks")
        self.refresh_button.clicked.connect(self.refresh_tasks)
        self.layout.addWidget(self.refresh_button)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Title")
        self.layout.addWidget(self.title_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.layout.addWidget(self.description_input)

        self.due_date_input = QDateTimeEdit(self)
        self.due_date_input.setDateTime(QDateTime.currentDateTime())
        self.layout.addWidget(self.due_date_input)

        self.priority_input = QLineEdit(self)
        self.priority_input.setPlaceholderText("Priority")
        self.layout.addWidget(self.priority_input)

        self.person_input = QLineEdit(self)
        self.person_input.setPlaceholderText("Person")
        self.layout.addWidget(self.person_input)

        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText("Location")
        self.layout.addWidget(self.location_input)

        self.create_task_button = QPushButton("Create Task")
        self.create_task_button.clicked.connect(self.create_task)
        self.layout.addWidget(self.create_task_button)

        self.update_task_button = QPushButton("Update Task")
        self.update_task_button.clicked.connect(self.update_task)
        self.layout.addWidget(self.update_task_button)

        self.delete_task_button = QPushButton("Delete Task")
        self.delete_task_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_task_button)

        self.selected_task_id = None

        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_list.clear()
        tasks = list_tasks()
        for task in tasks:
            item = QListWidgetItem(f"{task['title']} - {task['description']}")
            item.setData(1000, task.doc_id)
            self.task_list.addItem(item)

    def load_task(self, item):
        task_id = item.data(1000)
        task = read_task(task_id)
        self.selected_task_id = task_id
        self.title_input.setText(task['title'])
        self.description_input.setPlainText(task['description'])
        self.due_date_input.setDateTime(QDateTime.fromString(task['due_date'], Qt.ISODate))
        self.priority_input.setText(str(task['priority']))
        self.person_input.setText(task['person'])
        self.location_input.setText(task['location'])

    def create_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        due_date = self.due_date_input.dateTime().toPyDateTime()
        priority = int(self.priority_input.text())
        person = self.person_input.text()
        location = self.location_input.text()
        task_id = create_task(
            title=title,
            description=description,
            sub_tasks=[],
            attachments=[],
            due_date=due_date,
            priority=priority,
            tags=[],
            person=person,
            location=location,
            recur_interval={}
        )
        self.refresh_tasks()

    def update_task(self):
        if self.selected_task_id is None:
            return
        updates = {
            'title': self.title_input.text(),
            'description': self.description_input.toPlainText(),
            'due_date': self.due_date_input.dateTime().toPyDateTime().isoformat(),
            'priority': int(self.priority_input.text()),
            'person': self.person_input.text(),
            'location': self.location_input.text()
        }
        update_task(self.selected_task_id, updates)
        self.refresh_tasks()

    def delete_task(self):
        if self.selected_task_id is None:
            return
        delete_task(self.selected_task_id)
        self.refresh_tasks()
        self.selected_task_id = None
        self.clear_inputs()

    def clear_inputs(self):
        self.title_input.clear()
        self.description_input.clear()
        self.due_date_input.setDateTime(QDateTime.currentDateTime())
        self.priority_input.clear()
        self.person_input.clear()
        self.location_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
