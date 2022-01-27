SIMULATION_TIME = 500
SIMULATION_STEP_TIME = 50  # krok czasowy 50s
# iterations = simulation_time/simultaion_step_time
CONDUCTIVITY = 25
ALPHA = 300
AMBIENT_TEMPERATURE = 1200
DENSITY = 7800
INITIAL_TEMPERATURE = 100
SPECIFIC_HEAT = 700

def printGlobalData():
    print(f"Sim_time {SIMULATION_TIME}")
    print(f"dt {SIMULATION_STEP_TIME}")
    print(f"k {CONDUCTIVITY}")
    print(f"alpha {ALPHA}")
    print(f"tempOt {AMBIENT_TEMPERATURE}")
    print(f"density {DENSITY}")
    print(f"t0 {INITIAL_TEMPERATURE}")
    print(f"specific_heat {SPECIFIC_HEAT}")
