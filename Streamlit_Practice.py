import streamlit as st
import  pandas as pd
st.title('Startup Dashboard')
st.header('I am learning Stramlit')
st.subheader('Manish Sharma ')
st.write('This is the normal text')
st.markdown("""
    ### My Favorite Movies
    - Race 3 
    - Humshakals
""")

st.code("""
    def function(input):
        return function**2
    
    x = function(5)
""")

st.latex("x^3 + y^2 + z =45 ")



# Display Elements
df = pd.DataFrame({
    'name': ['Nitish','Ankit','Manish'],
    'Marks': [50,60,70]
})

st.dataframe(df)

st.metric('Manish','500','100%')

st.sidebar.title("SideBar ka title")

col1,col2 = st.columns(2)

with col1:
    st.write("Hello this is the column 1")
with col2:
    st.write("This is the column 2")



email = st.text_input("Enter the email")
number = st.number_input("Enter the phone no")
date = st.date_input("Enter the date")

btn = st.button("Login Button")


gender  = st.selectbox('Select Gender',['Male','Female','Other'])

file = st.file_uploader("Upload a csv file")

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())