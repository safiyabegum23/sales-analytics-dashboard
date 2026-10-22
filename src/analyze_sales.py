import pandas as pd

# Load the sales dataset
data = pd.read_csv("data/sales.csv")

# Display the complete dataset
print(data)

# Display the first five records
print("\nFirst five sales records:")
print(data.head())

# Calculate revenue for each order
data["Revenue"] = data["Quantity"] * data["Price"]

# Calculate total revenue
total_revenue = data["Revenue"].sum()

print("\nTotal Sales Revenue:", total_revenue)
# Calculate total profit
total_profit = data["Profit"].sum()
print("\nTotal Profit:", total_profit)

# Revenue by product
product_revenue = data.groupby("Product")["Revenue"].sum()
print("\nRevenue by Product:")
print(product_revenue)

# Revenue by city
city_revenue = data.groupby("City")["Revenue"].sum()
print("\nRevenue by City:")
print(city_revenue)
# Find the product generating the highest revenue
best_product = product_revenue.idxmax()
best_product_revenue = product_revenue.max()

print("\nBest Performing Product:", best_product)
print("Product Revenue:", best_product_revenue)

# Find the city generating the highest revenue
best_city = city_revenue.idxmax()
best_city_revenue = city_revenue.max()

print("\nBest Performing City:", best_city)
print("City Revenue:", best_city_revenue)
# Calculate the total number of orders
total_orders = data["Order_ID"].count()

print("\nTotal Number of Orders:", total_orders)

# Calculate the average order value
average_order_value = data["Revenue"].mean()

print("Average Order Value:", round(average_order_value, 2))

# Calculate profit by product
product_profit = data.groupby("Product")["Profit"].sum()

print("\nProfit by Product:")
print(product_profit)

# Find the most profitable product
best_profit_product = product_profit.idxmax()
highest_profit = product_profit.max()

print("\nMost Profitable Product:", best_profit_product)
print("Highest Product Profit:", highest_profit)
# Calculate overall profit margin
profit_margin = (total_profit / total_revenue) * 100

print("\nOverall Profit Margin:", round(profit_margin, 2), "%")
# Save the analyzed dataset to a CSV file
data.to_csv("reports/sales_analysis.csv", index=False)

print("\nAnalysis results saved successfully!")
# Create a sales summary report
summary = {
    "Total Orders": total_orders,
    "Total Revenue": total_revenue,
    "Total Profit": total_profit,
    "Average Order Value": round(average_order_value, 2),
    "Profit Margin (%)": round(profit_margin, 2),
    "Best Performing Product": best_product,
    "Best Performing City": best_city,
    "Most Profitable Product": best_profit_product
}

# Convert the summary into a table
summary_df = pd.DataFrame([summary])

# Save the summary report
summary_df.to_csv("reports/sales_summary.csv", index=False)

print("\nSales summary report saved successfully!")
import matplotlib.pyplot as plt

# Create a revenue chart by product
product_revenue.plot(kind="bar")

plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.tight_layout()

# Save the chart
plt.savefig("reports/revenue_by_product.png")

print("\nSales chart saved successfully!")
# Create a revenue chart by city
city_revenue.plot(kind="bar")

plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue (₹)")
plt.tight_layout()

# Save the chart
plt.savefig("reports/revenue_by_city.png")

plt.close()

print("\nCity revenue chart saved successfully!")
# Create a profit chart by product
product_profit.plot(kind="bar")

plt.title("Profit by Product")
plt.xlabel("Product")
plt.ylabel("Profit (₹)")
plt.tight_layout()

# Save the chart
plt.savefig("reports/profit_by_product.png")

plt.close()

print("\nProduct profit chart saved successfully!")
# Calculate profit by city
city_profit = data.groupby("City")["Profit"].sum()

# Create a profit chart by city
city_profit.plot(kind="bar")

plt.title("Profit by City")
plt.xlabel("City")
plt.ylabel("Profit (₹)")
plt.tight_layout()

# Save the chart
plt.savefig("reports/profit_by_city.png")

plt.close()

print("\nCity profit chart saved successfully!")
