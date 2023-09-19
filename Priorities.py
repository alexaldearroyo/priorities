# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QLabel, QShortcut, QAbstractItemView
from PyQt5.QtCore import Qt, QRectF, QEvent
from PyQt5.QtGui import QPalette, QColor, QPainterPath, QRegion, QKeySequence


class Priorities(QWidget):
    # Main application class

    def __init__(self, app):
        # Initialize the application
        super().__init__()
        
        # Set the application instance
        self.app = app
        self.offset = None
        self.editor = None
        
        # Initialize the user interface
        self.initUI()
        self.app.installEventFilter(self)
        self.listbox.installEventFilter(self)
        self.listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listbox.itemDoubleClicked.connect(self.edit_item)

        self.entry.installEventFilter(self)
        self.app.applicationStateChanged.connect(self.handleStateChange)
        
        # Keyboard shortcuts
        self.shortcutW = QShortcut(Qt.CTRL + Qt.Key_W, self)
        self.shortcutW.activated.connect(self.close)
        self.shortcutM = QShortcut(Qt.CTRL + Qt.Key_M, self)
        self.shortcutM.activated.connect(self.hide)
        self.shortcut = QShortcut(QKeySequence("Shift+Up"), self.listbox)
        self.shortcut.activated.connect(self.handleShiftUp)
        self.shortcutDown = QShortcut(QKeySequence("Shift+Down"), self.listbox)
        self.shortcutDown.activated.connect(self.handleShiftDown)
        
        # Shift navigation variables
        self.startedWithShiftUp = False
        self.startedWithShiftDown = False

    def handleShiftUp(self):
        # Enable shift up navigation
        currentRow = self.listbox.currentRow()
        if currentRow > 0:
            self.startedWithShiftUp = True
            if self.startedWithShiftDown:
                self.listbox.clearSelection()
                self.startedWithShiftDown = False
            previousItem = self.listbox.item(currentRow - 1)
            previousItem.setSelected(True)
            self.listbox.setCurrentRow(currentRow - 1)

    def handleShiftDown(self):
        # Enable shift down navigation
        currentRow = self.listbox.currentRow()
        if currentRow < self.listbox.count() - 1:
            self.startedWithShiftDown = True
            if self.startedWithShiftUp:
                self.listbox.clearSelection()
                self.startedWithShiftUp = False
            nextItem = self.listbox.item(currentRow + 1)
            nextItem.setSelected(True)
            self.listbox.setCurrentRow(currentRow + 1)

    def handleStateChange(self, state):
        # Handle the application state change
        if state == Qt.ApplicationActive:
            self.show()
        
    def initUI(self):
        # Initialize the user interface and set appearance of the interface
        self.initLayout()
        self.initTitleBar()
        self.initListbox()
        self.initEntry()
        self.initButtons()
        self.initWindow()
        
    def initLayout(self):
        # Initialize the main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(0)
        
    def initTitleBar(self):
        # Initialize the title bar
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(0, 0, 0, 0)
        title_bar.setSpacing(7)

        # Close and minimize buttons
        self.close_btn = self.createButton('x', '#FF605C', '#aa0400')
        self.minimize_btn = self.createButton('-', '#FFBD44', '#ba7800')

        # Title text
        self.title_label = QLabel('Priorities')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background:transparent; font-size: 14px;")

        # Add widgets to title bar
        title_bar.addWidget(self.close_btn)
        title_bar.addWidget(self.minimize_btn)
        title_bar.addSpacing(5)
        title_bar.addWidget(self.title_label, 1)
        title_bar.addSpacing(55)

        # Add title bar to main layout
        self.layout.addLayout(title_bar)

        # Empty label for spacing
        empty_label = QLabel()
        empty_label.setFixedHeight(15)
        self.layout.addWidget(empty_label)
        
    def createButton(self, text, bgColor, hoverColor):
        # Create a button with the given text and colors
        btn = QPushButton(text)
        btn.setFixedSize(15, 15)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bgColor};
                border-radius: 7px;
                border: none;
                color: {bgColor};
                font-size: 15px;
            }}
            QPushButton:hover {{
                color: {hoverColor};
            }}
        """)
        return btn
    
    def initListbox(self):
        # Initialize the listbox
        self.listbox = QListWidget()
        self.listbox.setWordWrap(True)
        self.listbox.setTabKeyNavigation(True)
        self.listbox.setSelectionMode(QListWidget.MultiSelection)
        self.listbox.setFocusPolicy(Qt.StrongFocus)
        self.listbox.setStyleSheet("QListWidget {border: none; font-size: 14px; padding: 7px; background-color: transparent}")
        self.listbox.setSpacing(5)

        # Set listbox background color and selection color
        palette = self.listbox.palette()
        palette.setColor(QPalette.Base, Qt.transparent)
        palette.setColor(QPalette.Text, QColor('#2e2e2e'))
        palette.setColor(QPalette.HighlightedText, QColor('#2e2e2e'))
        self.listbox.setPalette(palette)

        # Add listbox to main layout
        self.layout.addWidget(self.listbox)
        self.load_tasks()

        # Set tab order
        palette.setColor(QPalette.Base, QColor('#F5F5F5'))
        palette.setColor(QPalette.Highlight, QColor('#ffdcb8'))
        self.listbox.setPalette(palette)
        
    def initEntry(self):
        # Initialize the text entry box
        self.entry = QLineEdit()
        self.entry.text()
        self.entry.setFocusPolicy(Qt.StrongFocus)
        self.entry.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.entry.setPlaceholderText('                  Enter new priority')

        # Add entry to main layout
        self.layout.addWidget(self.entry)
        self.layout.addSpacing(10)
    
    def initButtons(self):
        # Initialize the bottom buttons
        self.add_btn = QPushButton("+")
        self.add_btn.setFocusPolicy(Qt.StrongFocus)
        self.complete_btn = QPushButton("-")
        self.complete_btn.setFocusPolicy(Qt.StrongFocus)

        # Create a horizontal layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.add_btn)
        buttonsLayout.addWidget(self.complete_btn)

        # Add horizontal layout to the main layout
        self.layout.addLayout(buttonsLayout)

        # Event Bindings
        self.add_btn.clicked.connect(self.add_task)
        self.complete_btn.clicked.connect(self.complete_task)
    
    def initWindow(self):
        # Initialize the window
        self.setLayout(self.layout)
        
        # Event Bindings
        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.hide)

        # Enter on buttons
        self.shortcutEnter = QShortcut(Qt.Key_Return, self)
        self.shortcutEnter.activated.connect(self.onReturnKeyPressed)
    
        # Set window size
        self.resize(300, 325)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Rounded corners
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        # Show Frame
        self.setWindowTitle('Priorities')
        self.show()

        # Set tab order
        self.setTabOrder(self.entry, self.add_btn)
        self.setTabOrder(self.add_btn, self.complete_btn)
        self.setTabOrder(self.complete_btn, self.listbox)

        self.load_tasks()
        self.update_window_color()
    
    def onReturnKeyPressed(self):
        # Events triggered when 'Enter' is pressed
        if self.add_btn.hasFocus():
            self.simulate_add_button_click()
        elif self.complete_btn.hasFocus():
            self.simulate_complete_button_click()
        elif self.entry.hasFocus():
            self.add_task()
        elif self.listbox.hasFocus():
            # 
            self.edit_item()
        elif self.editor and self.editor.hasFocus():
            currentRow = self.listbox.currentRow()
            if self.editor.text():
                self.finish_editing()
                # move focus to next task
                currentRow = self.listbox.currentRow()
                self.listbox.setCurrentRow(currentRow + 1)
            # Else delete current task on self.editor
            else:
                self.finish_editing()
                self.remove_current_task(currentRow)
                
    def remove_current_task(self, currentRow):
        self.listbox.takeItem(currentRow)
        if 0 <= currentRow + 1 < len(self.tasks):
            del self.tasks[currentRow + 1]
            with open("tasks.txt", "w", encoding='utf-8') as file:
                file.write("\n".join(self.tasks))
    
    def eventFilter(self, source, event):
        # Handle events for the application
        
        
        if event.type() == QEvent.KeyPress:
        # Handle key press events
            
            if self.editor and self.editor.hasFocus():
                # If the editor is active, do not change focus to entry
                if event.key() in [Qt.Key_Tab, Qt.Key_Backtab]:
                    return True
                
                elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    self.finish_editing()
                    return True
                return super().eventFilter(source, event)
            
            elif event.text().isalnum():
            # If the event is a key press of an alphanumeric character
                if not self.entry.hasFocus() and (self.editor is None or not self.editor.hasFocus()):
                    self.entry.setFocus()
                    self.entry.setText(self.entry.text() + event.text())
                    return True
            
            elif source is self.listbox:
            # If the listbox is the event source
            
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    self.edit_item()
                    return True
                
                elif event.key() == Qt.Key_Tab:
                    self.listbox.clearSelection()
                    currentRow = self.listbox.currentRow()
                    if currentRow < self.listbox.count() - 1:
                        self.listbox.setCurrentRow(currentRow + 1)
                        return True
                    else:
                        self.entry.setFocus()
                        return True
                    
                elif event.key() == Qt.Key_Down:
                    self.listbox.clearSelection()
                    currentRow = self.listbox.currentRow()
                    if currentRow < self.listbox.count() - 1:
                        self.listbox.setCurrentRow(currentRow + 1)
                    else:
                        self.entry.setFocus()
                    return True
                    
                elif event.key() == Qt.Key_Up:
                    currentRow = self.listbox.currentRow()
                    if currentRow > 0:
                        self.listbox.clearSelection()
                        self.listbox.setCurrentRow(currentRow - 1)
                    return True
                                        
                elif event.key() == Qt.Key_Backtab:
                    self.listbox.clearSelection()
                    currentRow = self.listbox.currentRow()
                    if currentRow > 0:
                        self.listbox.setCurrentRow(currentRow - 1)
                        return True
                    else:
                        self.complete_btn.setFocus()
                        return True
                    
                elif event.key() == Qt.Key_Backspace:
                    self.complete_task()
                    return True
                
            elif source is self.entry:
            # If the entry is the event source
            
                if event.key() == Qt.Key_Backtab:
                    self.listbox.setFocus()
                    self.listbox.setCurrentRow(self.listbox.count() - 1)
                    return True
                elif event.key() == Qt.Key_Up:
                    self.listbox.setFocus()
                    self.listbox.setCurrentRow(self.listbox.count() - 1)
                    return True
              
        elif event.type() == QEvent.MouseButtonPress:
        # Handle mouse button press events
        
            if source is self.minimize_btn:
                self.hide()
                return True
        
        return super().eventFilter(source, event)


    def simulate_add_button_click(self):
        # Simulate a click on the add button
        self.add_btn.click()
        
    def simulate_complete_button_click(self):
        # Simulate a click on the complete button
        self.complete_btn.click()
    
    def remove_last_task(self):
        # Remove last task from list and update listbox and file
        if self.tasks:
            self.tasks.pop()
            self.update_listbox()
            with open("tasks.txt", "w", encoding='utf-8') as file:
                file.write("\n".join(self.tasks))
            self.update_window_color()

    def mousePressEvent(self, event):
        # Enable window movement
        self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        # Enable window movement
       self.move(event.globalPos() - self.offset)

    def load_tasks(self):
        # Read tasks from file
        try:
            with open("tasks.txt", "r", encoding='utf-8') as file:
                tasks = file.readlines()
                self.tasks = [task.strip() for task in tasks]
        except FileNotFoundError:
            self.tasks = []
        
        self.update_listbox()

    def update_listbox(self):
        # Update the task list in the interface
        self.listbox.clear()
        for task in self.tasks:
            self.listbox.addItem(task)

    def add_task(self):
        # Add new task to list
        task = self.entry.text()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            with open("tasks.txt", "a", encoding='utf-8') as file:
                file.write(task + "\n")
            self.entry.clear()
            self.update_window_color()


    def complete_task(self):
        # Remove selected tasks from list and update listbox and file
        
        selected_items = self.listbox.selectedItems()
        last_selected_index = -1
        if selected_items:
            first_selected_index = self.listbox.row(selected_items[0])
            last_selected_index = self.listbox.row(selected_items[-1])
            if first_selected_index > 0:
                self.listbox.setCurrentItem(self.listbox.item(first_selected_index - 1))
            for item in selected_items:
                row = self.listbox.row(item)
                self.listbox.takeItem(row)
                del self.tasks[row]
            with open("tasks.txt", "w", encoding='utf-8') as file:
                file.write("\n".join(self.tasks))
            self.update_window_color()
        elif self.tasks:
            self.listbox.takeItem(0)
            del self.tasks[0]
            with open("tasks.txt", "w", encoding='utf-8') as file:
                file.write("\n".join(self.tasks))
            self.update_window_color()
            if last_selected_index > 0:
                self.listbox.setCurrentRow(last_selected_index - 1)

    def edit_item(self):
        item = self.listbox.currentItem()
        if item is not None:
            self.editor = QLineEdit(self.listbox)
            self.editor.text()
            self.editor.installEventFilter(self)
            self.editor.editingFinished.connect(self.finish_editing)
            self.editor.setFocus()

            rect = self.listbox.visualItemRect(item)
            self.editor.setGeometry(rect.x() + 7, rect.y() + 7, rect.width(), rect.height())
            self.editor.setText(item.text())
            highlight_color = self.listbox.palette().color(QPalette.Highlight).name()
            text_color = self.listbox.palette().color(QPalette.HighlightedText).name()
            self.editor.setStyleSheet(f"background-color: {highlight_color}; color: {text_color}; border: none;")
            self.editor.show()


    def finish_editing(self):
        edited_text = self.editor.text()
        item = self.listbox.currentItem()
        item.setText(edited_text)
        row = self.listbox.row(item)
        self.tasks[row] = edited_text
        with open("tasks.txt", "w", encoding='utf-8') as file:
            file.write("\n".join(self.tasks))
        self.editor.deleteLater()
        self.editor = None
        self.update_window_color()
        self.listbox.currentItem().setSelected(False)
        self.listbox.clearSelection()
        
       
    def update_window_color(self):
        # Update the window color based on the number of tasks
        num_tasks = len(self.tasks)
        text_color = '#2e2e2e'
        if num_tasks < 3:
            color = '#1882C5'  # Blue
            text_color = 'white'
            highlight_color = '#85c7f1' 
        elif num_tasks <= 4:
            color = '#FDC945'  # Yellow
            highlight_color = '#ffdcb8' 
        else:
            color = '#D65156'  # Red
            text_color = 'white'
            highlight_color = '#e17f7a' 
            
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(palette)

        # Update ui colors
        
        self.title_label.setStyleSheet(f"background:transparent; font-size: 14px; color: {text_color}")
        
        self.listbox.setStyleSheet(f"QListWidget {{border: none; font-size: 14px; padding: 7px; background-color: transparent; color: {text_color}}}")
        
        self.entry.setStyleSheet(f"QLineEdit {{background:transparent; border: none; font-size: 14px; color: {text_color}; outline: none; padding-top: 5px; padding-bottom: 5px; padding-left: 12px; padding-right: 12px;}}")
        

        self.add_btn.setStyleSheet(f"QPushButton {{border: none; border-radius: 25px; background-color: transparent; color: {text_color}; font-size: 24px; padding-bottom: 5px}} QPushButton:focus {{ border: 1.5px solid {text_color}; border-radius: 10px}}")
        
        self.complete_btn.setStyleSheet(f"QPushButton {{border: none; border-radius: 25px; background-color: transparent; color: {text_color}; font-size: 24px; padding-bottom: 5px}} QPushButton:focus {{ border: 1.5px solid {text_color}; border-radius: 10px}}")
        
        # Update the highlight color of listbox
        listbox_palette = self.listbox.palette()
        listbox_palette.setColor(QPalette.Highlight, QColor(highlight_color))
        self.listbox.setPalette(listbox_palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Priorities(app)
    sys.exit(app.exec_())