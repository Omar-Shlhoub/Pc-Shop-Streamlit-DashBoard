import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
# This library to make a connection with the database
import pyodbc
import webbrowser

# The code below for make background for the application
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.pexels.com/photos/8108727/pexels-photo-8108727.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
background-size: 100%;
background-position: top left;
background-repeat:no-repeat;
background-attachment: local;
 background-size:cover;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);

}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
[data-baseweb="tab"]{{
background-color:transparent;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#------------------------------------------------------------------

#Get the data from the csv file 
def get_data():
    sales = pd.read_csv('PCshop1.csv', sep=',', encoding="iso-8859-1",parse_dates=[9])
    return sales
sales=get_data()

# I use this code below because i had a problem with the date is object
sales["Date"]=pd.to_datetime(sales["Date"],format="%m/%d/%Y")
salesCO=get_data()
url = 'https://www.w3schools.com/sql/default.asp'

st.markdown("<h1 style='text-align: center;color:#8e0207;'>PC SHOP</h1>",
             unsafe_allow_html=True)





# Container for all tabs  

tab1, tab2,tab3 = st.tabs(["Home","Visuals", "Sql test "])

#First tab for information about the app and to learn sql 

    with tab1:
            st.markdown("<h4 style = 'color:#8e0207;'>INFO :</h4>",
             unsafe_allow_html=True)
            st.caption('In This app you can find all information about the PC shop in different countries and you can test your experience in sql')
            st.caption('so you can type the sql code to get all data about this shop .')
            st.caption('If you do not know about sql do not worry you can use the button below and the button will navigate you to web pages to help you with getting your code .')
            st.caption('')
        
            if st.button('Learn Sql',key='first button'):
                webbrowser.open_new_tab(url)

# Second tab to see all KPIs and visuals

    with tab2:
            option = st.selectbox('Choose witch KPI do you want to see :',('Home','Gender KPI', 'Date KPI', 'Country KPI')) 
            if option ==  'Home':
               st.write("")

    #first kpi based on Gender :

            elif option ==  'Gender KPI': 
                st.subheader("Gender KPI :")
                st.caption('Choose the right combination to see which combination is the most chosen : ')
                chooseCOM = st.multiselect(  key="chooseCOM", label='Choose which Gender do you want : ',
                                            options=sales['Gender'].unique())
                salesCOM=sales[sales["Gender"].isin(chooseCOM)]
                chooseCOM1 = st.multiselect(  key="chooseCOM1", label='Choose which City do you want : ',
                                            options=salesCOM['Combination'].unique())
                salesCOM=salesCOM[salesCOM["Combination"].isin(chooseCOM1)]
                
                KPICOM=(salesCOM    
                    .groupby(['Gender','Type','Color'], as_index=False)
                    .size()
                    .rename(columns={'size': 'amount'})
                    .sort_values('amount',ascending=False)
                    .assign(type_color=lambda x: x['Type']+" " + x['Color'])
                    .filter(['Gender','type_color','amount'])
                    )
                graphCOM=px.bar(KPICOM, x='type_color', y='amount', color='Gender', barmode='group')
                st.write(graphCOM)
                st.table(KPICOM)

                #-----------------------------------------------------

                col1,col2=st.columns(2)
                with col1:
                    choose0 = st.multiselect(  ' Choose a gender: ',sales['Gender'].unique())
                    sales0=sales[sales["Gender"].isin(choose0)]
                    sales1=sales[sales["Gender"].isin(choose0)]
                    sales2=sales[sales["Gender"].isin(choose0)]
                    genre = st.radio("What do you want to know based on Gender :",('SalesType','Type','Color'))
                    st.text("")
                    st.text("")
                    st.text("")
                    st.text("")

                #Sales type select

                    if genre == 'SalesType':
                        choose1 = st.multiselect('Choose your SalesType :',sales['SalesType'].unique())
                        sales0=sales0[sales0["SalesType"].isin(choose1)]
                        KPI0=(  sales0
                                .groupby(['Gender','SalesType'],as_index=False)
                                .size()
                                .rename(columns={'size': 'amount'})
                                .assign(prop=lambda x: x['amount'] / x['amount'].sum()*100)
                        )
                        graph0=px.bar(KPI0, x='Gender',y='prop',color='SalesType', barmode='group')
                        graph0.update_layout(yaxis_ticksuffix='%')
                        st.write(graph0)
                        st.table(KPI0)

                    
                #type select

                    elif genre == 'Type':
                        choose2 = st.multiselect('Choose your PcType :',sales['Type'].unique())
                        sales1=sales1[sales1["Type"].isin(choose2)]
                        KPI1=(  sales1
                                .groupby(['Gender','Type'],as_index=False)
                                .size()
                                .rename(columns={'size': 'amount'})
                                .sort_values('amount',ascending=False)
                                .groupby(['Gender','Type']).apply(lambda x: x.nlargest(1,'amount')).reset_index(drop=True)
                        )
                        graph1=px.bar(KPI1, x='Gender',y='amount',color='Type', barmode='group')
                        st.write(graph1)
                        st.table(KPI1)

                #Color select

                    elif genre == 'Color':
                        choose3 = st.multiselect('Choose your Pc Color :',sales['Color'].unique())
                        sales2=sales2[sales2["Color"].isin(choose3)]
                        KPI2=(  sales2
                                .groupby(['Gender','Color'],as_index=False)
                                .size()
                                .rename(columns={'size': 'amount'})
                                .sort_values('amount',ascending=False)
                                .groupby(['Gender','Color']).apply(lambda x: x.nlargest(1,'amount')).reset_index(drop=True)
                        )
                        graph2=px.bar(KPI2, x='Gender',y='amount',color='Color', barmode='group')
                        st.write(graph2)
                        st.table(KPI2)
                with col2:
                    if genre == 'SalesType':
                        with st.expander("See the sql or pandas code :"):
                            image = Image.open('Gender_salesType.jpeg')
                            st.image(image,caption='The graphic below shows the percentage of those who pay all or part of the price of the computer in related to gender')
                    elif genre == 'Type':
                        with st.expander("See the sql or pandas code :"):
                            image = Image.open('Gender_Type.jpeg')
                            st.image(image,caption='The graphic below shows What is the most preferred type of laptops for men and women')
                    elif genre == 'Color':
                        with st.expander("See the sql or pandas code :"):
                            image = Image.open('Gender_Color.jpeg')
                            st.image(image,caption='The graphic below shows Witch color is the most sale in the shop by every gender')

        #second kpi based on Date :                
            
            elif option ==  'Date KPI': 
                st.subheader("Date KPI :")
                st.caption('Choose a Year to see the revenue graph  : ')
                chooseD = st.multiselect(  key="chooseD", label='Choose which Year do you want : ',
                                            options=sales['Year'].unique())
                salesYM=sales[sales["Year"].isin(chooseD)]
                chooseD1 = st.multiselect(  key="chooseD1", label='Choose which Month do you want : ',
                                            options=sales['Month'].unique())
                salesYM=salesYM[salesYM["Month"].isin(chooseD1)]
                KPIYM=(salesYM    
                    .groupby(['Year','Month'], as_index=False)
                    .agg(revenue=('Price','sum'))
                    .sort_values(['Year'])
                    )
                graphYM=px.bar(KPIYM,x='Month', y='revenue', color='Year',barmode='group')

                # this code below for make you see all the  numbers in x axis 

                graphYM.update_xaxes(type='category')
                st.write(graphYM)
                st.table(KPIYM)

                st.caption('Choose a Year to see the cumulative graph  : ')
                chooseCU = st.multiselect(  key="chooseCU", label='Choose which Year do you want : ',
                                            options=sales['Year'].unique())
                salesCU=sales[sales["Year"].isin(chooseCU)]
                chooseCU1 = st.multiselect(  key="chooseCU1", label='Choose which Month do you want : ',
                                            options=sales['Month'].unique())
                salesCU=salesCU[salesCU["Month"].isin(chooseCU1)]
                KPICU=(salesCU    
                    .assign(    year=sales.Date.dt.strftime('%Y'),
                                month=sales.Date.dt.strftime('%b'),
                                monthno=sales.Date.dt.month
                                        )
                    .groupby(['year','month','monthno'], as_index=False)
                    .agg(sumprice=('Price','sum'))
                    .sort_values(['year', 'monthno'])
                    .assign(cumrev=lambda x: x.groupby('year').sumprice.cumsum())
                    )
                graphCU=px.bar(KPICU,x='month', y='cumrev', color='year', barmode='group')
                st.write(graphCU)
        
        #theird kpi based on Country : 

            elif option ==  'Country KPI':
                st.subheader("Country KPI:")
                st.caption('Choose a City and a country to see the revenue graph for each city and Country : ')
                chooseCO = st.multiselect(  key="chooseCO", label='Choose which Country do you want : ',
                                            options=sales['Country'].unique())
                salesCO=sales[sales["Country"].isin(chooseCO)]
                chooseCO1 = st.multiselect(  key="chooseCO1", label='Choose which City do you want : ',
                                            options=sales['City'].unique())
                salesCO=salesCO[salesCO["City"].isin(chooseCO1)]
                KPICO=(salesCO    
                    .groupby(['Country','City'],as_index=False)
                    .agg(revenue=('Price','sum'))
                    .sort_values('revenue',ascending=False)
                    )
                graphCO=px.bar(KPICO, x='City',y='revenue',color='Country')
                st.write(graphCO)
                st.table(KPICO)
                st.caption('Select the city and country to see the most profitable cities in each country : ')
                chooseMX = st.multiselect(  key="chooseMX", label='Choose which Country do you want : ',
                                            options=sales['Country'].unique())
                salesMX=sales[sales["Country"].isin(chooseMX)]
                chooseMX1 = st.multiselect(  key="chooseMX1", label='Choose which City do you want : ',
                                            options=sales['City'].unique())
                salesMX=salesMX[salesMX["City"].isin(chooseMX1)]
                KPIMX=(salesMX    
                    .groupby(['Country','City'],as_index=False)
                    .agg(revenue=('Price','sum'))
                    .sort_values('revenue',ascending=False)
                    .groupby(['Country']).apply(lambda x: x.nlargest(1,'revenue')).reset_index(drop=True)
                    .sort_values('revenue',ascending=False)
                    )
                graphMX=px.bar(KPIMX, x='Country',y='revenue',color='City', barmode='group')
                st.write(graphMX)
                st.table(KPIMX)
    with tab3:
        st.title("Test Your Might In Sql")
        st.subheader("Write sql from [PCshop] database :")
        #Columns layout
        col1,col2=st.columns(2)
        with col1:
            with st.form(key='query_form'):
                raw_code=st.text_area("SQL CODE HERE")
                submit_code=st.form_submit_button("Execute")
        #results Layouts
        with col2:
            if submit_code:
                st.info("Query submitted")
                st.code(raw_code)
            #results
                query = raw_code
                table = pd.read_sql(query, connection)
                st.write(table)

if __name__ =='__main__':
    main()
