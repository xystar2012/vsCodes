class MainForm(QDialog):
    def __init__(self, parent=None):
    super(MainForm, self).__init__(parent)
    self.model = WaterQualityModel(os.path.join(
    os.path.dirname(__file__), "waterdata.csv.gz"))
    self.tableView = QTableView()
    self.tableView.setAlternatingRowColors(True)
    self.tableView.setModel(self.model)
    self.waterView = WaterQualityView()
    self.waterView.setModel(self.model)
    scrollArea = QScrollArea()
    scrollArea.setBackgroundRole(QPalette.Light)
    scrollArea.setWidget(self.waterView)
    self.waterView.scrollarea = scrollArea
    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(self.tableView)
    splitter.addWidget(scrollArea)
    splitter.setSizes([600, 250])
    layout = QHBoxLayout()
    layout.addWidget(splitter)
    self.setLayout(layout)
    self.setWindowTitle("Water Quality Data")
    QTimer.singleShot(0, self.initialLoad)

class WaterQualityView(QWidget):
    FLOWCHARS = (unichr(0x21DC), unichr(0x21DD), unichr(0x21C9))478 Chapter 16. Advanced Model/View Programming
    def __init__(self, parent=None):
    super(WaterQualityView, self).__init__(parent)
    self.scrollarea = None
    self.model = None
    self.setFocusPolicy(Qt.StrongFocus)
    self.selectedRow = -1
    self.flowfont = self.font()
    size = self.font().pointSize()
    if platform.system() == "Windows":
    fontDb = QFontDatabase()
    for face in [face.toLower() for face in fontDb.families()]:
    if face.contains("unicode"):
    self.flowfont = QFont(face, size)
    break
    else:
    self.flowfont = QFont("symbol", size)
    WaterQualityView.FLOWCHARS = (
    chr(0xAC), chr(0xAE), chr(0xDE))

    def setModel(self, model):
        self.model = model
        self.connect(self.model,
        SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
        self.setNewSize)
        self.connect(self.model, SIGNAL("modelReset()"),
        self.setNewSize)
        self.setNewSize()

    def setNewSize(self):
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()

    def minimumSizeHint(self):
        size = self.sizeHint()
        fm = QFontMetrics(self.font())
        size.setHeight(fm.height() * 3)
        return size

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        size = fm.height()
        return QSize(fm.width("9999-99-99 99:99 ") + (size * 4),
        (size / 4) + (size * self.model.rowCount()))

    def paintEvent(self, event):
        if self.model is None:
            return
        fm = QFontMetrics(self.font())
        timestampWidth = fm.width("9999-99-99 99:99 ")
        size = fm.height()
        indicatorSize = int(size * 0.8)
        offset = int(1.5 * (size - indicatorSize))
        minY = event.rect().y()
        maxY = minY + event.rect().height() + size
        minY -= size
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        y = 0
        for row in range(self.model.rowCount()):
            x = 0
            if minY <= y <= maxY:
                painter.save()
                painter.setPen(self.palette().color(QPalette.Text))
            if row == self.selectedRow:
                painter.fillRect(x, y + (offset * 0.8),
                        self.width(), size,
                        self.palette().highlight())
                painter.setPen(self.palette().color(
                     QPalette.HighlightedText))
                timestamp = self.model.data(
                    self.model.index(row, TIMESTAMP)).toDateTime()
                painter.drawText(x, y + size,
                timestamp.toString(TIMESTAMPFORMAT))
            x += timestampWidth
            temperature = self.model.data(
                self.model.index(row, TEMPERATURE))
            temperature = temperature.toDouble()[0]
            if temperature < 20:
                color = QColor(0, 0,
                    int(255 * (20 - temperature) / 20))
            elif temperature > 25:
                color = QColor(int(255 * temperature / 100), 0, 0)
            else:
                color = QColor(0, int(255 * temperature / 100), 0)
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                indicatorSize)
            x += size