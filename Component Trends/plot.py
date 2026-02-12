import pandas as pd
import matplotlib.pyplot as plt

def plot_my_data():
    df = pd.read_csv("ebay_hardware_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    plt.figure(figsize=(10, 5))
    
    # Plot the Average
    plt.plot(df['Date'], df['Avg_Price'], marker='o', label='Market Average', color='blue')
    
    # Fill the area between the Low and High prices (The Market Spread)
    plt.fill_between(df['Date'], df['Floor_Price'], df['Ceiling_Price'], 
                     alpha=0.2, color='blue', label='Price Spread (Low/High)')

    plt.title("DDR5 32GB RAM: Live Market Tracking")
    plt.ylabel("Price ($)")
    plt.xlabel("Date")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("market_status.png")
    plt.show()

if __name__ == "__main__":
    plot_my_data()