from PySide6.QtCharts import QChartView


class ChartViewWidget(QChartView):
    """
    Custom widget that wraps QChartView for use in Qt Designer.
    This is a promoted widget that allows using QChartView in .ui files.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
