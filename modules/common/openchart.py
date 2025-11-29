from PySide6.QtCharts import QChart, QChartView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter


class OpenChart(QChartView):
    """
    Custom chart widget that wraps QChartView for use in Qt Designer.
    This is a promoted widget that allows using charts in .ui files.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a default chart
        chart = QChart()
        chart.setTitle("Chart")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
