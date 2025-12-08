from PySide6.QtCharts import QChart, QChartView
from PySide6.QtGui import QPainter


class OpenChart(QChartView):
    """
    Widget personalizado que envuelve QChartView para uso en Qt Designer.
    Es un widget promovido que permite usar gráficas en archivos .ui.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a default chart
        chart = QChart()
        chart.setTitle("Chart")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.setChart(chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
