import os
from ansys.mapdl.core import launch_mapdl
import femorph
import pyvista as pv


def build_disk(mapdl, params):
    r_bore = params['r_bore']
    z_front = params['z_front']
    bore_vert = params['bore_vert']
    bore_wide = params['bore_wide']
    web_wide = params['web_wide']
    web_up = params['web_up']
    web_up2 = params['web_up2']
    rim_start = params['rim_start']
    rim_up = params['rim_up']
    rim_wide = params['rim_wide']
    hole_r = params['hole_r']
    hole_r2 = params['hole_r2']
    
    mapdl.clear()
    mapdl.prep7()
    mapdl.k(1, 0, r_bore, z_front)
    mapdl.k(2, 0, r_bore, z_front + bore_wide)
    mapdl.k(3, 0, r_bore + bore_vert, z_front)
    mapdl.k(4, 0, r_bore + bore_vert, z_front + bore_wide)
    mapdl.k(5, 0, r_bore + bore_vert + web_up, z_front + bore_wide - (bore_wide - web_wide) * 0.5)
    mapdl.k(6, 0, r_bore + bore_vert + web_up, z_front +  (bore_wide - web_wide) * 0.5)
    mapdl.k(7, 0, r_bore + bore_vert + web_up + web_up2, z_front + bore_wide - (bore_wide - web_wide) * 0.5)
    mapdl.k(8, 0, r_bore + bore_vert + web_up + web_up2, z_front +  (bore_wide - web_wide) * 0.5)

    # Start rim
    mapdl.k(9, 0, r_bore + bore_vert + web_up + web_up2 + rim_start, z_front + bore_wide - (bore_wide - web_wide) * 0.5)
    mapdl.k(10, 0, r_bore + bore_vert + web_up + web_up2 + rim_start, z_front +  (bore_wide - web_wide) * 0.5)
    #rim axial bottom
    #temp added 0.25
    mapdl.k(11, 0, r_bore + bore_vert + web_up + web_up2 + rim_start + 0.25, z_front + bore_wide - (bore_wide - web_wide) * 0.5 + (rim_wide-web_wide) * 0.5)
    mapdl.k(12, 0, r_bore + bore_vert + web_up + web_up2 + rim_start + 0.25, z_front +  (bore_wide - web_wide) * 0.5 - (rim_wide-web_wide) * 0.5)
    # rim radial up
    mapdl.k(13, 0, r_bore + bore_vert + web_up + web_up2 + rim_start + rim_up, z_front + bore_wide - (bore_wide - web_wide) * 0.5 + (rim_wide-web_wide) * 0.5)
    mapdl.k(14, 0, r_bore + bore_vert + web_up + web_up2 + rim_start + rim_up, z_front +  (bore_wide - web_wide) * 0.5 - (rim_wide-web_wide) * 0.5)
    
    mapdl.k(1001, 0, 0, 0)
    mapdl.k(1002, 0, 0, 1)

    mapdl.l(1, 3)
    mapdl.l(2, 4)
    mapdl.l(3, 6)
    mapdl.l(4, 5)
    mapdl.l(6, 8)
    mapdl.l(5, 7)
    mapdl.l(8, 10)
    mapdl.l(7, 9)
    mapdl.l(9, 11)
    mapdl.l(10, 12)
    mapdl.l(11, 13)
    mapdl.l(12, 14)

    mapdl.lfillt(2, 4, 0.5)
    mapdl.lfillt(1, 3, 0.5)
    mapdl.lfillt(4, 6, 0.5)
    mapdl.lfillt(3, 5, 0.5)
    mapdl.lfillt(8, 9, 0.5)
    mapdl.lfillt(7, 10, 0.5)

    mapdl.l(26, 24) # line 19
    mapdl.l(12, 11)  #line20

    mapdl.askin(1, 2)
    mapdl.askin(14 ,13)
    mapdl.askin(3, 4)
    mapdl.askin(16, 15)
    mapdl.askin(5, 6)
    mapdl.askin(7, 8)
    mapdl.askin(18, 17)
    mapdl.al(9, 20, 10, 19)
    mapdl.askin(12, 11)

    mapdl.vrotat('ALL',pax1=1001, pax2=1002, arc=30)

    return mapdl
    
def add_bolthole(mapdl, params):
    hole_r = params['hole_r']
    hole_r2 = params['hole_r2']
    mapdl.cyl4(0, hole_r, hole_r2,'','','', 10)
    mapdl.csys(1)
    mapdl.vgen(2, 10, '', '' ,'' , 15)  # volume 6
    mapdl.vdele(10, kswp=1)

    mapdl.vsbv(5,11,'','DELETE','DELETE')

    return mapdl

    
def add_slot(mapdl):
    mapdl.csys(0)
    mapdl.k(201, 0.5, 10.5, 0)
    mapdl.k(202, -0.5, 10.5, 0)
    mapdl.k(203, 0.5, 9.0)
    mapdl.k(204, -0.5, 9.0, 0)
    mapdl.numstr('LINE',201)
    mapdl.l(201, 202)
    mapdl.l(203, 204)
    mapdl.numstr('AREA',201)
    mapdl.askin(201, 202)
    mapdl.numstr('VOLUME', 201)
    mapdl.vext(201,'','','','', 10)
    mapdl.csys(1)
    mapdl.vgen(2, 201, '', '' ,'' , 15)
    mapdl.vdele(201, kswp=1)
    mapdl.vsbv(9, 202,'','DELETE','DELETE')

    return mapdl

def add_dovetail(mapdl):
    mapdl.csys(0)
    mapdl.k(201, 0.5, 9.0)
    mapdl.k(202, -0.5, 9.0, 0)
    mapdl.k(203, 0.5, 9.5)
    mapdl.k(204, -0.5, 9.5, 0)
    mapdl.k(205, 0.25, 9.75)
    mapdl.k(206, -0.25, 9.75, 0)
    mapdl.k(207, 0.25, 10.5)
    mapdl.k(208, -0.25, 10.5, 0)
    mapdl.numstr('LINE',201)
    mapdl.l(201, 202)
    mapdl.l(201, 203)
    mapdl.l(202, 204)
    mapdl.l(203, 205)
    mapdl.l(204, 206)
    mapdl.l(205, 207)
    mapdl.l(206, 208)
    mapdl.lfillt(201, 202, 0.25)
    mapdl.lfillt(201, 203, 0.25)
    mapdl.lfillt(202, 204, 0.25)
    mapdl.lfillt(203, 205, 0.25)
    mapdl.lfillt(204, 206, 0.25)
    mapdl.lfillt(205, 207, 0.25)
    mapdl.l(207, 208)
    # mapdl.lplot()
    mapdl.numstr('AREA',201)
    
    mapdl.lsel('s','','',201)
    mapdl.lsel('a','','',209)
    mapdl.lsel('a','','',203)
    mapdl.lsel('a','','',211)
    mapdl.lsel('a','','',205)
    mapdl.lsel('a','','',213)
    mapdl.lsel('a','','',207)
    mapdl.lsel('a','','',214)
    mapdl.lsel('a','','',206)
    mapdl.lsel('a','','',212)
    mapdl.lsel('a','','',204)
    mapdl.lsel('a','','',210)
    mapdl.lsel('a','','',202)
    mapdl.lsel('a','','',208)

    mapdl.numstr('AREA',201)
    mapdl.al('ALL')

    mapdl.numstr('VOLUME', 201)
    mapdl.vext(201,'','','','', 10)
    mapdl.csys(1)
    mapdl.vgen(2, 201, '', '' ,'' , 15)
    mapdl.vdele(201, kswp=1)
    mapdl.vsbv(9, 202,'','DELETE','DELETE')

    return mapdl

def mesh_most(mapdl):
    mapdl.et(1, 186)
    mapdl.et(2, 200)
    mapdl.et(3, 281)
    mapdl.mshkey(2)

    mapdl.esize(0.1)
    mapdl.type(1)
    mapdl.vmesh(1,4)
    mapdl.vsweep(10, 50, 49)
    mapdl.vmesh(6, 8)

    return mapdl

def mesh_slot(mapdl):
    mapdl.vsweep(201, 206, 213)

    return mapdl

def mesh_dovetail(mapdl):
    mapdl.vsweep(201, 216, 233)

    return mapdl


params_1 = {'r_bore': 2.0 + 0.0,
            'z_front': 2.0,
            'bore_vert': 0.5 + 0.0,
            'bore_wide': 3.0 - 0.0,
            'web_wide': 1.0 + 0.0,
            'web_up': 1.0 + 0.0,
            'web_up2': 4.0,
            'rim_start': 0.5,
            'rim_wide': 2.0 + 0.0,
            'hole_r': 5.5,
            'hole_r2': 0.5}
params_1['rim_up'] = 10 - (params_1['r_bore'] +
                           params_1['bore_vert'] +
                           params_1['web_up'] +
                           params_1['web_up2'] +
                           params_1['rim_start'])


params_2 = {'r_bore': 2.0 + 0.5,
            'z_front': 2.0,
            'bore_vert': 0.5 + 0.5,
            'bore_wide': 3.0 - 0.5,
            'web_wide': 1.0 - 0.5,
            'web_up': 1.0 + 0.5,
            'web_up2': 3.0,
            'rim_start': 0.5,
            'rim_wide': 2.0 + 0.5,
            'hole_r': 5.75,
            'hole_r2': 0.25}
params_2['rim_up'] = 10 - (params_2['r_bore'] +
                           params_2['bore_vert'] +
                           params_2['web_up'] +
                           params_2['web_up2'] +
                           params_2['rim_start'])

mapdl.lsel('s', '', '', 1, 18)
mapdl.lsel('a', '', '', 22)
mapdl.lsel('a', '', '',28)
mapdl.save()

mapdl.view('ALL', 1, 0, 0)
mapdl.replot()
mapdl.lplot()
mapdl.show('JPEG')
mapdl()
#mapdl.print



# mapdl = launch_mapdl(run_location=path, override=True, loglevel='INFO')
mapdl = launch_mapdl()

mapdl.clear()
mapdl = build_disk(mapdl, params_1)
mapdl = add_bolthole(mapdl, params_1)
mapdl = add_slot(mapdl)
mapdl = mesh_most(mapdl)
mapdl = mesh_slot(mapdl)
mapdl.cdwrite('db', 'parent_mesh', 'cdb')


mapdl.clear()
mapdl = build_disk(mapdl, params_2)
mapdl = add_bolthole(mapdl, params_2)
mapdl = add_dovetail(mapdl)
# mapdl.allsel() mapdl.lplot()  # plot all lines
mapdl = mesh_most(mapdl)
mapdl = mesh_dovetail(mapdl)
mapdl.cdwrite('db', 'target_mesh', 'cdb')


# fem = femorph.Rotor(os.path.join(mapdl.directory, 'parent_mesh.cdb'))
# fem2 = femorph.Rotor(os.path.join(mapdl.directory, 'target_mesh.cdb'))
fem = femorph.Rotor('parent_mesh.cdb')
fem2 = femorph.Rotor('target_mesh.cdb')

surf = femorph.Surface(fem2.exsurf)

cpos_disk_side = ([(16.710794315488737, 9.458990757974526, 3.2880800486885997),
                   (-2.5, 5.86602540378445, 3.5),
                   (-0.18379134064773914, 0.982955141852842, 0.004464550141490883)])
cpos_disk_front = ([(-2.2042036375980363, 9.050783755759968, 24.42220625276661),
                    (-2.5, 5.86602540378445, 3.5),
                    (-0.2572779738300809, 0.9540632610493947, -0.15352960007009314)])


pl = pv.Plotter()
pl.add_mesh(surf, show_edges=False, smooth_shading=True)
pl.add_mesh(fem.exsurf_quad, color='w', show_edges=True, opacity=1.0, lighting=False)
pl.add_mesh(fem2.exsurf_quad, color='w', show_edges=True)
pl.camera_position = cpos_disk_front
pl.background_color = 'w'
cpos = pl.show(screenshot='disk_front_morphed.png')
pl.show()
femorph.open_logger()
settings = {'enable_ray_trace': True,
            'enable_local_morph': True,
            'enable_global_morph': True,
            'local_with_centroid': True,
            'global_cratio': 20.0,
            'local_steps': 200,
            'global_iter': 200}
fem.reset()
fem.morph(surf, settings=settings)

disk_cpos = ([(17.0465387471117, 10.285619651099998, 13.211248829212881),
              (-2.5, 6.0825317547305495, 3.25),
              (-0.2262003510055851, 0.971978749163678, -0.06395867712173095)])

front_cpos = ([(-3.5993935889082445, 4.335802552036804, 21.728704282864197),
               (-2.4999955912632155, 6.082535941232928, 3.25),
               (-0.4256432916298385, 0.9028980424393849, 0.06002427217087797)])

b_args = {'color': 'k'}
fem.animate(framerate=30, duration=10.0, cpos=cpos_disk_front, accuracy_scalars=True,
            filename='disk_front.mp4', background_color=None,
            mesh_kwargs={'color': 'w'}, target=surf,
            target_kwargs={'style': 'surface', 'opacity': 0.6})
