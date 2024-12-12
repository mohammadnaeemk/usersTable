from flight.flight_manager import FlightManager  # Corrected import

# Destinations and price per passenger
destinations = ["Tehran", "Yazd", "Abadan", "Kordestan", "Gilan", "Mashhad", "Isfahan", "Shiraz", "Tabriz", "Kish"]
price_per_passenger = 100
filename = "flights.csv"

if __name__ == "__main__":
    manager = FlightManager(filename, destinations, price_per_passenger)  # Corrected instantiation
    manager.start_threads()