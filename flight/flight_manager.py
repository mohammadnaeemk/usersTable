import threading
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os
from matplotlib.widgets import Slider

class FlightManager:
    def __init__(self, filename, destinations, price_per_passenger):
        self.filename = filename
        self.destinations = destinations
        self.price_per_passenger = price_per_passenger
        self.cost_per_flight = random.randint(2000, 10000)  # Simulated cost
        self.lock = threading.Lock()
        self.shared_data = []
        self.columns = ["Origin", "Destination", "Passengers", "Time", "Revenue", "Profit", "Ticket Price"]

        if not os.path.exists(self.filename):
            pd.DataFrame(columns=self.columns).to_csv(self.filename, index=False)

    def generate_flights(self):
        while True:
            origin = random.choice(self.destinations)
            destination = random.choice([city for city in self.destinations if city != origin])
            passengers = random.randint(50, 300)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            revenue = passengers * self.price_per_passenger
            profit = revenue - self.cost_per_flight
            ticket_price = revenue / passengers if passengers > 0 else 0

            flight = [origin, destination, passengers, current_time, revenue, profit, ticket_price]

            try:
                with self.lock:
                    file_exists = os.path.exists(self.filename)
                    df = pd.DataFrame([flight], columns=self.columns)
                    df.to_csv(self.filename, mode='a', header=not file_exists, index=False)
                    self.shared_data.append(flight)
                    print(f"Saved flight: {origin} -> {destination}, Passengers: {passengers}, Revenue: {revenue}, Profit: {profit}, Ticket Price: {ticket_price:.2f}")
            except Exception as e:
                print(f"Error saving to CSV: {e}")

            time.sleep(2)

    def plot_flights(self):
        plt.style.use('dark_background')  # Set dark background
        fig, ax = plt.subplots()
        profit_line, = ax.plot([], [], label='Profit', color='green')

        ax.set_xlim(0, 200)  # Adjust x limits based on expected data
        ax.set_ylim(-5000, 50000)  # Adjust y limits based on expected profit and revenue
        ax.set_xlabel('Flight Index')
        ax.set_ylabel('Profit')
        ax.set_title('Real-Time Flight Profit')
        ax.legend()

        # Slider setup
        slider_ax = fig.add_axes([0.1, 0.01, 0.8, 0.03])
        slider = Slider(slider_ax, 'Number of Trips', 1, 100, valinit=20, valstep=1)

        def update(frame):
            with self.lock:
                if self.shared_data:
                    profit_values = [flight[5] for flight in self.shared_data]
                    flight_indices = range(len(profit_values))

                    limit = int(slider.val)
                    profit_line.set_data(flight_indices[-limit:], profit_values[-limit:])

                    # Calculate and plot average ticket price and duration
                    avg_ticket_price = sum([flight[6] for flight in self.shared_data]) / len(self.shared_data) if self.shared_data else 0
                    avg_profit = sum([flight[5] for flight in self.shared_data]) / len(self.shared_data) if self.shared_data else 0

                    ax.set_title(f'Real-Time Flight Profit\nAvg Ticket Price: {avg_ticket_price:.2f}, Avg Profit: {avg_profit:.2f}')

            return profit_line,

        ani = FuncAnimation(fig, update, interval=1000)
        plt.show()

    def read_flights(self):
        """خواندن داده‌ها از فایل CSV و به‌روزرسانی shared_data"""
        while True:
            try:
                with self.lock:
                    if os.path.exists(self.filename):
                        df = pd.read_csv(self.filename)
                        self.shared_data = df.values.tolist()  # ذخیره داده‌ها به صورت لیست
                        print("Updated shared data:")
                        print(df)  # چاپ تمام داده‌ها
            except Exception as e:
                print(f"Error reading CSV: {e}")
            time.sleep(2)


    def start_threads(self):
        flight_thread = threading.Thread(target=self.generate_flights)
        flight_thread2 = threading.Thread(target=self.read_flights)
        flight_thread.start()
        flight_thread2.start()
        self.plot_flights()  # Call plotting in the main thread

if __name__ == "__main__":
    destinations = ["Tehran", "Yazd", "Abadan", "Kordestan", "Gilan", "Mashhad", "Isfahan", "Shiraz", "Tabriz", "Kish"]
    price_per_passenger = 100
    filename = "flights.csv"
    manager = FlightManager(filename, destinations, price_per_passenger)
    manager.start_threads()