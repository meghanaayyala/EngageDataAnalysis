### Importing Required Libraries ###
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
from streamlit_option_menu import option_menu
import seaborn as sns
from PIL import Image
import warnings
warnings.filterwarnings("ignore")


## Favicon of Page from Icons8
#Car icon by Icons8
carimg=Image.open('icons8-car-30.png')
st.set_page_config(page_title="Auto Advice",page_icon=carimg,initial_sidebar_state="expanded")




## Customizing app layout
hide_menu_style="""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
</style>
"""
st.markdown(hide_menu_style,unsafe_allow_html=True)





## Reading Required Databases
df_database = pd.read_csv("teamsdata - Copy.csv")
df_fuels=pd.read_csv("Fuels.csv")
df_carsreg=pd.read_csv("CarRegs.csv")
df_cars=pd.read_csv("CarsUsedData.csv")
df_predictor=pd.read_csv("carpredictor.csv")



## Defining Dictionaries for Plotting Graphs 
types = ["Mean","Absolute","Median","Maximum","Minimum"]
label_attr_dict = {"Registrations":"regs"}
label_attr_dict_companys = {"Registrations":"regs"}
label_attr_dict_fuels = {"Registrations":"regs"}
label_fact_dict = {"Registrations":"regs"}




### Utility Functions ###

@st.cache(suppress_st_warning=True, allow_output_mutation=True) 


## Methods to Get Unique values from Dataframe Columns

def get_unique_years_modified(df_data):
    return np.unique(df_data.year).tolist()

def get_unique_months(df_data):
    return np.unique(df_data.month).tolist()

def get_unique_seats(df_data):
    return np.unique(df_data.seats).tolist()

def get_unique_companys(df_data):
    unique_companys = np.unique(df_data.company).tolist()
    return unique_companys

def get_unique_bodytypes(df_data):
    unique_bodytypes=np.unique(df_data.body).tolist()
    return unique_bodytypes

def get_unique_transtypes(df_data):
    unique_transtypes=np.unique(df_data.transmission).tolist()
    return unique_transtypes
def get_unique_fuels(df_data):
    unique_fuels = np.unique(df_data.fuel).tolist()
    return unique_fuels

def get_unique_prices(df_data):
    prices_list=[100000,500000,1000000,1500000,200000,2500000,3000000,3500000,4000000,4500000,5000000,5500000,6000000,6500000,7000000,7500000,8000000,8500000,9000000,10000000,20000000,30000000]
    return prices_list

def get_unique_capacities(df_data):
    capacities_list=[50,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
    return capacities_list



## Methods to Filter Dataframe based on selections
def filter_year(df_data):
    df_filtered_year = pd.DataFrame()
    years = np.unique(df_data.year).tolist()
    start_raw = start_year
    end_raw = end_year
    start_index = years.index(start_raw)
    end_index = years.index(end_raw)+1
    years_selected = years[start_index:end_index]
    df_filtered_year = df_data[df_data['year'].isin(years_selected)]
    return df_filtered_year

def filter_month(df_data):
    df_filtered_month = pd.DataFrame()
    months_list = list(range(selected_months[0], selected_months[1]+1))
    df_filtered_month = df_data[df_data['month'].isin(months_list)]
    return df_filtered_month

def filter_seats(df_data):
    
    df_filtered_seat=pd.DataFrame()
    seats_list=list(range(selected_seats[0],selected_seats[1]+1))
    df_filtered_seat=df_data[df_data['seats'].isin(seats_list)]
    return df_filtered_seat


def filter_price(df_data):
    df_filtered_price=pd.DataFrame()
    price_list=list(range(selected_prices[0],selected_prices[1]+1))
    df_filtered_price=df_data[(df_data['price']>=selected_prices[0]) & (df_data['price']<=selected_prices[1]+1)]
    return df_filtered_price

def filter_capacity(df_data):
    df_filtered_capacity=pd.DataFrame()
    df_filtered_capacity=df_data[(df_data['engine']>=selected_capacities[0]) & (df_data['engine']<=selected_capacities[1])]
    return df_filtered_capacity

                        

def filter_companys(df_data):
    df_filtered_company = pd.DataFrame()
    if all_companys_selected == 'Select companys manually (choose below)':
        df_filtered_company = df_data[df_data['company'].isin(selected_companys)]
        return df_filtered_company
    return df_data

def filter_fuels(df_data):
    df_filtered_fuel = pd.DataFrame()
    if all_fuels_selected == 'Select fuels manually (choose below)':
        df_filtered_fuel = df_data[df_data['fuel'].isin(selected_fuels)]
        return df_filtered_fuel
    return df_data

def filter_bodytypes(df_data):
    df_filtered_bodytype = pd.DataFrame()
    if all_bodytypes_selected == 'Select bodytypes manually (choose below)':
        df_filtered_bodytype = df_data[df_data['body'].isin(selected_bodytypes)]
        return df_filtered_bodytype
    return df_data

def filter_transtypes(df_data):
    df_filtered_transtype=pd.DataFrame()
    if all_transtypes_selected == 'Select transtypes manually (choose below)':
        df_filtered_transtype=df_data[df_data['transmission'].isin(selected_transtypes)]
        return df_filtered_transtype
    return df_data

def stack_home_away_dataframe(df_data):
    df_total_sorted = df_data
    return df_total_sorted


def group_measure_by_attribute(df_data,aspect,attribute,measure):
    #df_data = df_data_filtered
    df_return = pd.DataFrame()
    if(measure == "Absolute"):
        if(attribute == "pass_ratio" or attribute == "tackle_ratio" or attribute == "possession"):
            measure = "Mean"
        else:
            df_return = df_data.groupby([aspect]).sum()            
    
    if(measure == "Mean"):
        df_return = df_data.groupby([aspect]).mean()
        
    if(measure == "Median"):
        df_return = df_data.groupby([aspect]).median()
    
    if(measure == "Minimum"):
        df_return = df_data.groupby([aspect]).min()
    
    if(measure == "Maximum"):
        df_return = df_data.groupby([aspect]).max()
    
    df_return["aspect"] = df_return.index
    if aspect == "fuel" or aspect == "company":
        df_return = df_return.sort_values(by=[attribute], ascending = False)
    return df_return


## Methods to Plot Graphs 

def plot_x_per_year(df_data,attr,measure):
    
    rc = {#'figure.figsize':(3,3.5),
          'axes.facecolor':'white',
          'axes.edgecolor': 'black',
          'axes.labelcolor': 'black',
          'figure.facecolor': 'white',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'black',
          'ytick.color': 'black',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### regs
    attribute = label_attr_dict[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute(df_data,"year",attribute,measure)
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot, color = "orange")
    y_str = measure + " " + attr + " " + " per company"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + " by a company"
        
    ax.set(xlabel = "Year", ylabel = y_str)           
    plt.ticklabel_format(style='plain', axis='y')
    cursor = mplcursors.cursor(hover=True)
    @cursor.connect("add")
    def on_add(sel):
        x, y, width, height = sel.artist[sel.target.index].get_bbox().bounds
        sel.annotation.set(text=f"{x_axis[sel.target.index]}: {width:g}",
                           position=(10, 0), anncoords="offset points")
        sel.annotation.xy = (x + width / 2, y + height / 2)
        sel.annotation.get_bbox_patch().set(alpha=0.8)
    #mpc.cursor(hover=True)
    st.pyplot(fig)

def plot_x_per_month(df_data,attr,measure):
    rc = {#'figure.figsize':(3,3.5),
          'axes.facecolor':'white',
          'axes.edgecolor': 'black',
          'axes.labelcolor': 'black',
          'figure.facecolor': 'white',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'black',
          'ytick.color': 'black',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### regs
    attribute = label_attr_dict[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute(df_data,"month",attribute,measure)
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), color = "yellow")
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)+1))
    y_str = measure + " " + attr + " per company"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + " by a company"
        
    ax.set(xlabel = "Month", ylabel = y_str)
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(fig)

def plot_x_per_company(df_data,attr,measure): 
    rc = {#'figure.figsize':(3,3.5),
          'axes.facecolor':'white',
          'axes.edgecolor': 'black',
          'axes.labelcolor': 'black',
          'figure.facecolor': 'white',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'black',
          'ytick.color': 'black',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### regs
    attribute = label_attr_dict_companys[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute(df_data,"company",attribute,measure)

    ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), palette = sns.color_palette("tab10"))
    
    y_str = measure + " " + attr + " " + "per Company"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + " by a Company"
    ax.set(xlabel = "Company", ylabel = y_str)
    plt.xticks(rotation=30)
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(fig)

def plot_x_per_fuel(df_data,attr,measure): #total #against, #conceived
    rc = {#'figure.figsize':(3,3.5),
          'axes.facecolor':'white',
          'axes.edgecolor': 'black',
          'axes.labelcolor': 'black',
          'figure.facecolor': 'white',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'black',
          'ytick.color': 'black',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### regs
    attribute = label_attr_dict_companys[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute(df_data,"fuel",attribute,measure)
    
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), palette = sns.color_palette("tab10"))

    
    y_str = measure + " " + attr + " " + "per Fuel"
    if measure == "Absolute":
        y_str = measure + " " + attr
    if measure == "Minimum" or measure == "Maximum":
        y_str = measure + " " + attr + " per Fuel"
    ax.set(xlabel = "Fuel", ylabel = y_str)
    plt.xticks(rotation=66,horizontalalignment="right")
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(fig)


## Main Navigation




## Sidebar for Navigation
with st.sidebar:
    nav=option_menu(
        menu_title="Auto Advice",
        options=["Home","Vahan Dashboard Data","Used Cars Data Analysis","Check Similar Cars","Predict Mileage","Predict CO2 Emission","Car Evaluation","Check User Reviews","Update Dataset"],
        icons=["house","bar-chart-fill","pie-chart-fill","card-checklist","speedometer","graph-up","check-circle","people-fill","pen-fill"],
        menu_icon="cast",
        )
    







## Page seperation based on Navigation

st.markdown(" ")
if nav=="Home":
    st.title("Welcome to Auto Advice")
    st.markdown("This is an app to help you make decisions for your automotive company based on data. Using a variety of methods such as data analysis, machine learning models we help you make your company get the best results.")
    st.image('carheader.jpg')

    st.markdown("Check out more about this project at [GitHub](www.github.com)")
















if nav=="Vahan Dashboard Data":
    st.title("Vehicle Registrations in India ")
    df_stacked = stack_home_away_dataframe(df_database)
    st.markdown("Let us look at the registrations of vehicles made by Indians.")
    st.markdown(" This data was obtained from the Government of India's official dashboard for vehicle registrations. Check it out at [Vahan Dashboard](https://vahan.parivahan.gov.in/vahan4dashboard/).")
    


    # Filter timeline through slider
    st.markdown("### Select the timeline for which you want to analyse")

    # Year Range
    unique_years = get_unique_years_modified(df_database)
    start_year, end_year = st.select_slider('Select the years range:', unique_years, value=[min(unique_years),max(unique_years)])
    df_data_filtered_year = filter_year(df_stacked)        

    # Month Range
    unique_months = get_unique_months(df_data_filtered_year) #min and max month
    selected_months = st.select_slider('Select the months range:', unique_months, value=[min(unique_months),max(unique_months)])
    df_data_filtered_month = filter_month(df_data_filtered_year)        

    
    # Selecting Required Companies
    unique_companys = get_unique_companys(df_data_filtered_month)
    all_companys_selected = st.selectbox('Do you want to only include specific companys? If the answer is yes, please check the box below and then select the company(s) in the new field.', ['Include all available companys','Select companys manually (choose below)'])
    if all_companys_selected == 'Select companys manually (choose below)':
        selected_companys = st.multiselect("Select and deselect the companys you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_companys, default = unique_companys)
    df_data_filtered = filter_companys(df_data_filtered_month)
    

    
    

    # Analysis Registrations per Company

    st.subheader('Registrations Per Company')
    st.markdown('Investigate the total vehicle registrations for each company. Which company has the most registrations? How does one company compare to another in terms of registrations?')

    with st.expander("View Details"):
        plot_x_per_company_selected = st.selectbox ("Which attribute do you want to analyze?", list(label_attr_dict_companys.keys()), key = 'attribute_company')
        plot_x_per_company_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_company')


        if all_companys_selected != 'Select companys manually (choose below)' or selected_companys:
            plot_x_per_company(df_data_filtered,plot_x_per_company_selected, plot_x_per_company_type)
        else:
            st.warning('Please select at least one company')

        st.markdown('')

        st.markdown(' #### Analysis')
        st.markdown('We can see that the most registrations made were of the brand Maruti Suzuki.')

    # Analysis of Registrations Per Year

    st.subheader('Registrations per year')
    st.markdown('Let us look at the overall registrations per year. Which year had the most registrations? Which had the least?')
    with st.expander("View Details"):
        plot_x_per_year_selected = st.selectbox ("Which attribute do you want to analyze?", list(label_attr_dict.keys()), key = 'attribute_year')
        plot_x_per_year_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_year')

        if all_companys_selected != 'Select companys manually (choose below)' or selected_companys:
            plot_x_per_year(df_data_filtered,plot_x_per_year_selected,plot_x_per_year_type)
        else:
            st.warning('Please select at least one company')
        
        st.markdown(' #### Analysis')
        st.markdown("2020 has the least number of registrations. This can be clearly explained through the Covid 19 pandemic. 2018 has the most registrations.")
        
    

    # Analysis of Registrations Per Month

    st.subheader('Registrations per month')
    st.markdown('Investigate stats over the course of a year. At what point in the year do companys score the most regs? Do companys run less towards the end of the year?')    
    with st.expander("View Details"):
        plot_x_per_month_selected = st.selectbox ("Which aspect do you want to analyze?", list(label_attr_dict.keys()), key = 'attribute_month')
        plot_x_per_month_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_month')

        if all_companys_selected != 'Select companys manually (choose below)' or selected_companys:
            plot_x_per_month(df_data_filtered,plot_x_per_month_selected, plot_x_per_month_type)
        else:
            st.warning('Please select at least one company')

        st.markdown(' #### Analysis')

        st.markdown('Generally, most registrations were made towards the beginning of the year and end of the year. Both these timelines correspond to major festivals in India (New Years, Diwali, Dussehra, Christmas etc) leading to lot of exciting offers and in turn leading to more purchases.')


    ## Fuels Analysis ##

    st.subheader('Fuels Used')
    st.markdown('Let us now look at the fuels used by these registered vehicles.')
        
    st.subheader('Registrations Per Fuel')
    with st.expander("View Details"):
        df_fuel_filtered_year=filter_year(df_fuels)
        df_fuel_filtered_month=filter_month(df_fuel_filtered_year)

        
        unique_fuels = get_unique_fuels(df_fuel_filtered_month)
        all_fuels_selected = st.selectbox('Do you want to only include specific fuels? If the answer is yes, please check the box below and then select the company(s) in the new field.', ['Include all available fuels','Select fuels manually (choose below)'])
        
        if all_fuels_selected == 'Select fuels manually (choose below)':
            selected_fuels = st.multiselect("Select and deselect the fuels you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_fuels, default = unique_fuels)

        df_fuel_filtered_data=filter_fuels(df_fuel_filtered_month)
        #st.table(df_fuel_filtered_data)
        st.markdown('Investigate the total vehicle registrations for each company. Which company has the most registrations? How does one company compare to another in terms of registrations?')
        plot_x_per_fuel_selected = st.selectbox ("Which attribute do you want to analyze?", list(label_attr_dict_fuels.keys()), key = 'attribute_fuel')
        plot_x_per_fuel_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_fuel')
        
        #specific_fuel_colors = st.checkbox("Use company specific color scheme")

        if all_fuels_selected != 'Select companys manually (choose below)' or selected_fuels:
            plot_x_per_fuel(df_fuel_filtered_data,plot_x_per_fuel_selected, plot_x_per_fuel_type)
        else:
            st.warning('Please select at least one type of fuel')

        st.markdown('')

        st.markdown(' #### Analysis')
        st.markdown('Clearly petrol is the most popular fuel in the registered vehicles. Although this does include two-wheelers, it is alarmingly high as compared to the other fuels.')













if nav=="Used Cars Data Analysis":


    st.title("Used Cars Data Analysis")
    st.markdown("Let us now look at the data for cars. Through this data, we can answer a lot of queries such as what type of car is most popular and when are most cars bought etc.")
    st.markdown('')
    st.markdown("This data is taken from Car Dekho. The data was collected from [Kaggle](https://www.kaggle.com/datasets/sukhmanibedi/cars4u) and cleaned for analysis.")




    ## Selecting time filters for analysis

    st.markdown("### Select the timeline for which you want to analyse")
    unique_years = get_unique_years_modified(df_carsreg)

    ### YEARS RANGE ### 
    start_year, end_year = st.select_slider('Select the years range:', unique_years, value=[min(unique_years),max(unique_years)])
    df_carsreg_filtered_year = filter_year(df_carsreg)        

    ### month RANGE ###
    unique_months = get_unique_months(df_carsreg_filtered_year) #min and max month
    selected_months = st.select_slider('Select the months range:', unique_months, value=[min(unique_months),max(unique_months)])
    df_carsreg_filtered_month = filter_month(df_carsreg_filtered_year)

    
     
    ## Per Year

    st.subheader('Car Registrations per Year')
    st.markdown('Let us look at the overall registrations per year. Which year had the most registrations? Which had the least?')
    
    plot_x_per_year_selected = st.selectbox ("Which attribute do you want to analyze?", list(label_attr_dict.keys()), key = 'attribute_year')
    plot_x_per_year_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_year')

    
    plot_x_per_year(df_carsreg_filtered_month,plot_x_per_year_selected,plot_x_per_year_type)
   
    st.markdown(' #### Analysis')
    st.markdown("2020 has the least number of registrations. This can be clearly explained through the Covid 19 pandemic. 2018 has the most registrations.")
    
    ### Per Month

    st.subheader('Registrations per month')
    st.markdown('Investigate stats over the course of a year. At what point in the year do companys score the most regs? Do companys run less towards the end of the year?')    
    plot_x_per_month_selected = st.selectbox ("Which aspect do you want to analyze?", list(label_attr_dict.keys()), key = 'attribute_month')
    plot_x_per_month_type = st.selectbox ("Which measure do you want to analyze?", types, key = 'measure_month')

    
    plot_x_per_month(df_carsreg_filtered_month,plot_x_per_month_selected, plot_x_per_month_type)
    

    st.markdown(' #### Analysis')

    st.markdown('Generally, most registrations were made towards the beginning of the year.')

    


    
    ## Car Manufacturers##
    st.subheader("Car Manufacturers")
    st.markdown("Look into the trends of different car manufacturers")
    
    with st.expander("View Details"):
        unique_companys = get_unique_companys(df_cars)
        all_companys_selected = st.selectbox('Do you want to only include specific companys? If the answer is yes, please check the box below and then select the company(s) in the new field.', ['Include all available companys','Select companys manually (choose below)'])
        if all_companys_selected == 'Select companys manually (choose below)':
            selected_companys = st.multiselect("Select and deselect the companys you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_companys, default = unique_companys)
        df_usedcars_filtered = filter_companys(df_cars)
        

        if all_companys_selected != 'Select companys manually (choose below)' or selected_companys:
            fig,ax=plt.subplots()
            df_usedcars_filtered.company.value_counts().plot(ax=ax, kind='bar',fontsize=10)
            ax.set_ylabel("")
            ax.set_title("Top Car Making Companies in India")
            st.pyplot(fig)
            st.markdown('Clearly as shown similar to the registrations data from Vahan Dashboard, Maruti Suzuki leads the manufacturing game. Hyundai, Honda, Toyota follow it. Sports car manufacturers and luxury cars are lesser in number.')

        else:
            st.warning('Please select at least one company')
    
        
   



    
    ## Number of Seats ##
    st.subheader("Number of Seats")
    st.markdown("How many seats does the most popular car have?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        df_cars.seats.value_counts().plot(ax=ax, kind='bar',color='orange',fontsize=10)
        ax.set_ylabel("")
            #plt.legend(title="Legend",loc='lower left',bbox_to_anchor=(0, 1),fontsize=3)
        ax.set_title("Number of Seats")
        st.pyplot(fig)
        st.markdown('Five seater cars are the most popular by a large margin, followed by seven seaters, eight seaters, four seaters and six seaters')


    
        
    
    
    
    ## Engine Capacity ##
    st.subheader("Engine Capacity")
    st.markdown("What is the most common engine capacity?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        ax=sns.histplot(df_cars.capacity,kde=False,bins=[0,500,1000,1500,2000,2500,3000,3500,4000],color='yellow')
        st.pyplot(fig)
        st.markdown('Most of the engine capacity lies between the range of 1000-2000 cc.')


    ## Mileage  ##
    st.subheader("Mileage in Km/L")
    st.markdown("What is the most common mileage?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        ax=sns.histplot(df_cars.mileage,kde=False,bins=[0,5,10,15,20,25,30,35,40],color='orange')
        st.pyplot(fig)
        st.markdown('Mileage in Km/L of most cars lies between 15 to 20 Km/L.')

    ## Power ##
    st.subheader("Power in BHP")
    st.markdown("How much power is most commonly occuring among used cars?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        ax=sns.histplot(df_cars.power,kde=False,bins=[0,50,100,150,200,250,300,350,400,450,500],color='yellow')
        st.pyplot(fig)
        st.markdown('Most cars have engine power less than 100 BHP.')

    ## Fuels ##
    st.subheader("Fuels")
    st.markdown("What is the most common fuel used?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        df_cars.fuel.value_counts().plot(ax=ax, kind='bar',color='green',fontsize=10)
        ax.set_ylabel("")
        ax.set_title("Fuels")
        st.pyplot(fig)
        st.markdown("Similar stats are shown for the type of fuel as well. Petrol and Diesel clearly dominate the market.")


    ## Body Type ##
    st.subheader("Body Type")
    st.markdown("What is the most common body type of car?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        df_predictor.body.value_counts().plot(ax=ax, kind='bar',color='pink')
        ax.set_ylabel("")
        ax.set_title("Body Types")
        st.pyplot(fig)
        st.markdown("The most popular body types of cars in India are SUV, Hatchback and Sedans.")


    ## Transmission ##
    st.subheader("Transmission Mode")
    st.markdown("Which transmission mode is most used?")
    with st.expander("View Details"):
        fig,ax=plt.subplots()
        df_predictor.transmission.value_counts().plot(ax=ax, kind='bar',color='green')
        ax.set_ylabel("")
        ax.set_title("Transmission Modes")
        st.pyplot(fig)
        st.markdown("Manual and Automatic Modes form the most used transmission modes.")




    ## Most Popular Car Conclusion##
    st.subheader("Most Popular Model")
    st.markdown("After analysing the data available through the used cars data set we came to the following conclusions")
    st.markdown("**Most popular car features are:**")
    c1,c2=st.columns((1,1))
    with c1:
        st.markdown("**Company:**")
        st.markdown("**Price:**")
        st.markdown("**Engine Capacity:**")
        st.markdown("**Fuel:**")
        st.markdown("**BodyType:**")
        st.markdown("**Seats:**")
        st.markdown("**Transmission:**")

    
    with c2:
        st.markdown("Maruti Suzuki")
        st.markdown("1 lakh to 10 lakhs")
        st.markdown("1000cc to 1500 cc")
        st.markdown("Diesel/Petrol")
        st.markdown("Hatchback/SUV/Sedan")
        st.markdown("5 Seats")
        st.markdown("Automatic/Manual")

    st.markdown("Through our car predictor, we can predict the most popular car model to be one of the following cars:")

    with st.expander("Show Most Popular Car Models"):
        g1,g2=st.columns((1,1))
        h1,h2=st.columns((1,1))

        with g1:
            st.markdown("**Maruti Suzuki Swift**")
            st.image("msswift.png")

        with g2:
            st.markdown("**Maruti Suzuki Baleno**")
            st.image("msbaleno.jpg")
        with h1:
            st.markdown("**Maruti Suzuki Vitara Brezza**")
            st.image("msvitarabrezza.jpg")
        with h2:
            st.markdown("**Maruti Suzuki Dzire**")
            st.image("msdzire.png")
    









if nav=="Check Similar Cars":
    st.title("Check Similar Cars")
    st.markdown("Using this feature, you can find out what existing car models are similar to your model. Find out statistics of your competitors cars.")
    st.markdown("Before launching a new car, you can figure out whether there any cars similar to your new car. We will find the similarities from a dataset of over 1000 cars.")


    ## Choosing requirements


    
    ## Car Manufacturer
    st.markdown('')
    st.subheader("Car Manufacturers")
    unique_companys = get_unique_companys(df_predictor)
    all_companys_selected = st.selectbox('Do you want to only include specific companys? If the answer is yes, please check the box below and then select the company(s) in the new field.', ['Include all available companys','Select companys manually (choose below)'])
    if all_companys_selected == 'Select companys manually (choose below)':
        selected_companys = st.multiselect("Select and deselect the companys you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_companys, default = unique_companys)
    if all_companys_selected != 'Select companys manually (choose below)' or selected_companys:
        st.markdown('')
    else:
        st.warning('Please select at least one company')
    df_predictor_comp_filtered = filter_companys(df_predictor)
    

    
    # Price
    st.subheader("Price")
    unique_prices = get_unique_prices(df_predictor_comp_filtered) #min and max month
    selected_prices = st.select_slider('Select the price range:', unique_prices, value=[min(unique_prices),max(unique_prices)])
    df_predictor_comp_price_filtered=filter_price(df_predictor_comp_filtered)
    st.write('Choosen range:',selected_prices[0]/100000,'lakhs to ',selected_prices[1]/100000,' lakhs')
    #st.table(df_predictor_comp_price_filtered)

    
    # Engine Capacity in cc
    st.subheader("Engine Capacity")
    unique_capacities=get_unique_capacities(df_predictor_comp_price_filtered)
    selected_capacities=st.select_slider('Select the range of capacity in cc:',unique_capacities,value=[min(unique_capacities),max(unique_capacities)])
    df_predictor_comp_price_cc_filtered=filter_capacity(df_predictor_comp_price_filtered)
    st.write('Choosen range:',selected_capacities[0],'cc to ',selected_capacities[1],' cc')
    


    
    # Fuel
    st.subheader("Fuel")
    unique_fuels = get_unique_fuels(df_predictor_comp_price_cc_filtered)
    all_fuels_selected = st.selectbox('Do you want to only include specific fuels? If the answer is yes, please check the box below and then select the company(s) in the new field.', ['Include all available fuels','Select fuels manually (choose below)'])
    if all_fuels_selected == 'Select fuels manually (choose below)':
        selected_fuels = st.multiselect("Select and deselect the fuels you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_fuels, default = unique_fuels)
        
    if all_fuels_selected != 'Select fuels manually (choose below)' or selected_fuels:
        st.markdown('')
    else:
        st.warning('Please select at least one fuel')

    df_predictor_comp_price_cc_fuel_filtered=filter_fuels(df_predictor_comp_price_cc_filtered)
    

    
    # Body Type
    st.subheader("Body Type")
    unique_bodytypes = get_unique_bodytypes(df_predictor_comp_price_cc_fuel_filtered)
    all_bodytypes_selected = st.selectbox('Do you want to only include specific bodytypes? If the answer is yes, please check the box below and then select the bodytype(s) in the new field.', ['Include all available bodytypes','Select bodytypes manually (choose below)'])
    if all_bodytypes_selected == 'Select bodytypes manually (choose below)':
        selected_bodytypes = st.multiselect("Select and deselect the bodytypes you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_bodytypes, default = unique_bodytypes)
    if all_bodytypes_selected !='Select bodytypes manually (choose below)' or selected_bodytypes:
        st.markdown('')
    else:
        st.warning('Please select at least one bodytype')

    df_predictor_comp_price_cc_fuel_body_filtered = filter_bodytypes(df_predictor_comp_price_cc_fuel_filtered)
    

    # Seats
    st.subheader("Seats")
    unique_seats=get_unique_seats(df_predictor_comp_price_cc_fuel_body_filtered)
    selected_seats=st.select_slider('Select the number of seats:', unique_seats,value=[min(unique_seats), max(unique_seats)])
    df_predictor_comp_price_cc_fuel_body_seat_filtered=filter_seats(df_predictor_comp_price_cc_fuel_body_filtered)
    
    
    # Transmission
    st.subheader("Transmission")
    unique_transtypes = get_unique_transtypes(df_predictor_comp_price_cc_fuel_body_filtered)
    all_transtypes_selected = st.selectbox('Do you want to only include specific transtypes? If the answer is yes, please check the box below and then select the transtype(s) in the new field.', ['Include all available transtypes','Select transtypes manually (choose below)'])
    if all_transtypes_selected == 'Select transtypes manually (choose below)':
        selected_transtypes = st.multiselect("Select and deselect the transtypes you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_transtypes, default = unique_transtypes)
    if all_transtypes_selected !='Select transtypes manually (choose below)' or selected_transtypes:
        st.markdown('')
    else:
        st.warning('Please select at least one transtype')
    df_predictor_comp_price_cc_fuel_body_seat_trans_filtered = filter_transtypes(df_predictor_comp_price_cc_fuel_body_seat_filtered)
    

    
    if st.button('Show similar cars'):
        st.markdown("Similar cars matching your description:")
        df=df_predictor_comp_price_cc_fuel_body_seat_trans_filtered[['company','model','Variant','price','total_details']]
        #st.table(df_carpredictor_results)
        g1,g2,g3,g4,g5=st.columns((1,1,1,1,1))
        with g1:
            st.write("Company")
        with g2:
            st.write("Model")
        with g3:
            st.write("Variant")
        with g4:
            st.write("Price")
        with g5:
            st.write("Further Details")
        for index,row in df.iterrows():
            
            url="https://www.google.com/search?q="
            url=url+row["total_details"]
            
            with g1:
                st.write(row["company"])
            with g2:
                st.write(row["model"])
            with g3:
                st.write(row["Variant"])
            with g4:
                st.write(row["price"])
            with g5:
                st.markdown("[Go to Car Details](%s)"%url)










## Update Dataset

if nav=='Update Dataset':
    st.title("Add details of your car to the dataset")
    st.markdown("Update your dataset with new details of the car for better analysis.")
    name=st.text_input('Enter name of car')
    man=st.text_input('Enter manufacturer')
    locat=st.text_input('Enter location')
    year=st.number_input('Enter year of purchase')
    km=st.number_input('Enter kilometers travelled')
    fuel=st.text_input('Enter fuel')
    trans=st.text_input('Enter type of transmission')
    owner=st.text_input('Ente owner type (first, second etc)')
    cap=st.number_input('Enter engine capacity in cc')
    power=st.number_input('Enter power')
    seats=st.number_input('Enter number of seats',step=1)
    mil=st.number_input('Enter mileage')
    #body=st.text_input('Body type')
    price=st.number_input('Enter price')
    
    if st.button("Submit"):
        to_add={"name":[name],"manufacturer":[man],"location":[locat],"year":[year],"kilometers":[km],"fuel":[fuel],"trans":[trans],"owner":[owner],"capacity":[cap],"power":[power],"seats":[seats],"mileage":[mil],"price":[price]}
        to_add=pd.DataFrame(to_add)
        to_add.to_csv("CarsUsedData.csv",mode='a',header=False,index=True)
        
        st.success("Thank you for submitting your data!")








## Mileage Predictor


if nav=='Predict Mileage':
    st.title("Predict Mileage of Car (mpg)")
    st.markdown("Mileage of a car is one of the most important details customers look for in buying a car. Normally mileage is predicted through [test runs](https://www.91wheels.com/news/what-is-arai-mileage-and-can-one-ever-surpass-it), leading to waste of precious resources. Using this mileage predictor you can predict mileage with over 90 percent accuaracy.")
    st.markdown("Lets calculate mileage of a car given input variables using a machine learning model.")
    st.markdown("The model was trained on dataset provided by [UCI](https://archive.ics.uci.edu/ml/datasets/auto+mpg), and hence we use American conventions.")
    st.markdown("This model has an accuracy of 80 percent. Refer to the Jupyter Notebook for the training of the model.")



    ## Taking Inputs

    cylinders=st.number_input('Enter number of cylinders of car',step=1)
    displacement=st.number_input('Enter displacement of car in cubic inches')
    horsepower=st.number_input('Enter horsepower of car')
    weight=st.number_input('Enter weight of car in lbs')


    ## Using Machine Learning Model to Predict the Mileage
    if st.button("Predict"):
       df=pd.read_csv('mlcar.csv')
       x=df.drop('mpg',axis=1)
       y=df['mpg']
       from sklearn.model_selection import train_test_split
       x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 101)
       from sklearn.ensemble import RandomForestRegressor
       randomforest=RandomForestRegressor(n_estimators=100,random_state=101)
       randomforest.fit(x_train,y_train)
       x_test=np.array([[cylinders,displacement,horsepower,weight]])
       y_prediction =  randomforest.predict(x_test)
       st.markdown("Predicted Mileage in miles per gallon: ")
       st.markdown(y_prediction)









## Predicting CO2 Emmission


if nav=='Predict CO2 Emission':
    st.title("Predict CO2 Emission of car(g/km)")
    st.markdown("Predicting the amount of carbon dioxide gas released by your car is very important. Not only does it help in keeping the enviroment little less polluted, you can also check what factors you have to change in your car model for it emit lesser carbon dioxide.")
    st.markdown("Lets calculate the CO2 gas emitted by a car given input variables using a machine learning model.")
    st.markdown("The model was trained on dataset provided by Canadian Goverment open website and cleaned up in [Kaggle](https://www.kaggle.com/code/drfrank/co2-emission-eda-visualization-machine-learnin/data), and hence we use American conventions")
    st.markdown("This model has an accuracy of 97 percent. Refer to Jupyter Notebook to see the training of the model.")
    # taking input of parameters
    cylinders=st.number_input('Enter number of cylinders of car',step=1)
    enginesize=st.number_input('Enter engine size of car in Litre')
    fuelcons=st.number_input('Enter fuel consumed by car in L/100km')


    # predicting co2 emmission using machine learning model
    if st.button("Predict"):
       df=pd.read_csv('co2emissions.csv')
       df = df.drop(['Make','Model','Vehicle Class','Fuel Consumption City (L/100 km)', 'Transmission', 'Fuel Type', 'Fuel Consumption Hwy (L/100 km)','Fuel Consumption Comb (mpg)'],axis=1)
       x = df.drop(['CO2 Emissions(g/km)'], axis= 1)
       y = df["CO2 Emissions(g/km)"]
       from sklearn.model_selection import train_test_split
       x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=101)
       from sklearn.ensemble import RandomForestRegressor
       rf = RandomForestRegressor(random_state = 42)
       rf.fit(x_train, y_train)
       x_test=np.array([[enginesize,cylinders,fuelcons]])
       #x_test=np.array([[3.5,6,11.1]])
       y_prediction =  rf.predict(x_test)
       st.markdown("CO2 emitted in g/km: ")
       st.markdown(y_prediction)
    





# Evaluating Car Model

if nav=='Car Evaluation':
    st.title("Lets evaluate your car model.")
    st.markdown("How can we make sure whether the car model passes all the checks? We can use machine learning to predict the evaluation of your car.")

    st.markdown("We will judge whether your car is acceptable by the help of a machine learning model.")
    st.markdown("The model was trained on dataset provided by [UCI](https://archive.ics.uci.edu/ml/datasets/car+evaluation), and hence we use American conventions")
    st.markdown("This model has an accuracy of 97 percent. Refer to the Jupyter Notebook for the training of the model.")
    # taking input parameters
    option = st.radio('Rate the buying price of your car',('Very High', 'High', 'Medium','Low'))
    if option=='Very High':
        bp=1
    elif option=='High':
        bp=2
    elif option=='Medium':
        bp=3
    elif option=='Low':
        bp=4
    option = st.radio('Rate the maintenance price of your car',('Very High', 'High', 'Medium','Low'))
    if option=='Very High':
        mp=1
    elif option=='High':
        mp=2
    elif option=='Medium':
        mp=3
    elif option=='Low':
        mp=4
    option = st.radio('Number of doors in your car',('2', '3', '4','5 or more'))
    if option=='2':
        doors=1
    elif option=='3':
        doors=2
    elif option=='4':
        doors=3
    elif option=='5 or more':
        doors=4
    option = st.radio('Persons Capacity',('2','4','5 or more'))
    if option=='2':
        pc=1
    elif option=='4':
        pc=2
    elif option=='5 or more':
        pc=3
    option = st.radio('Size of Luggage Boot',('Small','Medium','Big'))
    if option=='Small':
        lb=1
    elif option=='Medium':
        lb=2
    elif option=='Big':
        lb=3
    option = st.radio('Estimated safety of car',('Low','Medium','High'))
    if option=='Low':
        saf=1
    elif option=='Medium':
        saf=2
    elif option=='High':
        saf=3
        
    
    
    # evaluating safety of car using machine learning models
    if st.button("Evaluate"):
       data = pd.read_csv("car_evaluation.csv")
       col_names = ['buying','maint','doors','persons','lug_boot','safety','class']
       data.columns = col_names
       import category_encoders as ce
       encoder = ce.OrdinalEncoder(cols = ['buying','maint','doors','persons','lug_boot','safety','class'])
       data = encoder.fit_transform(data)
       x = data.drop(['class'], axis = 1)
       y = data['class']
       from sklearn.model_selection import train_test_split
       x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)
       from sklearn.ensemble import RandomForestRegressor
       from sklearn.ensemble import RandomForestClassifier
       from sklearn.metrics import recall_score, precision_score, accuracy_score, plot_confusion_matrix, classification_report, f1_score
       randomforest=RandomForestClassifier(n_estimators=100,random_state=101)
       randomforest.fit(x_train,y_train)
       x_test=np.array([[bp,mp,doors,pc,lb,saf]])
       y_prediction =  randomforest.predict(x_test)
       result=y_prediction[0]
       st.markdown("**Car evaluation result:**")
       if result==1:
           st.warning("Car is unacceptable")
       elif result==2:
           st.success("Car is acceptable")
       elif result==3:
           st.success("Car is good")
       elif result==4:
           st.success("Car is very good")
        
       


if nav=="Check User Reviews":

    st.title("Check user reviews")
    st.markdown("Check out what people are saying about your products. You can click on the links to know reviews your cars from different websites online.")
    #st.markdown([<img src="http://www.google.com.au/images/nav_logo7.png">](http://google.com.au/))
    st.subheader("Car Manufacturers")
    

    ## Selecting company to check reviews
    unique_companys = ["Toyota","Maruti-Suzuki","Hyundai","Kia","Mahindra","Audi","Bajaj","Ford","Honda","Nissan","Volkswagen","Tata","Volvo","Jaguar","Jeep","Isuzu","Premier","Porsche","Renault","Skoda"]
    selected_companys = st.multiselect("Select and deselect the companys you would like to include in the analysis. You can clear the current selection by clicking the corresponding x-button on the right", unique_companys, default = None)
    if selected_companys:
        st.markdown('')
    else:
        st.warning('Please select at least one company')
    
    
    for i in selected_companys:
        
        st.markdown("### **Company:** "+ i)
        g1,g2=st.columns((1,1))
        g3,g4=st.columns((1,1))
        with g1:
            st.markdown("[![Temp](https://companycontactinformation.com/wp-content/uploads/2021/09/Car-Dekho-Logo.png)](https://www.cardekho.com/cars/"+i+")")
            st.markdown("Check out reviews at Car Dekho for "+i)
        with g2:
            st.markdown("[![Foo](https://image3.mouthshut.com/images/imagesp/925052760s.jpg)](https://www.carwale.com/"+i+"/expert-reviews/)")
            st.markdown("Check out reviews at Car Wale for "+i)
        with g3:
            st.markdown("[![Foo](https://i.pinimg.com/280x280_RS/65/3f/45/653f45dd590789be58be89fb06b2b23e.jpg)](https://www.autocarindia.com/cars/"+i+")")
            st.markdown("Check out reviews at Auto Car India for "+i)
        with g4:
            st.markdown("[![Foo](https://assets.techcircle.in/uploads/article-image/2015/09/thumb/zigwheels-logo1-10446.jpg)](https://www.zigwheels.com/newcars/"+i+")")
            st.markdown("Check out reviews at Zig Wheels for "+i)
        



    
        
    
    
