import streamlit as st
import math

def calculate_cost_of_operation(current_cost_per_set, current_lbs_per_set, machine_parts_cost_per_4m, selected_volume):
    # Prevent division by zero
    if current_lbs_per_set <= 0:
        raise ValueError("Lbs processed per set must be greater than 0.")

    # Current Calculations
    sets_required = math.ceil(selected_volume / current_lbs_per_set)
    current_parts_cost = sets_required * current_cost_per_set

    # Prince Machine Calculations
    prince_parts_cost = machine_parts_cost_per_4m * (selected_volume / 4_000_000)

    # Summary
    summary = {
        "Current": {
            "Parts Cost": current_parts_cost
        },
        "Prince": {
            "Parts Cost": prince_parts_cost
        },
        "Comparison": {
            "Savings": current_parts_cost - prince_parts_cost
        }
    }

    return summary

# Streamlit App
try:
    st.image("https://princeindustriesinc.com/wp-content/uploads/2018/06/Prince-Logo_120x145.png", use_container_width=500)
except FileNotFoundError:
    st.warning("Company logo not found. Please ensure the file is in the correct directory.")

st.title("Cost of Operation Calculator")

st.write("Tell us about your current part expenditure.")
current_cost_per_set = st.number_input("Current Cost per Set ($)", min_value=0, value=1500)
current_lbs_per_set = st.number_input("Current Lbs Processed per Set", min_value=1, value=100000)

machine_options = {
    "2000C HV-RMJ": 11118,
    "2020 HV-R": 11118,
    "Mark III": 14058,
    "221C": 8090
}
selected_machine = st.selectbox("Select Prince Machine", list(machine_options.keys()))
machine_parts_cost_per_4m = machine_options[selected_machine]

volume_options = {
    "4 Million lbs": 4_000_000,
    "20 Million lbs": 20_000_000,
    "50 Million lbs": 50_000_000
}
selected_volume_label = st.selectbox("Select Volume to Process", list(volume_options.keys()))
selected_volume = volume_options[selected_volume_label]

if st.button("Calculate"):
    try:
        result = calculate_cost_of_operation(current_cost_per_set, current_lbs_per_set, machine_parts_cost_per_4m, selected_volume)

        st.header("Results")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Current")
            st.write(f"Parts Cost: ${result['Current']['Parts Cost']:,.2f}")

        with col2:
            st.subheader("Prince")
            st.write(f"Parts Cost: ${result['Prince']['Parts Cost']:,.2f}")

        st.subheader("Comparison")
        st.write(f"Savings: ${result['Comparison']['Savings']:,.2f}")
    except ValueError as e:
        st.error(str(e))
