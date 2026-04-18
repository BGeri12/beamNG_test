import numpy as np
import trimesh
import os
import re

hossz = 10.0      
szelesseg = 7.0   

x_bal = np.arange(-szelesseg/2, 0.5, 0.5)
x_katyu = np.arange(0.5, 2.5, 0.025)
x_jobb = np.arange(2.5, (szelesseg/2) + 0.1, 0.5)
x = np.unique(np.concatenate((x_bal, x_katyu, x_jobb)))

y_eleje = np.arange(0, 4.0, 0.5)
y_katyu = np.arange(4.0, 6.0, 0.025)
y_vege = np.arange(6.0, hossz + 0.1, 0.5)
y = np.unique(np.concatenate((y_eleje, y_katyu, y_vege)))

X, Y = np.meshgrid(x, y)

Z_alap = -np.abs(X) * 0.025

katyu_x = 1.5
katyu_y = 5.0
katyu_melyseg = 0.10  
katyu_sugar = 0.4     

R = np.sqrt((X - katyu_x)**2 + (Y - katyu_y)**2)
Z_godor = -katyu_melyseg * np.exp(-(R**2) / (katyu_sugar**2))

zaj_frekvencia = 40.0 
zaj_amplitudo = 0.02  
zaj_maszk = np.exp(-(R**2) / ((katyu_sugar * 1.3)**2))
Z_zaj = zaj_amplitudo * np.sin(zaj_frekvencia * X) * np.cos(zaj_frekvencia * Y) * zaj_maszk

Z_total = Z_alap + Z_godor + Z_zaj

u_meret = Z_total.shape[0]  
v_meret = Z_total.shape[1]  

vertices = []
faces = []
uvs = [] 

print("Csúcspontok és poligonok összeállítása...")

for i in range(u_meret):
    for j in range(v_meret):
        vertices.append([X[i,j], Y[i,j], Z_total[i,j]])
        uvs.append([X[i,j] / 5.0, Y[i,j] / 5.0])

# Háromszögelés (A Collada formátum a háromszögeket szereti)
for i in range(u_meret - 1):
    for j in range(v_meret - 1):
        v1 = i * v_meret + j
        v2 = i * v_meret + (j + 1)
        v3 = (i + 1) * v_meret + j
        v4 = (i + 1) * v_meret + (j + 1)
        
        # Első és második háromszög a négyzeten belül
        faces.append([v1, v2, v3])
        faces.append([v2, v4, v3])

# 4. EXPORTÁLÁS COLLADA (.dae) FÁJLBA
aktualis_mappa = os.path.dirname(os.path.abspath(__file__))
fajlnev = os.path.join(aktualis_mappa, 'ut_katyuval.dae').replace('\\', '/')

mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)
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

print(f"Az '{fajlnev}' sikeresen elmentve!")