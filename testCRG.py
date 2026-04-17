import os
import random
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy import ScenarioObject

bng_home = r'C:\Program Files\BeamNG\BeamNG.tech.v0.38.3.0'
bng = BeamNGpy('localhost', 64256, home=bng_home)
bng.open()

scenario_name = f'fizika_teszt_{random.randint(1, 99999)}'
scenario = Scenario('smallgrid', scenario_name)

vehicle = Vehicle('ego_vehicle', model='etk800', license='PROJEKT2')

crg_path = os.path.join(os.path.dirname(__file__), 'ut_katyuval_01.crg').replace('\\', '/')
katyus_ut = ScenarioObject(
        oid='generalt_ut',       
        name='generalt_ut',      
        otype='OpenCRG',             
        pos=(0, 0, 0.05),        
        rot_quat=(0.0, 0.0, 0.0, 1.0), 
        scale=(1.0, 1.0, 1.0),
        crgFile= crg_path,       
        material='Asphalt'      
    )
    
scenario.add_object(katyus_ut)

scenario.add_vehicle(vehicle, pos=(0, 0, 1.0), rot_quat=(0, 0, 0, 1))

print("Szimuláció generálása...")
scenario.make(bng)

print("Pálya betöltése...")
bng.scenario.load(scenario)

print("Start!")
bng.scenario.start()

input("Nyomj Entert a szimuláció bezárásához...")
bng.close()


