"""Car service."""


class Car:
    """Represent car model."""

    def __init__(self, color: str, make: str, engine_size: int):
        """
        Car class constructor.

        :param color: car color
        :param make: car make
        :param engine_size: car engine size
        """
        self.color = color
        self.make = make
        self.engine_size = engine_size


class Service:
    """Represent car service model."""

    def __init__(self, name: str, max_car_num: int):
        """
        Service class constructor.

        Car service should also have a database to keep and track all cars standing in queue for repair.
        :param name: service name
        :param max_car_num: max car number service can take for repair at one time
        """
        self.name = name
        self.max_car_num = max_car_num
        self.queue = []

    def can_add_to_service_queue(self, car: Car) -> bool:
        """
        Check if it possible to add car to service queue.

        Car can be added if:
        1. after adding new car, total car number in service does not exceed max_car_number (allowed car number in service)
        2. there is no car with the same color and make present in this service (yes, this world works this way).

        If car can be added, return True. Otherwise return False.
        """
        if len(self.queue) >= self.max_car_num:
            return False

        for existing_car in self.queue:
            if existing_car.color == car.color and existing_car.make == car.make:
                return False

        return True

    def add_car_to_service_queue(self, car: Car):
        """
        Add car to service if it is possible.

        The function does not return anything.
        """
        if self.can_add_to_service_queue(car):
            self.queue.append(car)

    def get_service_cars(self) -> list:
        """Get all cars is service."""
        return self.queue

    def repair(self) -> Car:
        """
        Repair car in service queue.

        Normally, the first car in queue is repaired.
        However, if there is a car in queue which color + make characters length is exactly 13 ->
        this car is chosen and is repaired (might be multiple suitable cars -> choose any).
        After the repair, car is no longer in queue (is removed).
        :return: chosen and repaired car
        """
        selected_car = None
        for car in self.queue:
            if len(car.color + car.make) == 13:
                selected_car = car

        if not selected_car and self.queue:
            selected_car = self.queue[0]

        if selected_car:
            self.queue.remove(selected_car)

        return selected_car

    def get_the_car_with_the_biggest_engine(self) -> list:
        """
        Return a list of cars (car) with the biggest engine size.

        :return: car (cars) with the biggest engine size
        """
        biggest_engine_car = None
        if not self.queue:
            return []

        max_size = max(car.engine_size for car in self.queue)
        return [car for car in self.queue if car.engine_size == max_size]