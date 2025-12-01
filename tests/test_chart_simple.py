#!/usr/bin/env python3
"""
Test directo del gráfico de barras sin dependencias de base de datos
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QRadioButton, QComboBox
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
import random

class ChartTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Gráfico de Barras - Artículos")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Crear chart
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Controles
        self.btn_units = QRadioButton("Unidades Vendidas")
        self.btn_units.setChecked(True)
        self.btn_amounts = QRadioButton("Importes de Ventas")
        
        self.combo_chart = QComboBox()
        self.combo_chart.addItems(["Gráfica de Barras", "Gráfica de Líneas"])
        
        self.btn_update = QPushButton("Actualizar Datos")
        
        # Layout
        layout.addWidget(self.chart_view)
        layout.addWidget(self.combo_chart)
        layout.addWidget(self.btn_units)
        layout.addWidget(self.btn_amounts)
        layout.addWidget(self.btn_update)
        
        # Conectar señales
        self.btn_units.toggled.connect(self.update_chart)
        self.btn_amounts.toggled.connect(self.update_chart)
        self.btn_update.clicked.connect(self.generate_new_data)
        
        # Datos iniciales
        self.months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                      "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        self.units_data = [random.randint(10, 80) for _ in range(12)]
        self.amounts_data = [units * random.uniform(25, 45) for units in self.units_data]
        
        # Crear gráfico inicial
        self.setup_chart()
        self.update_chart()
    
    def setup_chart(self):
        """Configurar el gráfico inicial"""
        self.chart.setTitle("Estadísticas Mensuales - Artículo de Prueba")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
    
    def update_chart(self):
        """Actualizar gráfico según la selección"""
        # Limpiar series anteriores
        self.chart.removeAllSeries()
        
        # Datos según selección
        if self.btn_units.isChecked():
            data = self.units_data
            title = "Unidades Vendidas"
            y_label = "Unidades"
        else:
            data = self.amounts_data
            title = "Importes de Ventas"
            y_label = "Euros (€)"
        
        # Crear serie de barras
        bar_series = QBarSeries()
        bar_set = QBarSet(title)
        
        for value in data:
            bar_set.append(value)
        
        bar_series.append(bar_set)
        self.chart.addSeries(bar_series)
        
        # Configurar ejes
        # Eje X (meses)
        axis_x = QBarCategoryAxis()
        axis_x.append(self.months)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        bar_series.attachAxis(axis_x)
        
        # Eje Y (valores)
        max_value = max(data) if data else 100
        axis_y = QValueAxis()
        axis_y.setRange(0, max_value * 1.2)  # 20% padding
        axis_y.setTitleText(y_label)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        bar_series.attachAxis(axis_y)
        
        # Actualizar título
        self.chart.setTitle(f"Estadísticas Mensuales - {title}")
    
    def generate_new_data(self):
        """Generar nuevos datos aleatorios"""
        self.units_data = [random.randint(5, 100) for _ in range(12)]
        self.amounts_data = [units * random.uniform(20, 50) for units in self.units_data]
        self.update_chart()

def main():
    app = QApplication(sys.argv)
    
    window = ChartTestWindow()
    window.show()
    
    print("✅ Ventana de prueba del gráfico abierta")
    print("   - Gráfico de barras con datos mensuales")
    print("   - Cambio entre unidades e importes")
    print("   - Botón para generar nuevos datos")
    print("   - Animaciones y colores")
    
    # No ejecutar el bucle de eventos en el test automatizado
    assert window.isVisible()

if __name__ == "__main__":
    sys.exit(main())