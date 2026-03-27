
import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels as sm


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


# Applying filters to create Interactive Dashboard

filtered_df=df

if selected_country:

    filtered_df = filtered_df[
    (filtered_df['country']==(selected_country))]
    filtered_df=filtered_df[(filtered_df['year'].between(year_filter[0], year_filter[1]))]


    st.dataframe(filtered_df)

# Dividing the Webage into Multiple parts

page=st.radio('choose an option',['Navigate','Analysis'])


if page=='Navigate':
    st.subheader('Data General View')


elif page=='Analysis':



    tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs(['Overview','Renewable Energy Over Time','Income-based Analysis',
    'Renewable Energy VS. Electricity','Renewable Energy by Continent','Energy Matrix','Summary'])

    with tab1:

        st.subheader('General KPIs')
        col1,col2=st.columns(2,gap='large')
        col3,col4=st.columns(2,gap='large')
        col5,col7=st.columns(2,gap='large')

        def format_number(value):
            if value >= 1e9:
                return f"{value/1e9:.2f}B"
            elif value >= 1e6:
                return f"{value/1e6:.2f}M"
            elif value >= 1e3:
                return f"{value/1e3:.2f}K"
            else:
                return f"{value:.2f}"


        avg_energy = round(filtered_df['electricity_generation'].mean(),2)
        avg_energy_per_capita = round(filtered_df['total_energy_per_capita'].mean(),2)
        avg_gdp =round(filtered_df['gdp'].mean(),2)
        total_pop = round(filtered_df['population'].sum(),2)
        electricity_demand =round(filtered_df['electricity_demand'].mean(), 2)
        energy_per_gdp=round(filtered_df['energy_per_gdp'].mean(), 2)

        col1.metric('average energy generation',format_number(avg_energy))
        col2.metric('average energy_per_capita',format_number(avg_energy_per_capita) )
        col3.metric('average GDP',format_number(avg_gdp))
        col4.metric('total population',format_number(total_pop))
        col5.metric('average energy_demand',format_number(electricity_demand))
        col7.metric('average energy_per_gdp',energy_per_gdp )

##############################################################################################################
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

        st.markdown('All kinds of renewable energy have generally increased over time')


#######################################################################################################
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

        st.markdown('All kinds of renewable energy resources correlates positively with total electricity generation (increased generation)')
        st.markdown('Hydro power has the strongest correlation and the most stable growth')               
##############################################################################################################################
    with tab5:

        col25,col26,col27=st.columns(3,gap='large')
        col28,col29=st.columns(2,gap='large')

        continent = df[(df['country'] == 'Africa')|
                      (df['country'] =='Australia')|
                      (df['country'] == 'Asia')|
                      (df['country'] == 'Europe')|
                      (df['country'] == 'North America')|
                      (df['country'] == 'South America')
                      ] 

        with col25:
            fig18=px.bar(continent,y='renewables_electricity',x='country')
            st.plotly_chart(fig18,use_container_width=True)

        with col26:
            fig18=px.bar(continent,y='solar_electricity',x='country')
            st.plotly_chart(fig18,use_container_width=True)



        with col27:
            fig19=px.bar(continent,y='wind_electricity',x='country')
            st.plotly_chart(fig18,use_container_width=True)



        with col28:
            fig20=px.bar(continent,y='biofuel_electricity',x='country')
            st.plotly_chart(fig18,use_container_width=True)


        with col29:
            fig21=px.bar(continent,y='hydro_electricity',x='country')
            st.plotly_chart(fig18,use_container_width=True)



######################################################################################################
    with tab6:

        st.subheader('renewable energy VS. energy access indicators')

        corr_matrix = px.imshow(df[[
                            'electricity_generation','total_energy_per_capita','energy_per_gdp',
                            'hydro_electricity', 'biofuel_electricity','solar_electricity', 
                            'wind_electricity','renewables_electricity'
                            ]].corr(),text_auto = True,color_continuous_scale=px.colors.sequential.Blues_r)

        st.plotly_chart(corr_matrix,use_container_width=True)

        st.markdown("""Renewable energy has a weak relationship with the individual share of energy and energy_per_gdp, 
        but correlates positively with electricity generation""")
######################################################################################################
    with tab7:
        st.markdown("""
        # Main Conclusion

        **Global Renewable Energy Trends**

        All kinds of renewable energy have generally increased over time, with 
        accelerated growth after 2000. Wind energy and Hydropower are the dominant 
        resources that have grown more rapidly than other renewables.

        However, despite this growth, traditional non-renewable resources(oil, gas, and fossil fuels) 
        and nuclear energy still contribute the largest share of global energy generation.
        """)

        st.markdown("""
        **Hydropower is the top renewable resource that maintains a 
        strong positive correlation with total electricity generation.**
        """)


        st.markdown("""
        Economic Impact:        
            Higher-income countries generally adopt renewable energy 
            than lower-income countries.
        """)


