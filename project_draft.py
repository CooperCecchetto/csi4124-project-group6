import numpy as np
import random

class Customer:
    def __init__(self, id):
        self.id = id
        self.arrival_time = 0
        self.interarrival_time = 0
        self.service_time = 0
        self.platform_arrival_time = 0
        self.wait_time = 0
        self.platform_departure_time = 0
        self.departure_time = 0
        self.system_time = 0

class Simulation:
    def __init__(self, num_customers, interarrival_mean, interarrival_sd):
        self.num_customers = num_customers
        self.interarrival_mean = interarrival_mean
        self.interarrival_sd = interarrival_sd
        self.customers = [Customer(i) for i in range(num_customers)]
        self.up_busy_server_remaining_times = []
        self.up_queue_service_times = []
        self.down_busy_server_remaining_times = []
        self.down_queue_service_times = []
        self.up_space_onPlatform = 20
        self.down_space_onPlatform = 20
        self.up_max_num_inQueue = 12
        self.down_max_num_inQueue = 12
        self.up_queue_length = 0
        self.down_queue_length = 0
        self.up_busy_servers = 0
        self.down_busy_servers = 0
        self.platform_arrival_times = []  # Store platform arrival times as an attribute

    def visit_MMc(self):
        return 0

    def visit_MMcc(self, exponential_mean, exponential_sd):
        serv_time = np.random.exponential(exponential_mean, exponential_sd)
        print(f"Generated MMcc Service Time: {serv_time}")
        return serv_time

    def visit_MGcc(self, general_mean, general_sd):
        serv_time = np.random.exponential(general_mean, general_sd)
        print(f"Generated MGcc Service Time: {serv_time}")
        return serv_time

    def arrival_process(self):
        print("\n=== Arrival Process ===")
        for customer in self.customers:
            if customer.id == 0:
                customer.arrival_time = 0
            else:
                customer.interarrival_time = max(0, np.random.normal(self.interarrival_mean, self.interarrival_sd))
                customer.arrival_time = self.customers[customer.id - 1].arrival_time + customer.interarrival_time

            customer.service_time += self.visit_MMc()
            customer.service_time += self.visit_MGcc(20, 2)
            if random.random() < 0.3:
                customer.service_time += self.visit_MGcc(20, 2)
            else:
                customer.service_time += self.visit_MMcc(15, 1)
            customer.service_time += self.visit_MMcc(12, 2)
            customer.service_time += self.visit_MMcc(20, 2)

            customer.platform_arrival_time = customer.arrival_time + customer.service_time
            self.platform_arrival_times.append(customer.platform_arrival_time)

            print(f"Customer {customer.id}: Arrival Time: {customer.arrival_time}, "
                  f"Service Time: {customer.service_time}, Platform Arrival Time: {customer.platform_arrival_time}")
        return self.platform_arrival_times

    def departure_process(self, customer):
        print(f"\n--- Departure Process for Customer {customer.id} ---")
        customer.service_time += self.visit_MGcc(20, 2)
        customer.service_time += self.visit_MMcc(12, 2)
        if random.random() < 0.5:
            if random.random() < 0.3:
                customer.service_time += self.visit_MGcc(20, 2)
            else:
                customer.service_time += self.visit_MMcc(15, 1)
            customer.service_time += self.visit_MMc()
        else:
            if random.random() < 0.3:
                customer.service_time += self.visit_MGcc(20, 2)
            else:
                customer.service_time += self.visit_MMcc(15, 1)
            customer.service_time += self.visit_MMc()

        customer.departure_time = customer.arrival_time + customer.wait_time + customer.service_time
        customer.system_time = customer.departure_time - customer.arrival_time

        print(f"Customer {customer.id}: Departure Time: {customer.departure_time}, System Time: {customer.system_time}")

    def platform_process(self):
        print("\n=== Platform Process ===")
        self.platform_arrival_times = self.arrival_process()

        for customer in self.customers:
            print(f"\nProcessing Customer {customer.id}: Platform Arrival Time: {self.platform_arrival_times[customer.id]}")
            self.departure_process(customer)
            if random.random() < 0.5:
                self.up_train(customer)
            else:
                self.down_train(customer)

            print(f"Customer {customer.id} Final Metrics - Departure Time: {customer.departure_time}, "
                  f"System Time: {customer.system_time}, Wait Time: {customer.wait_time}")

    def up_train(self, customer):
        arrival_time = self.platform_arrival_times[customer.id]
        print(f"\n--- Up Train Process for Customer {customer.id} at time {arrival_time} ---")

        if self.up_busy_servers < self.up_space_onPlatform:
            self.up_busy_servers += 1
            customer.wait_time = 0
            customer.platform_departure_time = arrival_time + customer.service_time
            self.up_busy_server_remaining_times.append(customer.service_time)
            print(f"Customer {customer.id} boarded up train. Departure Time: {customer.platform_departure_time}")
        elif self.up_queue_length < self.up_max_num_inQueue:
            self.up_queue_length += 1
            customer.wait_time = sum(self.up_busy_server_remaining_times) + sum(self.up_queue_service_times)
            customer.platform_departure_time = arrival_time + customer.wait_time + customer.service_time
            self.up_queue_service_times.append(customer.service_time)
            print(f"Customer {customer.id} queued for up train. Wait Time: {customer.wait_time}, "
                  f"Departure Time: {customer.platform_departure_time}")
        else:
            print(f"Customer {customer.id} blocked from boarding up train.")

    def down_train(self, customer):
        arrival_time = self.platform_arrival_times[customer.id]
        print(f"\n--- Down Train Process for Customer {customer.id} at time {arrival_time} ---")

        if self.down_busy_servers < self.down_space_onPlatform:
            self.down_busy_servers += 1
            customer.wait_time = 0
            customer.platform_departure_time = arrival_time + customer.service_time
            self.down_busy_server_remaining_times.append(customer.service_time)
            print(f"Customer {customer.id} boarded down train. Departure Time: {customer.platform_departure_time}")
        elif self.down_queue_length < self.down_max_num_inQueue:
            self.down_queue_length += 1
            customer.wait_time = sum(self.down_busy_server_remaining_times) + sum(self.down_queue_service_times)
            customer.platform_departure_time = arrival_time + customer.wait_time + customer.service_time
            self.down_queue_service_times.append(customer.service_time)
            print(f"Customer {customer.id} queued for down train. Wait Time: {customer.wait_time}, "
                  f"Departure Time: {customer.platform_departure_time}")
        else:
            print(f"Customer {customer.id} blocked from boarding down train.")

# Example usage
simulation = Simulation(num_customers=15, interarrival_mean=30, interarrival_sd=4)
simulation.platform_process()