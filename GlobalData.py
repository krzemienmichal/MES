simulation_time = 0
simultaion_step_time = 0  # krok czasowy 50s
# iterations = simulation_time/simultaion_step_time
conductivity = 0
alpha = 0
temperature = 0
density = 0
initial_temperature = 0
specific_heat = 0

def printGlobalData():
    print(f"Sim_time {simulation_time}")
    print(f"dt {simultaion_step_time}")
    print(f"k {conductivity}")
    print(f"alpha {alpha}")
    print(f"tempOt {temperature}")
    print(f"density {density}")
    print(f"t0 {initial_temperature}")
    print(f"specific_heat {specific_heat}")


    # iterations = 100
    # alpha = 300
    # conductivity = 25
    # temperature = 1200
    # specific_heat = 700
    # simultaion_step_time = 1 #krok czasowy 50s
    # initial_temperature = 100
    # density = 7800