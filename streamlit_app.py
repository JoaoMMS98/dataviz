
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


# Load the cleaned dataset
@st.cache_data
def load_data():
    df = pd.read_csv(
        "cleaned_health_fitness_data.csv"
    )  # Updated to cleaned dataset path

    # Convert gender values for better readability
    df["gender"] = df["gender"].map({"F": "Female", "M": "Male"})

    return df


df = load_data()

# Define a fixed categorical order for activity_type
activity_order = [
    "Running",
    "Cycling",
    "Swimming",
    "Yoga",
    "Walking",
    "HIIT",
    "Dancing",
    "Weight Training",
    "Tennis",
    "Basketball",
]
df["activity_type"] = pd.Categorical(
    df["activity_type"], categories=activity_order, ordered=True
)


# Define the navigation menu
def streamlit_menu():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Explore Data"],
        icons=["house", "bar-chart-line"],
        menu_icon="menu-button-wide",
        default_index=0,
        orientation="horizontal",
    )
    return selected


selected = streamlit_menu()

# Home Page - Group Presentation
if selected == "Home":
    st.title("Health & Fitness Data Analysis")
    st.image("team_photo.jpeg", use_container_width=True)
    st.subheader("Project Team")

    team_members = [
        ("Afonso Gamito", "20240752"),
        ("Gonçalo Pacheco", "20240695"),
        ("Gonçalo Varanda", "20240691"),
        ("Hassan Bhatti", "20241023"),
        ("João Sampaio", "20240748"),
    ]

    team_html = "<div style='border: 1px solid #ddd; border-radius: 10px; padding: 10px; background-color: #f9f9f9; text-align: center; font-size: 16px;'>"
    for name, student_id in team_members:
        team_html += f"<strong>{name}</strong> - Nº {student_id} <br>"
    team_html += "</div>"

    st.markdown(team_html, unsafe_allow_html=True)

# Explore Data Page - Interactive Visualizations
elif selected == "Explore Data":
    st.title("Explore Health & Fitness Data")

    # Line Chart for Activity Frequency
    st.subheader("Number of Participants per Activity")

    # Calculate the frequency of each activity
    activity_frequency = df["activity_type"].value_counts().reset_index()
    activity_frequency.columns = ["activity_type", "frequency"]

    # Filter out activities with 0 frequency for better visualization
    activity_frequency = activity_frequency[activity_frequency["frequency"] > 0]

    # Create a line chart of activity frequency with zoom and markers
    fig_line = px.line(
        activity_frequency,
        x="activity_type",
        y="frequency",
        title=None,
        labels={"activity_type": "Activity Type", "frequency": "Frequency"},
        markers=True,
    )

    fig_line.update_layout(
        xaxis_title="Activity Type",
        yaxis_title="Frequency",
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=False),
        plot_bgcolor="white",
        title_x=None,
        title_y=None,
        title="",
    )

    st.plotly_chart(fig_line)

    # Dual Line Chart divided by gender
    st.subheader("Dual Line Chart: Participants by Gender Across Activities")
    activity_frequency = (
        df.groupby(["activity_type", "gender"]).size().reset_index(name="frequency")
    )

    fig_dual_line = px.line(
        activity_frequency,
        x="activity_type",
        y="frequency",
        color="gender",
        title="Activity Frequency by Gender",
        labels={
            "activity_type": "Activity Type",
            "frequency": "Frequency",
            "gender": "Gender",
        },
        markers=True,
    )

    fig_dual_line.update_layout(
        xaxis_title="Activity Type",
        yaxis_title="Frequency",
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=False),
        plot_bgcolor="white",
        title_x=None,
        title_y=None,
        title="",
    )

    st.plotly_chart(fig_dual_line)

    # Top Activities Ranked by Calories Burned
    st.subheader("Bar Chart: Top Activities by Average Calories Burned")

    activity_stats = (
        df.groupby("activity_type", observed=True)
        .agg(
            avg_calories_burned=("calories_burned", "mean"),
            avg_duration=("duration_minutes", "mean"),
        )
        .reset_index()
    )

    top_activities = activity_stats.sort_values(
        "avg_calories_burned", ascending=False
    ).dropna()

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=top_activities,
        x="avg_calories_burned",
        y="activity_type",
        palette="Blues_d",
        order=top_activities["activity_type"],
    )

    plt.xlabel("Average Calories Burned", fontsize=20)
    plt.ylabel("Activity Type", fontsize=20)
    st.pyplot(plt.gcf())

    # Polar Area Chart
    st.subheader("Polar Area Chart: Activity Participation by Intensity Level")
    activity_summary = (
        df.groupby(["activity_type", "intensity"]).size().reset_index(name="count")
    )
    activity_summary = activity_summary[activity_summary["count"] > 0]
    activity_summary["intensity"] = activity_summary["intensity"].astype(str)

    custom_blues = [
    "#6baed6",
    "#4292c6",
    "#2171b5",
    "#08519c",
    "#08306b"   # Darkest blue
    ]   
    
    fig_polar = px.bar_polar(
        activity_summary,
        r="count",
        theta="activity_type",
        color="intensity",
        template="plotly_white",
        color_discrete_sequence=custom_blues,  # Adjusted for gradient effect
        title="Polar Area Chart: Number of People per Activity by Intensity Level",
        height=600,
        width=600,
        #label color to black

    )
    fig_polar.update_layout(
    font=dict(color="black"),
    polar=dict(
        radialaxis=dict(
            color="black",  # Outer radial axis color
            gridcolor="black",  # Gridlines in black
            linecolor="black",  # Outer circle border
        ),
        angularaxis=dict(
            color="black",  # Labels on the angular axis
            gridcolor="black",  # Angular gridlines in black
            linecolor="black",  # Outer lines
        ),
    )
    )   


    st.plotly_chart(fig_polar)

    # Scatter Plot for Duration vs Calories Burned
    st.subheader("Scatter Plot: Calories Burned vs. Activity Duration by Gender")

    gender = st.radio("Select Gender", options=["Male", "Female"])
    filtered_df = df[df["gender"] == gender].sort_values(by="activity_type")

    if not filtered_df.empty:
        fig_scatter = px.scatter(
            filtered_df,
            x="duration_minutes",
            y="calories_burned",
            color="activity_type",
            title="",
            labels={
                "duration_minutes": "Duration (Minutes)",
                "calories_burned": "Calories Burned",
                "activity_type": "Activity",
            },
            hover_name="activity_type",
        )
        st.plotly_chart(fig_scatter)
    else:
        st.warning("No data matches your selection. Try adjusting the filters.")

    # Sankey Diagram
    st.subheader(
        "Sankey Diagram: Average Calories Burned by Gender and Intensity")

    intensity_level = st.selectbox(
        "Select Intensity Level", options=["Low", "Medium", "High"]
    )
    filtered_sankey_data = df[df["intensity"] == intensity_level]

    sankey_data = (
        filtered_sankey_data.groupby(["activity_type", "gender"])
        .agg({"calories_burned": "mean"})
        .reset_index()
    )
    activity_labels = list(sankey_data["activity_type"].unique())
    gender_labels = list(sankey_data["gender"].unique())
    all_labels = activity_labels + gender_labels
    label_indices = {label: i for i, label in enumerate(all_labels)}
    sankey_data["source_index"] = sankey_data["activity_type"].map(label_indices)
    sankey_data["target_index"] = sankey_data["gender"].map(label_indices)

    fig_sankey = go.Figure(
        data=[
            go.Sankey(
                node=dict(label=all_labels),
                link=dict(
                    source=sankey_data["source_index"],
                    target=sankey_data["target_index"],
                    value=sankey_data["calories_burned"],
                ),
            )
        ]
    )

    fig_sankey.update_layout(
        font=dict(size=14),  # Increase font size
        xaxis=dict(
            tickfont=dict(size=12, color="black")
        ),  # Update legend font size and color
        yaxis=dict(tickfont=dict(size=12, color="black")),
    )

    st.plotly_chart(fig_sankey)

    # Stacked Bar Chart for Age Category vs Average Calories Burned
    # Stacked Bar Chart for Average Calories Burned per Activity by Age Category

    st.subheader("Grouped Bar Chart: Average Calories Burned by Activity and Age Category")

    # Select intensity level
    intensity_level = st.selectbox(
        "Select Intensity Level", 
        options=["Low", "Medium", "High"], 
        key="intensity_level_selectbox_age_category"
    )

    # Filter DataFrame by the selected intensity level
    filtered_df = df[df["intensity"] == intensity_level]

    # Calculate average calories burned per activity within each age category
    age_activity_stats = (
        filtered_df.groupby(["age_category", "activity_type"])
        .agg(avg_calories_burned=("calories_burned", "mean"))
        .reset_index()
    )

    # Create a Stacked Bar Chart
    fig_age_activity = px.bar(
        age_activity_stats,
        x="age_category",
        y="avg_calories_burned",
        color="activity_type",
        title=f"Average Calories Burned by Activity and Age Category ({intensity_level} Intensity)",
        labels={
            "age_category": "Age Category",
            "avg_calories_burned": "Average Calories Burned",
            "activity_type": "Activity Type",
        },
        barmode="stack"
    )

    st.plotly_chart(fig_age_activity)

