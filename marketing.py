import femorph
import femorph_blender
import pyansys
import pyvista as pv
import numpy as np 
import matplotlib.pyplot as plt
import os
# import importlib
# importlib.reload(femorph)

jcturb_surf = 'JC_Turbine.stl'
jcturb_cdb = 'JC_Turbine.cdb'
surf = femorph.Surface(jcturb_surf)
fem = femorph.Rotor(jcturb_cdb)
fem.replicate_cyclically()

jetcat_surf = '/home/jeff/Documents/FEMORPH/Study/jetcat_scan_sim.ply'
jetcat_cdb = '//home/jeff/Documents/FEMORPH/Study/jetcat_sector.cdb'

surf = femorph.Surface(jetcat_surf)
fem = femorph.Rotor(jetcat_cdb)
fem.replicate_cyclically()

pbs_surface = '/home/jeff/Documents/PBS/pbs_builder/morph/PBS Rotor 4 with out strain gages ~ 320 mv_standard 7june2018.ply'
pbs_cdb = '/home/jeff/Documents/PBS/pbs_builder/pbs4_sector_0319.cdb'

surf = femorph.Surface(pbs_surface)
fem = femorph.Rotor(pbs_cdb)
fem.replicate_cyclically()

fem.align(surf)
pbs_align_data = np.array([[ 0.99950425,  0.03136094, -0.00278345, -0.00343886],
       [-0.03136548,  0.9995067 , -0.001602  ,  0.00473506],
       [ 0.00273184,  0.00168851,  0.99999484,  0.91945161],
       [ 0.        ,  0.        ,  0.        ,  1.        ]])
fem.transform(pbs_align_data)

pbs_cpos = [(8.96453857421875e-05, 0.0032181739807128906, 32.802207228923336),
 (8.96453857421875e-05, 0.0032181739807128906, 0.9077184498310089),
 (0.0, 1.0, 0.0)]


pl = pv.Plotter()
pl.add_mesh(fem.exsurf_quad, color='w', show_edges=True, lighting=False)
pl.add_mesh(surf)
pl.background_color='w'
pl.camera_position = 'zy' #cpos #pbs_cpos # 'xy'
pl.show()
cpos = pl.show()
#pl.show(screenshot='pbs_fem.png')
pl.show(screenshot='pbs4_sector.png')
pl.show(screenshot='pbs4_surf.png')
#pl.show(screenshot='jcturb_morph_sn.png')

b_args = {'color': 'k'}
accuracy = fem.accuracy(surf)
# blade_mask = fem.exsurf_quad.point_arrays['BLADE_AREA_NODES']
# accuracy_blades = accuracy[blade_mask]
pl = pv.Plotter()
#pl.add_mesh(fem.exsurf_quad, scalars=accuracy_blades, rng=[-0.01, 0.01])
pl.add_mesh(fem.exsurf_quad, scalars=accuracy, show_edges=True, rng=[-0.001, 0.001], lighting=False, show_scalar_bar=True, stitle=' Deviation, in.', scalar_bar_args=b_args)
pl.camera_position = cpos #'xy'
pl.background_color = 'w'
#cpos = pl.show()
pl.show(screenshot='jetcat_deviation_morphed.png')

#fem.select_moving_from_components('DISK_NODE')
fem.select_moving(surf, 0.07, 0.5)  # for PBS_R4_Script

fem.select_moving(surf, 0.015, 0.5)

fem.select_moving_from_components(fixed='FIXED_NODES')
fem.select_moving_from_components(fixed='DI_NODES')
fem.plot_mesh_types()

set_morph = {'enable_ray_trace': True,
             'enable_local_morph': True,
             'enable_global_morph': True,
             'global_cratio': 5.0,
             'global_iter': 50}

fem.morph(surf, settings=set_morph)
fem.morph(surf)

jetcat_cpos = np.array([(-2.4869716723888207, 3.710105418036933, -0.3599879896645217),
                 (0.0, -1.1324882507324219e-06, -0.39299842331092805),
                 (0.008157354713202405, 0.014364288152432344, -0.9998635530860983)])
jetcat2_cpos = np.array([(-1.3420457413777038, 0.3339811645720238, 1.2785396296820362),
                 (-0.6408727684831644, 0.782467203372468, -0.6317357592983857),
                 (-0.6678662464974123, 0.7408674183463028, -0.07120495223186737)])


pbs_cpos = np.array([(-1.5229954050070758, 16.91478761571719, 3.6751002582168937),
                     (-0.17036343366427442, 2.6373661893020492, -0.28857149674767535),
                     (-0.025564186287430884, 0.26516431700800425, -0.9638642836857999)])

pbs_cpos2 = np.array([(9.362778435435558, 5.484808632476523, 3.2885504142249107),
                      (-1.502626956381973, 7.005190472295702, -2.264861698967431),
                      (0.2606232367566843, 0.9311584041953591, -0.2549893228329799)])

jcturb_cpos = np.array([(-0.9053315206210218, 1.5743842292706725, 1.62491801702098),
                    (-0.7227891548925319, 0.24513198695765137, 0.00029703852598093883),
                        (-0.9717995869745697, 0.11686718219397912, -0.20481119227741318)])


target_kwargs = {'opacity': 1.0,
                 'show_edges': False}
# fem.animate(framerate=20, duration=15.0, show_edges=True, surf=None, cpos=jcturb_cpos, filename='jcturb_morphvid.mp4')
fem.animate(framerate=20, duration=5.0, cpos=jetcat_cpos, accuracy_scalars=False, scalar_bar=False, filename='test.mp4', target=None, target_kwargs=target_kwargs)

fem.animate(framerate=20, duration=5.0, cpos=jetcat_cpos, accuracy_scalars=False, scalar_bar=False, filename='test.mp4')

fem.animate(framerate=20, duration=5.0, cpos=jetcat_cpos, accuracy_scalars=False, filename='test.mp4',
            mesh_kwargs={'color': 'w'}, target=surf, target_kwargs={'style': 'surface', 'opacity': 0.8})

fem.animate(framerate=20, duration=5.0, cpos=jetcat_cpos, accuracy_scalars=True, filename='test.mp4',
            mesh_kwargs={'color': 'w'}, target=surf, target_kwargs={'style': 'surface', 'opacity': 0.8})



pl = pv.Plotter()
pl.add_mesh(fem.exsurf_quad, color='w')
pl.add_mesh(fem.orig_pts, 'b')
#pl.add_mesh(surf,color='b')
pl.show()


accuracy_morph = fem.accuracy(surf)
# blade_mask = fem.exsurf_quad.point_arrays['BLADE_AREA_NODES']
# accuracy_blades = accuracy[blade_mask]
pl = pv.Plotter()
#pl.add_mesh(fem.exsurf_quad, scalars=accuracy_blades, rng=[-0.01, 0.01])
pl.add_mesh(fem.exsurf_quad, scalars=accuracy_morph, rng=[-0.001, 0.001], show_edges=True, lighting=False, show_scalar_bar=True, stitle=' Deviation, in.', scalar_bar_args=b_args)
pl.camera_position = cpos # 'xy'
pl.background_color = 'w'
pl.show(screenshot='pbs_morphdev.png')



import pyvista as pv
accuracy_morph = fem.accuracy(surf)
pl = pv.Plotter()
pl.add_mesh(fem.exsurf_quad, scalars=accuracy_morph, rng=[-0.001, 0.001], show_edges=True, lighting=False, show_scalar_bar=True, stitle=' Deviation, in.', scalar_bar_args=b_args)
pl.camera_position = cpos # 'xy'
pl.background_color = 'w'
pl.show(screenshot='pbs_morphdev.png')

# Blend DOE Plots
fem = femorph.Rotor(pbs_cdb)

spans = np.arange(2.25, 5.51, 1.0)
aspects = np.arange(0.5, 1.26, 0.5)  # Actually, Length
depths = np.arange(0.2, 0.51, 0.15)  # 0.5 - 0.75

blend = femorph_blender.Blender(fem)
blend.define_edge('LEAD_EDGE_NODE')

#blend.clip_blend_on_edge(-1.0, 35)
cpos = np.array([(-17.686528869042114, -6.227797349681913, -5.832027327494298),
 (-0.09352268273654973, -4.22205234505215, 0.06094883806175),
 (0.09316630649664437, -0.993833640036472, 0.06012266848393599)])

cpos_side = np.array([(-18.736877851059727, -3.3956832459257837, 0.1413849155459014),
 (-0.09352268273654973, -4.22205234505215, 0.06094883806175),
 (-0.04417627473242856, -0.9987818022771868, 0.02198563600853474)])

model_n = 0
for aspect in aspects:
    for depth in depths:
            for span in spans:
            model_n += 1
            blend.reset()
            blend.blend_on_edge(span, aspect, depth, 0, 0.0, 100)
            blend.repair()

            pl = pv.Plotter()
            pl.add_mesh(blend.exsurf_quad, color='w', show_edges=True, lighting=True)
            pl.background_color= 'w'
            pl.camera_position = cpos_side
            #cpos = pl.show()
            pl.show(screenshot='pbs4_blend_%s.png' % model_n)
            #cpos = pl.show(screenshot='pbs4_blend_mid.png')

import femorph

jetcat_surf = 'jetcat_scan.ply'
jetcat_cdb = 'jetcat_sector.cdb'

surf = femorph.Surface(jetcat_surf)
ppfem = femorph.Rotor(jetcat_cdb)
fem.replicate_cyclically()
fem.align(surf)
fem.morph(surf, settings=set_morph)
fem.write_cyclic_sectors()

blend = femorph_blender.Blender(fem)
blend.define_edge('LEAD_EDGE_NODE')
blend.blend_on_edge(spans[6], aspects[1], depths[3], 0, 0.0, 100)
blend.write_archive()


from femorph import examples

# load the fem
fem = femorph.Fem(examples.ptr_cdb)

# load the cmm: we need only sections 2:14
sections = np.load(examples.cmm_array)
cmm = femorph.Cmm(sections[1:-1]) 

# rotate and translate
cmm.rotate_y(-90)
cmm.rotate_z(-9.82487897)
cmm.translate([0, 0, -0.50718823])
cmm.rotate_z(200)

# refine
cmm.refine(100, 200)

# plot the initial accuracy
fem.plot_accuracy(cmm, show_both=False, rng=1E-2, cmap='jet')

# select the moving nodes and morph
fem.select_moving(cmm, 0.05, 0.15)
fem.morph(cmm)

# plot final accuracy
fem.plot_accuracy(cmm, show_both=False, rng=1E-3, cmap='jet')

# fem.write_nodes('nblock.inp')
cmm.secpts

cmm_cpos = np.array([(4.793295836278924, 5.595845320849496, -0.07075151319993145),
                     (4.9336039896016635, 0.9543500787472062, -0.45498522999999974),
                     (0.9999876344964208, 0.0019162776088425652, -0.004588979666453884)])


pl = pv.Plotter()
pl.add_mesh(pv.PolyData(cmm.secpts), color='k')
pl.background_color = 'w'
pl.camera_position = cmm_cpos
pl.show()
cpos = pl.show(screenshot='cmm_points.png')


import numpy as np; import femorph; from femorph import examples

sections = np.load(examples.cmm_array); cmm = femorph.Cmm(sections[1:-1]) 


cmm.rotate_y(-90); cmm.rotate_z(-9.82487897); cmm.translate([0, 0, -0.50718823]); cmm.rotate_z(200)


## -------------------
import pyansys
path = os.getcwd()
# /home/jeff/Downloads/install_libs.sh
mapdl = pyansys.launch_mapdl(run_location=path, override=True, loglevel='INFO', mode='console', nproc=4)

params_1 = {'r_bore': 2.0 + 0.0,
          'z_front': 2.0,
          'bore_vert': 0.5 + 0.0,
          'bore_wide': 3.0 - 0.0,
          'web_wide': 1.0 + 0.0,
          'web_up': 1.0 + 0.0,
          'web_up2': 4.0,
          'rim_start': 0.5,
          'rim_up': 10 - (r_bore + bore_vert + web_up + web_up2 + rim_start),
          'rim_wide': 2.0 + 0.0,
          'hole_r': 5.5,
          'hole_r2': 0.5}

params_2 = {'r_bore': 2.0 + 0.5,
            'z_front': 2.0,
            'bore_vert': 0.5 + 0.5,
            'bore_wide': 3.0 - 0.5,
            'web_wide': 1.0 - 0.5,
            'web_up': 1.0 + 0.5,
            'web_up2': 3.0,
            'rim_start': 0.5,
            'rim_up': 10 - (r_bore + bore_vert + web_up + web_up2 + rim_start),
            'rim_wide': 2.0 + 0.5,
            'hole_r': 5.75,
            'hole_r2': 0.25}

mapdl = build_disk(mapdl, params_1)
mapdl = add_bolthole(mapdl, params_1)
mapdl = add_slot(mapdl)
mapdl = mesh_most(mapdl)
mapdl = mesh_slot(mapdl)
mapdl.cdwrite('db', 'parent_mesh', 'cdb')


mapdl = build_disk(mapdl, params_2)
mapdl = add_bolthole(mapdl, params_2)
mapdl = add_dovetail(mapdl)
mapdl = mesh_most(mapdl)
mapdl = mesh_dovetail(mapdl )
mapdl.cdwrite('db', 'target_mesh', 'cdb')

fem = femorph.Rotor('parent_mesh.cdb')
fem2 = femorph.Rotor('target_mesh.cdb')

surf = femorph.Surface(fem2.exsurf)

pl = pv.Plotter()
pl.add_mesh(surf, show_edges=True)
pl.add_mesh(fem.exsurf_quad, color='w', show_edges=True)
pl.add_mesh(fem2.exsurf_quad, color='b', show_edges=True)
cpos = pl.show()

set_morph = {'enable_ray_trace': True,
             'enable_local_morph': True,
             'enable_global_morph': True,
             'global_cratio': 20.0,
             'global_iter': 500}
fem.reset()
fem.morph(surf)

disk_cpos = np.array([(17.0465387471117, 10.285619651099998, 13.211248829212881),
                      (-2.5, 6.0825317547305495, 3.25),
                      (-0.2262003510055851, 0.971978749163678, -0.06395867712173095)])

fem.animate(framerate=30, duration=15.0, cpos=disk_cpos, accuracy_scalars=True, filename='test.mp4',
            mesh_kwargs={'color': 'w'}, target=surf, target_kwargs={'style': 'surface', 'opacity': 0.6})


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

    

