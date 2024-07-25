import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import datetime


# Initialize OpenAI API
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def show_balance(balance):
    st.write("*********************")
    st.write(f"Your balance is ${balance:.2f}")
    st.write("*********************")

def deposit():
    st.write("*********************")
    amount = st.number_input("Enter an amount to be deposited:", min_value=0.0, step=0.01)
    st.write("*********************")
    return amount

def withdraw(balance):
    st.write("*********************")
    amount = st.number_input("Enter amount to be withdrawn:", min_value=0.0, step=0.01)
    st.write("*********************")
    
    if amount > balance:
        st.write("*********************")
        st.write("Insufficient funds")
        st.write("*********************")
        return 0
    else:
        return amount   

def is_fraud(transaction_history, amount, balance):
    # Ensure balance is treated as a float
    balance = float(balance)

    # Rule-based fraud detection logic
    # Initialize thresholds
    large_transaction_threshold = balance * 0.5
    frequent_transactions_threshold = 5
    time_window = datetime.timedelta(minutes=10)  # 10-minute window for frequent transactions
    unusual_hours = (0, 6)  # Transactions between midnight and 6 AM

    # Check for large transactions
    if amount > large_transaction_threshold:
        return True, "Transaction amount exceeds 50% of the balance."

    # Check for frequent small transactions
    now = datetime.datetime.now()
    recent_transactions = [t for t in transaction_history if t['time'] > now - time_window]
    if len(recent_transactions) >= frequent_transactions_threshold:
        return True, "Frequent small transactions detected within a short period."

    # Check for transactions at unusual hours
    if now.hour >= unusual_hours[0] and now.hour <= unusual_hours[1]:
        return True, "Transaction at unusual hours detected."

    # No fraud detected
    return False, ""

def get_financial_advice(api_key, messages):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=messages
    )
    advice = response.choices[0].message.content
    return advice


def main():
    st.title("Banking Program with AI Fraud Detection and Financial Advice")
    
    # Initialize session state variables
    if 'balance' not in st.session_state:
        st.session_state.balance = 0
    if 'is_running' not in st.session_state:
        st.session_state.is_running = True

    if 'transaction_history' not in st.session_state:
        st.session_state.transaction_history = []


    st.write("*********************")
    st.write("1. Show Balance")
    st.write("2. Deposit")
    st.write("3. Withdraw")
    st.write("4. Financial Advice")
    st.write("5. Exit")
    st.write("*********************")
    
    choice = st.selectbox("Enter your choice:", ('1', '2', '3', '4', '5'))
    
    if choice == '1':
        show_balance(st.session_state.balance)
    elif choice == '2':
        amount = deposit()
        is_fraudulent, reason = is_fraud(st.session_state.transaction_history, amount, st.session_state.balance)
        if is_fraudulent:
            st.warning(f"Fraudulent deposit detected: {reason}")
        else:
            st.session_state.balance += amount
            st.session_state.transaction_history.append({
                'type': 'deposit',
                'amount': amount,
                'time': datetime.datetime.now()
            })
    elif choice == '3':
        amount = withdraw(st.session_state.balance)
        if amount > 0:  # Check if a valid amount was entered
            is_fraudulent, reason = is_fraud(st.session_state.transaction_history, amount, st.session_state.balance)
            if is_fraudulent:
                st.warning(f"Fraudulent withdrawal detected: {reason}")
            else:
                st.session_state.balance -= amount
                st.session_state.transaction_history.append({
                    'type': 'withdrawal',
                    'amount': amount,
                    'time': datetime.datetime.now()
                    })
    elif choice == '4':
        query = st.text_input("Enter your financial question or query:")
        if query:
            # Define messages here
            messages = [
                {"role": "system", "content": "You are a helpful assistant that provides financial advice."},
                {"role": "user", "content": query}
            ]
            # Call get_financial_advice with messages
            advicefinal = get_financial_advice(api_key, messages)
            st.write("*********************")
            st.write("Financial Advice:")
            st.write(advicefinal)
            st.write("*********************")
    elif choice == '5':
        st.session_state.is_running = False
    
    if not st.session_state.is_running:
        st.write("*********************")
        st.write("Thank you! Have a nice day!")
        st.write("*********************")

if __name__ == '__main__':
    main()