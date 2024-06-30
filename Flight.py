import heapq

class Flight:
    def __init__(self, flight_id, start_city, dest_city, departure_time, arrival_time):
        self.flight_id = flight_id
        self.start_city = start_city
        self.dest_city = dest_city
        self.departure_time = departure_time
        self.arrival_time = arrival_time

class TripPlanner:
    def __init__(self):
        self.cities = set()
        self.flights = {}
        self.adj_list = {}
    
    def add_city(self, city_name):
        self.cities.add(city_name)
        self.adj_list[city_name] = []
    
    def add_flight(self, flight_id, start_city, dest_city, departure_time, arrival_time):
        if start_city not in self.cities or dest_city not in self.cities:
            raise ValueError("City not in database")
        if departure_time >= arrival_time:
            raise ValueError("Invalid departure or arrival times")
        if flight_id in self.flights:
            raise ValueError("Flight ID already exists")
        
        flight = Flight(flight_id, start_city, dest_city, departure_time, arrival_time)
        self.flights[flight_id] = flight
        self.adj_list[start_city].append(flight)
    
    def find_trip(self, start_city, dest_city, departure_time):
        if start_city not in self.cities or dest_city not in self.cities:
            raise ValueError("City not in database")
        
        return self._dijkstra(start_city, dest_city, departure_time)
    
    def _time_to_minutes(self, time):
        hours = time // 100
        minutes = time % 100
        return hours * 60 + minutes

    def _valid_layover(self, arrival, departure):
        layover = self._time_to_minutes(departure) - self._time_to_minutes(arrival)
        if layover >= 120:
            return True
        if layover >= 90:
            return True
        if layover >= 60:
            return True 
        return False
    
    def _dijkstra(self, start_city, dest_city, departure_time):
        pq = [(self._time_to_minutes(departure_time), start_city, [])]
        visited = set()
        
        while pq:
            current_time, current_city, path = heapq.heappop(pq)
            
            if current_city in visited:
                continue
            visited.add(current_city)
            
            if current_city == dest_city:
                return ','.join(path)
            
            for flight in self.adj_list[current_city]:
                if self._time_to_minutes(flight.departure_time) >= current_time:
                    if not path:
                        heapq.heappush(pq, (self._time_to_minutes(flight.arrival_time), flight.dest_city, path + [flight.flight_id]))
                    else:
                        last_flight = path[-1]
                        valid = self._valid_layover(self.flights[last_flight].arrival_time, flight.departure_time)
                        if valid:
                            heapq.heappush(pq, (self._time_to_minutes(flight.arrival_time), flight.dest_city, path + [flight.flight_id]))
        
        return "No Flight Exists"

planner = TripPlanner()

planner.add_city("A")
planner.add_city("B")
planner.add_city("C")
planner.add_city("D")
planner.add_city("E")
planner.add_city('F')

planner.add_flight("J1", "A", "B", 100, 200)
planner.add_flight("J2", "B", "C", 350, 430)
planner.add_flight("J3", "B", "D", 350, 530)
planner.add_flight("J4", "C", "E", 700, 1100)
planner.add_flight("J6", "F", "E", 900, 1000)
planner.add_flight("J7","D","F",700,800)


print(planner.find_trip("A", "E", 100))
