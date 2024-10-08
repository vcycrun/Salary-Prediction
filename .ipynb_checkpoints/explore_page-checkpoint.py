import streamlit as st # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedComp']]
    df = df[df['ConvertedComp'].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)


    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map) 
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >=10000]
    df = df[df['Country'] != "Other"]

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df
df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("""
             ###Stack Overflow Developer Survey 2020
             """)
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    fig1.patch.set_facecolor('none')
    ax1.set_facecolor('none') 
    colors = ['#cfe2f3', '#f4cccc', '#d9ead3', '#fff2cc', '#d0e0e3', '#cfe2f3', '#f9cb9c']
    ax1.pie(data, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=1.1, pctdistance=0.85)
    # centre_circle = plt.Circle((0,0),0.70,fc='none')
    # fig1.gca().add_artist(centre_circle)
    ax1.axis('equal')

    st.write(''' Number of Data from different Countries''')

    st.pyplot(fig1)

    st.write('''
             Mean Salary Based On Country
             ''')
    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write('''
             Mean Salary Based On Experience
             ''')
    
    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)