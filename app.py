
import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels as sm
import numpy as np

df= pd.read_csv('energy_clean.csv')

st.set_page_config(page_title='Energy',layout='wide')
st.title('Energy Dashboard')


# Year and Country Filters

st.sidebar.header('Filters')

selected_country=st.sidebar.selectbox('select country',df['country'].unique())

min_year=int(df['year'].min())
max_year= int(df['year'].max())
year_filter= st.sidebar.slider('year range',min_year,max_year,
                                (min_year,max_year))



# Economic and Energy Access Indicators Filters

min_electricity,max_electricity = st.sidebar.slider('electricity_generation_range',
                                    df['electricity_generation'].min(),
                                    df['electricity_generation'].max(),
                                    (float(df['electricity_generation'].min()),float(df['electricity_generation'].max())))

min_gdp,max_gdp = st.sidebar.slider('GDP_range',
                                    df['gdp'].min(),
                                    df['gdp'].max(),
                                    (float(df['gdp'].min()),float(df['gdp'].max())))

min_energy,max_energy= st.sidebar.slider('energy_per_capita_range',
                                    df['total_energy_per_capita'].min(),
                                    df['total_energy_per_capita'].max(),
                                    (float(df['total_energy_per_capita'].min()),float(df['total_energy_per_capita'].max())))

min_energy_gpd,max_energy_gpd=st.sidebar.slider('energy_per_gdp_range',
                                    df['energy_per_gdp'].min(),
                                    df['energy_per_gdp'].max(),
                                    (float(df['energy_per_gdp'].min()),float(df['energy_per_gdp'].max())))

# Applying filters to create Interactive Dashboard

filtered_df=df

if selected_country:
    filtered_df = filtered_df[
    (filtered_df['country']==(selected_country))]

filtered_df=filtered_df[(filtered_df['year'].between(min_year,max_year))&(filtered_df['country']==selected_country)&
                        (filtered_df['electricity_generation'].between(min_electricity,max_electricity))&
                        (filtered_df['gdp'].between(min_gdp,max_gdp))&
                        (filtered_df['total_energy_per_capita'].between(min_energy,max_energy))&
                        (filtered_df['energy_per_gdp'].between(min_energy_gpd,max_energy_gpd))
                        ]

st.dataframe(filtered_df)

# Dividing the Webage into Multiple parts

page=st.radio('choose an option',['navigate','Analysis'])


if page=='Navigate':
    st.dataframe(filtered_df)

elif page=='Analysis':

    tab1,tab2,tab3,tab4,tab5=st.tabs(['Overview','Renewable Energy Over Time','Income-based Analysis',
    'Impact of Renewable Energy','Top 5'])

    with tab1:

        st.subheader('General KPIs')
        col1,col2=st.columns(2,gap='large')
        col3,col4=st.columns(2,gap='large')
        col5,col6,col7=st.columns(3,gap='large')

        avg_energy = round(filtered_df['electricity_generation'].mean(),2)
        avg_energy_per_capita = round(filtered_df['total_energy_per_capita'].mean(),2)
        avg_gdp =round(filtered_df['gdp'].mean(),2)
        total_pop = round(filtered_df['population'].sum(),2)
        electricity_demand =round(filtered_df['electricity_demand'].mean(), 2)
        avg_energy_consumption=round(filtered_df['primary_energy_consumption'].mean(), 2)
        energy_per_gdp=round(filtered_df['energy_per_gdp'].mean(), 2)

        col1.metric('average energy generation', avg_energy)
        col2.metric('average energy_per_capita',avg_energy_per_capita )
        col3.metric('average GDP',avg_gdp )
        col4.metric('total population',total_pop )
        col5.metric('average energy_demand',electricity_demand )
        col6.metric('average energy_consumption',avg_energy_consumption )
        col7.metric('average energy_per_gdp',energy_per_gdp )

###########################################################################################

    with tab2:

        st.subheader('Time Series Analysis')
        col8,col9,col10=st.columns(3,gap='large')
        col11,col12=st.columns(2,gap='large')


        df1=df.groupby('year')[['solar_electricity', 'wind_electricity',
                            'biofuel_electricity','hydro_electricity',
                            'renewables_electricity']].sum().reset_index()

        with col8:

            fig1 = px.line(df1,y='renewables_electricity',x='year')
            st.plotly_chart(fig1,use_container_width=True)

        with col9:
            fig2=px.line(df1,y='solar_electricity',x='year')
            st.plotly_chart(fig2,use_container_width=True)

        with col10:
            fig3=px.line(df1,y='hydro_electricity',x='year')
            st.plotly_chart(fig3,use_container_width=True)


        with col11:
            fig4=px.line(df1,y='wind_electricity',x='year')
            st.plotly_chart(fig4,use_container_width=True)

        with col12:
            fig5=px.line(df1,y='biofuel_electricity',x='year')
            st.plotly_chart(fig5,use_container_width=True)

        st.markdown('All kinds of renewable energy generation have generally increased overtime.')


############################################################################


    with tab3:

        income = df[(df['country'] == 'Low-income countries')|
                        (df['country'] =='Lower-middle-income countries' )|
                        (df['country'] =='Upper-middle-income countries' )|
                        (df['country'] == 'High-income countries')]


        col13,col14,col15=st.columns(3,gap='large')
        col16,col17=st.columns(2,gap='large')
        col18,col19=st.columns(2,gap='large')

        with col13:
            fig6=px.bar(income,y='renewables_electricity',x='country')
            st.plotly_chart(fig6,use_container_width=True)


        with col14:
            fig7=px.bar(income,y='solar_electricity',x='country')
            st.plotly_chart(fig7,use_container_width=True)


        with col15:
            fig8=px.bar(income,y='wind_electricity',x='country')
            st.plotly_chart(fig8,use_container_width=True)


        with col16:
            fig9=px.bar(income,y='hydro_electricity',x='country')
            st.plotly_chart(fig9,use_container_width=True)

        with col17:
            fig10=px.bar(income,y='biofuel_electricity',x='country')
            st.plotly_chart(fig10,use_container_width=True)

        with col18:
            fig11=px.bar(income,y='nuclear_electricity',x='country')
            st.plotly_chart(fig11,use_container_width=True)

        with col19:
            fig12=px.bar(income,y='traditional_non_renewables',x='country')
            st.plotly_chart(fig12,use_container_width=True)

        st.markdown('High-income countries produce more renewable energy than low and middle-income countries')
        st.markdown('Hydro power and wind energy are the top two kinds of renewable energy adapted in high-income and upper-middle-income countries')
############################################################################################################################
    with tab4:

        st.subheader('Renewable Energy VS. Electricity Generation')

        col20,col21,col22=st.columns(3,gap='large')
        col23,col24=st.columns(2,gap='large')


        with col20:                
            fig13= px.scatter(df,x='electricity_generation',y='solar_electricity',
                   trendline='ols')
            st.plotly_chart(fig13,use_container_width=True)

        with col21:                
            fig14= px.scatter(df,x='electricity_generation',y='wind_electricity',
                   trendline='ols')
            st.plotly_chart(fig14,use_container_width=True)

        with col22:                
            fig15= px.scatter(df,x='electricity_generation',y='renewables_electricity',
                   trendline='ols')
            st.plotly_chart(fig15,use_container_width=True)

        with col23:                
            fig16= px.scatter(df,x='electricity_generation',y='hydro_electricity',
                   trendline='ols')
            st.plotly_chart(fig16,use_container_width=True)

        with col24:                
            fig17= px.scatter(df,x='electricity_generation',y='biofuel_electricity',
                   trendline='ols')
            st.plotly_chart(fig17,use_container_width=True)

        st.markdown('All kinds of renewable energy resources have a positive impact on total electricity generation (increased generation)')
        st.markdown('Hydro power has the biggest  impact')               
##############################################################################################################################

    with tab5:

        col25,col26,col27=st.columns(3,gap='large')
        col28,col29=st.columns(2,gap='large')


        with col25:
            df2=df.groupby('country')['renewables_electricity'].sum().reset_index().sort_values(by='renewables_electricity',ascending=False)
            pie_1=px.pie(df2.head(5),values='renewables_electricity',names='country')
            st.plotly_chart(pie_1,use_container_width=True)

        with col26:
            df3=df.groupby('country')['solar_electricity'].sum().reset_index().sort_values(by='solar_electricity',ascending=False)
            pie_2=px.pie(df3.head(5),values='solar_electricity',names='country')
            st.plotly_chart(pie_2,use_container_width=True)

        with col27:
            df4=df.groupby('country')['wind_electricity'].sum().reset_index().sort_values(by='wind_electricity',ascending=False)
            pie_3=px.pie(df4.head(5),values='wind_electricity',names='country')
            st.plotly_chart(pie_3,use_container_width=True)


        with col28:
            df5=df.groupby('country')['hydro_electricity'].sum().reset_index().sort_values(by='hydro_electricity',ascending=False)
            pie_4=px.pie(df5.head(5),values='hydro_electricity',names='country')
            st.plotly_chart(pie_4,use_container_width=True)

        with col29:
            df6=df.groupby('country')['biofuel_electricity'].sum().reset_index().sort_values(by='biofuel_electricity',ascending=False)
            pie_5=px.pie(df6.head(5),values='biofuel_electricity',names='country')
            st.plotly_chart(pie_5,use_container_width=True)








