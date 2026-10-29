import streamlit as st
import pandas as pd
from datetime import date

# ---------------- DREAMHOME CONFIGURATION ----------------
st.set_page_config(
    page_title="DreamHome - House Price Prediction",
    page_icon="🏡",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f7f4;
}
section[data-testid="stSidebar"] {
    background-color: #123f32;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #123f32, #34785c);
    padding: 28px;
    border-radius: 16px;
    color: white;
}
.hero h1 {
    color: white;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dce7df;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# DEMONSTRATION REFERENCE RATES (₹ PER SQ FT)
# Replace these example rates with verified local property data.
CITY_RATES = {
    "Pune": 9057,
    "Mumbai": 24885,
    "Nashik": 5043,
    "Nagpur": 5397,
    "Bengaluru": 11090,
    "Hyderabad": 7695,
    "Chennai": 9190,
    "Ahmedabad": 6023,
    "Kolkata": 6248,
    "Goa": 17840
}

# ---------------- SESSION DATA ----------------
if "properties" not in st.session_state:
    st.session_state.properties = []

def rupees(amount):
    return f"₹{amount:,.0f}"

def calculate_price(city, area, bedrooms, bathrooms, age):
    base_price = CITY_RATES[city] * area
    room_factor = (
        1
        + max(0, bedrooms - 2) * 0.025
        + max(0, bathrooms - 1) * 0.01
    )
    age_factor = max(0.70, 1 - age * 0.008)
    return base_price * room_factor * age_factor

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🏡 DreamHome")
    st.caption("House Price Estimation System")

    page = st.radio(
        "Choose Page",
        [
            "Dashboard",
            "Price Predictor",
            "Property Records",
            "Market Insights",
            "EMI Calculator"
        ]
    )

    st.markdown("---")
    st.caption("Mini Project")
    st.caption("Python | Streamlit | Pandas")

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🏡 Welcome to DreamHome</h1>
        <p>Smart house price estimation and property planning.</p>
    </div>
    """, unsafe_allow_html=True)

    records = pd.DataFrame(st.session_state.properties)

    total_properties = len(records)
    total_cities = (
        records["City"].nunique() if total_properties else 0
    )
    average_price = (
        records["Estimated Price (₹)"].mean()
        if total_properties else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Saved Properties", total_properties)
    c2.metric("Cities Covered", total_cities)
    c3.metric("Average Estimate", rupees(average_price))
    c4.metric("Reference Cities", len(CITY_RATES))

    left, right = st.columns(2)

    with left:
        st.subheader("📊 City Reference Rates")

        rate_data = pd.DataFrame({
            "City": list(CITY_RATES.keys()),
            "Rate": list(CITY_RATES.values())
        })

        st.bar_chart(rate_data.set_index("City"))

    with right:
        st.subheader("✨ Project Features")

        st.write("🏠 House price estimation")
        st.write("📊 City rate comparison")
        st.write("🗂️ Saved property records")
        st.write("🏦 Home loan EMI calculator")

        st.info(
            "Choose a page from the left sidebar to get started."
        )

    st.subheader("🗂️ Recent Property Records")

    if total_properties:
        st.dataframe(records, use_container_width=True, hide_index=True)
    else:
        st.info("No saved records yet. Try the Price Predictor.")

    st.warning(
        "The reference rates are illustrative demo values, "
        "not verified live market prices."
    )

# ---------------- PRICE PREDICTOR ----------------
elif page == "Price Predictor":

    st.title("💰 House Price Predictor")
    st.write("Enter the details of your property.")

    with st.form("price_form"):

        left, right = st.columns(2)

        with left:
            city = st.selectbox("Select City", list(CITY_RATES.keys()))

            area = st.number_input(
                "Area in square feet",
                min_value=100,
                max_value=20000,
                value=900,
                step=50
            )

            bedrooms = st.selectbox(
                "Number of Bedrooms", [1, 2, 3, 4, 5, 6], index=1
            )

        with right:
            bathrooms = st.selectbox(
                "Number of Bathrooms", [1, 2, 3, 4, 5]
            )

            age = st.slider("Property Age (years)", 0, 50, 5)

            st.caption(
                f"Demo reference rate: {rupees(CITY_RATES[city])} per sq ft"
            )

        submitted = st.form_submit_button(
            "✨ Estimate House Price",
            use_container_width=True
        )

    if submitted:
        price = calculate_price(
            city, area, bedrooms, bathrooms, age
        )

        st.success("Estimate calculated successfully!")

        a, b, c = st.columns(3)
        a.metric("Estimated Price", rupees(price))
        b.metric("Area", f"{area:,} sq ft")
        c.metric("City", city)

        st.caption(
            "This uses an illustrative formula, not a trained "
            "machine-learning model or verified property valuation."
        )

        if st.button("➕ Save Property"):
            st.session_state.properties.append({
                "Date": str(date.today()),
                "City": city,
                "Area (sq ft)": area,
                "Bedrooms": bedrooms,
                "Estimated Price (₹)": round(price)
            })
            st.success("Property saved for this app session!")

# ---------------- PROPERTY RECORDS ----------------
elif page == "Property Records":

    st.title("🗂️ Property Records")

    records = pd.DataFrame(st.session_state.properties)

    if records.empty:
        st.info("No saved properties. First use the Price Predictor.")
    else:
        st.dataframe(
            records,
            use_container_width=True,
            hide_index=True
        )

        csv_data = records.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Records as CSV",
            data=csv_data,
            file_name="dreamhome_records.csv",
            mime="text/csv"
        )

        if st.button("Clear All Records"):
            st.session_state.properties = []
            st.rerun()

# ---------------- MARKET INSIGHTS ----------------
elif page == "Market Insights":

    st.title("📈 Market Insights")
    st.write("Compare configured reference rates across cities.")

    rate_data = pd.DataFrame({
        "City": list(CITY_RATES.keys()),
        "Rate (₹ per sq ft)": list(CITY_RATES.values())
    })

    selected_cities = st.multiselect(
        "Choose Cities",
        rate_data["City"].tolist(),
        default=["Pune", "Mumbai", "Nashik", "Nagpur"]
    )

    selected_data = rate_data[
        rate_data["City"].isin(selected_cities)
    ].sort_values("Rate (₹ per sq ft)", ascending=False)

    if not selected_data.empty:
        st.bar_chart(
            selected_data.set_index("City")
        )
        st.dataframe(
            selected_data,
            use_container_width=True,
            hide_index=True
        )

    st.info(
        "Future improvement: connect a housing dataset and train "
        "a regression model to make genuine ML predictions."
    )

# ---------------- EMI CALCULATOR ----------------
elif page == "EMI Calculator":

    st.title("🏦 Home Loan EMI Calculator")

    with st.form("emi_form"):

        left, right = st.columns(2)

        with left:
            property_price = st.number_input(
                "Property Price (₹)",
                min_value=100000,
                max_value=100000000,
                value=5000000,
                step=100000
            )

            down_payment = st.number_input(
                "Down Payment (₹)",
                min_value=0,
                max_value=100000000,
                value=1000000,
                step=50000
            )

        with right:
            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                max_value=30.0,
                value=8.5,
                step=0.25
            )

            years = st.selectbox(
                "Loan Duration (years)",
                [5, 10, 15, 20, 25, 30],
                index=3
            )

        calculate = st.form_submit_button(
            "Calculate Monthly EMI",
            use_container_width=True
        )

    if calculate:

        if down_payment >= property_price:
            st.error(
                "Down payment must be less than property price."
            )
        else:
            principal = property_price - down_payment
            months = years * 12
            monthly_rate = interest_rate / 1200

            if monthly_rate == 0:
                emi = principal / months
            else:
                emi = (
                    principal * monthly_rate
                    * (1 + monthly_rate) ** months
                    / ((1 + monthly_rate) ** months - 1)
                )

            a, b, c = st.columns(3)

            a.metric("Monthly EMI", rupees(emi))
            b.metric("Loan Amount", rupees(principal))
            c.metric(
                "Total Interest",
                rupees(emi * months - principal)
            )

            st.caption(
                "Approximate EMI only; bank fees, insurance, "
                "taxes and lender terms are excluded."
            )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "DreamHome | Educational mini-project | "
    "Demo estimates are not financial advice."
)