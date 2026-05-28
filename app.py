import streamlit as st
import requests
import pandas as pd
server_location = st.secrets["be_servel_url"]
st.title("expense tracker")
opt = st.sidebar.selectbox("select opeartion",["add_expenses","view_expenses","update_expenses","delete_expenses","search_expenses","sort_expenses","filter_expenses","analyze_spending"])

if opt == "add_expenses":
    st.header("add expenses")
    with st.form("add_expenses"):
        title = st.text_input("Title")
        amount = st.text_input("Enter amount💵")
        category = st.selectbox("category",[" " ,"Paying house rent 🏠","Travel charges🚅🚎","Electricity Bill⚡💡","Restaurant bill🍝🍽️","Medical expenses 🏥"])
        date = st.date_input("expenses date")
        btn = st.form_submit_button("Submit")
        if btn:
            new_data = {"t":title,"a":amount,"c":category,"d":str(date)}
            response = requests.post(f"{server_location}/expense", json=new_data)
            st.write(response.json())
elif opt == "view_expenses":
    st.header("view expenses")
    response = requests.get(f"{server_location}/expense")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            df = pd.DataFrame(
                data,
                columns=["expense_id", "title", "amount", "category", "date"]
            )
            st.dataframe(df)
        else:
            st.error("Backend returned error")
            st.write(data)
    else:
        st.error("Backend request failed")
        st.write(response.text)
elif opt == "update_expenses":
    st.header("update expenses")
    expense_id = st.text_input("enter id ")
    title = st.text_input("enter new title")
    amount = st.number_input("enter amount")
    category = st.selectbox("change category",["  ", "Paying house rent 🏠","Travel charges🚅🚎","Electricity Bill⚡💡","Restaurant bill🍝🍽️","Medical expenses 🏥"])
    date = st.date_input("change date")
    btn = st.button("update")
    if btn:
        new_data = {
      "t": title,
      "a": str(amount),
      "c": category,
      "d": str(date)
            }
        response = requests.put(
    f"{server_location}/expense/{expense_id}",
    json=new_data)

    st.write(response.json())

elif opt == "delete_expenses":
    st.header("delete expenses")
    expense_id = st.number_input("expense_id", min_value=1)
    btn = st.button("Delete")
    if btn:
        response = requests.delete(f"{server_location}/expense/{expense_id}")
        st.write(response.json())

elif opt == "search_expenses":
    st.header("search expenses")
    keyword = st.selectbox("select category",["  ", "Paying house rent 🏠","Travel charges🚅🚎","Electricity Bill⚡💡","Restaurant bill🍝🍽️","Medical expenses 🏥"])
    btn = st.button("Search")
    if btn:
        response = requests.get(f"{server_location}/expense/search/{keyword}")
        data = response.json()
        df = pd.DataFrame(data, columns=["expense_id", "title", "amount", "category", "date"])
        st.dataframe(df)

elif opt =="sort_expenses":
    st.header("sort expenses")
    sort_by = st.selectbox("Sort by", ["amount", "date", "category", "title"])
    btn = st.button("Sort")

    if btn:
        response = requests.get(f"{server_location}/expense/sort/{sort_by}")
        data = response.json()
        df = pd.DataFrame(data, columns=["expense_id", "title", "amount", "category", "date"])
        st.dataframe(df)

elif opt =="filter_expenses":
    st.header("filter expenses")
    category = st.selectbox(
        "Select category",
        ["Paying house rent 🏠", "Travel charges🚅🚎", "Electricity Bill⚡💡", "Restaurant bill🍝🍽️", "Medical expenses 🏥"]
    )
    btn = st.button("Filter")
    if btn:
        response = requests.get(f"{server_location}/expense/filter/{category}")
        data = response.json()
        df = pd.DataFrame(data, columns=["expense_id", "title", "amount", "category", "date"])
        st.dataframe(df)

elif opt == "analyze_spending":
    st.header("analyze spending")
    response = requests.get(f"{server_location}/expense/analyze")
    data = response.json()
    df = pd.DataFrame(data, columns=["category", "total_amount"])
    st.dataframe(df)
    st.bar_chart(df.set_index("category"))