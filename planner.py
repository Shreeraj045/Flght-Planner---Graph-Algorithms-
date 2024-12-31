from flight import Flight, Heap , LinkedQueue
class Planner:
    def __init__(self, flights):
        self.flights = flights
        self.max_city = max(max(i.start_city,i.end_city) for i in flights) + 2
        self.city_adj_list = [[] for _ in range(self.max_city)]
        for flight in flights: self.city_adj_list[flight.start_city].append(flight)
        self.graph = [[] for _ in range(len(flights))]
        for flight in flights:
            for next_flight in self.city_adj_list[flight.end_city]:
                if self._is_valid_connection(flight, next_flight): self.graph[flight.flight_no].append(next_flight)
    def _is_valid_connection(self, flight1: Flight, flight2: Flight):
        return flight2.departure_time >= flight1.arrival_time + 20
    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city: return []
        optimal_path = [float('inf'), [], float('inf')]
        for start_flight in self.city_adj_list[start_city]:
            if t1 <= start_flight.departure_time  and start_flight.arrival_time <= t2:
                back_track = [None] * len(self.flights)
                path_optimal = [float('inf'), None, float('inf')]
                queue = LinkedQueue()
                visited = [False] * len(self.flights)
                queue.append([start_flight, 0, start_flight.arrival_time])
                visited[start_flight.flight_no] = True
                while not queue.is_empty():
                    current_flight, depth, current_arrival = queue.pop()
                    if depth > path_optimal[0]:
                            break
                    if current_flight.end_city == end_city:
                        if depth < path_optimal[0] or (depth == path_optimal[0] and current_arrival < path_optimal[2]): path_optimal = [depth, current_flight, current_arrival]
                    for next_flight in self.graph[current_flight.flight_no]:
                        if (next_flight.departure_time >= current_flight.arrival_time and next_flight.arrival_time <= t2 and not visited[next_flight.flight_no]):
                            visited[next_flight.flight_no] = True
                            back_track[next_flight.flight_no] = current_flight
                            queue.append([next_flight, depth + 1, next_flight.arrival_time])
                if path_optimal[0] < optimal_path[0] or (
                        path_optimal[0] == optimal_path[0] and path_optimal[2] < optimal_path[2]):
                    good_path = []
                    current = path_optimal[1]
                    while current is not None:
                        good_path.append(current)
                        current = back_track[current.flight_no]
                    optimal_path = [ path_optimal[0], good_path[::-1], path_optimal[2]]
        return optimal_path[1]
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city: return []
        num_flights = len(self.flights)
        distances = [(float('inf'), float('inf'))] * num_flights
        prev_flight = [None] * num_flights
        def flight_cost_comparator(a, b):
            if a[0][0] != b[0][0] : return a[0][0] < b[0][0]
            return a[0][1] < b[0][1]
        pq = Heap(flight_cost_comparator, [])
        for flight in self.city_adj_list[start_city]:
            if t1 <= flight.departure_time and flight.arrival_time <= t2:
                distances[flight.flight_no] = (1, flight.fare)
                pq.insert(((1, flight.fare), flight))
        while len(pq) > 0:
            (current_flights, current_cost), current_flight = pq.extract()
            if current_flight.end_city == end_city:
                path = []
                curr = current_flight
                while curr is not None:
                    path.append(curr)
                    curr = prev_flight[curr.flight_no]
                return path[::-1]
            for next_flight in self.graph[current_flight.flight_no]:
                if next_flight.arrival_time > t2: continue
                new_flights = current_flights + 1
                new_cost = current_cost + next_flight.fare
                current_best = distances[next_flight.flight_no]
                if (new_flights < current_best[0] or(new_flights == current_best[0] and new_cost < current_best[1])):
                    distances[next_flight.flight_no] = (new_flights, new_cost)
                    prev_flight[next_flight.flight_no] = current_flight
                    pq.insert(((new_flights, new_cost), next_flight))
        return []
    def cheapest_route(self, start_city, end_city, t1, t2):
            if start_city == end_city: return []
            num_flights = len(self.flights)
            distances = [float('inf')] * num_flights
            prev_flight = [None] * num_flights
            def fare_comparator(a, b): return a[0] < b[0]
            pq = Heap(fare_comparator, [])
            for flight in self.city_adj_list[start_city]:
                if t1 <= flight.departure_time and flight.arrival_time <= t2:
                    distances[flight.flight_no] = flight.fare
                    pq.insert((flight.fare, flight))
            while len(pq) > 0:
                current_cost, current_flight = pq.extract()
                if current_flight.end_city == end_city:
                    path = []
                    curr = current_flight
                    while curr is not None:
                        path.append(curr)
                        curr = prev_flight[curr.flight_no]
                    return path[::-1]
                for next_flight in self.graph[current_flight.flight_no]:
                    if next_flight.arrival_time > t2: continue
                    new_cost = current_cost + next_flight.fare
                    if new_cost < distances[next_flight.flight_no]:
                        distances[next_flight.flight_no] = new_cost
                        prev_flight[next_flight.flight_no] = current_flight
                        pq.insert((new_cost, next_flight))
            return []