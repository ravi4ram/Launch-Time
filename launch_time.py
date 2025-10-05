import numpy as np
from datetime import datetime, timedelta, timezone
import pytz


# """       
# The launch time is the time when the launch site on the surface of the Earth passes through the orbital plane.
# 
# The launch site must pass through the orbit, which impose three conditions:
#     1. No launch window: φ > i or φ > 180∘ − i(retrograde)
#     2. One launch window: φ = i or φ = 180∘ − i(retrograde)
#     3. Two launch windows: φ < i or φ < 180∘ − i(retrograde)
# 
# Given Data:
#     i, orbit inclination.
#     φ, launch site latitude.
#     Ω, right ascension of the ascending node (RAAN)
#     t, UTC 0 hr launch datetime -(Y, M, D, 0, 0, 0) 
#     
# To compute Launch time, we need to calculate local sidereal time (LST) through the parameters:
#     δ, window location angle.
#     α, direction auxiliary angle.
#     β, launch azimuth: the angle from the north to the launch direction, positive clockwise.
# 
# Launch time:    
# t = LST / 360 * sidereal day  (time since equinox)   
# launch time = UTC 0 hr launch datetime + time since equinox
# 
# 
# Based on:
#     1. Time, Calendars and Launch Windows — Introduction to Spacecraft Dynamics
#        [https://www.angadhn.com/SpacecraftDynamics/orbital-mechanics/Lecture10/Lecture10.html ]
#     2. Chapter 5 – Launch Windows and Time
#        [ https://colorado.pressbooks.pub/introorbitalmechanics/chapter/launch-windows-and-time/ ]
#     3. Astronautics-The Physics of Space Flight. Walter, Ulrich
#        [ Chapter 8.6.1 Launch Phase ]
#     4. MISSION DESIGN AND ANALYSIS FOR IRNSS-1A
#        [ https://www.researchgate.net/publication/277475032_MISSION_DESIGN_AND_ANALYSIS_FOR_IRNSS-1A ]
d
# 
# Author: Ravi Ram       
# """


# sidereal day on earth is approximately 86164.0916 seconds
# (23 * 60 * 60 + 56 * 60 + 4.0916  (seconds)
sidereal_day = 86164.0916
    
# datetime format
dt_format = "%Y-%m-%d %H:%M:%S"

# convert UTC datetime to IST datetime
def UTCtoIST(dt):  
    return dt.astimezone(pytz.timezone('Asia/Kolkata'))

# check input data
#     i is the orbit inclination.
#     φ is the launch site latitude.
# returns True/False on validity
def check_input(i, lat):
    output = False
    if (lat > i) or (lat > 180 - i ):
        # No launch window: φ => i or φ > 180∘ − i (retrograde)
        output =  False
    elif (lat == i) or (lat == 180 - i ):
        # One launch window: φ = i or φ = 180∘ − i (retrograde)
        output =  True
    elif (lat < i) or (lat < 180 - i ):
        # Two launch windows: φ < i or φ < 180∘ − i (retrograde)
        output = True 
    else:
        # Unknown ∘
        output = False
        
    # if i < 90:
    #     print(f'Prograde Orbit (i={i} < 90∘ ) and Northern Hemisphere\n')
    # else:    
    #     print(f'Retrograde Orbit (i={i} ≥ 90∘ ) and Northern Hemisphern')

    return output


# calculate from the given inputs[ i-inclination, φ-launch site latitude]:
# NOTE: launch sites have constraints on launch azimuth.
#     δ is the window location angle.
#     α is the direction auxiliary angle.
#     β is the launch azimuth: the angle from the north to the launch direction,
#       positive clockwise.
# 1 Ascending Node:
#     β = δ
#     LST = Ω + δ
# 2 Descending Node:
#     β = 180∘ - γ
#     LST = Ω + 180∘ - δ

def calculate_launch_time(launch_datetime, i, lat, az_bound, RAAN):
    # validity check    
    status = check_input(i, lat)
    if not status:
        printf(f'Not valid inputs : φ={lat}  i={i}')
        return
    
    # γ: Launch-Direction Auxiliary Angle,  cos(i) =  sin(γ) cos(φ)
    gamma_rad = np.arcsin(np.cos(np.radians(i)) / np.cos(np.radians(lat)))
    gamma_deg = np.degrees(gamma_rad)

    # δ: Launch-Window Location Angle
    delta_rad = np.arccos(np.cos(np.radians(gamma_deg)) / np.sin(np.radians(i)))
    delta_deg = np.degrees(delta_rad)

    # launch azimuth for ascending node
    azimuth_an_deg = delta_deg

    # launch azimuth for descending node
    azimuth_dn_deg = 180 - gamma_deg

    # find azimuth within boundaries
    azimuth = [azimuth_an_deg, azimuth_dn_deg]
    azi =  [i for i in azimuth if az_bound[0] <= i <= az_bound[1]]

    # check azimuth
    if not azi:
        print(f'ERROR: no possible azimuth within boundaries : {azi}' )
        exit()

    # find angle that the Earth must rotate
    for val in azi:
        if val == azimuth_an_deg:
            print(f'ascending node for launch azimuth: {azimuth_an_deg:.4f}°')
            
            # LST at the ascending node: LWSTAN = Ω + δ
            LST_AN_deg = RAAN + delta_deg
            # adding a convenient angle of 360 deg
            LST_AN_deg = LST_AN_deg % 360
            # time since equinox
            t = LST_AN_deg / 360 * sidereal_day
            launch_time = launch_datetime + timedelta(seconds=t)
        elif val == azimuth_dn_deg:
            print(f'descending node for launch azimuth: {azimuth_dn_deg:.4f}°')        

            # LST at the descending node: LWSTDN = Ω + 180 - δ
            LST_DN_deg = RAAN + 180 - delta_deg
            # adding a convenient angle of 360 deg
            LST_DN_deg = LST_DN_deg % 360
            # time since equinox
            t = LST_DN_deg / 360 * sidereal_day
            #print(f'time since vernal equinox = {t:.4f} sec' )  
            launch_time = launch_datetime + timedelta(seconds=t)
        # end-if else    
        print(f'launch time UTC : [{launch_time.strftime(dt_format)}]  IST : [{UTCtoIST(launch_time).strftime(dt_format)}]' )
    # end function
    return

# estimate targeted RAAN given azimuth on a launch_time
# calculate from the given inputs[ azimuth, launch_time, i-inclination, φ-launch site latitude]:
#     t time since equinox from launch_time
#     δ is the window location angle.
#     α is the direction auxiliary angle.
#     β is the launch azimuth: the angle from the north to the launch direction,
#       positive clockwise.
# 1 Ascending Node:
#     β = δ
#     Ω = LST - δ
# 2 Descending Node:
#     β = 180∘ - γ
#     Ω = LST - 180∘ + δ
def calculate_launch_raan(launch_time, i, lat, azimuth):
    # validity check    
    status = check_input(i, lat)
    if not status:
        printf(f'Not valid inputs : φ={lat}  i={i}')
        return

    # time since 0hr UTC
    t = int(launch_time.hour) * 3600 + int(launch_time.minute) * 60 + int(launch_time.second)
    
    # local sidereal time
    LST_deg = t * 360 / sidereal_day
    
    # γ: Launch-Direction Auxiliary Angle,  cos(i) =  sin(γ) cos(φ)
    gamma_rad = np.arcsin(np.cos(np.radians(i)) / np.cos(np.radians(lat)))
    gamma_deg = np.degrees(gamma_rad)

    # δ: Launch-Window Location Angle
    delta_rad = np.arccos(np.cos(np.radians(gamma_deg)) / np.sin(np.radians(i)))
    delta_deg = np.degrees(delta_rad)
    
    # launch azimuth for ascending node
    azimuth_an_deg = delta_deg

    # launch azimuth for descending node
    azimuth_dn_deg = 180 - gamma_deg
    
    # find which one is close within 10 degrees to decide asc/dec node
    ch_an = np.isclose(azimuth, azimuth_an_deg, atol=10.0, equal_nan=False)
    ch_dn = np.isclose(azimuth, azimuth_dn_deg, atol=10.0, equal_nan=False)
    
    # determine ascending/descending node
    if ch_an:
        # assume launch azimuth as ascending node
        delta_deg = azimuth
        # LST at the ascending node: LWSTAN = Ω + δ
        RAAN_deg = ( LST_deg - delta_deg )  % 360   
        return RAAN_deg
        
    if ch_dn:
        # assume launch azimuth as descending node
        gamma_deg = 180 - azimuth
        # LST at the descending node: LWSTDN = Ω + 180 - δ
        RAAN_deg = ( LST_deg + delta_deg - 180 )  % 360
        return RAAN_deg
    
    # return an error code otherwise
    return -1

# PSLV-C22/IRNSS-1A was launched on 1831(UTC), July 01, 2013
# MISSION DESIGN AND ANALYSIS FOR IRNSS-1A
# https://www.researchgate.net/publication/277475032_MISSION_DESIGN_AND_ANALYSIS_FOR_IRNSS-1A
def test_case_1():
    # sriharikota constraints on launch azimuth.
    az_constraints = [0, 140]
    
    # launch site latitude in ∘, launch site longitude in ∘ 
    lat = 13.7   
    lon = 80.25
    
    # launch_datetime (UTC 0 hr)    
    launch_datetime = datetime(2013, 7, 1, 0, 0, 0).replace(tzinfo=pytz.utc)
    
    # orbit spec
    RAAN = 143       # Ω, orbit RAAN in ∘
    i = 17.877       # i, orbit inclination in ∘
    
    print(f'launch time for IRNSS-1A')
    print(f'RAAN = {RAAN},  inclination  = {i}')
    print('---------------------------------')
    
    # launch_time 
    calculate_launch_time(launch_datetime, i, lat, az_constraints, RAAN)
    # 2013-07-01 18:12:38.153591+00:00 sec
    print('---------------------------------\n')

   
    # reverse calculation (using azimuth check RAAN matches original) for testing
    azimuth = 101.5964
    launch_datetime = datetime(2013, 7, 1, 18, 31, 25).replace(tzinfo=pytz.utc)
    
    print(f'Reverse calculation (Find RAAN using azimuth, launch_datetime)')
    print(f'inclination  = {i}')
    print(f'Azimuth = {azimuth},  Launch Datetime  = {launch_datetime}')
    print('---------------------------------')
    RAAN = calculate_launch_raan(launch_datetime, i, lat, azimuth)

    print(f'RAAN        = {RAAN:.4f}°')
    print('---------------------------------\n')

    # end-test_case
    return


# main function
if __name__ == "__main__":
    
    # launch_time of PSLV-C22/IRNSS-1A 
    test_case_1()
    
    """
    python3 launch_time.py
    
    launch time for IRNSS-1A
    RAAN = 143,  inclination  = 17.877
    ---------------------------------
    ascending node for launch azimuth: 49.0931°
    launch time UTC : [2013-07-01 12:46:16]  IST : [2013-07-01 18:16:16]
    descending node for launch azimuth: 101.5964°
    launch time UTC : [2013-07-01 18:12:38]  IST : [2013-07-01 23:42:38]
    ---------------------------------

    Reverse calculation (Find RAAN using azimuth, launch_datetime)
    inclination  = 17.877
    Azimuth = 101.5964,  Launch Datetime  = 2013-07-01 18:31:25+00:00
    ---------------------------------
    RAAN        = 147.7080°
    ---------------------------------
    """
    
