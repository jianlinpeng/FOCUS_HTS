import json
import jax.numpy as np
from jax import jit, vmap
import scipy.interpolate as si
import plotly.graph_objects as go
import h5py
from test_coil_cal import CoilSet
import sys 
sys.path.append('/home/nxy/codes/coil_spline_HTS/iteration')
import read_init
import fourier
import spline
import self_B

pi = np.pi
with open('/home/nxy/codes/coil_spline_HTS/initfiles/init_args.json', 'r') as f:    # 传入地址
    args = json.load(f)
globals().update(args)


nc = args['number_coils'] = 1
args['number_independent_coils'] = 1
ns = args['number_segments'] = 100



fr = np.zeros((2, nc, args['number_fourier_rotate'])) 
theta = np.linspace(0, 2 * np.pi, ns + 1)
fc = np.load('/home/nxy/codes/coil_spline_HTS/fc_HSX.npy')[:, np.newaxis, :]
rc = fourier.compute_r_centroid(fc, 6, nc, ns, theta)
coil = rc[:, :-1, :]
def average_length(coil):      #new
    al = np.zeros((coil.shape[0], 3))   
    r_coil = coil  # 有限截面平均
    al = al.at[:-1, :].set(r_coil[1:, :] - r_coil[:-1, :])
    al = al.at[-1, :].set(r_coil[0, :] - r_coil[-1, :])
    len = np.sum(np.linalg.norm(al, axis=-1))
    return len

len = average_length(coil[0])
# fig = go.Figure()
# for i in range(10):
#     fig.add_scatter3d(x=coil[i*10:(i+1)*10, 0],y=coil[i*10:(i+1)*10, 1],z=coil[i*10:(i+1)*10, 2], name='coil{}'.format(i), mode='markers', marker_size = 1.5)   
# # fig.add_scatter3d(x=coil[:, 0],y=coil[:, 1],z=coil[:, 2], name='coil', mode='markers', marker_size = 1.5)   
# fig.update_layout(scene_aspectmode='data')
# fig.show()

der1 = fourier.compute_der1(fc, 6, nc, ns, theta)
dl = der1[:, :-1, :] * (2*np.pi/ns)
coil_cal = CoilSet(args)


# circle
I = 1e6
params = (fc, fr, I)
coil, dl, normal, binormal, curva = coil_cal.get_args_sec_circle(params)
B_coil = self_B.coil_B_section_circle(args, coil, I, dl, normal, binormal, curva)
r = len/2/np.pi/100
fig = go.Figure(data=
    go.Contour(
        z=B_coil,
        x = np.linspace(-r, r, 80),
        y = np.linspace(-r, r, 80),
        contours_coloring='lines',
        line_width=2,
        colorbar = dict(tickfont = dict(size=20))
    )
)
fig.update_xaxes(tickfont = dict(size=25))
fig.update_yaxes(tickfont = dict(size=25))
fig.show()


# square
# I = 1.5e5
# params = (fc, fr, I)
# coil, dl, normal, binormal, curva = coil_cal.get_args_sec_square(params)
# B_coil = self_B.coil_B_section_square(args, coil, I, dl, v1, v2, binormal, curva)
# print(B_coil)
# fig = go.Figure(data=
#     go.Contour(
#         z=B_coil,
#         x = np.linspace(-2.84, 2.84, 80),
#         y = np.linspace(-6.48, 6.48, 80),
#         contours_coloring='lines',
#         line_width=2,
#         colorbar = dict(tickfont = dict(size=20))
#     )
# )
# fig.update_xaxes(tickfont = dict(size=25))
# fig.update_yaxes(tickfont = dict(size=25))
# fig.show()

