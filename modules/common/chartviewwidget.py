from PySide6.QtCharts import QChartView


class ChartViewWidget(QChartView):
    """
    Widget personalizado que envuelve QChartView para uso en Qt Designer.
    Es un widget promovido que permite usar QChartView en archivos .ui.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
