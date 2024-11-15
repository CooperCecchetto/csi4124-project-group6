# Group 6 Project
import numpy as np
import random

num = 15  # Number of customers

# Tables storing data describing simulation results
# Proportion of time waiting line exceeds some value k
# Detect platform capacity >= 100%

# Arrival process data
Arrival_Time = [0] * num  # Time each customer arrived at the system
interarrival_time = [0] * num
Service_Time = [0] * num

# Platform process data
Platform_Arrival_Time = [0] * num
Wait_Time = [0] * num  # Total time customer spends waiting,        Avg Customer Wait-Time
Platform_Departure_Time = [0] * num

# Departure process data
Depart_Arrival_Time = [0] * num
Departure_Time = [0] * num
System_Time = [0] * num  # Total time customer spends in the system   Avg Customer System-Time

# Interrarival time distribution occuring outside of the In-Gates
interarrival_mean = 30
interarrival_sd = 4


def visit_MMc():  # When a customer visits an In-Gate or Out-Gate
    # No queue, and Service Time does not increase?
    return 0


def visit_MMcc(exponential_mean, exponential_sd):
    # No queue, but Service Time increases exponentially distributed
    serv_time = round(np.random.exponential(exponential_mean, exponential_sd))
    return serv_time


def visit_MGcc(general_mean, general_sd):  # ??????How to implement this General Distribution??????
    # No queue, but Service Time increases Generally distributed
    serv_time = round(np.random.exponential(general_mean, general_sd))
    return serv_time


def Arrival_Process(
        i):  # Arrival time is decided, then a sequence of transport nodes adds serviec time. Output time at which customer departs this process
    # Arrival
    if (i == 0):
        Arrival_Time[i] = 0
    else:
        interarrival_time[i] = round(np.random.normal(interarrival_mean,
                                                      interarrival_sd))  # A randome variate for this customer's interarrival time is randomly generated following the normal distribution
        Arrival_Time[i] = Arrival_Time[i - 1] + interarrival_time[i]

    # Service at each Transport Node, adds a certain amount of service time according to the appropriate distribution, but no wait-time as c/c => That there is no queue
    Service_Time[i] += visit_MMc()  # Customers passes through In-Gate
    Service_Time[i] += visit_MGcc(20, 2)  # Walkway 1
    if random.random() < 0.3:  # 30% of the time, the staircase is chosen. The other 70% of customers chose the escalator
        Service_Time[i] += visit_MGcc(20, 2)  # Staircase: Mean=   ; Standard Deviation=
    else:
        Service_Time[i] += visit_MMcc(15, 1)  # Escalator: Mean=   ; Standard Deviation=

    Service_Time[i] += visit_MMcc(12,
                                  2)  # Hall: Mean=   ; Standard Deviation=       ???????Area of Interest: Does merging of queues generate traffic when flow is normal????????????
    Service_Time[i] += visit_MMcc(20, 2)  # Staircase again

    return Arrival_Time[i] + Service_Time[
        i]  # The output designates the time the customers exits the arrival process, equal to the time they arrive at the boarding process
    # &&&Consideration: Multiple service times for arrival/platform/departure processes to seperate for calrity


def Departure_Process(i):  # Calls one of the three visits to expound time serviced, how to do input?

    Service_Time[i] += visit_MGcc(20, 2)  # Staircase: Mean=   ; Standard Deviation=
    Service_Time[i] += visit_MMcc(12, 2)  # Hall: Mean=   ; Standard Deviation=

    if random.random() < 0.5:  # Split between two exits, West or East
        if random.random() < 0.3:  # 30% of the time, the staircase is chosen. The other 70% of customers prefer the efficiency of the escalator
            Service_Time[i] += visit_MGcc(20, 2)  # Staircase: Mean=   ; Standard Deviation=
        else:
            Service_Time[i] += visit_MMcc(15, 1)  # Escalator: Mean=   ; Standard Deviation=
        Service_Time[i] += visit_MMc()  # Customers passes through Out-Gate
    else:
        if random.random() < 0.3:  # 30% of the time, the staircase is chosen. The other 70% of customers chose the escalator
            Service_Time[i] += visit_MGcc(20, 2)  # Staircase: Mean=   ; Standard Deviation=
        else:
            Service_Time[i] += visit_MMcc(15, 1)  # Escalator: Mean=   ; Standard Deviation=
        Service_Time[i] += visit_MMc()  # Customers passes through Out-Gate

    Departure_Time[i] = Arrival_Time[i] + Wait_Time[i] + Service_Time[i]
    System_Time[i] = Departure_Time[i] - Arrival_Time[i]
    return 1


def Platform_Process(i):  # The tricky part, integrate Arrival_Proces output & Offboarding output with Departure input
    Arrival_Time = Platform_Arrival_Time[i]

    print()

    # Outputs Depart_arriv = Platform_arriv + plat_serv_time()


for i in range(0, num):
    # Call arrival process to instantiate Arrival Time, calculate Arrival-Process Service Time to find time at which customer arrives at Platform-Process
    Platform_Arrival_Time[i] = Arrival_Process(i)

    # Call departure process to
    Platform_Departure_Time[i] = Platform_Process(i)

    if random.random() < 0.5:  # uptrain
        Platform_Process(i)
    else:  # downtrain
        Platform_Process(i)

    print()

# Overview of next steps
# 1.Finalize the platform model
# Splitting arrival into two for up/down
# Setting up a reusable alighting-boarding process function for up/down
# Offboarding - Can be viewed as IAT just like normal arrival time, dealt with first
# Boarding - As customers arrive, they enter boarding queue, which is served every mu(service time) ???????How to in code represent multiple people boarding sequentially (many are served at a time) ??????????

# 2.Testing for validation, does the model work how it should. Fine-tuning parameters
# Does each transport gate work correctly, are its parameters well chosen and work well?
# Run simulation, are there any breaks?
# View output, is everything as expected? Correct results that are wildly incorrect/unexpected

# 3.Practical Testing to find the optimization of sought parameters,
# Average customer wait-time,
# Average time a customer spends in the system,
# Proportion of time the waiting line exceeds some value k
# Detect frequency of dangerous capacity (>95% capacity reached)


# Questions
# Q1 Merging of Escalators & Staircases into 1 Hall in Arrival process
# ???????Area of Interest: Does merging of queues generate traffic when flow is normal????????????

# Q2How to implement the General Distribution in visit_M/G/c/c

# Q3 Think about how to handle offboarding ontop of arrival, how to deal with multiple people getting off at once in code?
# Q4 How to handle serving multple people at once, but at the same time (service time distribution is equal)

# Q5 Omar's getting off train queue


# Simulation runtime needs to be atleast min800-1000 observations for confidence interval and prediction interval
# 3 expectations
# Are you trying to implement a comprehensive queueing model
# That the simulation is run for sufficient observations

# Indepth understanding of what is occuring