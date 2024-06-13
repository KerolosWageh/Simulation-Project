import random
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class InventoryManagementSystem:
    def __init__(self, showroom_capacity, inventory_capacity, selling_car_price, shipping_order_cost, holding_car_cost, review_period, simulation_days):
        self.showroomCapacity = showroom_capacity
        self.inventoryCapacity = inventory_capacity
        self.inventory = 3
        self.showroom = 4
        self.order = 5
        self.dayordercome = 2
        self.leadTime = 1

        # Price Parameters
        self.sellingcar = selling_car_price
        self.shippingorder = shipping_order_cost
        self.holdingcar = holding_car_cost

        # Simulation Parameters
        self.reviewPeriod = review_period
        self.simulationDays = simulation_days

        # Simulation Variables
        self.endingUnitsShowroom = []
        self.endingUnitsInventory = []
        self.leadTimelisthis = []
        self.demandlist = []
        self.netProfitdaylist = []
        self.leadTimelist = []
        self.shortageDays = 0
        self.netProfit = 0

        # Demand Probabilities
        self.demandProbabilities = np.array([0.2, 0.34, 0.36, 0.1])

        # Lead Time Probabilities
        self.leadTimeProbabilities = np.array([0.0, 0.4, 0.35, 0.25])

    def refill(self, number):
        if (self.showroom + number) > self.showroomCapacity:
            if (self.inventory + number - (self.showroomCapacity - self.showroom)) > self.inventoryCapacity:
                self.inventory = self.inventoryCapacity
            else:
                self.inventory += number - (self.showroomCapacity - self.showroom)
            self.showroom = self.showroomCapacity
        else:
            self.showroom += number

    def simulate_day(self, day):
        # Demand Simulation
        self.demand = np.random.choice(np.arange(4), p=self.demandProbabilities)

        # Initial Condition for Order
        if self.leadTime == 0:
            if day == self.dayordercome:
                self.leadTime = 0
                self.refill(self.order)
            else:
                self.refill(self.showroomCapacity + self.inventoryCapacity)

        # Shortage Count
        if self.inventory + self.showroom < self.demand:
            self.shortageDays += 1

        # Sell from inventory
        soldFromInventory = min(self.inventory, self.demand)
        self.inventory -= soldFromInventory

        # Sell from showroom if needed
        remainingDemand = self.demand - soldFromInventory
        soldFromShowroom = min(self.showroom, remainingDemand)
        self.showroom -= soldFromShowroom

        # Net Profit
        netProfitday = (((self.demand) * self.sellingcar) if ((self.inventory + self.showroom) > 0) else 0
                        ) - ((self.inventory + self.showroom) * self.holdingcar) - (self.shippingorder if (self.leadTime == 0) else 0)
        self.netProfit += netProfitday

        if (day % self.reviewPeriod == 0) & ((self.showroom + self.inventory) < (2 * (self.showroomCapacity + self.inventoryCapacity) / 3)):
            self.leadTime = np.random.choice(np.arange(4), p=self.leadTimeProbabilities)  # Lead Time Simulation
            self.leadTimelisthis.append(self.leadTime)

        # Ending Units
        self.endingUnitsShowroom.append(self.showroom)
        self.endingUnitsInventory.append(self.inventory)

        self.demandlist.append(self.demand)
        self.netProfitdaylist.append(netProfitday)
        if (self.leadTime < 0):
            self.leadTime = 0
        self.leadTimelist.append(self.leadTime)

        self.leadTime -= 1

    def print_results(self):
        # experimental average demand and lead time
        Experimental_Average_leadTime = sum(self.leadTimelisthis) / len(self.leadTimelisthis)
        Experimental_Average_Demand = sum(self.demandlist) / len(self.demandlist)

        # theoretical average demand and lead time
        theoretical_Average_leadTime = np.sum(self.leadTimeProbabilities * np.arange(4))
        theoretical_Average_Demand = np.sum(self.demandProbabilities * np.arange(4))

        # Average Ending Units
        average_ending_units_showroom = sum(self.endingUnitsShowroom) / len(self.endingUnitsShowroom)
        average_ending_units_inventory = sum(self.endingUnitsInventory) / len(self.endingUnitsInventory)

        # Average Net Profit par Day
        average_netprofit = self.netProfit / self.simulationDays

        # Result
        output = ""
        output += "Average Ending Units in Showroom: {}\n".format(average_ending_units_showroom)
        output += "Average Ending Units in Inventory: {}\n".format(average_ending_units_inventory)
        output += "Shortage Days: {}\n".format(self.shortageDays)
        output += "Average Net Profit per Day: {}\n\n".format(average_netprofit)

        output += "Experimental Average Demand: {}\n".format(Experimental_Average_Demand)
        output += "Theoretical Average Demand: {}\n".format(theoretical_Average_Demand)
        if abs(Experimental_Average_Demand - theoretical_Average_Demand) < 0.1:
            output += "Experimental Average Demand Almost Equal to Theoretical Average Demand\n"
        else:
            output += "Experimental Average Demand Not Equal to Theoretical Average Demand\n"

        output += "\nExperimental Average Lead Time: {}\n".format(Experimental_Average_leadTime)
        output += "Theoretical Average Lead Time: {}\n".format(theoretical_Average_leadTime)
        if abs(Experimental_Average_leadTime - theoretical_Average_leadTime) < 0.1:
            output += "Experimental Average Lead Time Almost Equal to Theoretical Average Lead Time\n"
        else:
            output += "Experimental Average Lead Time Not Equal to Theoretical Average Lead Time\n"

        # Histogram
        plt.hist(self.demandlist, bins=20)
        plt.xlabel("Demand")
        plt.ylabel("Frequency")
        plt.title("Demand Probabilities")
        plt.show()
        plt.close()

        plt.hist(self.leadTimelisthis, bins=20)
        plt.xlabel("Lead Time")
        plt.ylabel("Frequency")
        plt.title("Lead Time Probabilities")
        plt.show()
        plt.close()

        # Print a Table for Simulation Problem
        header = ["Day", "Showroom", "Inventory", "Daily Demand", "Lead Time", "Net Profit Day"]
        Day = list(range(1, self.simulationDays + 1))
        data = list(zip(Day, 
                        self.endingUnitsShowroom, 
                        self.endingUnitsInventory, 
                        self.demandlist, 
                        self.leadTimelist,
                        self.netProfitdaylist))
        output += tabulate(data, headers=header, tablefmt="grid")

        return output

    def run_simulation(self):
        for day in range(1, self.simulationDays + 1):
            self.simulate_day(day)
        result = self.print_results()
        return result

def run_gui():
    def start_simulation():
        try:
            showroom_capacity = int(showroom_entry.get())
            inventory_capacity = int(inventory_entry.get())
            selling_car_price = int(selling_price_entry.get())
            shipping_order_cost = int(shipping_cost_entry.get())
            holding_car_cost = int(holding_cost_entry.get())
            review_period = int(review_period_entry.get())
            simulation_days = int(simulation_days_entry.get())

            inventory_system = InventoryManagementSystem(showroom_capacity, 
                                                        inventory_capacity, 
                                                        selling_car_price,
                                                        shipping_order_cost, 
                                                        holding_car_cost, 
                                                        review_period,simulation_days)
            result = inventory_system.run_simulation()
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Error", "Invalid input values. Please enter valid integer values.")

    root = tk.Tk()
    root.title("Inventory Management System Simulation")
    root.geometry("600x600")

    parameters_frame = ttk.LabelFrame(root, text="Simulation Parameters")
    parameters_frame.pack(padx=40, pady=20)

    showroom_label = ttk.Label(parameters_frame, text="Showroom Capacity:")
    showroom_label.grid(row=0, column=0, padx=5, pady=5)
    showroom_entry = ttk.Entry(parameters_frame)
    showroom_entry.grid(row=0, column=1, padx=5, pady=5)

    inventory_label = ttk.Label(parameters_frame, text="Inventory Capacity:")
    inventory_label.grid(row=1, column=0, padx=5, pady=5)
    inventory_entry = ttk.Entry(parameters_frame)
    inventory_entry.grid(row=1, column=1, padx=5, pady=5)

    selling_price_label = ttk.Label(parameters_frame, text="Selling Car Price:")
    selling_price_label.grid(row=2, column=0, padx=5, pady=5)
    selling_price_entry = ttk.Entry(parameters_frame)
    selling_price_entry.grid(row=2, column=1, padx=5, pady=5)

    shipping_cost_label = ttk.Label(parameters_frame, text="Shipping Order Cost:")
    shipping_cost_label.grid(row=3, column=0, padx=5, pady=5)
    shipping_cost_entry = ttk.Entry(parameters_frame)
    shipping_cost_entry.grid(row=3, column=1, padx=5, pady=5)

    holding_cost_label = ttk.Label(parameters_frame, text="Holding Car Cost:")
    holding_cost_label.grid(row=4, column=0, padx=5, pady=5)
    holding_cost_entry = ttk.Entry(parameters_frame)
    holding_cost_entry.grid(row=4, column=1, padx=5, pady=5)

    review_period_label = ttk.Label(parameters_frame, text="Review Period:")
    review_period_label.grid(row=5, column=0, padx=5, pady=5)
    review_period_entry = ttk.Entry(parameters_frame)
    review_period_entry.grid(row=5, column=1, padx=5, pady=5)

    simulation_days_label = ttk.Label(parameters_frame, text="Simulation Days:")
    simulation_days_label.grid(row=6, column=0, padx=5, pady=5)
    simulation_days_entry = ttk.Entry(parameters_frame)
    simulation_days_entry.grid(row=6, column=1, padx=5, pady=5)

    start_button = ttk.Button(root, text="Start Simulation", command=start_simulation)
    start_button.pack(pady=10)

    result_text = tk.Text(root, height=40, width=140)
    result_text.pack(padx=20, pady=10)

    root.mainloop()

run_gui()