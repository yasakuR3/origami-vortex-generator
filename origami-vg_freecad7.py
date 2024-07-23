import pandas as pd
import FreeCAD as App
import FreeCADGui as Gui
import Part
import openpyxl 

#このプログラムは正しいプログラム

# エクセルファイルのパス
file_path = 'C:\\Users\\fml_user\\Desktop\\origami-vortex generator\\origami-vg設計\\origami-vg.xlsx'

# STLファイルの出力パス
output_file_path = 'C:\\Users\\fml_user\\Desktop\\origami-vortex generator\\origami-vg設計\\origami-vg11.stl'

# openpyxlを使用してエクセルファイルを読み込む
wb = openpyxl.load_workbook(file_path)
sheet = wb['Sheet1']

# 特定のセルの値を読み取る
specific_value = sheet['C1'].value
print(f"Specific value in A1: {specific_value}")

# エクセルシートのデータを読み込む
df = pd.read_excel(file_path, sheet_name='Sheet1', header=1)

# 座標点を辞書形式に変換
points = {f'P{int(row["number"]):02d}': [row['x'], row['y'], row['z']] for index, row in df.iterrows()}

# FreeCADドキュメントを作成
doc = App.newDocument("ShellViewer")

# シェルとソリッドの作成関数
def MakeShellAndSolid(points, faces):
    def EntryVertex(name, pos):
        from FreeCAD import Base
        v = App.ActiveDocument.addObject("Part::Vertex", name)
        v.X, v.Y, v.Z = pos
        v.Placement = Base.Placement(Base.Vector(*pos), Base.Rotation(0, 0, 0, 1))
        App.ActiveDocument.recompute()
        return v.Name

    def EntryFace(name, vnames):
        pol = [getattr(App.ActiveDocument, vn).Shape.Vertex1.Point for vn in vnames]
        face = Part.Face(Part.makePolygon(pol, True))
        if face.isNull():
            raise RuntimeError('Failed to create face')
        f = App.ActiveDocument.addObject('Part::Feature', name)
        f.Shape = face
        App.ActiveDocument.recompute()
        return f.Name

    def EntryShell(face_names):
        shells = []
        for fn in face_names:
            faces = getattr(App.ActiveDocument, fn).Shape.Faces
            shells.extend(faces)
        shell = Part.Shell(shells)
        if shell.isNull():
            raise RuntimeError('Failed to create shell')
        return shell

    # 頂点を作成
    vertex_names = [EntryVertex(name, pos) for name, pos in points.items()]
    # 面を作成
    face_names = [EntryFace(name, vnames) for name, vnames in faces.items()]
    # シェルを作成
    shell = EntryShell(face_names)

    # シェルからソリッドを作成
    solid = Part.Solid(shell)
    obj = App.ActiveDocument.addObject('Part::Feature', 'Solid')
    obj.Shape = solid
    App.ActiveDocument.recompute()

    # ソリッドをSTLファイルとしてエクスポート
    Part.export([obj], output_file_path)

flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag5 = 0
flag6 = 0
flag7 = 0
flag8 = 0
k = 0

faces = {}

for j in range(0, specific_value):
 for i in range(1, 10):
    if i == 1:
        if j == 0 and flag6 == 0:
            k = k + 1
            flag6 = 1

            faces[f"F{str(k).zfill(2)}"] = [f"P{str(1).zfill(2)}", f"P{str(2).zfill(2)}", f"P{str(10).zfill(2)}", f"P{str(4).zfill(2)}", f"P{str(13).zfill(2)}"]

        else:
            k = k + 1

            faces[f"F{str(k).zfill(2)}"] = [f"P{str(1+17*j).zfill(2)}", f"P{str(2+17*j).zfill(2)}", f"P{str(10+17*j).zfill(2)}", f"P{str(4+17*j).zfill(2)}", f"P{str(14+17*(j-1)).zfill(2)}"]

    elif i == 2:
        k = k + 1

        faces[f"F{str(k).zfill(2)}"] = [f"P{str(5+17*j).zfill(2)}", f"P{str(6+17*j).zfill(2)}", f"P{str(10+17*j).zfill(2)}", f"P{str(4+17*j).zfill(2)}", f"P{str(14+17*j).zfill(2)}"]

    elif i == 3:
        k = k + 1 

        faces[f"F{str(k).zfill(2)}"] = [f"P{str(2+17*j).zfill(2)}", f"P{str(10+17*j).zfill(2)}", f"P{str(15+17*j).zfill(2)}", f"P{str(12+17*j).zfill(2)}"]

    elif i == 4:
        k = k + 1

        faces[f"F{str(k).zfill(2)}"] = [f"P{str(6+17*j).zfill(2)}", f"P{str(10+17*j).zfill(2)}", f"P{str(15+17*j).zfill(2)}", f"P{str(8+17*j).zfill(2)}"]

    elif i == 5 and flag7 == 0:
       k = k + 1
       flag7 = 1

       faces[f"F{str(k).zfill(2)}"] = [f"P{str(16).zfill(2)}", f"P{str(12).zfill(2)}", f"P{str(2).zfill(2)}"]

    elif i == 6 and flag8 == 0:
       k = k + 1
       flag8 = 1

       faces[f"F{str(k).zfill(2)}"] = [f"P{str(2).zfill(2)}", f"P{str(16).zfill(2)}", f"P{str(13).zfill(2)}"]

    elif i == 7:
        if specific_value == 1 and flag4 == 0:
           k = k + 1
           flag4 = 1

           faces[f"F{str(k).zfill(2)}"] = [f"P{str(17).zfill(2)}", f"P{str(8).zfill(2)}", f"P{str(6).zfill(2)}"]

        elif flag5 == 0: 
           k = k + 1
           flag5 = 1
           
           faces[f"F{str(k).zfill(2)}"] = [f"P{str(17*specific_value).zfill(2)}", f"P{str(8+17*(specific_value-1)).zfill(2)}", f"P{str(6+17*(specific_value-1)).zfill(2)}"]
           
    elif i == 8:
        if specific_value == 1 and flag2 == 0:
         k = k + 1
         flag2 = 1

         faces[f"F{str(k).zfill(2)}"] = [f"P{str(6).zfill(2)}", f"P{str(17).zfill(2)}", f"P{str(14).zfill(2)}"]

        elif flag3 == 0:
         k = k + 1
         flag3 = 1
         
         faces[f"F{str(k).zfill(2)}"] = [f"P{str(6+17*(specific_value-1)).zfill(2)}", f"P{str(17*specific_value).zfill(2)}", f"P{str(14+17*(specific_value-1)).zfill(2)}"]

    elif i == 9:
        if j == 0 and flag1 == 0:
           flag1 = 1
           k = k + 1

           faces[f"F{str(k).zfill(2)}"] = [f"P{str(4).zfill(2)}", f"P{str(13).zfill(2)}", f"P{str(16).zfill(2)}",  f"P{str(15).zfill(2)}"]

           k = k + 1

           faces[f"F{str(k).zfill(2)}"] = [f"P{str(4+17*(specific_value-1)).zfill(2)}", f"P{str(14+17*(specific_value-1)).zfill(2)}", f"P{str(17+17*(specific_value-1)).zfill(2)}", f"P{str(15+17*(specific_value-1)).zfill(2)}"]

        else:
           k = k + 1

           faces[f"F{str(k).zfill(2)}"] = [f"P{str(4+17*(j-1)).zfill(2)}", f"P{str(14+17*(j-1)).zfill(2)}", f"P{str(21+17*(j-1)).zfill(2)}",f"P{str(32+17*(j-1)).zfill(2)}", f"P{str(8+17*(j-1)).zfill(2)}", f"P{str(15+17*(j-1)).zfill(2)}"]

print(faces)

# シェルとソリッドの作成
MakeShellAndSolid(points, faces)

# ビューワーを表示
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewAxonometric()
