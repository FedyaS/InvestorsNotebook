import os
import sys
from datetime import datetime

# Constants
STOCK_NAME = "GameStop"
DATA_FILE = "stock_data.txt"
LOG_FILE = "log.txt"

# Function to log errors
def log_error(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

# Function to read the last recorded price
def read_last_price():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            if not lines:
                return None
            last_line = lines[-1]
            return float(last_line.split()[1])
    except Exception as e:
        log_error(f"Error reading last price: {e}")
        return None

# Function to write the current price to the data file
def write_current_price(current_price):
    try:
        with open(DATA_FILE, "a") as file:
            file.write(f"{datetime.now().date()} {current_price}\n")
    except Exception as e:
        log_error(f"Error writing current price: {e}")

# Function to calculate percentage change
def calculate_percentage_change(old_price, new_price):
    try:
        return ((new_price - old_price) / old_price) * 100
    except ZeroDivisionError:
        return float('inf')
    except Exception as e:
        log_error(f"Error calculating percentage change: {e}")
        return None

# Function to display results in color
def display_result(current_price, change, percent_change):
    if change > 0:
        color_start = "\033[92m"  # Green
    else:
        color_start = "\033[91m"  # Red
    color_end = "\033[0m"  # Reset color

    print(f"Current price: {current_price}")
    print(f"{color_start}Change: {change:.2f}{color_end}")
    print(f"{color_start}Percent change: {percent_change:.2f}%{color_end}")

# Main function to handle the workflow
def main():
    try:
        last_price = read_last_price()
        current_price = float(input(f"Enter the current price for {STOCK_NAME}: "))
        write_current_price(current_price)

        if last_price is not None:
            change = current_price - last_price
            percent_change = calculate_percentage_change(last_price, current_price)
            display_result(current_price, change, percent_change)
        else:
            print("No previous data available. Current price recorded.")
    except ValueError:
        log_error("Invalid input. Please enter a valid number.")
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        print("An unexpected error occurred. Please check the log file.")

if __name__ == "__main__":
    main()
