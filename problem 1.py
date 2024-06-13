import random
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt

class SystemMeasuresModel:
    def __init__(self, initial_regular_length, initial_express_length, initial_average_express_service_time, initial_average_regular_service_time, initial_average_express_waiting_time, initial_average_regular_waiting_time, initial_probability_wait_in_express_queue, intital_express_portion_idle_time, initial_regular_portion_idle_time, initial_time_between_arrivals_comparison, initial_express_service_time_comparison, initial_regular_service_time_comparison, initial_num_of_days):
        self.maximum_regular_length = initial_regular_length
        self.maximum_express_length = initial_express_length
        self.average_express_service_time = initial_average_express_service_time
        self.average_regular_service_time = initial_average_regular_service_time
        self.average_express_waiting_time = initial_average_express_waiting_time
        self.average_regular_waiting_time = initial_average_regular_waiting_time
        self.probability_wait_in_express_queue = initial_probability_wait_in_express_queue
        self.express_portion_idle_time = intital_express_portion_idle_time
        self.regular_portion_idle_time = initial_regular_portion_idle_time
        self.time_between_arrivals_comparison = initial_time_between_arrivals_comparison
        self.express_service_time_comparison = initial_express_service_time_comparison
        self.regular_service_time_comparison = initial_regular_service_time_comparison
        self.num_of_days = initial_num_of_days

def generate_time_between_arrivals():
    random_number = random.random()
    if 0.0 <= random_number < 0.16:
        return 0
    elif 0.16 <= random_number < 0.39:
        return 1
    elif 0.39 <= random_number < 0.69:
        return 2
    elif 0.69 <= random_number < 0.9:
        return 3
    else:
        return 4


def generate_Express_Customers_Service_Time():
    random_number = random.random()
    if 0.0 <= random_number < 0.30:
        return 1
    elif 0.30 <= random_number < 0.70:
        return 2
    elif 0.70 <= random_number < 1:
        return 3


def generate_Regular_Customers_Service_Time():
    random_number = random.random()
    if 0.0 <= random_number < 0.20:
        return 3
    elif 0.20 <= random_number < 0.70:
        return 5
    elif 0.70 <= random_number < 1:
        return 7


# a function to shuffle the type of customers 

def generate_customer_type_list(num_customers, percentage):
    percentage = percentage / 100
    num_express = int(percentage * num_customers)
    num_regular = num_customers - num_express

    customer_list = ["express"] * num_express + ["regular"] * num_regular

    random.shuffle(customer_list)

    return customer_list



def simulate(num_of_customers, percentage, num_of_days):
    total_maximum_express_length = list()
    total_maximum_regular_length = list()
    total_average_express_service_time = list()
    total_average_regular_service_time = list()
    total_average_express_waiting_time = list()
    total_average_regular_waiting_time = list()


    total_avg_time_bit_arrival_list = list()

    for d in range(num_of_days):
        # Inner Loop
        express_count = 0
        regular_count = 0
        express_total_service_time = 0            
        regular_total_service_time = 0            
        express_total_waiting_time = 0            
        regular_total_waiting_time = 0            
        time_between_arrivals = [0.0] * num_of_customers
        arrival_time = [0.0] * num_of_customers
        waiting_time = [0.0] * num_of_customers
        express_queue_list = [0.0] * num_of_customers
        regular_queue_list = [0.0] * num_of_customers
        service_start_time = [0.0] * num_of_customers
        service_time = [0.0] * num_of_customers
        express_queue = 0
        regular_queue = 0
        express_completion_time = [0.0] * num_of_customers
        regular_completion_time = [0.0] * num_of_customers
        customers_type = generate_customer_type_list(num_of_customers, percentage)

        express_service_time = list()
        regular_service_time = list()

        express_waiting_time = list()
        regular_waiting_time = list()

        express_portion_idle_time = 0
        regular_portion_idle_time = 0

        for i in range(num_of_customers):
            time_between_arrivals[i] = generate_time_between_arrivals()
            if i == 0:

                arrival_time[i] = time_between_arrivals[i]
                waiting_time[i] = 0
                express_queue_list[i] = 0
                regular_queue_list[i] = 0

                service_start_time[i] = arrival_time[i]
                # check for customer type
                if customers_type[i] == "express":
                    service_time[i] = generate_Express_Customers_Service_Time()
                    express_completion_time[i] = service_time[i] + service_start_time[i]
                    regular_completion_time[i] = 0
                else:  # if regular
                    service_time[i] = generate_Regular_Customers_Service_Time()
                    express_completion_time[i] = 0
                    regular_completion_time[i] = service_time[i] + service_start_time[i]

            # if he isn't the first customer
            else:
                arrival_time[i] = time_between_arrivals[i] + arrival_time[i - 1]

                if customers_type[i] == "regular":
                    waiting_time[i] = max(regular_completion_time[i - 1] - arrival_time[i], 0)
                    if waiting_time[i] > 0:
                        regular_queue = regular_queue + 1
                    else:
                        # if regular customer
                        if regular_queue != 0:
                            regular_queue = regular_queue - 1
                    express_queue_list[i] = express_queue
                    regular_queue_list[i] = regular_queue
                    service_start_time[i] = arrival_time[i] + waiting_time[i]
                    service_time[i] = generate_Regular_Customers_Service_Time()
                    regular_completion_time[i] = service_start_time[i] + service_time[i]
                    express_completion_time[i] = express_completion_time[i - 1]
                    # if express customer
                else:  ###########################################################################################
                    if regular_queue != 0 and express_queue > 1.5 * regular_queue:
                        waiting_time[i] = max(
                            regular_completion_time[i - 1] - arrival_time[i], 0
                        )
                        customers_type[i] = "Switched to regular"
                        if waiting_time[i] > 0:
                            regular_queue = regular_queue + 1
                        else:
                            if regular_queue != 0:
                                regular_queue = regular_queue - 1
                        express_queue_list[i] = express_queue
                        regular_queue_list[i] = regular_queue
                        service_start_time[i] = arrival_time[i] + waiting_time[i]
                        service_time[i] = generate_Regular_Customers_Service_Time()
                        regular_completion_time[i] = service_start_time[i] + service_time[i]
                        express_completion_time[i] = express_completion_time[i - 1]
                        continue

                    waiting_time[i] = max(express_completion_time[i - 1] - arrival_time[i], 0)
                    if waiting_time[i] > 0:
                        express_queue = express_queue + 1
                    else:
                        if express_queue != 0:
                            express_queue = express_queue - 1
                    express_queue_list[i] = express_queue
                    regular_queue_list[i] = regular_queue
                    service_start_time[i] = arrival_time[i] + waiting_time[i]
                    service_time[i] = generate_Express_Customers_Service_Time()
                    express_completion_time[i] = service_start_time[i] + service_time[i]
                    regular_completion_time[i] = regular_completion_time[i - 1]
                    # Calculate averages and probabilities
            if customers_type[i] == "express":
                express_total_service_time += service_time[i]
                express_total_waiting_time += waiting_time[i]
                express_count += 1
                express_service_time.append(service_time[i])
                express_waiting_time.append(waiting_time[i])
            else:
                regular_total_service_time += service_time[i]
                regular_total_waiting_time += waiting_time[i]
                regular_count += 1
                regular_service_time.append(service_time[i])
                regular_waiting_time.append(waiting_time[i])

        for i in range(num_of_customers):
            if customers_type[i] == "express":
                if service_start_time[i]-express_completion_time[i-1] > 0:
                        express_portion_idle_time += service_start_time[i]-express_completion_time[i-1]
            else:
                    if service_start_time[i]-regular_completion_time[i-1] > 0:
                        regular_portion_idle_time += service_start_time[i]-regular_completion_time[i-1]
        express_portion_idle_time = express_portion_idle_time / max(express_completion_time)
        regular_portion_idle_time = regular_portion_idle_time / max(regular_completion_time) #<<<<<<<<<-------------------------------
        avg_time_bet_arrival =sum(time_between_arrivals) / len(time_between_arrivals)
        total_avg_time_bit_arrival_list.append(avg_time_bet_arrival)
        

        
        

        
        maximum_regular_length = max(regular_queue_list)
        maximum_express_length = max(express_queue_list)
        
        total_maximum_regular_length.append( maximum_regular_length)
        total_maximum_express_length.append(maximum_express_length)

        average_express_service_time = express_total_service_time / express_count if express_count > 0 else 0
        average_regular_service_time = regular_total_service_time / regular_count if regular_count > 0 else 0
        average_express_waiting_time = express_total_waiting_time / express_count if express_count > 0 else 0
        average_regular_waiting_time = regular_total_waiting_time / regular_count if regular_count > 0 else 0
        probability_wait_in_express_queue = express_count / num_of_customers if num_of_customers > 0 else 0
        
        total_average_express_service_time.append(average_express_service_time)
        total_average_regular_service_time.append(average_regular_service_time)
        total_average_express_waiting_time.append(average_express_waiting_time)
        total_average_regular_waiting_time.append(average_regular_waiting_time)

    total_avg_time_bit_arrival = sum(total_avg_time_bit_arrival_list) / len(total_avg_time_bit_arrival_list)
    total_average_express_service_time_int = sum(total_average_express_service_time) / len(total_average_express_service_time)

    total_maximum_regular_length_int = max(total_maximum_regular_length)
    total_maximum_express_length_int = max(total_maximum_express_length)

    total_average_regular_service_time_int = sum(total_average_regular_service_time) / len(total_average_regular_service_time)

    total_average_express_waiting_time_int = sum(total_average_express_waiting_time) / len(total_average_express_waiting_time)
    total_average_regular_waiting_time_int = sum(total_average_regular_waiting_time) / len(total_average_regular_waiting_time)
    
    #theoritical and experiemental comparisons
    time_between_arrivals_comparison = tuple()
    express_service_time_comparison = tuple()
    regular_service_time_comparison = tuple()
    therotical_time_bet_arrivals=1.86
    therotical_avg_exp_service= 2
    therotical_avg_reg_service= 5.2

    if total_average_express_service_time_int == therotical_avg_exp_service:
        express_service_time_comparison = (True, therotical_avg_exp_service)
    else:
        express_service_time_comparison = (False, total_average_express_service_time_int)        

    if total_average_regular_service_time_int == therotical_avg_reg_service:
        regular_service_time_comparison = (True, therotical_avg_reg_service)
    else:
        regular_service_time_comparison = (False, total_average_regular_service_time_int)        

    if total_avg_time_bit_arrival==therotical_time_bet_arrivals:
      time_between_arrivals_comparison = (True, therotical_time_bet_arrivals)
    else :
      time_between_arrivals_comparison = (False, total_avg_time_bit_arrival)
    
    system_measures = SystemMeasuresModel(
    total_maximum_regular_length_int,
    total_maximum_express_length_int,
    total_average_express_service_time_int,
    total_average_regular_service_time_int,
    total_average_express_waiting_time_int,
    total_average_regular_waiting_time_int,
    probability_wait_in_express_queue,
    express_portion_idle_time,
    regular_portion_idle_time,
    time_between_arrivals_comparison,
    express_service_time_comparison,
    regular_service_time_comparison,
    num_of_days
    )

    customers = list(range(1, num_of_customers+1))

    return customers, customers_type, arrival_time, waiting_time, express_queue_list, regular_queue_list, service_start_time, service_time, express_completion_time, regular_completion_time, system_measures, regular_service_time, express_service_time, regular_waiting_time, express_waiting_time

def gui():
    
    def measures_frame(measures, title):
        measures_frame = tk.Toplevel()
        measures_frame.title("System Measures")
        width = 700
        height = 400
        measures_frame.geometry(f"{width}x{height}")

        measures_frame.columnconfigure(0)
        measures_frame.columnconfigure(1)

        frame_title = tk.Label(measures_frame, text=title, font=('Arial', 20))
        frame_title.grid(row=0, columnspan=2)

        label1_description = tk.Label(measures_frame, text="maximum regular Queue length : ")
        label1 = tk.Label(measures_frame, text=measures.maximum_regular_length)
        label1.grid(row=1, column=1)
        label1_description.grid(row=1, column=0)

        description_label2 = tk.Label(measures_frame, text="maximum express Queue length : ")
        label2 = tk.Label(measures_frame, text=measures.maximum_express_length)
        label2.grid(row=2, column=1)
        description_label2.grid(row=2, column=0)

        label3_description = tk.Label(measures_frame, text="average express service time : ")
        label3 = tk.Label(measures_frame, text=measures.average_express_service_time)
        label3.grid(row=3, column=1)
        label3_description.grid(row=3, column=0)

        label4_description = tk.Label(measures_frame, text="average regular service time : ")
        label4 = tk.Label(measures_frame, text=measures.average_regular_service_time)
        label4.grid(row=4, column=1)
        label4_description.grid(row=4, column=0)

        label5_description = tk.Label(measures_frame, text="average express waiting time :")
        label5 = tk.Label(measures_frame, text=measures.average_express_waiting_time)
        label5.grid(row=5, column=1)
        label5_description.grid(row=5, column=0)

        label6_description = tk.Label(measures_frame, text="average regular waiting time")
        label6 = tk.Label(measures_frame, text=measures.average_regular_waiting_time)
        label6.grid(row=6, column=1)
        label6_description.grid(row=6, column=0)

        label7_description = tk.Label(measures_frame, text="probability wait in express queue : ")        
        label7 = tk.Label(measures_frame, text=measures.probability_wait_in_express_queue)
        label7.grid(row=7, column=1)
        label7_description.grid(row=7, column=0)

        label8_description = tk.Label(measures_frame, text="express portion idle time : ")        
        label8 = tk.Label(measures_frame, text=measures.express_portion_idle_time)
        label8.grid(row=8, column=1)
        label8_description.grid(row=8, column=0)

        label9_description = tk.Label(measures_frame, text="regular portion idle time : ")        
        label9 = tk.Label(measures_frame, text=measures.probability_wait_in_express_queue)
        label9.grid(row=9, column=1)
        label9_description.grid(row=9, column=0)
        
        #theoritical and experiemental average time between arrivals comparison
        time_between_arrivals_comparison_tuple = measures.time_between_arrivals_comparison
        if (time_between_arrivals_comparison_tuple[0] == True):
            # matched labels
            label10 = tk.Label(measures_frame, text="Average Time between Arrivals matches the Theoritical Averae time between Arrivals : "+ str(time_between_arrivals_comparison_tuple[1]) +".", foreground="green")
            label10.grid(row=10, column=0, columnspan=2, pady=20)
        else:
            # not matched labels
            label10 = tk.Label(measures_frame, text="Average Time between Arrivals "+ str(time_between_arrivals_comparison_tuple[1]) + " does not match the Theoritical Averae time between Arrivals : '1.86'", foreground="red")
            label10.grid(row=10, column=0, columnspan=2, pady=20)

        #theoritical and experiemental average service time comparison
        express_service_time_comparison_tuple = measures.express_service_time_comparison
        regular_service_time_comparison_tuple = measures.regular_service_time_comparison
        if (express_service_time_comparison_tuple[0] == True):
            # matched labels
            label11 = tk.Label(measures_frame, text="Average Express service time matches the Theoritical Average express service time : "+ str(express_service_time_comparison_tuple[1]) +".", foreground="green")
            label11.grid(row=11, column=0, columnspan=2, pady=20)
        else:
            # not matched labels
            label11 = tk.Label(measures_frame, text="Average Express Service Time "+ str(express_service_time_comparison_tuple[1]) + " does not match the Theoritical Average express Service Time : '2'", foreground="red")
            label11.grid(row=11, column=0, columnspan=2, pady=20)
            
        if (regular_service_time_comparison_tuple[0] == True):
            # matched labels
            label12 = tk.Label(measures_frame, text="Average Regular service time matches the Theoritical Average Regular service time : "+ str(regular_service_time_comparison_tuple[1]) +".", foreground="green")
            label12.grid(row=12, column=0, columnspan=2, pady=20)
        else:
            # not 2atched labels
            label12 = tk.Label(measures_frame, text="Average Regular Service Time "+ str(regular_service_time_comparison_tuple[1]) + " does not match the Theoritical Average Regular Service Time : '5.2'", foreground="red")
            label12.grid(row=12, column=0, columnspan=2, pady=20)
            
        

    def draw_histogram(list, xlable, ylable, color):
        plt.hist(list, bins=7, edgecolor=color)

        plt.xlabel(xlable)
        plt.ylabel(ylable)
        plt.title(xlable)
        plt.show()
 
    
    def submit():
        num_of_customers =  int(customers_text_input.get("1.0", "end-1c"))
        express_percentage =  int(percentage_text_input.get("1.0", "end-1c"))
        num_of_days_sim =  int(days_input.get("1.0", "end-1c"))
        _customers, _customers_type, _arrival_time, _waiting_time, _express_queue_list, _regular_queue_list, _service_start_time, _service_time, _express_completion_time, _regular_completion_time, measures, _regular_service_time, _express_service_time, _regular_waiting_time, _express_waiting_time  =simulate(num_of_customers, express_percentage, num_of_days_sim)
        
        
        measures_frame(measures, "Express Customers 60%")
            
        if express_percentage != 60:
            variables = simulate(num_of_customers, express_percentage, num_of_days_sim)
            new_measures = variables[10]
            measures_frame(new_measures, "Express Customers "+ str(express_percentage)+"%")
        
        for i in range (num_of_customers):
            customer_num = _customers[i]
            customer_type = _customers_type[i]
            customer_arrival_time = _arrival_time[i]
            customer_waiting_time = _waiting_time[i]
            system_express_queue_list = _express_queue_list[i]
            system_regular_queue_list = _regular_queue_list[i]
            system_service_start_time = _service_start_time[i]
            system_service_time = _service_time[i]
            system_express_completion_time = _express_completion_time[i]
            system_regular_completion_time = _regular_completion_time[i]

            data = (customer_num, 
                    customer_type, 
                    customer_arrival_time, 
                    customer_waiting_time, 
                    system_express_queue_list, 
                    system_regular_queue_list, 
                    system_service_start_time,
                    system_service_time,
                    system_express_completion_time,
                    system_regular_completion_time
                )
            table.insert(parent='', index=i, values=data)
            
        
        draw_histogram(_regular_service_time, "regular srvice time", "frequency", "red")
        draw_histogram(_express_service_time, "express srvice time", "frequency", "blue")
        
        draw_histogram(_regular_waiting_time, "regular waiting time", "frequency", "red")
        draw_histogram(_express_waiting_time, "express waiting time", "frequency", "blue")
        
            
    def on_vertical_scroll(*args):
        table.yview(*args)

    def on_horizontal_scroll(*args):
        table.xview(*args)

    root = tk.Tk()
    root.title("SImulation")
    width = 900
    height = 900
    root.geometry(f"{width}x{height}")
    label = tk.Label(root, text="Cashier Simulator", font=('Arial', 18))
    label.pack(padx=10, pady=10)

    inputFrame = tk.Frame(root)
    inputFrame.columnconfigure(0)
    inputFrame.columnconfigure(1)
    inputFrame.columnconfigure(2)
    inputFrame.columnconfigure(3)

    text_label = tk.Label(inputFrame, text="Insert Number of Customers", font=('Arial', 13))
    text_label.grid(row=0, column=0, padx=(0, 15))

    customers_text_input = tk.Text(inputFrame, font=('Arial', 13), height=1, width=25)
    customers_text_input.grid(row=0, column=1)

    days_label = tk.Label(inputFrame, text="Number of Simulation Days :", font=('Arial', 13))
    days_label.grid(row=0, column=2, padx=(15, 15),)

    days_input = tk.Text(inputFrame, font=('Arial', 13), height=1, width=5)
    days_input.grid(row=0, column=3)
    
    percentage_text_label = tk.Label(inputFrame, text="Insert Express Customers Percentage", font=('Arial', 13))
    percentage_text_label.grid(row=1, column=0)
    
    percentage_text_input = tk.Text(inputFrame, font=('Arial', 13), height=1, width=9)
    percentage_text_input.insert("1.0", 60)
    percentage_text_input.grid(row=1, column=1) 


    submit_button = tk.Button(inputFrame, text="Start Simulation", command=submit)
    # submit_button.pack(pady=5)
    submit_button.grid(row=1, column=2, pady=15)
    
    inputFrame.pack(padx=20, pady=10)
    #Table Part
    header_list = ["Customer", "Customer Type", "arrival Time",
        "Waiting Time",
        "express Queue",
        "regular Queue",
        "Service Start Time",
        "Service Time",
        "Express Completion Time",
        "Regular Completion Time",]
    table_columns = ("Customer", "Customer Type", "arrival Time",
        "Waiting Time",
        "express Queue",
        "regular Queue",
        "Service Start Time",
        "Service Time",
        "Express Completion Time",
        "Regular Completion Time",)
    
    table = ttk.Treeview(root, columns=table_columns, show="headings")

    for heading in header_list:
        table.heading(heading, text=(heading))

    # Create Vertical Scrollbar
    vsb = ttk.Scrollbar(root, orient="vertical", command=on_vertical_scroll)
    vsb.pack(side="right", fill="y")

    # Create Horizontal Scrollbar
    hsb = ttk.Scrollbar(root, orient="horizontal", command=on_horizontal_scroll)
    hsb.pack(side="bottom", fill="x")

    # Configure TreeView to use Scrollbars
    table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    table.pack(expand=True, fill="both")

    root.mainloop()
    # measures_frame.mainloop()

if __name__ == "__main__":
    gui()
