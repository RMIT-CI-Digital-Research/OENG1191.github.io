import ifcopenshell
import ifcopenshell.geom
import pyvista as pv
import numpy as np

# 打开 IFC 文件
ifc_file = ifcopenshell.open("test2.ifc")

# 创建几何生成的 settings
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

# 创建一个 PyVista Plotter
plotter = pv.Plotter()

for space in ifc_file.by_type("IfcSpace"):
    try:
        shape = ifcopenshell.geom.create_shape(settings, space)
        verts = shape.geometry.verts
        faces = shape.geometry.faces
        
        # 转换为 numpy 并 reshpae
        verts_np = np.array(verts).reshape((-1, 3))
        faces_np = np.array(faces).reshape((-1, 3))

        # PyVista 需要将 faces 转换为 vtk 需要的形式
        # faces 需要是 [Nverts, i0, i1, i2, ..., Nverts, i0, i1, i2, ...]
        # 这里的 Nverts 为单个多边形的顶点数（对三角形来说就是3）
        poly_faces = []
        for tri in faces_np:
            poly_faces.append(3)
            poly_faces.extend(tri)
        poly_faces = np.array(poly_faces)
        
        # 创建一个 PyVista mesh
        mesh = pv.PolyData(verts_np, poly_faces)
        
        # 如果想把它放到一个大的集合里，最终一次性展示：
        plotter.add_mesh(mesh, color="lightblue", show_edges=True)
    except:
        pass

# 最后统一显示
plotter.show()
