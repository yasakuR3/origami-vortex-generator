import numpy as np
import pandas as pd 
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from stl import mesh
import trimesh

# 日本語フォントの設定をする。
plt.rcParams['font.family'] = 'MS Gothic'

def get_input():
    while True:
        try:
            # 1ユニットの折り紙構造体を一つに決定する5変数を入力する。
            a = float(input("幅l[mm]：　")) 
            c = float(input("傾斜θ[°]：　"))
            d = float(input("区間a[mm]：　"))
            e = float(input("区間b[mm]：　"))
            b = float(input("なす角φ[°]：　"))

            # 折り紙構造体のユニット数を入力する。
            f = int(input("ユニット数[個]：　"))

            # エラー処理 折り紙構造体の必要十分条件を満たす必要がある。0以上である必要がある。
            if (d - a / math.cos(math.radians(c))) < 0:
                print(f"折り紙構造体の必要十分条件を満たしてください。：{d - a / math.cos(math.radians(c))}です。")
                continue

            # エラー処理 aの値は、0より大きく入力する必要がある。
            if a <= 0:
                print("幅l[mm]の値は0より大きく入力してください。")
                continue
            
            # エラー処理 bの値は、0以上180以下で入力する必要がある。
            if b > 180 or b < 0:
                print("なす角φ[°]の値は0以上180以下で入力してください。")
                continue

            # エラー処理 cの値は、0より大きく90未満である必要がある。
            if c >= 90 or c <= 0:
                print("傾斜θ[°]の値は0より大きく90未満で入力してください。")
                continue

            # エラー処理 dの値は、0より大きく入力する必要がある。
            if d <= 0:
                print("区間a[mm]の値は0より大きく入力してください。")
                continue

            # エラー処理 eの値は、0より大きく入力する必要がある。
            if e <= 0:
                print("区間b[mm]の値は0より大きく入力してください。")
                continue

            # エラー処理 fの値は、正の整数で入力する必要がある。
            if f <= 0:
                print("ユニット数[個]の値は正の整数で入力してください。")
                continue

            return a, b, c, d, e, f

        except ValueError:
            print("無効な入力です。もう一度入力してください。")

# 値を入力する。
a, b, c, d, e, f = get_input()

# 中間変数の定義する。
def calculate_f1(a, b, c, d, e):# θ_J[°]の関数
    return math.degrees(math.atan((math.tan(math.radians(c))) * (math.cos(math.radians(b / 2)))))

def calculate_f2(a, b, c, d, e):# 線分D'X[mm]の関数
    return (d - a / math.tan(math.radians(c))) + (a * (math.cos(math.radians(b / 2))) / math.tan(math.radians(2 * calculate_f1(a, b, c, d, e))))

def calculate_f3(a, b, c, d, e):# 線分XI'[mm]の関数
    return e + (a * (math.cos(math.radians(b / 2))) / math.tan(math.radians(2 * calculate_f1(a, b, c, d, e))))

def calculate_f4(a, b, c, d, e):# 線分DI'[mm]の関数
    return math.sqrt(calculate_f2(a, b, c, d, e) ** 2 + calculate_f3(a, b, c, d, e) ** 2 - 2 * calculate_f2(a, b, c, d, e) * calculate_f3(a, b, c, d, e) * math.cos(math.radians(180 - 2 * calculate_f1(a, b, c, d, e))))

def calculate_f5(a, b, c, d, e):# θ_D[°]の関数
    return math.degrees(math.asin((calculate_f3(a, b, c, d, e) / calculate_f4(a, b, c, d, e)) * math.sin(math.radians(180 - 2 * calculate_f1(a, b, c, d, e)))))

def calculate_f6(a, b, c, d, e):# θ_L[°]の関数
    return 2 * calculate_f1(a, b, c, d, e) - calculate_f5(a, b, c, d, e)

def calculate_f7(a, b, c, d, e):# 幅l'[mm]の関数
    return a * math.cos(math.radians(b / 2))

def calculate_f8(a, b, c, d, e):# 間隔AE[mm]の関数
    return 2 * a * math.sin(math.radians(b / 2))

# 特徴点を格納する点を定義する。
origamis = np.zeros((f + 2, 20, 5))

# 点A
origamis[0][1][0] = - calculate_f7(a, b, c, d, e) * math.cos(math.radians(90 - calculate_f5(a, b, c, d, e)))
origamis[0][1][1] = - calculate_f8(a, b, c, d, e) / 2
origamis[0][1][2] = calculate_f7(a, b, c, d, e) * math.sin(math.radians(90 - calculate_f5(a, b, c, d, e)))

# 点B
origamis[0][2][0] = origamis[0][1][0] + (d - a / math.tan(math.radians(c))) * math.cos(math.radians(calculate_f5(a, b, c, d, e)))
origamis[0][2][1] = origamis[0][1][1]
origamis[0][2][2] = origamis[0][1][2] + (d - a / math.tan(math.radians(c))) * math.sin(math.radians(calculate_f5(a, b, c, d, e)))
    
# 点C
origamis[0][3][0] = (d - a / math.tan(math.radians(c))) * math.cos(math.radians(calculate_f5(a, b, c, d, e)))
origamis[0][3][1] = 0
origamis[0][3][2] = (d - a / math.tan(math.radians(c))) * math.sin(math.radians(calculate_f5(a, b, c, d, e)))

# 点D
origamis[0][4][0] = 0
origamis[0][4][1] = 0
origamis[0][4][2] = 0

# 点E
origamis[0][5][0] = origamis[0][1][0]
origamis[0][5][1] = - origamis[0][1][1]
origamis[0][5][2] = origamis[0][1][2]

# 点F
origamis[0][6][0] = origamis[0][2][0]
origamis[0][6][1] = - origamis[0][2][1]
origamis[0][6][2] = origamis[0][2][2]

# 点G
origamis[0][7][0] = calculate_f4(a, b, c, d, e) - e * math.cos(math.radians(calculate_f6(a, b, c, d, e)))
origamis[0][7][1] = origamis[0][6][1]
origamis[0][7][2] = e * math.sin(math.radians(calculate_f6(a, b, c, d, e)))
    
# 点H
origamis[0][8][0] = calculate_f4(a, b, c, d, e)
origamis[0][8][1] = origamis[0][7][1]
origamis[0][8][2] = 0
    
# 点I
origamis[0][9][0] = calculate_f4(a, b, c, d, e) + calculate_f7(a, b, c, d, e) * math.cos(math.radians(90 - calculate_f6(a, b, c, d, e)))
origamis[0][9][1] = 0
origamis[0][9][2] = calculate_f7(a, b, c, d, e) * math.sin(math.radians(90 - calculate_f6(a, b, c, d, e)))

# 点J
origamis[0][10][0] = origamis[0][9][0] - e * math.cos(math.radians(calculate_f6(a ,b, c, d, e)))
origamis[0][10][1] = 0
origamis[0][10][2] = origamis[0][9][2] + e * math.sin(math.radians(calculate_f6(a, b, c, d, e)))

# 点K
origamis[0][11][0] = calculate_f4(a, b, c, d, e) - e * math.cos(math.radians(calculate_f6(a, b, c, d, e)))
origamis[0][11][1] = - origamis[0][8][1]
origamis[0][11][2] = e * math.sin(math.radians(calculate_f6(a, b, c, d, e)))

# 点L
origamis[0][12][0] = calculate_f4(a, b, c, d, e)
origamis[0][12][1] = origamis[0][11][1]
origamis[0][12][2] = 0

# 点M(前)
origamis[0][13][0] = (origamis[0][1][0] - (origamis[0][1][2] / (origamis[0][2][2] - origamis[0][1][2])) * (origamis[0][2][0] - origamis[0][1][0]))
origamis[0][13][1] = origamis[0][12][1]
origamis[0][13][2] = 0

# 点N(後)
origamis[0][14][0] = origamis[0][13][0]
origamis[0][14][1] = - origamis[0][13][1]
origamis[0][14][2] = 0

# 点O(中央)
origamis[0][15][0] = origamis[0][9][0] - (origamis[0][9][2] / (origamis[0][10][2] - origamis[0][9][2])) * (origamis[0][10][0] - origamis[0][9][0])
origamis[0][15][1] = 0
origamis[0][15][2] = 0

# 点P(前)
origamis[0][16][0] = origamis[0][10][0] - (origamis[0][10][2] / (origamis[0][11][2] - origamis[0][10][2])) * (origamis[0][11][0] - origamis[0][10][0])
origamis[0][16][1] = origamis[0][10][1] - (origamis[0][10][2] / (origamis[0][11][2] - origamis[0][10][2])) * (origamis[0][11][1] - origamis[0][10][1])
origamis[0][16][2] = 0
    
# 点Q(後)
origamis[0][17][0] = origamis[0][10][0] - (origamis[0][10][2] / (origamis[0][11][2] - origamis[0][10][2])) * (origamis[0][11][0] - origamis[0][10][0])
origamis[0][17][1] = -(origamis[0][10][1] - (origamis[0][10][2] / (origamis[0][11][2] - origamis[0][10][2])) * (origamis[0][11][1] - origamis[0][10][1]))
origamis[0][17][2] = 0

# y軸の正の方向に点を新たに作る。
for i in range(1, f):
    for j in range(1, 18):
        origamis[i][j][0] = origamis[i - 1][j][0]
        origamis[i][j][1] = origamis[i - 1][j][1] + calculate_f8(a, b, c, d, e)
        origamis[i][j][2] = origamis[i - 1][j][2]

# 必要ない点などを削除する。
for i in range(0, f):
    for j in range(1, 18):
        for k in range(0, f - 1):
            if (i == k and j == 17) or (i == k + 1 and j == 13) or (i == k + 1 and j == 16):
               origamis[i][j][0] = 0
               origamis[i][j][1] = 0
               origamis[i][j][2] = 0

for i in range(0, f):
    for j in range(1, 18):
        if (j == 1) or (j == 3) or (j == 5) or (j == 7) or (j == 9) or (j == 11) or (i == 0 and j == 12) or (f == 1 and i == 0 and j == 8) or (f != 1 and i == f - 1 and j == 8):
            origamis[i][j][0] = 0
            origamis[i][j][1] = 0
            origamis[i][j][2] = 0

# エクセルに書き込むデータフレームを作成する。
df_list = []
for i in range(0, f):
    for j in range(1, 18):
        df_list.append([origamis[i][j][0], origamis[i][j][1], origamis[i][j][2], j + 17 * i])

# 配列に格納したエクセルに書き込む。
df = pd.DataFrame(df_list, columns = ['x', 'y', 'z', 'number'])

file_name =  f"origami-vg_a{a:.1f}_b{b:.1f}_c{c:.1f}_d{d:.1f}_e{e:.2f}_f{f:.1f}.xlsx"

with pd.ExcelWriter(file_name) as writer:
    # 最初の行に 'mm' を書き込む。
    pd.DataFrame([['mm', 'unit', f, '']]).to_excel(writer, header = False, index = False, startrow = 0)
    # 次の行に 'x', 'y', 'z' を書き込む。
    pd.DataFrame([['x', 'y', 'z', 'number']]).to_excel(writer, header = False, index = False, startrow = 1)
    # 3行目以降に座標データを書き込む。
    df.to_excel(writer, header = False, index = False, startrow = 2)

with pd.ExcelWriter("origami-vg.xlsx") as writer:
    # 最初の行に 'mm' を書き込む。
    pd.DataFrame([['mm', 'unit', f, '']]).to_excel(writer, header = False, index = False, startrow = 0)
    # 次の行に 'x', 'y', 'z' を書き込む。
    pd.DataFrame([['x', 'y', 'z', 'number']]).to_excel(writer, header = False, index = False, startrow = 1)
    # 3行目以降に座標データを書き込む。
    df.to_excel(writer, header = False, index = False, startrow = 2)

print("折り紙構造体のxyz座標の値をorigami-vg%.1f_%.1f_%.1f_%.1f_%.1f_%.1f.xlsxに保存しました。" % (a, b, c, d, e, f))

# 面を定義する。
flag1 = flag2 = flag3 = flag4 = flag5 = flag6 = flag7 = 0

faces = []
for j in range(0, f):
    for i in range(1, 12):
        if i == 1 and flag1 == 0:# 面1 この面はユニット数に関係なしに常に存在する。
            faces.append([2, 13, 16])
            flag1 = 1# 一回のみ実行する。
    
        elif i == 2 and flag2 == 0:# 面2 この面はユニット数に関係なしに常に存在する。
            faces.append([2, 10, 16]), faces.append([10, 15, 16])
            flag2 = 1# 一回のみ実行する。

        elif i == 3 and flag3 == 0:# 面3 この面と面1は対応している。この面はユニット数に関係なしに常に存在する。
            faces.append([6 + 17 * (f - 1), 14 + 17 * (f - 1), 17 + 17 * (f - 1)])
            flag3 = 1# 一回のみ実行する。

        elif i == 4 and flag4 == 0:# 面4 この面と面2は対応している。この面はユニット数に関係なしに常に存在する。
            faces.append([6 + 17 * (f - 1), 10 + 17 * (f - 1), 17 + 17 * (f - 1)]), 
            faces.append([10 + 17 * (f - 1), 15 + 17 * (f - 1) , 17 + 17 * (f - 1)])
            flag4 = 1# 一回のみ実行する。

        elif i == 5 and flag5 == 0:# 面5 この面はユニット数に関係なしに常に存在する。
            faces.append([4, 13, 16]), faces.append([4, 15, 16])
            flag5 = 1# 一回のみ実行する。
        
        elif i == 6 and flag6 == 0:# 面6 この面は面5と同じ面上に存在する。この面はユニット数に関係なしに常に存在する。
           faces.append([4 + 17 * (f - 1), 14 + 17 * (f - 1), 17 + 17 * (f - 1)]), 
           faces.append([4 + 17 * (f - 1), 15 + 17 * (f - 1), 17 + 17 * (f - 1)])
           flag6 = 1# 一回のみ実行する。

        elif i == 7:# 面7 この面は面5と同じ面上に存在する。
           if not j == 0:
            faces.append([4 + 17 * (j - 1), 14 + 17 * (j - 1), 21 + 17 * (j - 1)]),
            faces.append([4 + 17 * (j - 1), 8 + 17 * (j - 1), 21 + 17 * (j - 1)]),
            faces.append([4 + 17 * (j - 1), 8 + 17 * (j - 1), 15 + 17 * (j - 1)]),
            faces.append([8 + 17 * (j - 1), 21 + 17 * (j - 1), 32 + 17 * (j - 1)])
        
        elif i == 8:# 面8 
            if j == 0:
             faces.append([2, 4, 13]), 
             faces.append([2, 4, 10])

            else: 
             faces.append([2 + 17 * j, 4 + 17 * j, 14 + 17 * (j - 1)]), 
             faces.append([2 + 17 * j, 4 + 17 * j, 10 + 17 * j])

        elif i == 9:# 面9
            faces.append([4 + 17 * j, 6 + 17 * j, 14 + 17 * j]), 
            faces.append([4 + 17 * j, 6 + 17 * j, 10 + 17 * j])

        elif i == 10:# 面10
            if not j == 0:
             faces.append([6 + 17 * (j - 1), 8 + 17 * (j - 1), 10 + 17 * (j - 1)]), 
             faces.append([8 + 17 * (j - 1), 10 + 17 * (j - 1), 15 + 17 * (j - 1)])

        elif i == 11:# 面11
            if not j == 0:
             faces.append([2 + 17 * j, 10 + 17 * j, 12 + 17 *j]), 
             faces.append([10 + 17 * j, 12 + 17 * j, 15 + 17 * j])

# 3Dプロットを作成する。
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

# 各ユニットのポイントをプロットする。
for face in faces:
    x = [origamis[math.ceil(idx // 17.5)][idx - 17 * math.ceil(idx // 17.5)][0] for idx in face]
    y = [origamis[math.ceil(idx // 17.5)][idx - 17 * math.ceil(idx // 17.5)][1] for idx in face]
    z = [origamis[math.ceil(idx // 17.5)][idx - 17 * math.ceil(idx // 17.5)][2] for idx in face]
    ax.plot_trisurf(x, y, z, color = 'b', alpha = 0.5, edgecolor = 'gray')

# グラフの端に情報を表示する。
info_text = f"幅 l: {a} mm\nなす角 φ: {b} °\n傾斜 θ: {c} °\n区間 a: {d} mm\n区間 b: {e} mm\nユニット数: {f} 個\n最大高さ: {origamis[0][10][2]:.1f} mm\n最大縦幅: {(origamis[f - 1][17][1] - origamis[0][16][1]):.1f} mm\n最大横幅: {(origamis[0][15][0] - origamis[0][13][0]):.1f} mm"
ax.text2D(0.05, 0.95, info_text, transform = ax.transAxes, fontsize = 12, verticalalignment = 'top', color = 'red')

ax.set_xlabel('X軸')
ax.set_ylabel('Y軸')
ax.set_zlabel('Z軸')

# 各軸の範囲を取得し、同じスケールにする。
x_limits = ax.get_xlim3d()
y_limits = ax.get_ylim3d()
z_limits = ax.get_zlim3d()

x_range = abs(x_limits[1] - x_limits[0])
y_range = abs(y_limits[1] - y_limits[0])
z_range = abs(z_limits[1] - z_limits[0])

max_range = max(x_range, y_range, z_range)

x_middle = np.mean(x_limits)
y_middle = np.mean(y_limits)
z_middle = np.mean(z_limits)

ax.set_xlim3d([x_middle - max_range / 2, x_middle + max_range / 2])
ax.set_ylim3d([y_middle - max_range / 2, y_middle + max_range / 2])
ax.set_zlim3d([z_middle - max_range / 2, z_middle + max_range / 2])

# グラフを画像として保存する。
plt.savefig("origami-vg.png", dpi = 300, bbox_inches = 'tight')

# 座標を定義する。
vertices = []

vertices.append([0, 0, 0])

for i in range(0, f):
    for j in range(1, 18):
        x = origamis[i][j][0] 
        y = origamis[i][j][1] 
        z = origamis[i][j][2] 

        vertices.append([x, y, z])

# numpy配列に変換する。
vertices = np.array(vertices)

# 面を定義する。
faces = np.array(faces)

# trimeshオブジェクトを作成する。
mesh_obj = trimesh.Trimesh(vertices = vertices, faces = faces)

# メッシュの内部を埋める処理する。
# メッシュが閉じているか確認し、閉じていない場合は修正を試みる。
if not mesh_obj.is_watertight:
    mesh_obj = trimesh.repair.fill_holes(mesh_obj)

# Convex Hullでなく元の形をできるだけ維持するため、ソリッド化を行う。
# is_volumeメッシュにすることで、形状を維持しつつボリュームメッシュにする。
solid_mesh = mesh_obj.copy()

# 最後にメッシュをSTLファイルにエクスポートする。
solid_mesh.export('origami-vg.stl')

plt.show()
