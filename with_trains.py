import numpy as np
import random

# Define the Customer class
class Customer:
    def __init__(self, id):
        self.id = id  # Unique identifier for the customer
        self.arrival_time = 0  # Time at which the customer arrives at the station
        self.interarrival_time = 0  # Time difference between this customer's arrival and the previous customer
        self.service_time = 0  # Total service time for the customer
        self.platform_arrival_time = 0  # Time at which the customer arrives at the platform
        self.wait_time = 0  # Time spent waiting for a train
        self.platform_departure_time = 0  # Time at which the customer departs from the platform
        self.departure_time = 0  # Time at which the customer leaves the system
        self.system_time = 0  # Total time the customer spends in the system

# Define the Train class
class Train:
    def __init__(self, id, departure_time, capacity):
        self.id = id  # Unique train identifier
        self.departure_time = departure_time  # Train departure time
        self.capacity = capacity # Train capacity (number of passengers)
        self.current_load = 0  # Current number of passengers onboard
        self.busy_time = 0  # Total time the train is busy serving customers
        self.idle_time = 0  # Time the train remains idle

# Define the Simulation class
class Simulation:
    def __init__(self, num_customers, interarrival_mean, interarrival_sd, train_interval, train_capacity, num_trains):
        # Customer-related attributes
        self.num_customers = num_customers
        self.interarrival_mean = interarrival_mean
        self.interarrival_sd = interarrival_sd
        self.customers = [Customer(i) for i in range(num_customers)]

        #self.num_offboarding_customers = int((max(0, min(np.random.normal(4, 2), 100)) / 100) * self.num_customers)
        self.train_capacity= train_capacity  #- self.num_offboarding_customers

        # Train-related attributes
        self.train_interval = train_interval
        self.up_train_queue = []  # Queue for customers waiting for up-trains
        self.down_train_queue = []  # Queue for customers waiting for down-trains
        
        
        
        self.num_leaving_customers =int(max(0, np.random.normal(200, 20)))
        self.trains = [Train(i, i * train_interval, int(max(0, np.random.normal(200, 20)))) for i in range(num_trains)]

        # List to store departing customers
        self.departing_customers = []

        # Create departing customers for each train
        for train in self.trains:
            # Create departing customer objects
            for i in range(self.num_leaving_customers):
                departing_customer = Customer(f"D{train.id}_{i}")
                departing_customer.arrival_time = train.departure_time
                self.departing_customers.append(departing_customer)

    def departure_process(self):
        print("\n=== Departure Process ===")
        for customer in self.departing_customers:
            train_id = customer.id.split('_')[0][1:]  # Extract train ID from customer ID
            
            print(f"Departing Customer {customer.id} (from Train {train_id}):")
            print(f"Started exit process at time {customer.arrival_time:.2f}")
            
            # Platform exit
            platform_exit = self.visit_MMcc(20, 2)
            print(f"Departing Customer {customer.id}: Exiting platform took {platform_exit:.2f} seconds")
            
            # Hall exit
            hall_exit = self.visit_MMcc(12, 2)
            print(f"Departing Customer {customer.id}: Walking through hall took {hall_exit:.2f} seconds")
            
            # Random choice between escalator and stairs
            if random.random() < 0.3:
                vertical_exit = self.visit_MGcc(20, 2)  # stairs
                print(f"Departing Customer {customer.id}: Taking stairs took {vertical_exit:.2f} seconds")
            else:
                vertical_exit = self.visit_MMcc(15, 1)  # escalator
                print(f"Departing Customer {customer.id}: Taking escalator took {vertical_exit:.2f} seconds")
                
            # Walkway exit
            walkway_exit = self.visit_MGcc(20, 2)
            print(f"Departing Customer {customer.id}: Walking through Walkway 1 took {walkway_exit:.2f} seconds")
            
            # Out gate
            out_gate = self.visit_MMc()
            print(f"Departing Customer {customer.id}: Passing through Out-Gate took {out_gate:.2f} seconds")
            
            total_exit_time = platform_exit + hall_exit + vertical_exit + walkway_exit + out_gate
            customer.departure_time = customer.arrival_time + total_exit_time
            
            print(f"\nDeparting Customer {customer.id} Final Metrics:")
            print(f"- Started exit at: {customer.arrival_time:.2f}")
            print(f"- Total exit time: {total_exit_time:.2f}")
            print(f"- Final departure: {customer.departure_time:.2f}\n")


    def visit_MMc(self):
        return np.random.exponential(5)  # Example MMc service time

    def visit_MMcc(self, exponential_mean, _):
        return np.random.exponential(exponential_mean)

    def visit_MGcc(self, general_mean, general_sd):
        return max(0, np.random.normal(general_mean, general_sd))

    def arrival_process(self):
        print("\n=== Arrival Process ===")
        for customer in self.customers:
            if customer.id == 0:
                customer.arrival_time = 0
                print(f"Customer {customer.id}: Arrives at the station at time 0.")

            else:
                customer.interarrival_time = max(0, np.random.normal(self.interarrival_mean, self.interarrival_sd))
                customer.arrival_time = self.customers[customer.id - 1].arrival_time + customer.interarrival_time
                print(f"Customer {customer.id}: Arrives at the station at time {customer.arrival_time:.2f}, "
                    f"after an interarrival time of {customer.interarrival_time:.2f}.")


            in_gate_time = self.visit_MMc()
            customer.service_time += in_gate_time
            print(f"Customer {customer.id}: Passing through the In-Gate took {in_gate_time:.2f} seconds.")


            walkway_time = self.visit_MGcc(20, 2)
            customer.service_time += walkway_time
            print(f"Customer {customer.id}: Walking through Walkway 1 took {walkway_time:.2f} seconds.")


            if random.random() < 0.3:
                staircase_time = self.visit_MGcc(20, 2)
                customer.service_time += staircase_time
                print(f"Customer {customer.id}: Choosing the staircase took {staircase_time:.2f} seconds.")

            else:
                escalator_time = self.visit_MMcc(15, 1)
                customer.service_time += escalator_time
                print(f"Customer {customer.id}: Choosing the escalator took {escalator_time:.2f} seconds.")


            hall_time = self.visit_MMcc(12, 2)
            customer.service_time += hall_time
            print(f"Customer {customer.id}: Walking through the hall took {hall_time:.2f} seconds.")




            second_staircase_time = self.visit_MMcc(20, 2)
            customer.service_time += second_staircase_time

            customer.platform_arrival_time = customer.arrival_time + customer.service_time

            print(f"Customer {customer.id} Metrics:")
            print(f"- Arrival Time: {customer.arrival_time:.2f} seconds")
            print(f"- Inter-arrival Time: {customer.interarrival_time:.2f} seconds")
            print(f"- Service Time: {customer.service_time:.2f} seconds")
            print(f"- Platform Arrival Time: {customer.platform_arrival_time:.2f} seconds\n")

    def assign_to_train(self):
        print("\n=== Assigning Customers to Trains ===")
        for customer in self.customers:
            if random.random() < 0.5:
                self.up_train_queue.append(customer)
                print(f"Customer {customer.id} assigned to Up Train queue.")
            else:
                self.down_train_queue.append(customer)
                print(f"Customer {customer.id} assigned to Down Train queue.")

    def train_boarding(self):
        print("\n=== Train Boarding Process ===")
        for i, train in enumerate(self.trains):
            print(f"\nTrain {train.id} - Departure Time: {train.departure_time}, Capacity: {train.capacity}")

            if i > 0:
                train.idle_time = max(0, train.departure_time - self.trains[i - 1].departure_time - train.busy_time)

            print(f"- Idle Time: {train.idle_time:.2f} seconds")

            self.process_queue(train, self.up_train_queue, "Up")
            self.process_queue(train, self.down_train_queue, "Down")

    def process_queue(self, train, queue, direction):
        print(f"\nProcessing {direction} Train {train.id} - Departure Time: {train.departure_time}, Capacity: {train.capacity}")

        # Customers eligible for this train
        eligible_customers = [customer for customer in queue if customer.platform_arrival_time <= train.departure_time]
        num_eligible = len(eligible_customers)
        print(f"{num_eligible} customers are eligible for {direction} Train {train.id}.")

        boarded_customers = []
        remaining_capacity = train.capacity - train.current_load
        num_to_board = min(len(eligible_customers), remaining_capacity)

        for i in range(num_to_board):
            customer = eligible_customers[i]
            print(f"Customer {customer.id} boarded {direction} Train {train.id}. there are now {train.current_load} customers on board and {len(queue) - 1} customers in the queue.")
            customer.wait_time = train.departure_time - customer.platform_arrival_time
            customer.platform_departure_time = train.departure_time
            customer.departure_time = train.departure_time + customer.service_time
            customer.system_time = customer.departure_time - customer.arrival_time

            train.current_load += 1
            train.busy_time += customer.service_time
            boarded_customers.append(customer)

            # Print customer final metrics
            print(f"Customer {customer.id} Metrics:")
            print(f"- Wait Time: {customer.wait_time:.2f} seconds")
            print(f"- Platform Departure Time: {customer.platform_departure_time:.2f} seconds")
            print(f"- Departure Time: {customer.departure_time:.2f} seconds")
            print(f"- System Time: {customer.system_time:.2f} seconds\n")

        # Remove boarded customers from the queue
        for customer in boarded_customers:
            queue.remove(customer)

        remaining_in_queue = len(queue)
        print(f"{len(boarded_customers)} customers boarded {direction} Train {train.id}.")
        print(f"{remaining_in_queue} customers are still waiting for the next {direction} train.")

    def run(self):
        self.arrival_process()
        self.assign_to_train()
        self.train_boarding()
        self.departure_process()

# Example usage
simulation = Simulation(
    num_customers=1000,
    interarrival_mean=30,
    interarrival_sd=5,
    train_interval=5000,
    train_capacity=200,
    num_trains=10,
)
simulation.run()
