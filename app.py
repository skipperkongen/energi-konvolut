import streamlit as st
import pandas as pd
import numpy as np

# https://www.gasel.dk/vaerd-at-vide/hvor-meget-stroem-producerer-en-vindmoelle
# https://nyheder.tv2.dk/klima/2022-08-30-her-er-de-danske-havvindmoelleeventyr

st.title('Dæk Danmarks energibehov med vedvarende kilder')

st.warning('Advarsel: Antager at solen altid skinner og vinden altid blæser. TODO: batterier', icon="⚠️")

with st.sidebar:
    solar_GW = st.slider('Solpaneler GW', 0, 200, 0)  # min: 0h, max: 23h, default: 17h
    vind_GW = st.slider('Vindmøller GW', 0, 10, 2)  # min: 0h, max: 23h, default: 17h
    battery_cap_GWh = st.slider('Batteri kapacitet GWh', 0, 100, 0)  # min: 0h, max: 23h, default: 17h

def get_consumption_TWh():
    return 34.3

def get_production_TWh():
    solar_TWh = solar_GW
    vind_TWh = vind_GW * 5333 / 1000
    return round(solar_TWh + vind_TWh, 2)

def get_hourly_solar():
    day_cycle = 24
    annual_cycle = 365
    n_hours = day_cycle*annual_cycle
    X = np.arange(n_hours)
    Y = np.sin(X/daycycle) + np.sin_()

def pv_dist():
    """
    Normalised PV output distribution computed from monthly means in PVWatts file
    - Array indices = month (0 indexed), hour of day (0 indexed)
    """
    return array([
         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.038, 0.126, 0.225, 0.251, 0.213, 0.119, 0.019, 0., 0.,0., 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0., 0., 0., 0.056,0.169, 0.277, 0.328, 0.336, 0.32 , 0.26 , 0.162, 0.041, 0.,0., 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0., 0.005, 0.068, 0.202, 0.333, 0.439, 0.504, 0.512, 0.455, 0.357, 0.234, 0.126, 0.024, 0., 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0.007, 0.057, 0.183, 0.333, 0.463, 0.549, 0.575, 0.543, 0.523, 0.451, 0.337, 0.214, 0.087, 0.015, 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0.005, 0.047, 0.126, 0.276, 0.438, 0.571, 0.655, 0.679, 0.646, 0.623, 0.54 , 0.414, 0.282, 0.143, 0.054, 0.009, 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0.015, 0.062, 0.138, 0.277, 0.426, 0.547, 0.65 , 0.709, 0.713, 0.669, 0.58 , 0.45 , 0.312, 0.177, 0.08 , 0.03 , 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0.007, 0.047, 0.112, 0.236, 0.377, 0.503, 0.612, 0.675, 0.671, 0.645, 0.571, 0.452, 0.32 , 0.179, 0.075, 0.025, 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0.016, 0.075, 0.205, 0.359, 0.483, 0.6 , 0.658, 0.658, 0.608, 0.51 , 0.373, 0.242, 0.113, 0.032, 0.003, 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0., 0.02 , 0.108, 0.226, 0.329, 0.422, 0.474, 0.477, 0.439, 0.363, 0.246, 0.13 , 0.033, 0.001, 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0., 0., 0.027, 0.138, 0.248, 0.34 , 0.385, 0.371, 0.35 , 0.255, 0.116, 0.019, 0., 0., 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0., 0., 0., 0.018, 0.111, 0.183, 0.223, 0.206, 0.18 , 0.092, 0.009, 0., 0., 0., 0., 0., 0., 0., 0. ],
         [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.054, 0.141, 0.205, 0.19 , 0.152, 0.058, 0., 0., 0., 0., 0., 0., 0., 0., 0. ]]
     ])

def demand_dist():
    """
    About:
    - Distribution follows nordpool spot prices
    - Array indices = hour of day
    """
    return np.array([0.03529578, 0.03315591, 0.03214982, 0.03167976, 0.03195537,
       0.0342873 , 0.04257203, 0.0500294 , 0.0525266 , 0.04836528,
       0.04389886, 0.04096723, 0.03785774, 0.03547746, 0.0345392 ,
       0.03643008, 0.04011653, 0.0476938 , 0.05329773, 0.05576439,
       0.05228627, 0.04783387, 0.0438787 , 0.0379409 ])

def demand_by_hour(annual_demand_TWh=34.3):
    year_hours = 24*365
    mean_demand = annual_demand_TWh / year_hours
    daily = demand_dist()
    return np.concatenate([daily for _ in range(365)]) * mean_demand * 24


col1, col2, col3, col4 = st.columns(4)
col1.metric("Årlig production", f"{get_production_TWh()} TWh", "")
col2.metric("Årligt forbrug", f"{get_consumption_TWh()} TWh", "")
col3.metric("Dækning", f"{round(get_production_TWh()/get_consumption_TWh(), 2)*100}%", "")
