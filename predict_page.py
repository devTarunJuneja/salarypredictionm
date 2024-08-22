import streamlit as st
import pickle 
import numpy as np
import plotly.graph_objects as go

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""#### We need some information to predict the Salary""")
    st.write("""Please provide the following details to estimate the salary of a Software Developer.""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada", 
        "Brazil",
        "France",
        "Spain",
        "Netherlands",
        "Poland", 
        "Italy",
        "Russian Federarion",
        "Sweden",
    )

    education_levels = (
        "Less than a Bachelors",
        "Bachelors degree", 
        "Masters degree",
        "Post grad"
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education_levels)
    experience = st.slider("Years of experience", 0, 50, 3)

    ok = st.button("Compute Salary")

    if ok:
        X = np.array([[country, education, experience]])
        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:,.2f}")


        ### Animated Bar Graph

        fig = go.Figure(
            data=[
                go.Bar(
                    x=["Salary"],
                    y=[salary[0]],
                    marker_color='indianred',
                    text=[f"${salary[0]:,.2f}"],
                    textposition='auto'
                )
            ],
            layout=go.Layout(
                title="Estimated Salary",
                updatemenus=[
                    dict(
                        type="buttons",
                        showactive=False,
                        buttons=[dict(label="Play", method="animate", args=[None])],
                    )
                ],
                    yaxis=dict(range=[0, max(salary[0] * 1.2, 100000)]),
                    xaxis=dict(range=[-0.5, 0.5]),
                ),
                frames=[
                    go.Frame(
                        data=[
                            go.Bar(
                                x=["Salary"],
                                y=[v],
                                marker_color='indianred',
                                text=[f"${v:,.2f}"],
                                textposition='auto'
                            )
                        ]
                    ) for v in np.linspace(0, salary[0], 20)
                ]
            )

        st.plotly_chart(fig)
        st.write("""
            ### Insights
            - Salaries vary significantly based on Country and Education Level
            - Experience plays a crucial role in determining the salary.
            - This prediction model uses machine learning to provide an estimate based on historical data[i.e 2020].
        """)