import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

hour_df_cleaned = pd.read_csv("dashboard/hour_df_cleaned.csv")

st.title("🚴‍♂️ Bike Sharing Usage Dashboard 🚴‍♀️")

st.markdown(
    """
Welcome to the **Bike Sharing Usage Dashboard**! Here, you can explore how time, holidays, and user types impact the usage of bikes in a bike-sharing system.

Use the filters below to interact with the data, and uncover insights to optimize operations for better efficiency and customer experience.
"""
)

st.sidebar.header("Filter Data")
selected_hour_range = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))
selected_month = st.sidebar.multiselect(
    "Select Months", range(1, 13), default=range(1, 13)
)

filtered_data = hour_df_cleaned[
    (hour_df_cleaned["hr"] >= selected_hour_range[0])
    & (hour_df_cleaned["hr"] <= selected_hour_range[1])
    & (hour_df_cleaned["mnth"].isin(selected_month))
]

st.header("📊 Insights from Bike Sharing Data")

st.subheader("1. How does time (hour and month) affect bike usage trends?")

st.write("### Hourly Bike Usage")
hourly_usage = filtered_data.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(
    x=hourly_usage.index, y=hourly_usage.values, ax=ax, color="blue", marker="o"
)
ax.set_title("Average Bike Usage by Hour", fontsize=14)
ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Average Usage (cnt)", fontsize=12)
ax.grid(True)
st.pyplot(fig)

st.write("### Monthly Bike Usage")
monthly_usage = filtered_data.groupby("mnth")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(
    x=monthly_usage.index, y=monthly_usage.values, ax=ax, color="green", marker="o"
)
ax.set_title("Average Bike Usage by Month", fontsize=14)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Average Usage (cnt)", fontsize=12)
ax.grid(True)
st.pyplot(fig)

st.subheader("2. How do holidays affect bike usage compared to regular days?")

st.write("### Holiday vs Non-Holiday Bike Usage")
holiday_usage = hour_df_cleaned.groupby("holiday")["cnt"].mean()
fig, ax = plt.subplots()
sns.boxplot(x="holiday", y="cnt", data=hour_df_cleaned, ax=ax, palette="Set2")
ax.set_title("Average Bike Usage: Holiday vs Non-Holiday", fontsize=14)
ax.set_xlabel("Holiday (0 = No, 1 = Yes)", fontsize=12)
ax.set_ylabel("Average Usage (cnt)", fontsize=12)
st.pyplot(fig)


st.write("### Working Day vs Non-Working Day Bike Usage")
workingday_usage = filtered_data.groupby("workingday")["cnt"].mean()
fig, ax = plt.subplots()
sns.barplot(x=workingday_usage.index, y=workingday_usage.values, ax=ax, palette="Set3")
ax.set_title("Average Bike Usage: Working Day vs Non-Working Day", fontsize=14)
ax.set_xlabel("Working Day (0 = No, 1 = Yes)", fontsize=12)
ax.set_ylabel("Average Usage (cnt)", fontsize=12)
st.pyplot(fig)

st.subheader("3. Casual vs Registered Users")

st.write("### Bike Usage by Casual and Registered Users")
casual_registered = filtered_data[["casual", "registered"]].mean()
fig, ax = plt.subplots()
sns.barplot(
    x=casual_registered.index, y=casual_registered.values, ax=ax, palette="coolwarm"
)
ax.set_title("Average Usage: Casual vs Registered Users", fontsize=14)
ax.set_xlabel("User Type", fontsize=12)
ax.set_ylabel("Average Usage (cnt)", fontsize=12)
st.pyplot(fig)

st.markdown(
    """
## Conclusion
- Peak bike usage occurs in the **evening (18-23)** and **afternoon (12-17)**, with the lowest usage during the night (0-5).
- Bike usage is highest during **summer months**, particularly in June and September.
- **Holidays** see a lower bike usage compared to regular working days, indicating that bikes are mostly used for daily commuting.
- **Registered users** tend to use bikes more frequently compared to casual users.
"""
)
