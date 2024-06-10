from rocketpy import Environment, SolidMotor, Rocket, Flight
from rocketpy.plots.compare import CompareFlights
import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

# Initialise MRC LaunchPad
env = Environment(latitude=52.668650, longitude= -1.524493, elevation=0)

launchday = (2024, 6, 12, 12)

env.set_date(launchday)

# env.set_atmospheric_model(
#     type="Forecast", file="GFS"
# )

env.max_expected_height = 1000

# Define vehicle geometry here:

length = 0.59
diameter = 41.1 / 1000

centre_of_mass = 0.28

mass_without_motor = 0.493
Ixx = 0.25 * mass_without_motor * (diameter/2)**2 + 1/12 * mass_without_motor * length**2
Iyy = Ixx
Irr = 0.5 * mass_without_motor * (diameter/2)**2

motor_dry_mass = 0.086
motor_diameter = 29 / 1000
MIxx = 0.25 * motor_dry_mass * (motor_diameter/2)**2 + 1/12 * motor_dry_mass * length**2
MIyy = MIxx
MIrr = 0.5 * mass_without_motor * (motor_diameter/2)**2

fin_root = 80 / 1000
fin_tip = 20 / 1000
fin_half_span = 30 / 1000
fin_sweep_angle = 65.2

#  FARG Setup

farg_mass = 99 / 1000


# Motor Setup

Pro29G126 = SolidMotor(
    thrust_source="./data/Cesaroni_116G126-13A.csv",     #import
    dry_mass=motor_dry_mass,
    dry_inertia= (MIxx, MIyy, MIrr),
    nozzle_radius=29 / 2000,                #find
    grain_number=2,
    grain_density=1.129,                    #find
    grain_outer_radius=26 / 2000,           #find
    grain_initial_inner_radius=15 / 1000,   #find
    grain_initial_height=70 / 1000,        #find
    grain_separation=5 / 1000,              #find
    grains_center_of_mass_position=0.7 / 1000,     #find
    center_of_dry_mass_position=0.7 / 1000,        #find
    nozzle_position=-0.1,
    burn_time=0.93,
    throat_radius=5 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber"
)

# Vehicle Setup

stilltesting = Rocket(
    radius = diameter/2,
    mass = mass_without_motor,
    center_of_mass_without_motor = 0,
    inertia=(Ixx, Iyy, Irr),
    power_off_drag="./data/powerOffDragCurve.CSV",
    power_on_drag="./data/powerOffDragCurve.CSV",
    coordinate_system_orientation="nose_to_tail",
)

stilltesting_fargs = Rocket(
    radius = diameter/2,
    mass = mass_without_motor + farg_mass,
    center_of_mass_without_motor = 0,
    inertia=(Ixx, Iyy, Irr),
    power_off_drag="./data/powerOffDragCurve.CSV",
    power_on_drag="./data/powerOffDragCurve.CSV",
    coordinate_system_orientation="nose_to_tail",
)

stilltesting.add_motor(Pro29G126, position= -centre_of_mass + length)

stilltesting_fargs.set_rail_buttons(0.115, length-0.09, 45)

nosecone = stilltesting.add_nose(
    length = 0.125,
    kind = "parabolic",
    position = -centre_of_mass
)

fins = stilltesting.add_fins(
    n = 4,
    root_chord = fin_root,
    tip_chord = fin_tip,
    span = fin_half_span,
    sweep_angle = fin_sweep_angle,
    cant_angle = 0.1,
    position = -centre_of_mass + length
)

# tail = stilltesting.add_tail(

# )

main = stilltesting.add_parachute(
    name="main",
    cd_s=0.8 * 3.1415926 * (0.457/2)**2,
    trigger="apogee",   
)

simulation = Flight(
    rocket=stilltesting,
    name="Flight",
    environment=env,
    rail_length=2,
    inclination=85,
    heading=270,
)

stilltesting.all_info()
simulation.all_info()
# simulation.export_data(
#     "data/flight_data.csv",
# )