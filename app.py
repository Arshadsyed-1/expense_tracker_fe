import streamlit as st
import requests
import pandas as pd

server_location = st.secrets["be_servel_url"]

st.title("Expense Tracker")

opt = st.sidebar.selectbox(
    "Select operation",
    [
        "add_expenses",
        "view_expenses",
        "update_expenses",
        "delete_expenses",
        "search_expenses",
        "sort_expenses",
        "filter_expenses",
        "analyze_spending"
    ]
)

def show_table(data, columns):
    if isinstance(data, list):
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.error("Backend returned error")
        st.write(data)

if opt == "add_expenses":
    st.header("Add Expenses")

    with st.form("add_expenses"):
        title = st.text_input("Title")
        amount = st.number_input("Enter amount💵", min_value=0.0)
        category = st.selectbox(
            "Category",
            [
                "Paying house rent 🏠",
                "Travel charges🚅🚎",
                "Electricity Bill⚡💡",
                "Restaurant bill🍝🍽️",
                "Medical expenses 🏥"
            ]
        )
        date = st.date_input("Expenses date")
        btn = st.form_submit_button("Submit")

        if btn:
            new_data = {
                "t": title,
                "a": amount,
                "c": category,
                "d": str(date)
            }

            response = requests.post(f"{server_location}/expense", json=new_data)
            st.write(response.json())

elif opt == "view_expenses":
    st.header("View Expenses")

    response = requests.get(f"{server_location}/expense")

    if response.status_code == 200:
        data = response.json()
        show_table(data, ["expense_id", "title", "amount", "category", "date"])
    else:
        st.error("Backend request failed")
        st.write(response.text)

elif opt == "update_expenses":
    st.header("Update Expenses")

    expense_id = st.number_input("Enter ID", min_value=1)
    title = st.text_input("Enter new title")
    amount = st.number_input("Enter amount", min_value=0.0)
    category = st.selectbox(
        "Change category",
        [
            "Paying house rent 🏠",
            "Travel charges🚅🚎",
            "Electricity Bill⚡💡",
            "Restaurant bill🍝🍽️",
            "Medical expenses 🏥"
        ]
    )
    date = st.date_input("Change date")
    btn = st.button("Update")

    if btn:
        new_data = {
            "t": title,
            "a": amount,
            "c": category,
            "d": str(date)
        }

        response = requests.put(
            f"{server_location}/expense/{expense_id}",
            json=new_data
        )

        st.write(response.json())

elif opt == "delete_expenses":
    st.header("Delete Expenses")

    expense_id = st.number_input("Expense ID", min_value=1)
    btn = st.button("Delete")

    if btn:
        response = requests.delete(f"{server_location}/expense/{expense_id}")
        st.write(response.json())

elif opt == "search_expenses":
    st.header("Search Expenses")

    keyword = st.text_input("Enter title or category")
    btn = st.button("Search")

    if btn:
        response = requests.get(f"{server_location}/expense/search/{keyword}")
        data = response.json()
        show_table(data, ["expense_id", "title", "amount", "category", "date"])

elif opt == "sort_expenses":
    st.header("Sort Expenses")

    sort_by = st.selectbox("Sort by", ["amount", "date", "category", "title"])
    btn = st.button("Sort")

    if btn:
        response = requests.get(f"{server_location}/expense/sort/{sort_by}")
        data = response.json()
        show_table(data, ["expense_id", "title", "amount", "category", "date"])

elif opt == "filter_expenses":
    st.header("Filter Expenses")

    category = st.selectbox(
        "Select category",
        [
            "Paying house rent 🏠",
            "Travel charges🚅🚎",
            "Electricity Bill⚡💡",
            "Restaurant bill🍝🍽️",
            "Medical expenses 🏥"
        ]
    )
    btn = st.button("Filter")

    if btn:
        response = requests.get(f"{server_location}/expense/filter/{category}")
        data = response.json()
        show_table(data, ["expense_id", "title", "amount", "category", "date"])

elif opt == "analyze_spending":
    st.header("Analyze Spending")

    response = requests.get(f"{server_location}/expense/analyze")

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            df = pd.DataFrame(data)
            st.dataframe(df)

            if not df.empty:
                st.bar_chart(df.set_index("category"))

        else:
            st.error("Backend returned error")
            st.write(data)
    else:
        st.error("Backend request failed")
        st.write(response.text)