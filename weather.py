import sys
import requests
from PyQt5.QtWidgets import  QApplication, QMainWindow, QPushButton,QLabel, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt

class Weather_report(QMainWindow):
    def __init__(self):
        super().__init__()
        self.API_KEY = "b4cb35c73ce52f5eb30531954cede6ee"
        self.setWindowTitle("Weather Report")
        self.setGeometry(300, 200, 420, 450)
        self.title = QLabel("Weather App")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        """)
        self.label1 = QLabel("Enter City Name")
        self.label1.setStyleSheet("font-size: 14px;")
        self.textbox1 = QLineEdit()
        self.textbox1.setPlaceholderText("e.g. Delhi")
        self.textbox1.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            border-radius: 6px;
        """)
        self.b = QPushButton("Get Weather 🌤️")
        self.b.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 10px;
            font-size: 15px;
            border-radius: 8px;
        """)
        self.b.clicked.connect(self.get_weather)
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("""
            font-size: 16px;
            margin-top: 15px;
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addSpacing(10)
        layout.addWidget(self.label1)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.b)
        layout.addWidget(self.result_label)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    def get_weather(self):
        city = self.textbox1.text()
        if not city:
            self.result_label.setText("⚠️ Please enter a city name")
            return
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] != 200:
                self.result_label.setText("❌ City not found")
                return
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"]
            description = data["weather"][0]["description"].title()
            emoji = self.get_weather_emoji(condition)
            weather_info = f"""
{emoji}  {city.upper()}
🌡 Temperature: {temp}°C
💧 Humidity: {humidity}%
☁ Condition: {description}
"""
            self.result_label.setText(weather_info)
        except Exception:
            self.result_label.setText("⚠️ Error fetching data")
    def get_weather_emoji(self, condition):
        if condition == "Clear":
            return "☀️"
        elif condition == "Clouds":
            return "☁️"
        elif condition == "Rain":
            return "🌧️"
        elif condition == "Drizzle":
            return "🌦️"
        elif condition == "Thunderstorm":
            return "⛈️"
        elif condition == "Snow":
            return "❄️"
        else:
            return "🌫️"

def main():
    app = QApplication(sys.argv)
    window = Weather_report()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
