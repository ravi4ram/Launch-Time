# Launch Time
> Program implemented to calculate the ideal time to launch into an orbit for a given RAAN and an inclination.  
> Also functions are provided to calculate RAAN for a specific launch time at certain azimuth and inclination.    


## Table of contents
* [General info](#general-info)
* [References](#references)
* [Setup](#setup)
* [How to run ](#how)
* [Updates](#updates)
* [To-do list](#to-do)


## General info
### Launch Time    
It defines the moment in time when the launch site is in the targeted orbital plane and the satellite can be launched with the least effort (delta-v budget).      
&nbsp;         
### Launch Window    
Allowable range of launch time period is called launch window.
&nbsp;         

Apart from orbital mechanics, there are other restrictions defining other kinds of launch windows on different time scales. An important consideration is the sun angle, which is the angle between the direction to the sun and the targeted orbital plane. The sun angle is important for visibility conditions and for solar power generation.
&nbsp;        

For a given launch site, the range of permitted launch azimuths is usually restricted due to safety concerns of flying a launch vehicle over densely populated areas. For instance, the launch azimuth restrictions at Sriharikota Launch Center (SDSC) are 0° < β < 140°    
&nbsp;        
For azimuth restrictions on other spaceports refer :    https://ofrohn.github.io/seh-doc/list-lc.html
&nbsp;    
   

*The launch site must pass through the orbit, thus three conditions:*    
[ i is the orbit inclination and φ is the launch site latitude ]    

1. No launch window: φ > i or φ > 180∘ − i(retrograde)    
2. One launch window: φ = i or φ = 180∘ − i(retrograde)    
3. Two launch windows: φ < i or φ < 180∘ − i(retrograde)   

In order to determine when to launch, we need to find the local sidereal time (LST) when the intersections of the launch site and the orbital plane happens.    

*Using the input data,*   
i, orbit inclination.
φ, launch site latitude.
Ω, right ascension of the ascending node (RAAN)
t, UTC 0 hr launch datetime -(Y, M, D, 0, 0, 0) 

*To compute local sidereal time (LST), we need to calculate:*    
δ, the window location angle.     
α, the direction auxiliary angle.      
β, the launch azimuth: the angle from the north to the launch direction, positive clockwise.  
  
*Launch time:*     
t = LST / 360 * sidereal day  (time since equinox)   
launch time = UTC 0 hr launch datetime + time since equinox    

 

&nbsp;      

                              ^ launch azimuth
                              |  β  /
                              |   /
                              | /
                         (c)  O Launch site
                            / |
                          /   |
                        /   γ |
                      /       |
              orbit /         | φ = local latitude of the launch site
                  /           |
                /             |
              /               |
            /  i              |
    ---------------------------  Equator
       (a) | <------ δ -----> | (b)
        


&nbsp;    
To calculate δ and α, We use the right spherical triangle identities    

*Law of sines :*      
sin α / sin a = sin β / sin b = sin γ / sin c     
      
*Law of cosines :*       
cos a = cos b cos c + sin b sin c cos α     
cos α = -cos β cos γ + sin β sin γ cos a     

&nbsp;    

**Launch time for prograde orbit (i < 90∘) and northern hemisphere **    
***     
cos(i) = - cos(90) cos(γ) + sin(90) sin(γ) cos(φ)     

since   
cos(90°) = 0 and sin(90°) = 1      

cos(i) =  sin(γ) cos(φ)      

=>      
sin(γ) = cos(i) / cos(φ) =>  γ = arcsin( cos(i) / cos(φ)  )     
cos(δ) = cos(γ) / sin(i) =>  δ = arccos( cos(γ) / sin(i)  )     

Two solutions possible exists:    

1. Ascending node opportunity:    
β = δ    
LST = Ω + δ     

2. Descending node opportunity:   
β = 180∘ - γ   
LST = Ω + 180∘ - δ    

    
&nbsp;    
LST in degrees can be converted in terms of time using,    
LST time (degrees) = LST time (hours) * 15°/hr  
&nbsp;    


### Test Case    
    
*To calculate launch time for a given RAAN, inclination form Sriharikota   
and     
To calculate RAAN for a given launch time, azimuth and inclination form Sriharikota*          

PSLV-C22/IRNSS-1A was launched on 1831(UTC), July 01, 2013   

Paper: MISSION DESIGN AND ANALYSIS FOR IRNSS-1A   
[ https://www.researchgate.net/publication/277475032_MISSION_DESIGN_AND_ANALYSIS_FOR_IRNSS-1A ]    
&nbsp;       

### Results    
launch time for IRNSS-1A    
RAAN = 143,  inclination  = 17.877    
-    

ascending node for launch azimuth: 49.0931°    
launch time UTC : [2013-07-01 12:46:16]  IST : [2013-07-01 18:16:16]    

descending node for launch azimuth: 101.5964°     
launch time UTC : [2013-07-01 18:12:38]  IST : [2013-07-01 23:42:38]     
-    


Reverse calculation (Find RAAN using azimuth, launch_datetime)    
inclination  = 17.877    
Azimuth = 101.5964,  Launch Datetime  = 2013-07-01 18:31:25+00:00     
-      
RAAN        = 147.7080°     
-      
&nbsp;   
## References   

1. Time, Calendars and Launch Windows - Introduction to Spacecraft Dynamics    
[https://www.angadhn.com/SpacecraftDynamics/orbital-mechanics/Lecture10/Lecture10.html ]       
2. Chapter 5 – Launch Windows and Time   
[ https://colorado.pressbooks.pub/introorbitalmechanics/chapter/launch-windows-and-time/ ]   
3. Astronautics-The Physics of Space Flight. Walter, Ulrich    
[ Chapter 8.6.1 Launch Phase ]      
4. MISSION DESIGN AND ANALYSIS FOR IRNSS-1A   
[ https://www.researchgate.net/publication/277475032_MISSION_DESIGN_AND_ANALYSIS_FOR_IRNSS-1A ]

## Setup
Script is written with python (Version: 3.6) on linux. Additional modules required :   

* numpy  (tested with Version: 1.21.5 )
* pytz   (tested with Version:  2022.1 )
* 

## How to run   
* Verify and install required modules 
* run `python3 launch_time.py`. 


## Updates   
*   
*    

## To-do list
* Retrograde Orbit (i ≥ 90∘) and northern hemisphere   
* Southern hemisphere

