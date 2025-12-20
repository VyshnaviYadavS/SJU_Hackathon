import streamlit as st
import requests

BACKEND = "http://127.0.0.1:5000"

st.set_page_config(page_title="Expense Tracker", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

# ---------- LOGIN / SIGNUP ----------
def auth():
    st.title("💸 Smart Expense App")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            r = requests.post(f"{BACKEND}/login", json={"username": u, "password": p}).json()
            if r["status"] == "success":
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username", key="sign_u")
        p = st.text_input("New Password", type="password", key="sign_p")
        st.caption("Password must contain letters, numbers & special char")
        if st.button("Sign Up"):
            r = requests.post(f"{BACKEND}/signup", json={"username": u, "password": p}).json()
            if r["status"] == "success":
                st.success("Account created! Login now 💖")
            else:
                st.error(r["msg"])

# ---------- DASHBOARD ----------
def dashboard():
    st.sidebar.title("📊 Menu")
    page = st.sidebar.radio("Navigate", [
        "Add Expense",
        "Summary"
    ])

    if page == "Add Expense":
        st.header("➕ Add Expense")
        category = st.selectbox("Category", [
            "Food 🍕", "Travel 🚗", "Shopping 🛍",
            "Gaming 🎮", "Entertainment 🎬",
            "Bills 🏠", "Medical 💊",
            "Education 📚", "Investment 💼"
        ])
        amt = st.number_input("Amount", min_value=1.0)
        note = st.text_input("Note (optional)")
        if st.button("Save Expense"):
            requests.post(f"{BACKEND}/add_expense", json={
                "username": st.session_state.user,
                "category": category,
                "amount": amt,
                "note": note
            })
            st.success("Saved successfully 🎉")

    if page == "Summary":
        st.header("📈 Summary")
        r = requests.get(f"{BACKEND}/summary/{st.session_state.user}").json()
        st.metric("Today's Spend", f"₹{r['daily']}")
        st.metric("Monthly Spend", f"₹{r['monthly']}")

# ---------- ROUTING ----------
if st.session_state.user is None:
    auth()
else:
    dashboard()
