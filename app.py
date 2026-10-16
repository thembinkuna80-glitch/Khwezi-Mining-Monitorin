
import streamlit as st
import pandas as pd

# --- APP FRAMEWORK & LAYOUT SETUP ---
st.set_page_config(
    page_title="Khwezi Mining Monitoring Application",
    page_icon="⛏️",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

st.title("⛏️ Khwezi Mining Health, Safety & Equipment Monitoring Application")
st.markdown("*A centralized digital monitoring platform for operational decision-making.*")
st.divider()


# --- EQUIPMENT DATABASE (DEMONSTRATION DATA) ---
equipment = pd.DataFrame({
    "Equipment_ID": ["TRK-001", "TRK-002", "DRL-001"],
    "Equipment_Type": ["Haul Truck", "Haul Truck", "Drill"],
    "Operating_Hours": [1250, 1680, 2300],
    "Temperature_C": [72, 85, 108],
    "Vibration_mm_s": [3.2, 5.7, 8.7],
    "Downtime_Hours": [25, 45, 140],
    "Maintenance_Status": ["Operational", "Due", "Overdue"]
})


# --- EQUIPMENT CONDITION FUNCTIONS ---
def check_temperature(value):
    if value < 80:
        return "NORMAL"
    elif value <= 100:
        return "WARNING"
    return "CRITICAL"


def check_vibration(value):
    if value < 5:
        return "NORMAL"
    elif value <= 8:
        return "WARNING"
    return "CRITICAL"


def calculate_availability(operating_hours, downtime_hours):
    total = operating_hours + downtime_hours

    if total == 0:
        return 0.0

    return round(100 * operating_hours / total, 2)


def overall_condition(row):
    statuses = (
        row["Temperature_Status"],
        row["Vibration_Status"]
    )

    if "CRITICAL" in statuses:
        return "CRITICAL"
    elif "WARNING" in statuses:
        return "WARNING"
    return "NORMAL"


# --- PROCESS EQUIPMENT DATA ---
equipment["Temperature_Status"] = equipment[
    "Temperature_C"
].apply(check_temperature)

equipment["Vibration_Status"] = equipment[
    "Vibration_mm_s"
].apply(check_vibration)

equipment["Overall_Condition"] = equipment.apply(
    overall_condition,
    axis=1
)

equipment["Availability_Percent"] = equipment.apply(
    lambda row: calculate_availability(
        row["Operating_Hours"],
        row["Downtime_Hours"]
    ),
    axis=1
)


# --- LOGIN PORTAL & RBAC ---
if not st.session_state["logged_in"]:

    st.subheader("🔒 User Access Control Portal")
    st.write("Please authenticate your credentials and select your operational role.")

    with st.form("login_form"):
        input_user = st.text_input("Username / Personnel ID")

        input_role = st.selectbox(
            "Select System Role:",
            [
                "Administrator",
                "Safety Officer",
                "Mining Engineer",
                "Maintenance Engineer",
                "Manager"
            ]
        )

        login_button = st.form_submit_button("Authenticate & Enter")

        if login_button:
            if not input_user or not input_user.strip():
                st.error("⚠️ Error Prevention: Username cannot be empty.")
            else:
                st.session_state["logged_in"] = True
                st.session_state["username"] = input_user.strip()
                st.session_state["role"] = input_role
                st.rerun()

else:
    user = st.session_state["username"]
    role = st.session_state["role"]

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("Navigation Menu")
    st.sidebar.write(f"**User:** {user}")
    st.sidebar.write(f"**Role:** {role}")
    st.sidebar.divider()

    allowed_pages = ["View Dashboard"]

    if role in [
        "Administrator",
        "Safety Officer",
        "Mining Engineer",
        "Manager"
    ]:
        allowed_pages.extend([
            "Worker Safety Data",
            "Safety Incidents",
            "Risk Assessment"
        ])

    if role in [
        "Administrator",
        "Mining Engineer",
        "Maintenance Engineer",
        "Manager"
    ]:
        allowed_pages.extend([
            "Equipment Data",
            "Maintenance Data"
        ])

    allowed_pages.append("Generate Reports")

    if role == "Administrator":
        allowed_pages.append("Manage Users")

    selected_page = st.sidebar.selectbox(
        "Select Function",
        allowed_pages
    )

    st.sidebar.divider()

    if st.sidebar.button("Log Out"):
        st.session_state["logged_in"] = False
        st.rerun()

    # --- CENTRAL DASHBOARD ---
    if selected_page == "View Dashboard":
        st.subheader("📊 Central Monitoring Dashboard")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Total Workers", "142", "Active")
        k2.metric(
            "Safety Incidents",
            "3",
            "-1 today",
            delta_color="inverse"
        )
        k3.metric(
            "Equipment Availability",
            f"{equipment['Availability_Percent'].mean():.1f}%"
        )
        k4.metric(
            "Critical Equipment",
            int(
                (equipment["Overall_Condition"] == "CRITICAL").sum()
            )
        )

        st.caption(
            "Worker and incident figures are demonstration placeholders."
        )
        st.info(
            "💡 Use the sidebar navigation menu to access specific system modules."
        )

    # --- WORKER SAFETY ---
    elif selected_page == "Worker Safety Data":
        st.subheader("👷 Worker Health and Safety Monitoring")
        st.write(
            "Placeholder ready for the worker safety database records."
        )

    # --- SAFETY INCIDENTS ---
    elif selected_page == "Safety Incidents":
        st.subheader("🚨 Safety Incident Database")
        st.write(
            "Placeholder ready for the safety incident tracking repository."
        )

    # --- RISK ASSESSMENT ---
    elif selected_page == "Risk Assessment":
        st.subheader(
            "⚠️ Risk Assessment Matrix (Likelihood × Consequence)"
        )

        l_val = st.slider("Likelihood (1-5)", 1, 5, 2)
        c_val = st.slider("Consequence (1-5)", 1, 5, 3)

        r_score = l_val * c_val
        st.write(f"Calculated Risk Score: **{r_score}**")

        if r_score <= 4:
            st.success("Low Risk")
        elif r_score <= 9:
            st.warning("Medium Risk")
        elif r_score <= 16:
            st.error("High Risk - Warning Triggered!")
        else:
            st.error(
                "CRITICAL RISK - Immediate Action Required!"
            )

    # --- EQUIPMENT DATA ---
    elif selected_page == "Equipment Data":
        st.subheader(
            "🚛 Equipment Database & Condition Monitoring"
        )

        st.dataframe(
            equipment[
                [
                    "Equipment_ID",
                    "Equipment_Type",
                    "Operating_Hours",
                    "Temperature_C",
                    "Temperature_Status",
                    "Vibration_mm_s",
                    "Vibration_Status",
                    "Overall_Condition"
                ]
            ],
            use_container_width=True
        )

        st.write("### Equipment Condition Summary")

        a, b, c = st.columns(3)

        a.metric("Total Equipment", len(equipment))

        b.metric(
            "Critical Equipment",
            int(
                (equipment["Overall_Condition"] == "CRITICAL").sum()
            )
        )

        c.metric(
            "Equipment Warnings",
            int(
                (equipment["Overall_Condition"] == "WARNING").sum()
            )
        )

        st.write("### Individual Equipment Monitoring")

        selected_id = st.selectbox(
            "Select Equipment ID",
            equipment["Equipment_ID"]
        )

        selected = equipment.loc[
            equipment["Equipment_ID"] == selected_id
        ].iloc[0]

        st.write(
            f"**Temperature:** {selected['Temperature_C']} °C "
            f"— {selected['Temperature_Status']}"
        )

        st.write(
            f"**Vibration:** {selected['Vibration_mm_s']} mm/s "
            f"— {selected['Vibration_Status']}"
        )

        st.write(
            f"**Overall Condition:** {selected['Overall_Condition']}"
        )

        st.write("### Equipment Condition Alerts")

        for _, row in equipment.iterrows():

            if row["Temperature_Status"] == "CRITICAL":
                st.error(
                    f"{row['Equipment_ID']}: "
                    "Critical temperature detected!"
                )

            elif row["Temperature_Status"] == "WARNING":
                st.warning(
                    f"{row['Equipment_ID']}: "
                    "High temperature warning!"
                )

            if row["Vibration_Status"] == "CRITICAL":
                st.error(
                    f"{row['Equipment_ID']}: "
                    "Critical vibration detected!"
                )

            elif row["Vibration_Status"] == "WARNING":
                st.warning(
                    f"{row['Equipment_ID']}: "
                    "High vibration warning!"
                )

    # --- MAINTENANCE DATA ---
    elif selected_page == "Maintenance Data":
        st.subheader("🔧 Equipment Maintenance Monitoring")

        st.write("### Equipment Maintenance Database")

        st.dataframe(
            equipment[
                [
                    "Equipment_ID",
                    "Operating_Hours",
                    "Downtime_Hours",
                    "Maintenance_Status",
                    "Availability_Percent"
                ]
            ],
            use_container_width=True
        )

        st.write("### Equipment Availability")

        for _, row in equipment.iterrows():
            st.write(
                f"{row['Equipment_ID']}: "
                f"{row['Availability_Percent']}%"
            )

        st.write("### Maintenance Alerts")

        for _, row in equipment.iterrows():

            if row["Maintenance_Status"] == "Overdue":
                st.error(
                    f"{row['Equipment_ID']}: "
                    "Maintenance is overdue!"
                )

            elif row["Maintenance_Status"] == "Due":
                st.warning(
                    f"{row['Equipment_ID']}: "
                    "Maintenance is due!"
                )

            elif row["Maintenance_Status"] == "Under Maintenance":
                st.info(
                    f"{row['Equipment_ID']}: "
                    "Equipment is under maintenance."
                )

            if row["Availability_Percent"] < 90:
                st.warning(
                    f"{row['Equipment_ID']}: "
                    "Low equipment availability!"
                )

            if row["Downtime_Hours"] > 100:
                st.error(
                    f"{row['Equipment_ID']}: "
                    "Excessive equipment downtime!"
                )

    # --- GENERATE REPORTS ---
    elif selected_page == "Generate Reports":
        st.subheader("📄 Generate Operational Reports")

        if st.button("Generate Summary Report"):
            st.success(
                "Report button clicked. Report export is not implemented yet."
            )

    # --- MANAGE USERS ---
    elif selected_page == "Manage Users":
        st.subheader(
            "⚙️ User Management Portal (Administrator Only)"
        )

        st.text_input("New User ID")
        st.button("Grant Access")
        st.caption(
            "User management is a placeholder and does not create accounts yet."
        )
