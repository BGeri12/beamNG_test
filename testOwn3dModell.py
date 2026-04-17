import random
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy import ScenarioObject

bng_home = r'C:\Program Files\BeamNG\BeamNG.tech.v0.38.3.0'
bng = BeamNGpy('localhost', 64256, home=bng_home)
bng.open()

scenario_name = f'fizika_teszt_{random.randint(1, 99999)}'
scenario = Scenario('smallgrid', scenario_name)

vehicle = Vehicle('ego_vehicle', model='etk800', license='PROJEKT2')


for i in range(150):
    road_model = ScenarioObject(
        oid=f'custom_road_mesh{i}',
        name=f'custom_road_mesh{i}',
        otype='TSStatic',
        pos=(0.0, i*(-10), 0.2),     
        rot_quat=(0.0, 0.0, 0.0, 1.0), 
        scale=(1.0, 1.0, 1.0),
        shapeName='/levels/smallgrid/art/shapes/test/pothole2.dae', 

        collisionType='Visible Mesh',
        decalType='None'
    )
    scenario.add_object(road_model)

scenario.add_vehicle(vehicle, pos=(0, 0, 1.0), rot_quat=(0, 0, 0, 1))

print("Szimuláció generálása...")
scenario.make(bng)

print("Pálya betöltése...")
bng.scenario.load(scenario)

print("Start!")
bng.scenario.start()

input("Nyomj Entert a szimuláció bezárásához...")
bng.close()