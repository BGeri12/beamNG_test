import os
import time
import csv
import cv2
import numpy as np
from ultralytics import YOLO
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera

bng_home = r'C:\Program Files\BeamNG\BeamNG.tech.v0.38.3.0'
beamng = BeamNGpy('localhost', 64251, home=bng_home)

save_dir = r'D:\Egyetem\6.felev\Szakdoga1\Implementacio\Saved_Detections'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

csv_path = os.path.join(save_dir, 'detections_log.csv')
if not os.path.exists(csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Kep_neve', 'Idopont', 'X', 'Y', 'Z', 'Conf'])

model = YOLO('D:/Egyetem/6.felev/Szakdoga1/Implementacio/FRDC_RDD/YOLOv10/weights/yolov10_x_best.pt')

scenario = Scenario('gridmap_v2', 'we_export')
thePlayer = Vehicle('thePlayer', 'covet')
scenario.add_vehicle(thePlayer, pos=(132, 187.2, 100.2))

img_counter = 0
last_save_time = 0

try:
    print("Csatlakozás és BeamNG indítása...")
    beamng.open()
    scenario.make(beamng)
    beamng.scenario.load(scenario)
    beamng.scenario.start()

    print("Várakozás a rendszerre (5 mp)...")
    time.sleep(5)

    camera_1 = Camera('Camera 1', beamng, vehicle=thePlayer, requested_update_time=0.05,
                  pos=(0.004691, -0.477, 1.142), 
                  dir=(0, -1, 0), 
                  up=(0, 0, 1),
                  resolution=(600, 1200), 
                  field_of_view_y=70, 
                  near_far_planes=(0.05, 100), 
                  is_visualised=True)
                      

    print("Detektálás indul! Nyomj 'q'-t a kilépéshez.")

    while True:
        try:
            sensor_data = camera_1.poll()
            
            if sensor_data is None or 'colour' not in sensor_data or sensor_data['colour'] is None:
                print("Adatfolyam várakozás...")
                time.sleep(0.5)
                continue

            img_pil = sensor_data['colour'].convert('RGB')
            frame_rgb = np.array(img_pil)
            
            results = model.predict(frame_rgb, conf=0.35, verbose=False)
            
            if len(results[0].boxes) > 0:
                current_time = time.time()
                if current_time - last_save_time > 2.0:
                    thePlayer.sensors.poll()
                    pos = thePlayer.state['pos']
                    
                    annotated_frame = results[0].plot()
                    bgr_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
                    fname = f"katyu_{img_counter}.jpg"
                    cv2.imwrite(os.path.join(save_dir, fname), bgr_frame)
                    
                    with open(csv_path, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([fname, time.ctime(current_time), pos[0], pos[1], pos[2], f"{float(results[0].boxes.conf[0]):.2f}"])
                    
                    print(f"SZAKDOGA: Kátyú mentve ({fname}) - Pozíció: {pos[0]:.1f}, {pos[1]:.1f}")
                    img_counter += 1
                    last_save_time = current_time

            display_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            cv2.imshow('Kutatasi Monitor', display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as loop_e:
            print(f"Hiba az adatfogadásban, újrapróbálkozás: {loop_e}")
            time.sleep(1)
            continue
        
except Exception as main_e:
    print(f"Váratlan hiba: {main_e}")
finally:
    cv2.destroyAllWindows()
    try:
        beamng.close()
    except:
        pass