import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import matplotlib.dates as mdates

with st.echo(code_location='below'):
    """
    ## Привет! Давайте обсудим немного коронавирусной статистики 
    """

    option = st.selectbox(
        'Вы болели коронавирусом?',
        ('-', 'Да', 'Нет'))

    if option == '-':
        st.write("Пожалуйста, выберите вариант ответа")

    else:
        if option == 'Да':
            st.write("Вы один из многих")

        if option == 'Нет':
            st.write("Вам повезло")

        """
        ## Давайте посмотрим на графики для одной страны
        """

        @st.cache
        def get_data():
            data_url = ("https://covid.ourworldindata.org/data/owid-covid-data.csv" )
            return (pd.read_csv(data_url))

        df = get_data()

        """
            Сначала я хочу предложить вам посмотреть на прирост заболеваемости (количество новых случаев) или на прирост смертей от коронавируса в зависимости от даты в любой интересующей вас стране.
            
            Так же я предлагаю вам выбрать тип графика, на который вым хотелось бы посмотреть. 
            На гистограмме вы сможете выбрать и приблизить тот "кусок", который интересует вас больше всего.
            А на точечном графике, наведя 
        """

        country = st.selectbox("Выберете, пожалуйста, страну:", df["location"].unique())

        df_selection = df[lambda x: x["location"] == country]

        option_category = st.selectbox("На какие данный вы хотите посмотреть?",
                                       ('Новые случаи заболевания', 'Новые случаи смертей от коронавируса'))

        option_figures = st.selectbox("Какой график вы хотели бы увидеть?", ('-', 'Гистограмма', 'Точечная диаграмма'))

        if option_category == 'Новые случаи заболевания':

            if option_figures == 'Точечная диаграмма':
                fig0 = (alt.Chart(df_selection).mark_point()
                    .encode(x=alt.X("date:T"), y="new_cases", tooltip = 'new_cases')
                    .configure_mark(
                    opacity=0.1,
                    color='red')
                    )
                st.altair_chart(fig0)

            if option_figures == 'Гистограмма':
                fig1 = px.histogram(df_selection, x="date", y="new_cases",
                                    nbins=30, title="Прирост заболевших в стране")
                st.plotly_chart(fig1)

                """ 
                Вы можете приблизить и подробнее посмотреть на интересующую вас часть.
                """

        else:
            if option_figures == 'Точечная диаграмма':
                fig0 = (alt.Chart(df_selection).mark_point()
                    .encode(x=alt.X("date:T"), y="new_deaths", tooltip = 'new_deaths')
                    .configure_mark(
                    opacity=0.1,
                    color='black')
                )
                st.altair_chart(fig0)

            if option_figures == 'Гистограмма':
                fig1 = px.histogram(df_selection, x="date", y="new_deaths",
                                    nbins=30, title="Прирост смертей от ковида в стране")
                st.plotly_chart(fig1)

                """ 
                Вы можете приблизить и подробнее посмотреть на интересующую вас часть.
                """

        """
        ## Теперь давайте сравним две страны
        
        Здесь я предлагаю вам выбрать две страны, коронавирусную статистику по которым вы хотите сравнить.
        
        Вы так же можете выбрать критерий, по которому хотите их сравнивать.
        Вы можете сравнивать эти страны по общему количеству заболевших, по новым случаям и по смертям как в абсолютных величинах, так и в относительных.
        """
        
        first_country = st.selectbox('Выберите первую страну:', df['location'].unique())
        second_country = st.selectbox('Выберите вторую страну:', df['location'].unique())

        compare_category = st.selectbox('Выберите категорию для сравнения',
                                        ('-', 'total_cases', 'new_cases', 'total_cases_per_million',
                                         'new_cases_per_million', 'total_deaths', 'total_deaths_per_million',
                                         'new_deaths', 'new_deaths_per_million'))

        if compare_category == '-':
            st.write("Вы еще не выбрали интересующую вас категорию")

        else:
            plot_df = df[df['location'].isin((first_country, second_country))]
            plot_df = plot_df.loc[:, ['location', 'date', compare_category]]
            plot_df = plot_df.pivot('date', 'location', compare_category)
            locator = mdates.DayLocator(interval=90)

            fig = sns.lineplot(data = plot_df)
            fig.xaxis.set_major_locator(locator)
            fig.set_ylabel(compare_category)
            plt.xticks(rotation = 45, horizontalalignment = 'right')

            st.pyplot(plt, clear_figure=True)

        """
        ## Еще больше стран
        
        Здесь представлены 8 стран, в которых на сегодняшний день зафиксированно наибольшее число смертей от Covid-19.
        Благодаря круговой диаграмме вы можете визуально оценить соотношение количества смертей в этих странах.
        """

        df_deaths = df[df['date'] == '2022-05-13']
        df_deaths = df_deaths.loc[:, ['location', 'total_deaths']]
        df_deaths = df_deaths.sort_values(by=['total_deaths'], ascending = False)
        df_deaths = df_deaths.set_index('location')

        df_deaths = df_deaths.loc[['United States', 'Brazil', 'India', 'Russia', 'Mexico', 'Peru',
                                   'United Kingdom', 'Italy'], :]
        deathes = []

        colors = ("brown", "red", "orange", "yellow", "green", "blue", "purple", "pink")

        if st.button('Выделить Россию'):
            explode = (0, 0, 0, 0.4, 0, 0, 0, 0)
        else:
            explode = (0, 0, 0, 0, 0, 0, 0, 0)

        for i in range(len(df_deaths)):
            deathes.append(df_deaths.iloc[i][0])

        plt.pie(deathes, colors = colors, explode = explode, labels = df_deaths.index)

        st.pyplot(plt, clear_figure = True)