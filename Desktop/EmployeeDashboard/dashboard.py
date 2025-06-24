
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel("Cleaned_Employee_Data_For_Dashboard.xlsx")

# -------------------------------
# 🔍 Filters Section
# -------------------------------
st.sidebar.header("🔎 Filters")

# Unique values
departments = df["Department"].unique()
genders = df["Gender"].unique()

# Filter widgets
selected_dept = st.sidebar.multiselect("Select Department(s)", departments, default=list(departments))
selected_gender = st.sidebar.multiselect("Select Gender(s)", genders, default=list(genders))

# Apply filters
filtered_df = df[
    (df["Department"].isin(selected_dept)) &
    (df["Gender"].isin(selected_gender))
]

# -------------------------------
# 🚨 Alerts Toggle
# -------------------------------
show_alerts = st.sidebar.checkbox("⚠️ Show Performance Alerts", value=True)

if show_alerts:
    st.subheader("🚨 Alerts")

    # 1. Department avg performance score ≤ 2
    dept_avg_perf = filtered_df.groupby("Department")["Performance_Score"].mean().reset_index()
    low_perf_depts = dept_avg_perf[dept_avg_perf["Performance_Score"] <= 2]

    if not low_perf_depts.empty:
        for _, row in low_perf_depts.iterrows():
            st.error(f"⚠️ Department **{row['Department']}** has low average Performance Score: {row['Performance_Score']:.2f}")

    # 2. Employees with performance score ≤ 2
    low_perf_emps = filtered_df[filtered_df["Performance_Score"] <= 2]
    if not low_perf_emps.empty:
        st.warning(f"⚠️ {len(low_perf_emps)} employee(s) have Performance Score ≤ 2")
        with st.expander("View Low Performing Employees"):
            st.dataframe(low_perf_emps[["Employee_ID", "Department", "Job_Title", "Performance_Score"]])

# -------------------------------
# 👩‍💼 Dashboard Title & KPIs
# -------------------------------
st.title("👩‍💼 Employee Analytics Dashboard")

# KPIs
total_employees = len(filtered_df)
avg_perf_score = round(filtered_df["Performance_Score"].mean(), 2)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Employees", total_employees)
with col2:
    st.metric("Average Performance Score", avg_perf_score)

# -------------------------------
# 👥 Gender Distribution
# -------------------------------
st.subheader("👥 Gender Distribution")
gender_fig = px.pie(filtered_df, names="Gender", title="Gender Split", hole=0.4)
st.plotly_chart(gender_fig, use_container_width=True)

# -------------------------------
# 🏢 Avg Performance Score by Department (Color-coded)
# -------------------------------
st.subheader("🏢 Avg Performance Score by Department")
avg_perf_by_dept = filtered_df.groupby("Department")["Performance_Score"].mean().reset_index()
avg_perf_by_dept["Color"] = avg_perf_by_dept["Performance_Score"].apply(
    lambda x: "crimson" if x <= 2 else "steelblue"
)

bar_fig = px.bar(avg_perf_by_dept, 
                 x="Department", 
                 y="Performance_Score", 
                 color="Color",
                 color_discrete_map="identity",
                 title="Avg Performance Score by Department")
bar_fig.update_layout(showlegend=False)
st.plotly_chart(bar_fig, use_container_width=True)

# -------------------------------
# 💰 Performance Score vs Monthly Salary
# -------------------------------
st.subheader("💰 Performance Score vs Monthly Salary")
fig1 = px.scatter(filtered_df, 
                  x="Monthly_Salary", 
                  y="Performance_Score", 
                  color="Department",
                  size="Years_At_Company",
                  hover_data=["Employee_ID", "Job_Title"],
                  title="Performance Score vs Monthly Salary")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 📊 Years at Company vs Monthly Salary
# -------------------------------
st.subheader("📊 Years at Company vs Monthly Salary")
fig2 = px.bar(filtered_df, 
              x="Years_At_Company", 
              y="Monthly_Salary", 
              color="Department",
              title="Years at Company vs Monthly Salary")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 📈 Team Size vs Performance Score
# -------------------------------
st.subheader("📈 Team Size vs Performance Score")
fig3 = px.line(filtered_df.sort_values(by="Team_Size"), 
               x="Team_Size", 
               y="Performance_Score", 
               markers=True,
               title="Team Size vs Performance Score")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 😊 Satisfaction vs Performance
# -------------------------------
st.subheader("😊 Satisfaction vs Performance")
fig4 = px.scatter(filtered_df, 
                  x="Employee_Satisfaction_Score", 
                  y="Performance_Score", 
                  color="Department", 
                  title="Satisfaction Score vs Performance")
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# 🔥 Performance vs Productivity
# -------------------------------
st.subheader("🔥 Performance vs Productivity")
fig5 = px.density_heatmap(filtered_df, 
                          x="Performance_Score", 
                          y="Productivity score", 
                          marginal_x="histogram", 
                          marginal_y="histogram", 
                          title="Heatmap: Performance vs Productivity")
st.plotly_chart(fig5, use_container_width=True)
