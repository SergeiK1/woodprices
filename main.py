from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
import seaborn as sns
from tabulate import tabulate

class PriceMonitor:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.threshold = 8.55  # Example threshold value



    def visualize_data(self):
        # Create a 3D bar plot using the preprocessed numeric base values
        unique_base_values = self.data['base(in)'].unique()

        for base_value in unique_base_values:
            subset = self.data[self.data['base(in)'] == base_value]
            plt.figure(figsize=(10, 6))
            sns.barplot(x='height', y='price', data=subset)
            plt.xlabel('Height')
            plt.ylabel('Price')
            plt.title(f'Price Trends for Base {base_value}')
            plt.xticks()
            plt.tight_layout()
            plt.show()

    def check_price_threshold(self, max_record):
        latest_price = max_record['price']

        if latest_price > self.threshold:
            self.send_alert_email(max_record)

    
    def send_alert_email(self, max_record):
        msg = MIMEText(f"Price exceeded the threshold. Max record:\n\n{max_record}")
        msg['Subject'] = 'Price Alert'
        smtp_server = "smtp.gmail.com"
        port = 587
        #YOU NEED TO PUT HERE SENDER EMAIL ADDRESS
        sender = "johnjamesclock@gmail.com"
        #NEED TO PROVIDE APP PASSWORD OF THE ACCOUNT FROM GOOGLE
        password = "JohnJamesClock"
        msg["From"] = sender
        #YOU NEED TO PUT HERE RECIEVER EMAIL ADDRESS
        msg["To"] = "johnjamesclock@gmail.com"

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            #YOU NEED TO PUT HERE SENDER EMAIL ADDRESS
            server.sendmail(sender, "johnjamesclock@gmail.com", msg.as_string())



    def update_data(self, new_data_file, output_file):
        self.new_data = pd.read_csv(new_data_file)

        # Add current date to the new data
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.new_data['date'] = current_date

        # Save the updated dataframe to a new CSV file without column headers
        self.new_data.to_csv(output_file, index=False, header=False, mode='a')



class PriceMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.new_data_file = 'output_example.csv'
        self.root.title("Price Monitor GUI")

        self.data_file = ""
        self.threshold_var = tk.DoubleVar()
        self.date_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Data File:").pack()
        self.data_entry = tk.Entry(self.root, width=50)
        self.data_entry.pack()
        tk.Button(self.root, text="Browse", command=self.browse_data).pack()

        tk.Label(self.root, text="Threshold:").pack()
        self.threshold_entry = tk.Entry(self.root, textvariable=self.threshold_var)
        self.threshold_entry.pack()

        tk.Label(self.root, text="Date (yyyy-mm-dd):").pack()
        self.date_entry = tk.Entry(self.root, textvariable=self.date_var)
        self.date_entry.pack()
        tk.Button(self.root, text="Search", command=self.search_data).pack()

        tk.Button(self.root, text="Visualize Data", command=self.visualize_data).pack()

        tk.Button(self.root, text="Clear", command=self.clear_ui).pack()

        # Create a Text widget with a scrollbar
        self.text_widget = tk.Text(self.root, height=20, width=80)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.root, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=scrollbar.set)
        
    def browse_data(self):
        self.data_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.data_entry.insert(0, self.data_file)
        price_monitor = PriceMonitor(self.data_file)
        
        price_monitor.update_data(self.data_file,self.new_data_file)

    def clear_ui(self):
        self.data_entry.delete(0, tk.END)
        self.threshold_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.text_widget.delete("1.0", tk.END)

    
    def visualize_data(self):
        price_monitor = PriceMonitor(self.data_file)
        unique_base_values = price_monitor.data['base(in)'].unique()

        for base_value in unique_base_values:
            subset = price_monitor.data[price_monitor.data['base(in)'] == base_value]
            table = tabulate(subset, headers='keys', tablefmt='psql')
            self.text_widget.insert(tk.END, f'Price Trends for Base {base_value}:\n{table}\n\n')
        max_record = price_monitor.data.loc[price_monitor.data['price'].idxmax()]
        price_monitor.check_price_threshold(max_record)

    def search_data(self):  
        date_to_search = self.date_var.get()
        if date_to_search:
            data = pd.read_csv(self.new_data_file)
            filtered_data = data[data['date'] == date_to_search]
            if not filtered_data.empty:
                table = tabulate(filtered_data, headers='keys', tablefmt='psql')
                self.text_widget.delete("1.0", "end")  # Clear existing text
                self.text_widget.insert("1.0", table)
            else:
                self.text_widget.delete("1.0", "end")  # Clear existing text
                self.text_widget.insert("1.0", "No data found for the specified date.")

        else:
            self.text_widget.delete("1.0", "end")  # Clear existing text
            self.text_widget.insert("1.0", "Please enter a valid date.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceMonitorGUI(root)
    root.mainloop()