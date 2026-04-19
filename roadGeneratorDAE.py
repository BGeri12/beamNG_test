import numpy as np
import trimesh
import os
import re

hossz = 10.0      
szelesseg = 7.0   
katyu_x = 1.5
katyu_y = 5.0
katyu_sugar = 0.4
katyu_melyseg = 0.12  

x = np.unique(np.concatenate((np.arange(-szelesseg/2, 0.5, 0.5), np.arange(0.5, 2.5, 0.025), np.arange(2.5, (szelesseg/2)+0.1, 0.5))))
y = np.unique(np.concatenate((np.arange(0, 4.0, 0.5), np.arange(4.0, 6.0, 0.025), np.arange(6.0, hossz+0.1, 0.5))))
X, Y = np.meshgrid(x, y)

Z_alap = -np.abs(X) * 0.025
R = np.sqrt((X - katyu_x)**2 + (Y - katyu_y)**2)

Z_godor = -katyu_melyseg / (1.0 + np.exp(10.0 * (R - katyu_sugar)))
Z_total = Z_alap + Z_godor

u_meret = len(x)
v_meret = len(y)

vertices = []
faces = []
uvs = []
colors = []

print("Geometria és Vertex Color (Sötétítés) kiszámítása...")

for i in range(v_meret):     
    for j in range(u_meret): 
        curr_x = X[i,j]
        curr_y = Y[i,j]
        curr_z = Z_total[i,j]
        
        vertices.append([curr_x, curr_y, curr_z])
        uvs.append([curr_x / 5.0, curr_y / 5.0])
        
        dist = np.sqrt((curr_x - katyu_x)**2 + (curr_y - katyu_y)**2)
        if dist < katyu_sugar:
            colors.append([40, 40, 40, 255])
        else:
            colors.append([255, 255, 255, 255])

# Háromszögelés a hálóhoz
for i in range(v_meret - 1):
    for j in range(u_meret - 1):
        v1 = i * u_meret + j
        v2 = i * u_meret + (j + 1)
        v3 = (i + 1) * u_meret + j
        v4 = (i + 1) * u_meret + (j + 1)
        faces.append([v1, v2, v3])
        faces.append([v2, v4, v3])

# ==========================================
# 4. EXPORTÁLÁS 
# ==========================================
aktualis_mappa = os.path.dirname(os.path.abspath(__file__))
fajlnev = os.path.join(aktualis_mappa, 'ut_katyuval.dae').replace('\\', '/')

mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)
mesh.visual.vertex_colors = colors  
mesh.fix_normals() 
_ = mesh.vertex_normals 

mesh.export(fajlnev)

with open(fajlnev, 'r', encoding='utf-8') as f:
    dae_data = f.read()

dae_data = dae_data.replace('<up_axis>Y_UP</up_axis>', '<up_axis>Z_UP</up_axis>')
dae_data = dae_data.replace('"defaultmaterial"', '"asphalt_mesh_road"')
dae_data = dae_data.replace('#defaultmaterial', '#asphalt_mesh_road')

with open(fajlnev, 'w', encoding='utf-8') as f:
    f.write(dae_data)

print(f"KÉSZ! A .dae fájl mérete optimális, a kátyú sötétítve!")

# ==========================================
# 5. HAJLÉKONY MESH DECAL GENERÁLÁSA A KÁTYÚHOZ
# ==========================================
print("Hajlékony matrica 3D háló generálása...")

matrica_meret = katyu_sugar * 2.5 
felbontas = 20

vertices_matrica = []
faces_matrica = []
uvs_matrica = []

for i in range(felbontas + 1):
    for j in range(felbontas + 1):
        x_lokalis = (i / felbontas - 0.5) * matrica_meret
        y_lokalis = (j / felbontas - 0.5) * matrica_meret
        
        tavolsag_kozep = np.sqrt(x_lokalis**2 + y_lokalis**2)
        
        z_alap = -np.abs(katyu_x + x_lokalis) * 0.025 
        
        if tavolsag_kozep < katyu_sugar:
            sullyedes = (1.0 - (tavolsag_kozep / katyu_sugar)**2) * katyu_melyseg
            z_vegleges = z_alap - sullyedes + 0.01 
        else:
            z_vegleges = z_alap + 0.01

        vertices_matrica.append([x_lokalis, y_lokalis, z_vegleges])
        uvs_matrica.append([i / felbontas, j / felbontas])

for i in range(felbontas):
    for j in range(felbontas):
        idx = i * (felbontas + 1) + j
        p1 = idx
        p2 = idx + 1
        p3 = idx + (felbontas + 1)
        p4 = idx + (felbontas + 1) + 1
        
        faces_matrica.append([p1, p3, p2])
        faces_matrica.append([p2, p3, p4])

mesh_matrica = trimesh.Trimesh(
    vertices=vertices_matrica, 
    faces=faces_matrica, 
    process=False
)
mesh_matrica.visual = trimesh.visual.TextureVisuals(uv=uvs_matrica)
mesh_matrica.fix_normals()

matrica_fajl = os.path.join(aktualis_mappa, 'matrica.dae').replace('\\', '/')
mesh_matrica.export(matrica_fajl)

with open(matrica_fajl, 'r', encoding='utf-8') as f:
    dae_matrica = f.read()

dae_matrica = dae_matrica.replace('<up_axis>Y_UP</up_axis>', '<up_axis>Z_UP</up_axis>')
dae_matrica = dae_matrica.replace('"defaultmaterial"', '"road_damage_01"')
dae_matrica = dae_matrica.replace('#defaultmaterial', '#road_damage_01')

with open(matrica_fajl, 'w', encoding='utf-8') as f:
    f.write(dae_matrica)

print("KÉSZ! A hajlékony matrica legenerálva.")