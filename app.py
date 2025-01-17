from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import scipy.stats as stats
import pymannkendall as mk
from tabulate import tabulate
import warnings
import matplotlib.pyplot as plt
import os
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
import logging
import textwrap
import streamlit as st
from scipy.stats import linregress
import plotly.express as px
import plotly.graph_objs as go
try:
    import statsmodels.api as sm
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'statsmodels'])
    import statsmodels.api as sm

import socket

try:
    import openpyxl
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'openpyxl'])
    import openpyxl  # Retry importing the library
# Rest of your Streamlit app code

# Ignore FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)
# Filter out the warning you want to suppress
warnings.filterwarnings("ignore", message="PyplotGlobalUseWarning")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="IIIT-Hyderabad timberline analysis", page_icon=":rocket:", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
        width: 200%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Set the page width to 800 pixels


st.markdown(
    """
    <style>
    h1 {
        color: #2e7d32;
    }
    p {
        font-size: 16px;
    }
    .widget-label {
        color: #1976D2;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Create a list of users and passwords
# users = {
#     "lokesh": "123",
#     "avantika": "123",
# }
# # Initialize session state
# if 'access_granted' not in st.session_state:
#     st.session_state.access_granted = False
# # Create a login form
# username = st.text_input("Username")
# password = st.text_input("Password", type="password")
access_granted = True
log_filename = './static/Logfiles.log'
logging.basicConfig(filename=log_filename, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
logging.info("Your Computer Name is:" + hostname)
logging.info("Your Computer IP Address is:" + IPAddr)

# Check the username and password against the list of users and passwords
 # Check if the form is submitted
# if st.button("Login"):
#     if username in users and password == users[username]:
#         # Allow the user to access the app
#         st.write("Welcome, {}!".format(username))
#         st.session_state.access_granted = True
#     else:
#         # Display an error message
#         st.write("Invalid username or password")
#         st.session_state.access_granted = False
# else:
#     access_granted = False
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = True 

# If access is granted, display the navigation options
if st.session_state.access_granted:    
 

    def getgetR_square(state,_path):
        if state == 'J&K':
            return 42
        df = pd.read_excel(_path)
        # Select rows where 'Month' is 'Annual'
        df = df[df['State'] == state]
        df['Year'] = df['Year'].astype(str)
        # Sort the DataFrame by 'R-squared' in descending order
        sorted_df = df.sort_values(by='R-squared', ascending=False)
        # Display the sorted table
        st.write("Sorted On basis of R-square value:")
        st.write(sorted_df)
        # Get the interpolation method with the highest R-squared
        best_interpolation = sorted_df.iloc[0]['InterpolationType']
        st.write(f"The interpolation method with the highest R-squared is: {best_interpolation}\n You should use this method for your analysis.")
        st.write('')



    def doIntroduction():
        # Title and Introduction

        st.title("Climate Change Impact on the Himalayan Timberline: Trend and Analysis")

        # Create columns for each person
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("**Dr. Rehana Shaik**")
            st.write("Associate Professor, Lab for Spatial Informatics(LSI), IIIT-Hyderabad")
            
            
            st.image("./static/Images/srehana.jpg", use_column_width=True)
            st.write(" **Area of research:** Hydrologic Impacts of Climate Change,  Regional Hydrologic Modeling,Reservoir Operation, Irrigation Planning and Management, Drought Assessment, Climate Extremes Analysis, Hydroinformatics")
            # Link to Advisor's LinkedIn Profile
            advisor_linkedin = "[LinkedIn Profile](https://www.linkedin.com/in/dr-rehana-shaik-1b59276b)"
            st.markdown(advisor_linkedin, unsafe_allow_html=True)
            # Link to Advisor's Research Papers
            advisor_papers = "[Advisor's Profile](https://lsi.iiit.ac.in/website/faculty/srehana/srehana.htm)"
            st.markdown(advisor_papers, unsafe_allow_html=True)
        
        with col2:
            st.subheader("**Avantika Latwal**")
            st.write("Research Associate and Ph.D. Scholar, Lab for Spatial Informatics(LSI), IIIT-Hyderabad")
            st.image("./static/Images/avantika.jpg", use_column_width=True)
            # Link to Guide's LinkedIn Profile
            guide_linkedin = "[LinkedIn Profile](https://www.linkedin.com/in/avantika-latwal/)"
            st.markdown(guide_linkedin, unsafe_allow_html=True)
            # Link to Guide's Research Papers
            # guide_papers = "[Guide's Research Papers](Guide's Research Papers URL)"
            # st.markdown(guide_papers, unsafe_allow_html=True)

        # Information about Your Advisoravantika

        # Information about You
        with col3:
            st.subheader("**Lokesh Sharma**")
            st.write("Masters in Technology - Computer Science and Eng 2022-24, IIIT-Hyderabad")



            # Link to Your LinkedIn Profile
            st.image("./static/Images/lokesh.jpg", width=280)

            st.write("Machine Learning enthusiast, Natural Language Processing, Geographical Information System")
            your_linkedin = "[LinkedIn Profile](www.linkedin.com/in/lokesh-sharma-iiith/)"
            st.markdown(your_linkedin, unsafe_allow_html=True)
            githubcode = "[All Code github links](https://github.com/Lokeshiiith/Climate_change_monitoring_tool)"
            st.markdown(githubcode, unsafe_allow_html=True)

    def executive_summary():
        st.title("Executive Summary")

        st.markdown(
            """
            The study of precipitation trends and temperature trends in the states of Uttarakhand, Jammu & Kashmir (J&K), Sikkim, Himachal Pradesh, and Arunachal Pradesh holds paramount significance due to its profound implications for regional development, environmental sustainability, and climate adaptation strategies. This project leveraged the Aphrodite dataset as the primary data source.

            **Aphrodite Dataset**: Aphrodite stands for "Asian Precipitation - Highly-Resolved Observational Data Integration Towards Evaluation." It offers comprehensive and reliable precipitation data from (1951-2015) and Temperature Data (1961-2015), making it a valuable resource for climate research.

            [Link to Aphrodite dataset](http://aphrodite.st.hirosaki-u.ac.jp/download/)

            The core motivation for this endeavor was to address critical concerns related to precipitation and temperature patterns in these ecologically diverse and geographically complex regions, necessitating an in-depth spatial analysis.
            """
        )
    def getdetails():
        st.header("Data Preprocessing")

        # Data Clipping Section
        with st.expander("Data Clipping", expanded=True):
            st.subheader("**Data Clipping**")

            # Data Preparation
            st.markdown("Data Preparation:")
            st.write('''Initially, the Aphrodite dataset in NetCDF format (.nc) was imported using the `xarray` library. This dataset 
                contained information on precipitation, latitude, longitude, and time for each year from 1951 to 2015.
                ''')

            # Loading Shapefiles
            st.markdown("**Loading Shapefiles:**")
            st.write("The shapefiles representing the boundaries of the five states were obtained and loaded into the script using the `geopandas` library. These shapefiles define the spatial extent of each state.")
            image = "./static/Images/shape.png"  # Replace with the actual image file path
            st.image(image, width=200)
            # Spatial Clipping
            st.markdown("**Spatial Clipping:**")
            st.write("To clip the precipitation data to the boundaries of each state for each year, a masking operation was performed. This was done using the `xarray` capabilities, where the precipitation data was masked based on the geometries defined by the shapefiles of the respective state.")

        # Analysis and Visualization Section
        with st.expander("Analysis and Visualization"):
            st.subheader("Analysis and Visualization")

            # Statement 1: Data Aggregation
            st.markdown("**1. Data Aggregation**:")
            st.write("We began by performing spatial aggregation of the precipitation data. The previously clipped data for each state was meticulously combined to create state-specific datasets, covering the entire study period.")
            st.write("This process involved the summation of daily precipitation values recorded at each coordinate point over the course of a year. It's a fundamental step in understanding annual precipitation trends and patterns.")

            # Statement 2: Yearly Totals
            st.markdown("**Yearly Totals**:")
            st.write("In this pivotal data processing step, we aggregated the Aphrodite dataset on an annual basis for each coordinate point, taking into account latitude and longitude.")
            st.write("The aggregation entailed summing the daily precipitation values recorded for each point throughout the year. The result is a crucial dataset for investigating annual precipitation patterns and variations.")

            # Statement 3: Purpose
            st.markdown("**Purpose**:")
            st.write("The annual total precipitation values hold immense significance. They provide a foundational dataset for in-depth analysis, enabling researchers to discern annual precipitation trends, patterns, and fluctuations at specific geographic points.")
            st.write("These aggregated values are invaluable for understanding the long-term climate characteristics and variability of precipitation in these regions.")

            # Statement 4: Analysis Ready
            st.markdown("**Analysis Ready**:")
            st.write("With the data now structured and aggregated, it is poised for various forms of climate and hydrological analyses. This includes trend analysis, anomaly detection, and investigations into regional precipitation patterns.")
            st.write("The groundwork has been laid for gaining insights into the intricate workings of climate in these geographically diverse states.")


            # Interpolation Methods
        with st.expander("3. Interpolation Methods"):
            st.subheader("Interpolation Methods  used  `scipy` library")

            # add image
            st.markdown("<span style='color:blue'>**Aphrodite Dataset Points (blue color) : The Aphrodite dataset provides precipitation data at a spatial resolution of 0.25° (approximately 25 km)**</span>", unsafe_allow_html=True)
            image = "./static/Images/aphrodite_points.png"  # Replace with the actual image file path
            st.image(image, use_column_width=True)
            st.markdown("<span style='color:red'>**Predicting or Interpolating timberline points on basis of Aphrodite points**</span>", unsafe_allow_html=True)
            st.write("<span style='color:red'>However, the timberline points are located at a much finer spatial resolution, approximately 30 meters apart.**</span>", unsafe_allow_html=True)
            image = "./static/Images/timberlinepoints.png"  # Replace with the actual image file path
            st.image(image, use_column_width=True)
            # Linear Interpolation
            st.markdown("***Linear Interpolation***:")
            st.write("- **Explanation**: Estimates values between data points assuming a linear relationship.")
            st.write("- **Reason**: Simple and efficient for regions with consistent gradients.")

            # Cubic Interpolation
            st.markdown("***Cubic Interpolation***:")
            st.write("- **Explanation**: Uses cubic polynomial functions for smoother, accurate estimations.")
            st.write("- **Reason**: Captures complex, nonlinear precipitation patterns.")

            # Nearest Neighbor Interpolation
            st.markdown("***Nearest Neighbor Interpolation***:")
            st.write("- **Explanation**: Assigns the closest known data point's value to the target point.")
            st.write("- **Reason**: Preserves extreme values, suitable for unevenly distributed or abrupt data changes.")

            # IDW Interpolation
            st.markdown("***Inverse Distance Weighted (IDW) Interpolation***:")
            st.write("- **Explanation**: Estimates values based on the inverse distance-weighted average of neighboring data points.")
            st.write("- **Reason**: Effective for capturing spatial variability when the influence of nearby data points is significant.")

            # MIDW Interpolation
            st.markdown("***Modified Inverse Distance Weighted (MIDW) Interpolation***:")
            st.write("- **Explanation**: A variation of IDW that adapts the power parameter based on local point distribution.")
            st.write("- **Reason**: Provides flexibility in capturing variability and reducing the impact of distant data points.")

        with st.expander("4. Trend Analysis"):
            st.subheader("Trend Analysis")

            # Kendall's Tau Test
            st.markdown("1. ***Kendall's Tau Test***:")
            st.write('''
                    Kendall's Tau test is a non-parametric statistical test used to assess the presence and strength
            of trends in data over time or across different conditions. In the context of this project, Kendall's
            Tau test was employed to identify and quantify precipitation trends within specific altitude ranges
            in the specified states (Uttarakhand, Jammu & Kashmir, Sikkim, Himachal Pradesh, and
            Arunachal Pradesh.''')
            st.write('''- Procedure: For each altitude range and state, the annual total precipitation data for all")
                    years from 1951 to 2015 were subjected to Kendall's Tau test. This test measures the
                    correlation or concordance between data points in time series data, helping determine
                    whether there is a statistically significant trend, whether it's increasing or decreasing.''')
            st.write('''- Results: The results of Kendall's Tau test were used to identify whether there was a)
                    statistically significant trend in precipitation within each altitude range for each state. The
                    results indicated the direction (positive or negative) and significance level of the trend.''')
            st.markdown(
                """
                **Procedure:**
                For each altitude range and state, the annual total precipitation data for all years from 1951 to 2015 were subjected to Kendall's Tau test. This test measures the correlation or concordance between data points in time series data, helping determine whether there is a statistically significant trend, whether it's increasing or decreasing.

                **Results:**
                The results of Kendall's Tau test were used to identify whether there was a statistically significant trend in precipitation within each altitude range for each state. The results indicated the direction (positive or negative) and significance level of the trend.
                **Formula:**
                Kendall's Tau is calculated using the following formula:
                ```
                τ = (P - Q) / (n * (n - 1) / 2)
                ```
                where:
                - τ is the Kendall's Tau coefficient (-1 <= τ <= 1)
                - P is the number of concordant pairs (pairs where the second value is greater than or equal to the first)
                - Q is the number of discordant pairs (pairs where the second value is less than the first)
                - n is the number of data points

                **Interpretation:**
                - A value of τ closer to 1 indicates a stronger positive trend (increasing values over time).
                - A value of τ closer to -1 indicates a stronger negative trend (decreasing values over time).
                - A value of τ closer to 0 indicates no significant trend.
                The significance of the trend is determined using a p-value obtained from a statistical test (e.g., Z-test). A p-value less than a chosen significance level (e.g., 0.05) indicates that the observed trend is statistically significant.
                """
            )

            # SEN Slope Test
            st.markdown("2. ***SEN Slope Test***:")

            st.markdown(
                """
                SEN (Seasonal Mann-Kendall) Slope Test is a statistical test used to detect monotonic trends in seasonal time series data. It's a variation of the Mann-Kendall test that focuses on seasonal trends.
                **Procedure:**
                For each altitude range and state, the annual total precipitation data was subjected to the SEN Slope Test to identify the direction and significance of the seasonal trend. This test is useful for analyzing precipitation trends specific to each season.

                **Results:**
                The SEN Slope Test results provide insights into the direction (positive or negative) and significance of the seasonal trend in precipitation data for each altitude range and state.

                **Formula:**
                The SEN slope is calculated using the formula:
                
                SEN slope = (Σ(X_i - X̄)) / (Σ(Y_i - Ȳ))
                
                Where:
                - X_i and Y_i are the seasonal time series data points.
                - X̄ and Ȳ are the means of the seasonal time series data.
                - n is the number of data points in the seasonal time series.
                """
            )


            # Conclusion
        with st.expander("Conclusion"):
        
            # st.write("Sum up the main findings of your analysis and reiterate their importance in the context of climate studies and regional planning.")
            # Header
            st.title("Understanding Climate Change Impact on the Himalayan Timberline")

            # Overview
            st.header("Overview:")
            st.write("The study analyzed climatic variations, particularly air temperature and precipitation, at the timberline elevation in the Indian Himalayas.")
            st.write("It aimed to establish the relationship between climatic parameters and timberline altitude.")

            # Key Findings
            st.header("Key Findings:")
            st.write("- Regions closer to the snow line are more vulnerable to climate change compared to inner regions, which maintain their climatic features.")
            st.write("- Over approximately four decades of climate warming, timberline areas experienced increased rainfall, particularly in inner timberline sites.")
            st.write("- Despite global warming, the upward shift of the timberline was limited. However, areas with higher temperature rises saw an increase in timberline elevation.")
            st.write("  - Example: In Sikkim, areas above 3800 meters experienced a temperature difference of 1.33 °C, leading to an upward shift in timberline elevation.")
            st.write("- The study highlighted the sensitivity of the timberline ecotone to climate change, with temperature and precipitation being natural drivers of altitude changes.")

            # Urgent Action Needed
            st.header("Urgent Action Needed:")
            st.write("Urgent measures are necessary to mitigate the impacts of climate change on the Himalayan timberline.")
            st.write("Solutions should address immediate and long-term challenges, including:")
            st.write("  - Reducing greenhouse gas emissions.")
            st.write("  - Promoting sustainable land use practices.")
            st.write("  - Enhancing forest conservation efforts.")
            st.write("  - Investing in climate-resilient infrastructure.")
            st.write("- Community-based adaptation strategies are essential to empower local communities to cope with and adapt to changing climate conditions.")

            # Conclusion
            st.subheader("Conclusion")
            st.write("- Proactive steps to protect and restore the Himalayan timberline region are crucial.")
            st.write("- By safeguarding biodiversity, ensuring water and food security, and promoting sustainable development, we can secure a resilient and thriving future for the Himalayan timberline and its inhabitants.")
                

       



    def ProjectInformation():

        # st.title("Report: Trend Analysis of Precipitation Data (1951-2015) and Temperature Data (1961-2015) in the Himalayan Region")
        st.title("Objective of the Project")
        st.write('The main aim of this study is to assess the impact of climate change across the Himalayan Timberline. This involves developing a novel tool that facilitates the analysis of correlations between Himalayan Timberline elevation and temperature, as well as precipitation patterns. The objective is to enhance our understanding of the intricate relationships between climate variables and the Himalayan ecosystem, ultimately contributing valuable insights for effective climate change mitigation and adaptation strategies in the region.')
        
        st.title("Study Area")
        st.write('The study area was defined by the careful selection of five states within the Indian Himalaya, as depicted in the figure, in order to accomplish the objective.')
        st.image("./static/Images/studyarea.jpeg", use_column_width=True)
        st.title("Framework")
        st.image("./static/Images/framework.png", use_column_width=True)
        st.markdown("Framework of the project")


        st.title("Detailed Methodology")
        executive_summary()
        getdetails()


    # Information about Temperature Analysis
    navigation = st.sidebar.radio("Select a Page", ["Introduction", "Team Analysis", "About Project",
                                "Objective and Framework" ,"Timberline Points", "Problem Visualize", "Temperature Analysis", "Precipitation Analysis"])

    # Introduction Page
    if navigation == "Introduction":
        hackathon_image_url = "./static/Images/Cloudera.jpeg"  # Replace with the actual URL of the image
        st.image(hackathon_image_url, caption='', use_column_width=True)
        st.title("Climate and Sustainability Hackathon with Cloudera")
        st.write("Welcome to the Cloudera Hackathon showcase by team - IIIT-Hyderabad!")

        # Add a link to the hackathon
        hackathon_link = "https://www.hackerearth.com/challenges/hackathon/climate-and-sustainability-hackathon-with-cloudera-and-amd/"  # Replace with the actual URL of the hackathon
        st.markdown(f"**[Link to Hackathon]({hackathon_link})**")
        
    if navigation == "Team Analysis":
            # Add an image of the institute
        institute_image = "./static/Images/iiit_logo.png"  # Replace with the actual image file path
        st.image(institute_image, use_column_width=True)
        doIntroduction()

    if navigation == "Objective and Framework":
        ProjectInformation()

    if navigation == "About Project":
        st.title('Background')
        st.write('The Himalayan timberline, situated at the upper limit of tree growth in the high mountain range, is a critical ecological zone characterized by its unique vegetation and sensitive balance. Spanning across various altitudes (e.g. between 3,500 to 4,500 meters above sea level), this region serves as a vital transition zone between the forested slopes below and the barren alpine terrain above. Here, a diverse array of plant species, including hardy shrubs, grasses, and stunted & scattered trees, have adapted to harsh environmental conditions, including extreme temperatures, high winds, and low oxygen levels. The timberline plays a crucial role in stabilizing slopes, regulating water flow, and providing habitat for numerous wildlife species. However, the Himalayan timberline faces increasing threats from climate change, with rising temperatures, shifting precipitation patterns, and changing weather extremes challenging the delicate balance of this fragile ecosystem. Understanding and mitigating these impacts are essential for preserving the ecological integrity and biodiversity of the Himalayan timberline for future generations.')
        st.image("./static/Images/timberline.jpg", use_column_width=True)
        st.markdown("**Pictorial Representation of Himalayan Timberline Ecosystem**")
        st.markdown("*Source: Dieterich T (2018) Biodiversity Monitoring and Conservation Programs for Kintrishi PAs in Georgia, Caucasus*")
        
        st.title('Problem Statement')
        st.write('The Himalayan timberline is experiencing rapid warming trends, outpacing global averages, particularly evident in high-elevation regions such as the Trans-Himalayan cold deserts. These warming trends render the Himalayan timberline increasingly vulnerable to the impacts of climate change, including shifts in precipitation patterns, extreme weather events, and alterations in temperature gradients.')
        st.image("./static/Images/climatechange.jpeg", use_column_width=True)
        st.markdown("**Pictorial Representation of High Mountain environments in a changing climate**")
        st.markdown("*Source: https://journals.sagepub.com/doi/10.1177/03091333231193844*")
        st.markdown("""
            • Changes in temperature and precipitation significantly impact timberline dynamics, with temperature lapse rates indicating elevation-dependent warming. Understanding the response of timberline vegetation to these changes is essential for predicting future ecosystem shifts.

            • The implications of climate change on the Himalayan timberline extend beyond vegetation dynamics, affecting slope stability, water regulation, and wildlife habitat. Preservation of the delicate balance of this ecosystem is paramount for maintaining biodiversity and ecosystem services.

            • Addressing the challenges posed by climate change in the Himalayan timberline requires effective mitigation and adaptation strategies tailored to the unique environmental conditions and socio-economic context of the region.
            """)
        st.markdown("**Thus, to understand these challenges the study of impact of different climatic parameters (temperature and precipitation) on timberline ecosystem is important. So that researchers and policymakers can work towards safeguarding the ecological integrity and resilience of the Himalayan timberline ecosystem in the face of ongoing climate change.**")


    if navigation == "Timberline Points":
        st.title("Mapping Captured Timberline points which are approx 30 meter distance")
        state_mapping = {
        'Select State': 'Select State',
        'Uttarakhand': 'UK_TL_2015.xlsx',
        'Jammu & Kashmir': 'J&K_TL_2015.xlsx',
        'Arunachal Pradesh': 'AP_TL_2015.xlsx',
        'Himachal Pradesh': 'HP_TL_2015.xlsx',
        'Sikkim': 'SK_TL_2015.xlsx',
        }
        mask_state_mapping = {
        'Select State': 'Select State',
        'Uttarakhand': 'UK/UK.shp',
        'Jammu & Kashmir': 'J&K/J&K.shp',
        'Arunachal Pradesh': 'AP/AP.shp',
        'Himachal Pradesh': 'HP/HP.shp',
        'Sikkim': 'SK/SK.shp',
        }
        # Function to create a folium map with markers


        
        def create_folium_map(df_subset, mask_file):
            map_center = [df_subset['Latitude'].mean(), df_subset['Longitude'].mean()]
            my_map = folium.Map(location=map_center, zoom_start=7)

            for index, row in df_subset.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    tooltip=f"Latitude: {row['Latitude']:.2f}<br>Longitude: {row['Longitude']:.2f}<br>Altitude: {row['Altitude']:.2f}",
                ).add_to(my_map)
                # Load the shapefile
            gdf = gpd.read_file(mask_file)
            mask_group = folium.FeatureGroup(name='Mask')
            for geo in gdf.geometry:
                folium.GeoJson(geo).add_to(mask_group)
            mask_group.add_to(my_map)
            # Add the shapefile to the map
            folium.GeoJson(data=gdf).add_to(my_map)
            folium_static(my_map)


        files = os.listdir("./static/TimberlinePoints/")
        selected_file = st.selectbox("Select a state to know about timberline points", list(state_mapping.keys()))
        if st.button("Submit"):
            if selected_file != 'Select State':
                # import ipdb
                # ipdb.set_trace()
                real_file_name =  state_mapping[selected_file]
                mask_file = mask_state_mapping[selected_file]
                file_path = os.path.join("./static/TimberlinePoints/", real_file_name)
                mask_path = os.path.join("./static/State_Boundary/", mask_file)
                df = pd.read_excel(file_path)
                st.subheader(f"Displaying contents of {selected_file} file:")
                st.write("Number of timberline points selected are :", df.shape[0])  
                st.write(df)
                n = 300
                st.write(f"Showing random {n} points on {selected_file},out of {df.shape[0]} which shows how disperse the points")
                create_folium_map(df.sample(n), mask_path)
                st.write(f"- Displayed on this map are a carefully selected subset of {n} points out of a vast dataset comprising {df.shape[0]}  locations within a particular region.")
                st.write("-While showcasing the entire dataset would be too heavy for seamless web performance, these 300 points offer a comprehensive and precise representation")
                st.write("- Each point intricately reflects the depth of our captured information, providing a descriptive and meaningful glimpse into the expansive landscape we've meticulously documented.")
            else:
                st.warning("Please select a state.")
            

    if navigation == "Temperature Analysis":
        def highlight_trend_column(val):
                if val != 'no trend':
                    return f'background-color: red'  # Change the background color to yellow for rows with trend
                return ''  # Default style
        def highlight_result_column(val):
            if val == 'Reject':
                return f'background-color: red'  # Change the background color to yellow for rows with trend
            return ''  # Default style
        def PrintSenSlopeTest(df, state_name, month, interpolation, YearRange, Season):
            if Season == 'Annually':
                month = ['Annual']
            results = []

            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            # Create a selection box for states with full names
            selected_state = state_mapping[state_name]
            YearRange = [str(year) for year in YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted} years timeseries)'
            df = df.loc[:, YearRange]
            for altitude_range in df.index:
                # Extract the precipitation values for the current altitude range
                values = df.loc[altitude_range].values
                first_value = values[0]  # Capture the first value
                precipitation = values[1:]  # Extract precipitation data

                # Convert precipitation data and years to NumPy arrays
                precipitation = np.array(precipitation, dtype=float)
                years = np.array(df.columns[1:], dtype=int)
                # Perform linear regression to calculate the slope
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    years, precipitation)
                # Find the p-value
                # Calculate t-statistic
                # t = slope / (std_err / np.sqrt(np.sum((years - np.mean(years))**2)))
                # p_value2 = 2 * (1 - stats.t.cdf(np.abs(t), len(years) - 2))
                r_square = r_value**2
                if p_value < 0.05:
                    result = "Reject"
                else:
                    result = "Fail to reject"
                results.append([selected_state, month, altitude_range, interpolation,  p_value, slope, result,year_range])

            # Print the extracted state name
            # Create a DataFrame from the results list
            results_df = pd.DataFrame(results, columns=[
                'State', 'Month', 'Altitude Range', 'Interpolation', 'p-value', 'slope', 'Result', 'year_range'])
            styled_df = results_df.style.applymap(highlight_result_column, subset=['Result'])
            st.dataframe(styled_df, width=1500)
            # st.dataframe(results_df)
            # Display result explanations
            st.write("Result Explanations:")
            outcomes = {
                "- Reject": "This means that the data provides sufficient evidence to conclude that the null hypothesis is false.",
                "- Fail to reject": "This means that the data does not provide sufficient evidence to conclude that the null hypothesis is false.",
            }

            for outcome, description in outcomes.items():
                st.write(f"{outcome}:\n{description}",)
        # Define the custom style function
 

        def PrintMankendallTest(df, State, month, interpolation, YearRange, Season):
            # Create a list to store the results
            if Season == 'Annually':
                month = ['Annual']
            results = []
            # Change YearRange to string as df.columns is string
            # modify the df now
            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            # Create a selection box for states with full names
            selected_state = state_mapping[State]
            YearRange = [str(year) for year in YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted} years timeseries)'
            df = df.loc[:, YearRange]
            for altitude_range in df.index:
                # Filter the data frame to the current altitude range
                values = df.loc[altitude_range].values
                first_value = values[0]  # Capture the first value
                values = values[1:]

                # Perform the Mann-Kendall test
                mann_kendall_test_result = mk.original_test(values)

                # Extract relevant test statistics
                tau = mann_kendall_test_result.Tau
                trend = mann_kendall_test_result.trend
                p_value = mann_kendall_test_result.p
                slope = mann_kendall_test_result.slope
                z_test_statics = mann_kendall_test_result.z
                tau = round(float(tau), 5)
                p_value = round(float(p_value), 5)
                slope = round(float(slope), 5)

                # Append the results to the list
                results.append([selected_state, month, altitude_range,
                                interpolation, p_value, z_test_statics, trend, year_range])

            # results_df = pd.DataFrame(results, columns=['Altitude Range', 'Interpolation', 'Trend', 'Tau', 'p-value', 'Slope'])
            results_df = pd.DataFrame(results, columns=[
                'State', 'Month', 'Altitude Range', 'Interpolation', 'p-value', 'z_test_statics', 'Trend', 'year_range'])
            # Print the DataFrame beautifully
            # Apply the style function to the DataFrame
            styled_df = results_df.style.applymap(highlight_trend_column, subset=['Trend'])
            st.dataframe(styled_df)
            tabulate(results_df, headers='keys',
                        tablefmt='fancy_grid', showindex=False)
            outcomes = {
                '- **p-value < 0.05, z-test statistics > 0**': '*Statistically significant increasing trend*',
                '- **p-value < 0.05, z-test statistics < 0**': '*Statistically significant decreasing trend*',
                '- **p-value > 0.05**': '*Fail to reject the null hypothesis of no trend*',
                '- *Note*': '_It is a non-parametric measure, so it does not make any assumptions about the distribution of the data._'
            }
            for outcome, description in outcomes.items():
                formatted_text = textwrap.fill(description, width=60)
                st.write(f"{outcome}:\n{formatted_text}",)

        def ShowGraphTemp(df, month, State, interpolation, x_ticks, YearRange, Season, type):
            # Set the 'Altitude Range' column as the index
            # print(Season)
            if Season == 'Annually':
                month = ['Annual']
            if 'Altitude Range' in df.columns:#any name possible
                df.set_index('Altitude Range', inplace=True)
            elif 'Altitude range' in df.columns:
                df.set_index('Altitude range', inplace=True)
            # Set the figure size before creating the plot
            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            # Create a selection box for states with full names
            selected_state = state_mapping[State]
            YearRange = [str(year) for year in YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted} years timeseries)'
            extrayear = '2015'
            # Customize the plot (labels, title, etc.)
            # plt.xlabel('Years of Time Series')
            # plt.ylabel('Average Annual Temperature (°C)')
            title = None
            if Season == 'Seasonally':
                title = f'State={selected_state}, interpolation={interpolation}, Season = {Season}, Months = {month} on Mean Average Temperature\n{year_range}'
            elif Season == 'Annually':
                title = f'State={selected_state}, interpolation={interpolation}, Annually on Mean Average Temperature\n{year_range}'
            else:
                title = f'State = {selected_state} using {interpolation} interpolation \nfor month = {month} ,{Season}\n mean Average Temperature\n{year_range}'

            # Customize the x-axis tick labels to emphasize every 10 years
            x_values = list(df.columns)
 
            df= df.loc[:, YearRange]
            # trendline_trace = gettrendline(df, x_values)
            # Create a checkbox for adding a trendline
            fig = None
            # Create two figures: one with a line plot and one with a scatter plot with a trendline
            fig1 = px.line(df.T, x=df.columns, y=df.index, markers=True, title=title)
            # Fit a linear regression model
            if type == "whole-range":
                # Extract the years and temperature values
                x = [int(year) for year in df.columns]  # Years as integers
                y = df.iloc[0].values
                
                # Fit a linear regression model
                X = sm.add_constant(x)  # Add a constant (intercept) term to the x variable
                model = sm.OLS(y, X).fit()
                r_squared = model.rsquared
                slope = model.params[1]
                p_value = model.pvalues[1]
                fig2 = px.scatter(df.T, x=df.columns, y=df.index, trendline="ols", opacity=0.2, render_mode='svg',color_discrete_sequence=["red"])
                fig = go.Figure(data=fig1.data + fig2.data)
            else:
                # Show only the line plot if the trendline is not selected
                fig = fig1
            x_labels = [year if int(year[-1]) % 10 in x_ticks or year ==
                        extrayear else '' for year in x_values]
            fig.update_xaxes(title="Year")
            fig.update_yaxes(title="Temperature (°C)")
            fig.update_xaxes(tickvals=x_labels, ticktext=x_values)
                # Customize the legend
            fig.update_traces(hovertemplate='<br>Year: %{x}<br>Temperature (°C):%{y} ')
            # add r_square value, p-value and slope to graph to legend
            fig.update_layout(legend_title_text='Altitude(200 mtr) range')
            st.plotly_chart(fig)
            if type == "whole-range":
                 #upto 4 decimal print r2, p-value and slope
                r_squared = round(r_squared, 4)
                p_value = round(p_value, 4)
                slope = round(slope, 4)
                st.write(f'- R-square value = {r_squared}')
                st.write(f'- p-value = {p_value}')
                st.write(f'- Slope = {slope}')

        def getresults(results, MinMaxRange):
            year_wise_data = results.iloc[0:, 0:]
            result_mean = year_wise_data.mean().to_frame().T
            result_mean.insert(0, 'Altitude Range', MinMaxRange)
            result_mean = result_mean.set_index('Altitude Range')
            return result_mean

        def getmaxminAltitudeVAlues(df):
            minAltitude = df.iloc[1, 0].split('-')[0]
            maxAltitude = df.iloc[-1, 0].split('-')[1]
            MinMaxRange = f'{minAltitude}-{maxAltitude}'
            AltitudeRange = df['Altitude Range'].values
            return MinMaxRange, AltitudeRange

        def DoComputations(state, Analysis_type, Months, interpolation, x_ticks, YearsRange, Season):
            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            _pathR_square = './static/TemperatureAnalysis/CorelationTable/TempAnnualCorelation.xlsx'
            getgetR_square(state,_pathR_square)
            # Create a selection box for states with full names
            selected_state = state_mapping[state]
            interpolatoinRangeWisePath = './static/TemperatureAnalysis/InterpolateRangeWise'
            name = state
            if Analysis_type == 'Monthly':
                _path_ = interpolatoinRangeWisePath + \
                    f'/{state}/{interpolation}200'
                monthname = None
                for month in Months:
                    monthname = month
                    # ShowingBy altitude Range
                    st.write(
                        f'State = {selected_state}, Month = {month}, Interpolation = {interpolation}')
                    st.write('Showing by various altitude range')
                    logging.info(
                        f'---State = {selected_state} , {month}--, interpoation = {interpolation}-----')
                    monthfilename = [file for file in os.listdir(
                        _path_) if month in file][0]
                    df = pd.read_excel(os.path.join(_path_, monthfilename))
                    ShowGraphTemp(df, month, state, interpolation,
                                x_ticks, YearsRange, Season)
                    logging.info(
                        f'---Plotted graph for {selected_state}-{interpolation}-{month}----')

                    st.write('Showing Mankendall test for month', month)
                    PrintMankendallTest(
                        df, state, month, interpolation, YearsRange, Season)
                    logging.info(
                        f'---Showing Sen Slope test for {selected_state}-{interpolation}-{month}----')

                    st.write(
                        f'---Showing Sen Slope test for {selected_state}-{interpolation}-{month}----')
                    PrintSenSlopeTest(df, state, month,
                                    interpolation, YearsRange, Season)
                    logging.info('')
                    st.write('Shoing Complete state graph')
                    # Now get mean of all rows leaving first column
                    # now create a new dataframe give name = {state}-Timberline to first column
                    # and mean of rows from 2nd colmn to last

                # Now go for complete state graph for that month
                _path_ = f'./static/TemperatureAnalysis/MonthlyMeanInWholeState/{state}/{interpolation}'
                monthMeanFilename = [file for file in os.listdir(
                    _path_) if monthname in file][0]
                df = pd.read_excel(os.path.join(_path_, monthMeanFilename))
                with st.expander("Complete State Temp Graph"):
                    ShowGraphTemp(df, monthname, state, interpolation,
                                x_ticks, YearsRange, Season, "altitude-wise")
                    logging.info(
                        f'---Plotted graph for {selected_state}-{interpolation}-{monthname} mean----')
                with st.expander("Complete State Temp Mankendall Test"):
                    st.write(
                        'Temperature Analysis:Showing Mankendall test for month', monthname)
                    PrintMankendallTest(
                        df, state, month, interpolation, YearsRange, Season)

                    st.write(
                        f'-Temperature Analysis : Showing Sen Slope test for {selected_state}-{interpolation}-{monthname} mean----')
                    logging.info(
                        f'---Temperature Analysis : Showing Sen Slope test for {selected_state}-{interpolation}-{monthname} mean----')
                with st.expander("Complete State Temp Sen Slope Test"):
                    PrintSenSlopeTest(df, state, monthname,
                                    interpolation, YearsRange, Season)
            elif Analysis_type == 'Annually' or Analysis_type == 'Seasonally':
                _path_ = interpolatoinRangeWisePath + \
                    f'/{state}/{interpolation}200'
                # with range and without range
                YearsRange = [str(year) for year in YearsRange]
                # with altitude range
                results = None
                altitude_range = None
                desired_months_files = []  # Getting desired files
                for month in Months:
                    for monthfile in os.listdir(_path_):
                        if month in monthfile:
                            desired_months_files.append(monthfile)
                            break
                # It will be used when we combine a whole month file
                tempfile = desired_months_files[0]
                tempdf = pd.read_excel(os.path.join(_path_, tempfile))
                MinMaxRange, altitude_range = getmaxminAltitudeVAlues(tempdf)

                for monthfile in desired_months_files:
                    file_path_ = os.path.join(_path_, monthfile)
                    df = pd.read_excel(file_path_)
                    # Store altitude_range if it's not already stored

                    df = df.loc[:, YearsRange]
                    # if results is empty then copy df to results
                    # Extract data (excluding first row and first column)
                    data = df.iloc[0:, 0:]
                    # Initialize results DataFrame if it's None
                    if results is None:
                        results = data
                    else:
                        # Add the data to the results DataFrame
                        results = results.add(data, fill_value=0)
                # Calculate the mean by dividing by the number of files
                results_mean = results / len(desired_months_files)
                # now get year of results
                results_mean.insert(0, 'Altitude Range', altitude_range)
                results_mean = results_mean.set_index('Altitude Range')

                df = results_mean
                # Set the altitude range and years as the first row and first column
                st.write('***Altitude range wise***')
                with st.expander("Range wise State Temp Graph"):
                    ShowGraphTemp(df, Months, state, interpolation,
                                x_ticks, YearsRange, Season, "altitude-wise")
                    logging.info(
                        f'---Plotted graph for {selected_state}-{interpolation}-{Months}----')

                with st.expander("Range wise Complete State Temp Mankendall Test"):
                    st.write('Temperature analysis Showing Mankendall test for month', Months)
                    PrintMankendallTest(df, state, Months,
                                        interpolation, YearsRange, Season)
                    logging.info(
                        f'---Showing Sen Slope test for {selected_state}-{interpolation}-{Months}----')

                with st.expander("Range wise Complete State Temp Sen Slope Test"):
                    st.write(f'Temperature analysis Showing Sen Slope test for {selected_state}-{interpolation}-{Months}')
                    PrintSenSlopeTest(df, state, Months,
                                    interpolation, YearsRange, Season)
                    # Now show complete analysis for all altitude range

                st.write('***Now for all altitude range***')
                modified_df = getresults(df, MinMaxRange)
                with st.expander("Complete State Temp Graph"):
                    ShowGraphTemp(modified_df, Months, state, interpolation,
                                x_ticks, YearsRange, Season, "whole-range")
                    logging.info(
                        f'---Plotted graph for {selected_state}-{interpolation}-Annual----')

                with st.expander("Complete State Temp Mankendall Test"):
                    st.write('Temperature analysis Showing Mankendall test ')
                    PrintMankendallTest(modified_df, state, Months,
                                        interpolation, YearsRange, Season)
                    logging.info(f'---Showing Sen Slope test for {selected_state}-{interpolation}-Annual----')

                with st.expander("Complete State Temp Sen Slope Test"):
                    st.write(f'Temperature analysis Showing Sen Slope test for {selected_state}-{interpolation}-Annually')
                    PrintSenSlopeTest(modified_df, state, Months,
                                    interpolation, YearsRange, Season)
                
        ## ------------------------------------------Python code for Streamlit App------------------------------------------##
        # Set up logging
        log_filename = './static/Logfiles.log'
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Output widget for displaying results
        st.title('Temperature Analysis')
        githubcode = "[Temperature Github code](https://github.com/Lokeshiiith/Climate_change_monitoring_tool/blob/main/TemperatureAnalysis.ipynb)"
        st.markdown(githubcode, unsafe_allow_html=True)
        selected_state = None
        selected_analysis_type = None
        selected_months = []
        selected_interpolation = None
        selected_years_to_show = [1, 5]
        selected_years_to_extract = [1961, 2015]
        selected_season = None
        Season = None
        st.write('## Select Analysis Parameters')

        state_mapping = {
            'Select State': 'Select State',
            'Uttarakhand': 'UK',
            'Jammu & Kashmir': 'J&K',
            'Aruranchal Pradesh': 'AP',
            'Himachal Pradesh': 'HP',
            'Sikkim': 'SK',
        }
        # Create a selection box for states with full names
        selected_full_state = st.selectbox('States:', list(state_mapping.keys()))

        selected_state = state_mapping[selected_full_state]

        # Create dropdown widget for interpolation
        selected_interpolation = st.selectbox('Interpolation:', [
            'Select Interpolation', 'Linear', 'Cubic', 'Nearest', 'IDW', 'MIDW'])

        # Create a multi-option widget for 'yearstoshow_Multioption'
        st.write("Years to Show: To customize the graph's time scale. For instance, choosing '1' and '5' displays ticks at years like 1951, 1955, 1961, 1965 and so on..")
        selected_years_to_show = st.multiselect(
            'Years to Show:', list(range(10)), [1, 5])

        # Create a range slider widget for 'yearstoextract_slider'
        selected_years_to_extract = st.slider(
            'Years to Extract:', 1961, 2015, (1961, 2015), 1)

        # selected_year_wise_analysis = st.radio(
        #     'Year Wise Analysis:', [1, 2, 3, 4, 5]
        # )
        # Create dropdown widget for type of analysis
        selected_analysis_type = st.selectbox(
            'Type of Analysis:', ['Select Analysis','Annually', 'Seasonally'])

        def on_analysis_dropdown_change(selected_analysis):
            selected_months = []
            global Season
            Season = selected_analysis
            if selected_analysis == 'Monthly':
                selected_months = [st.selectbox(
                    'Select a Month:', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
                ]
            elif selected_analysis == 'Seasonally':
                selected_season = st.selectbox(
                    'Select a Season:', ['Winter', 'Summer', 'Monsoon', 'PostMonsoon'])
                Season = selected_season
                if selected_season == 'Winter':
                    selected_months = st.multiselect(
                        'Select Months:', ['Jan', 'Feb', 'Mar', 'Apr'])
                elif selected_season == 'Summer':
                    selected_months = st.multiselect(
                        'Select Months:', ['Mar', 'Apr', 'May', 'Jun', 'Jul'])
                elif selected_season == 'Monsoon':
                    selected_months = st.multiselect(
                        'Select Months:', ['Jun', 'Jul', 'Aug', 'Sep'])
                elif selected_season == 'PostMonsoon':
                    selected_months = st.multiselect(
                        'Select Months:', ['Sep', 'Oct', 'Nov', 'Dec'])

            elif selected_analysis == 'Annually':
                selected_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                                'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return selected_months

        # Attach the change event handler to the analysis dropdown
        selected_months = on_analysis_dropdown_change(selected_analysis_type)

        st.write('## Select Analysis Parameters')
        st.write(f'Selected State: {selected_state}')
        st.write(f'Selected Analysis Type: {selected_analysis_type}')
        st.write(f'Selected Months: {selected_months}')
        st.write(f'Selected Interpolation: {selected_interpolation}')
        st.write(f'Selected Years to Show: {selected_years_to_show}')
        st.write(f'Selected Years to Extract: {selected_years_to_extract}')
        st.write(f'Selected Season: {Season}')
        # Add a submit button
        # Define an output area
        output = st.empty()
        if st.button('Submit'):
            if selected_state == 'Select State' or selected_interpolation == 'Select Interpolation':
                output.error("Please select the State and Interpolation before submitting.")
            elif selected_analysis_type == 'Select Analysis':
                output.error("Please select the Analysis Type before submitting.")
            elif selected_analysis_type == 'Seasonally' and selected_months == []:
                output.error("Please select the months for that season before submitting.")
            else:
                # Log the selected values
                logging.info(f'States: {selected_state}')
                logging.info(f'Season: {Season}')
                logging.info(f'Analysis_type: {selected_analysis_type}')
                logging.info(f'Months: {selected_months}')
                logging.info(f'Interpolation: {selected_interpolation}')
                logging.info(f'Years to Show: {selected_years_to_show}')
                logging.info(f'Years to Extract: {selected_years_to_extract}')
                logging.info('Selected values logged.')

                # Call the DoComputations function
                # Call the DoComputations function
                state, Analysis_type, Months, Interpolation, ModVal = selected_state, selected_analysis_type, selected_months, selected_interpolation, selected_years_to_show
                Years = list(
                    range(selected_years_to_extract[0], selected_years_to_extract[1] + 1))

                DoComputations(state, Analysis_type, Months, Interpolation,
                        ModVal, Years, Season)  # Fixed this line

        # Add a clear button
        if st.button('Clear'):
            selected_state = None
            selected_analysis_type = None
            selected_months = []
            selected_interpolation = None
            selected_years_to_show = [1, 5]
            selected_years_to_extract = [1961, 2015]
            selected_year_wise_analysis = 1
            Season = 'Monthly'

        # Display the output area
        output = st.empty()

        # Button to switch to Precipitation Analysis Page


    if navigation == "Precipitation Analysis":
        st.title("Precipitation Analysis Page")
        githubcode = "[Precipitaion Github code](https://github.com/Lokeshiiith/Climate_change_monitoring_tool/blob/main/PrecipitaionAnalysis.ipynb)"
        st.markdown(githubcode, unsafe_allow_html=True)
        # Your precipitation analysis code here
        def highlight_trend_column(val):
            if val != 'no trend':
                return f'background-color: red'  # Change the background color to yellow for rows with trend
            return ''  # Default style
        def highlight_result_column(val):
            if val == 'Reject':
                return f'background-color: green'  # Change the background color to yellow for rows with trend
            return ''  # Default style
        def PrintSenSlopeTest(df, state_name, interpolation, YearRange, Season):
            results = []
            YearRange = [str(year) for year in YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            # Get the year range
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted} years timeseries)'
            df = df.loc[:, YearRange]
            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            selected_state = state_mapping[state_name]
            for altitude_range in df.index:
                # Extract the precipitation values for the current altitude range
                values = df.loc[altitude_range].values
                first_value = values[0]  # Capture the first value
                precipitation = values[1:]  # Extract precipitation data

                # Convert precipitation data and years to NumPy arrays
                precipitation = np.array(precipitation, dtype=float)
                years = np.array(df.columns[1:], dtype=int)
                # Perform linear regression to calculate the slope
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    years, precipitation)
                # Find the p-value
                # Calculate t-statistic
                # t = slope / (std_err / np.sqrt(np.sum((years - np.mean(years))**2)))
                # p_value2 = 2 * (1 - stats.t.cdf(np.abs(t), len(years) - 2))
                if p_value < 0.05:
                    result = "Reject"
                else:
                    result = "Fail to reject"
                results.append([selected_state, altitude_range,
                                interpolation,  p_value, slope, result, year_range])

            # Print the extracted state name
            # Create a DataFrame from the results list
            results_df = pd.DataFrame(results, columns=[
                'State', 'Altitude Range', 'Interpolation', 'p-value', 'Slope', 'Result', 'Year Range'])
            styled_df = results_df.style.applymap(highlight_result_column, subset=['Result'])
            st.dataframe(styled_df)

            # Display result explanations
            st.write("Result Explanations:")
            outcomes = {
                "Reject": "This means that the data provides sufficient evidence to conclude that the null hypothesis is false.",
                "Fail to reject": "This means that the data does not provide sufficient evidence to conclude that the null hypothesis is false.",
            }

            for outcome, description in outcomes.items():
                st.write(f"{outcome}:\n{description}")
            # Print formatted outcomes
            # for outcome, description in outcomes.items():
            #     # Adjust the width as needed
            #     formatted_text = textwrap.fill(description, width=60)
            #     print(f"{outcome}:\n{formatted_text}\n")

        def PrintMankendallTest(df, State, interpolation, YearRange, Season):
            # Create a list to store the results

            results = []
            # Change YearRange to string as df.columns is string
            # modify the df now
            YearRange = [str(year) for year in YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted} years timeseries)'
            df = df.loc[:, YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            # Get the year range
            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            selected_state = state_mapping[State]
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted})'
            for altitude_range in df.index:
                # Filter the data frame to the current altitude range
                values = df.loc[altitude_range].values
                first_value = values[0]  # Capture the first value
                values = values[1:]

                # Perform the Mann-Kendall test
                mann_kendall_test_result = mk.original_test(values)

                # Extract relevant test statistics
                tau = mann_kendall_test_result.Tau
                trend = mann_kendall_test_result.trend
                p_value = mann_kendall_test_result.p
                slope = mann_kendall_test_result.slope
                z_test_statics = mann_kendall_test_result.z

                tau = round(float(tau), 5)
                p_value = round(float(p_value), 5)
                slope = round(float(slope), 5)

                # Append the results to the list
                results.append([selected_state, altitude_range,
                                interpolation, p_value, z_test_statics, trend, year_range])

            # results_df = pd.DataFrame(results, columns=['Altitude Range', 'Interpolation', 'Trend', 'Tau', 'p-value', 'Slope'])
            results_df = pd.DataFrame(results, columns=[
                'State', 'Altitude Range', 'Interpolation', 'p-value', 'z_test_statics', 'Trend', 'Year Range'])
            styled_df = results_df.style.applymap(highlight_trend_column, subset=['Trend'])
            
            st.dataframe(styled_df)
            # print(tabulate(results_df, headers='keys',
                        # tablefmt='fancy_grid', showindex=False))
            outcomes = {
                'p-value < 0.05, z_test_statics > 0':	'Statistically significant increasing trend',
                'p-value < 0.05, z_test_statics < 0':	'Statistically significant decreasing trend',
                'p-value > 0.05':	'Fail to reject the null hypothesis of no trend',
                'Note ': 'It is a non-parametric measure, so it does not make any assumptions about the distribution of the data.'
            }
            for outcome, description in outcomes.items():
                formatted_text = textwrap.fill(description, width=100)
                st.write(f"{outcome}:\n{formatted_text}")

        def ShowGraphPrecip(df, State, interpolation, x_ticks, YearRange, Season):
            # Set the 'Altitude Range' column as the index
            st.write(Season)
            if 'Altitude Range' in df.columns:
                df.set_index('Altitude Range', inplace=True)
            elif 'Altitude range' in df.columns:
                df.set_index('Altitude range', inplace=True)
            # Set the figure size before creating the plot
            YearRange = [str(year) for year in YearRange]
            yearcounted = int(YearRange[-1]) - int(YearRange[0]) + 1
            year_range = f'{YearRange[0]} - {YearRange[-1]} #({yearcounted} years timeseries)'
            plt.figure(figsize=(12, 20))
            state_mapping = {
                'Select State': 'Select State',
                'UK': 'Uttarakhand',
                'J&K': 'Jammu & Kashmir',
                'AP': 'Aruranchal Pradesh',
                'HP': 'Himachal Pradesh',
                'SK': 'Sikkim',
            }
            selected_state = state_mapping[State]
            # Create a line plot
            ax = df.T.plot(kind='line', marker='o')
            x_values = list(df.columns)
            # Add a trendline to the plot
            # for altitude_range in df.index:
            #     values = df.loc[altitude_range].values
            #     x = np.arange(len(x_values))
            #     slope, intercept, r_value, p_value, std_err = linregress(x, values)
            #     trendline = intercept + slope * x
            #     ax.plot(x, trendline, label=f'Trendline ({altitude_range})', linestyle='--')
            extrayear = '2015'
            # Customize the plot (labels, title, etc.)
            # plt.xlabel('Years of Time Series')
            # plt.ylabel('Average Average Precipitation')
            title = f'State - {selected_state} using {interpolation} interpolation \n for Annual Average Precipitation\n{year_range}'
            # Customize the x-axis tick labels to emphasize every 10 years
            df= df.loc[:, YearRange]
            x_values = YearRange
            # trendline_trace = gettrendline(df, x_values)
            fig1 = px.line(df.T, x=df.columns, y=df.index, markers=True, title=title)
            fig2 = px.scatter(df.T, x=df.columns, y=df.index, trendline="ols", opacity = 0.2, render_mode = 'svg')
            fig = go.Figure(data = fig1.data + fig2.data)
            x_labels = [year if int(year[-1]) % 10 in x_ticks or year ==
                        extrayear else '' for year in x_values]
            fig.update_xaxes(title="Years of Time Series")
            fig.update_yaxes(title="Average Precipiataion (mm)")
            fig.update_xaxes(tickvals=x_labels, ticktext=x_values)
            fig.update_traces(hovertemplate='<br>Year: %{x}<br>Precipitation(mm):%{y} ')

                # Customize the legend
            fig.update_layout(legend_title_text='Altitude(200 mtr) range')
            st.plotly_chart(fig)
        def getresults(results, MinMaxRange):
            if 'Altitude Range' in results.columns:#any name possible
                results.set_index('Altitude Range', inplace=True)
            elif 'Altitude range' in results.columns:
                results.set_index('Altitude range', inplace=True)
            year_wise_data = results.iloc[0:, 0:]
            result_mean = year_wise_data.mean().to_frame().T
            result_mean.insert(0, 'Altitude Range', MinMaxRange)
            result_mean = result_mean.set_index('Altitude Range')
            return result_mean

        def getmaxminAltitudeVAlues(df):

            minAltitude = df['Altitude Range'][0].split('-')[0]
            maxAltitude = df['Altitude Range'][df.shape[0]-1].split('-')[1]
            MinMaxRange = f'{minAltitude}-{maxAltitude}'
            AltitudeRange = df['Altitude Range'].values
            return MinMaxRange, AltitudeRange

        def DoComputations(state, interpolation, x_ticks, YearsRange, Season):
            YearsRange = [str(year) for year in YearsRange]
            interpolatoinRangeWisePath = './static/PrecipitaionAnalysis/InterpolateRangeWise'
            name = state
            _path_ = interpolatoinRangeWisePath + f'/{interpolation}200'
            # ShowingBy altitude Range
            st.write('Showing by various altitude range')
            logging.info(
                f'---State = {state} --, interpoation = {interpolation}-----')
            df = pd.read_excel(os.path.join(_path_, f'{state}.xlsx'))
            selected_columns = ['Altitude Range'] + \
                [str(year) for year in YearsRange]
            df = df[selected_columns]
            df_modified = df
            df = df.set_index('Altitude Range')
            # print(df)
            ShowGraphPrecip(df, state, interpolation, x_ticks, YearsRange, Season)
            logging.info(f'---Plotted graph for {name}-{interpolation}----')

            st.write('PrecipitaionAnalysis  Showing Mankendall test for state', state)
            PrintMankendallTest(df, state, interpolation, YearsRange, Season)
            logging.info(
                f'---Showing Sen Slope test for {name}-{interpolation}-----')

            st.write(
                f'PrecipitaionAnalysis ---Showing Sen Slope test for {name}-{interpolation}- ----')
            PrintSenSlopeTest(df, state, interpolation, YearsRange, Season)

            logging.info('')
            st.write(f'Showing Complete {state} Precipitaion  graph and analysis')
            MinMaxRange, altitude_range = getmaxminAltitudeVAlues(df_modified)

            # now get year of results
            # df.insert(0, 'Altitude Range', altitude_range)

            # Now show complete analysis for all altitude range
            modified_df = getresults(df_modified, MinMaxRange)
            ShowGraphPrecip(modified_df, state, interpolation,
                        x_ticks, YearsRange, Season)
            logging.info(f'---Plotted graph for {name}-{interpolation}-Annual----')

            st.write('Showing Mankendall test for whole state', state)
            PrintMankendallTest(modified_df, state,
                                interpolation, YearsRange, Season)
            logging.info(
                f'---Showing Sen Slope test for {name}-{interpolation}-Annual----')

            st.write(
                f'---Showing Sen Slope test for {name}-{interpolation}-Annual----')
            PrintSenSlopeTest(modified_df, state,
                            interpolation, YearsRange, Season)

        def flatten_list(input_list):
            result = []
            for item in input_list:
                if isinstance(item, tuple):
                    result.extend(item)
                else:
                    result.append(item)
            return result

        log_filename = './static/Logfiles.log'
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Output widget for displaying results
        st.title('Precipitaion Analysis')
        selected_state = None
        selected_months = []
        selected_interpolation = None
        selected_years_to_show = [1, 5]
        selected_years_to_extract = [1951, 2015]
        selected_season = None
        Season = None
        st.write('## Select Analysis Parameters')
        Months = []
        Analysis_type = None
        Season = 'ANNUALLY'
        state_mapping = {
            'Select State': 'Select State',
            'Uttarakhand': 'UK',
            'Jammu & Kashmir': 'J&K',
            'Aruranchal Pradesh': 'AP',
            'Himachal Pradesh': 'HP',
            'Sikkim': 'SK',
        }
        # Create a selection box for states with full names
        selected_full_state = st.selectbox('States:', list(state_mapping.keys()))

        selected_state = state_mapping[selected_full_state]

        # Create dropdown widget for interpolation
        selected_interpolation = st.selectbox('Interpolation:', [
            'Select Interpolation', 'Linear', 'Cubic', 'Nearest', 'IDW', 'MIDW'])

        # Create a multi-option widget for 'yearstoshow_Multioption'
        st.write("Years to Show: To customize the graph's time scale. For instance, choosing '1' and '5' displays ticks at years like 1951, 1955, 1961, 1965 and so on..")
        selected_years_to_show = st.multiselect(
            'Years to Show:', list(range(10)), [1, 5])

        # Create a range slider widget for 'yearstoextract_slider'
        selected_years_to_extract = st.slider(
            'Years to Extract:', 1951, 2015, (1951, 2015), 1)

        st.write('## Select Analysis Parameters')
        st.write(f'Selected State: {selected_state}')
        st.write(f'Selected Interpolation: {selected_interpolation}')
        st.write(f'Selected Years to Show: {selected_years_to_show}')
        st.write(f'Selected Years to Extract: {selected_years_to_extract}')
        st.write(f'Selected Season: {Season}')

        # Always annually so no problem
        # Add a submit button
        if st.button('Submit'):
            # Log the selected values
            logging.info(f'States: {selected_state}')
            logging.info(f'Season: {Season}')
            logging.info(f'Interpolation: {selected_interpolation}')
            logging.info(f'Years to Show: {selected_years_to_show}')
            logging.info(f'Years to Extract: {selected_years_to_extract}')
            logging.info('Selected values logged.')

            # Call the DoComputations function
            # Call the DoComputations function
            state,   Interpolation, ModVal = selected_state, selected_interpolation, flatten_list(
                selected_years_to_show)
            Years = list(
                range(selected_years_to_extract[0], selected_years_to_extract[1]+1))

            DoComputations(state, Interpolation, ModVal,Years, Season)  # Fixed this line

        # Add a clear button
        # Add a clear button
        if st.button('Clear'):
            selected_state = None
            selected_analysis_type = None
            selected_months = []
            selected_interpolation = None
            selected_years_to_show = [1, 5]
            selected_years_to_extract = [1951, 2015]
            Season = 'ANNUAL'

        # Display the output area
        output = st.empty()


    if navigation == "Problem Visualize":
        plt.title("Himalayan Mountain")

        def printSinCurve():
            """
            The Himalayan mountain range is a diverse landscape with a wide range of vegetation types.
            Vegetation changes with elevation, and each type is adapted to the specific climate conditions at that altitude.
            """
        def printTimberline():
            """
            The timberline is the boundary between where trees can and cannot grow.
            It's a critical line for biodiversity and an important indicator of climate change.
            As the climate warms, the timberline is moving higher up the mountain, shrinking the area where trees can grow.
            """
        def printtreeline():
            """
            The treeline is the boundary between where trees can and cannot grow.
            The trees in the treeline are stunted and gnarled, and the vegetation is sparse.
            The treeline is also moving higher up the mountain as the climate warms.
            """
        def printbelowTimberline():
            """
            Below the timberline, the vegetation is lush and diverse.
            There are a wide range of tree species, as well as shrubs, wildflowers, and grasses.
            This vegetation provides habitat for a wide range of animals.
            """
        def printaboveTimber_belowTreeline():
            """
            Between the timberline and the treeline is a transition zone where the vegetation is mixed.
            This vegetation is more tolerant of cold and wind than the vegetation below the timberline.
            """
        def printaboveTreeline():
            """
            Above the treeline, the vegetation is sparse.
            There are a few hardy plants, such as lichens and mosses, but there are no trees.
            The climate in this area is cold and windy, and the growing season is short.
        """

        def printWhatsProblem():
           
            """What and why is that happpeing ?:
            The shift of alpine meadows to higher altitudes is primarily a consequence of global climate change.
            As temperatures rise due to various environmental factors, including the increase in greenhouse gases, these previously stable ecosystems are now experiencing significant shifts.

            The key factors contributing to this shift are:

            1. Temperature Increase: Rising global temperatures are causing a "thermal migration" of plant life, including alpine meadows. 
            As temperatures become warmer, these meadows are gradually moving to higher altitudes in search of cooler conditions that are essential for their survival.

            2. Altered Precipitation Patterns: Changes in precipitation patterns further influence the distribution of alpine meadows. 
            Inconsistent rainfall and altered snowfall patterns are affecting the availability of water in these ecosystems, prompting them to move to more favorable locations.

            3. Competitive Advantage: Alpine meadows are often highly adaptable and competitive plant species. 
            They may outcompete endemic species in their new locations, leading to a displacement of the native flora.

            4. Loss of Endemic Species: The shift of alpine meadows into higher altitudes can indeed pose a threat to endemic species. 
            As these meadows spread, they may displace the native plant life, potentially leading to the extinction of endemic species that are adapted to the unique conditions of their original habitats.
            """
        # make alist of these print functions

        def sincurve():
            angles = np.linspace(0, 180, 1000)
            y = np.sin(np.deg2rad(angles))
            plt.plot(angles, y)

        def timberline():
            sincurve()
            timberline = 0.3
            plt.axhline(y=timberline, color='g', linestyle='--', label='')
            plt.text(180, timberline, 'timberline', verticalalignment='bottom', horizontalalignment='right', color='r')
            plt.legend(loc='upper right', frameon=False)

        def treeline():
            sincurve()
            timberline()
            treeline = 0.7
            plt.axhline(y=treeline, color='r', linestyle='--', label='')
            plt.text(180, treeline, 'treeline', verticalalignment='bottom', horizontalalignment='right', color='r')
            plt.legend(loc='upper right', frameon=False)

        def belowTimberline():
            sincurve()
            timberline()
            treeline()
            x = np.random.uniform(25, 150, 300)
            y = np.random.uniform(0, 0.28, 300)
            plt.scatter(x, y, c='g', s=50)
            plt.annotate("Well Flourished", xy=(155, 0.2), xytext=(160, 0.1),
                        arrowprops=dict(facecolor='green', shrink=0.05), fontsize=12)

        def aboveTimber_belowTreeline():
            sincurve()
            timberline()
            treeline()
            belowTimberline()
            x = np.random.uniform(50, 130, 70)
            y = np.random.uniform(0.3, 0.7, 70)
            plt.scatter(x, y, c='g', s=50)
            plt.annotate("Less dense", xy=(135, 0.6), xytext=(140, 0.5),
                        arrowprops=dict(facecolor='green', shrink=0.05), fontsize=12)

        def aboveTreeline():
            endemic_points = [
                (50, .75),
                (52, .8),
                (54, .8),
                (75, .74),
                (77, .87),
                (79, .8),
                (110, .8),
                (102, .8),
                (104, .8),
                (120, .74),
                (127, .75),
                ]   
            sincurve()
            timberline()
            treeline()
            belowTimberline()
            aboveTimber_belowTreeline()
            selected_indices = np.random.choice(range(len(endemic_points)), 6)
            selected_endemic_points = [endemic_points[i] for i in selected_indices]
            x_endemic, y_endemic = zip(*selected_endemic_points)
            
            plt.scatter(x_endemic, y_endemic, c='r', s=50, label='Endemic Species')
            plt.legend(loc='upper right')  # Add a legend for clarity
            plt.annotate("Endemic species", xy=(125, 0.8), xytext=(130, 0.8),
                        arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12)
        
        def WhatsProblem():
            sincurve()
            timberline()
            treeline()
            plt.annotate("What is the problem then", xy=(135, 0.6), xytext=(140, 0.5),
                        arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12)
            plt.annotate("Alpine meadow shift", xy=(115, 0.85), xytext=(120, 0.2),
                        arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12)
        # Initial data
            red_x = np.random.uniform(70, 110, 2)
            red_y = np.random.uniform(0.75, .9, 2)
            green_x = np.random.uniform(90, 110, 5)
            green_y = np.random.uniform(0.75, .9, 5)
            plt.scatter(red_x, red_y, c='r', s=50)
            plt.scatter(green_x, green_y, c='g', s=50)

        printfunctions = [printSinCurve, printTimberline, 
                        printtreeline, printbelowTimberline, 
                        printaboveTimber_belowTreeline, printaboveTreeline, printWhatsProblem]
        functions = [sincurve, timberline, 
                    treeline, belowTimberline,
                    aboveTimber_belowTreeline, 
                    aboveTreeline, WhatsProblem]
        current_function_index = st.session_state.get("current_function_index", 0)


        # Call the selected function and display it
        st.write(functions[current_function_index].__doc__)
        st.write(printfunctions[current_function_index].__doc__)
        functions[current_function_index]()
        st.pyplot()
        if st.button("Previous"):
            current_function_index = (current_function_index - 1) % len(functions)
            st.session_state.current_function_index = current_function_index

        if st.button("Next"):
            current_function_index = (current_function_index + 1) % len(functions)
            st.session_state.current_function_index = current_function_index


 