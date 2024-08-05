
## 所需初始参数总览，
## 写为字典格式，存为json文件
import sys
import json
sys.path.append('iteration')
from iteration import main
# 待添加：电流优化项, 磁面数据生成
args = {

## 参数名简写，在程序正文中由参数全称转换
## 在保存hdf5文件时，不能有None的值
##   参数类别/参数名             参数值       简写    类型     解释

# 优化器

    #迭代方式
    'iter_method':              'for',     #       str,    优化方式, 'for', 'min', 'nlopt', #'for-min', 'min-for'
    'number_iteration':         1,        # (ni)  int,    优化器迭代次数（for循环）, 若为0, 则不迭代
    'minimize_method':          'BFGS',   #       str,    minimize方法, https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    'minimize_tol':             1e-2,       # (mint)float,  （minimize）目标残差, 若为0, 不考虑此项                                   
                        
    # 优化算法参数
    'optimizer_coil':           'momentum', # (opt) str,    线圈参数迭代方法,  (sgd, gd, momentum, or adam)  
    'optimizer_fr':             'momentum', # (opt) str,    旋转参数迭代方法,  (sgd, gd, momentum, or adam)  
    'optimizer_I':              'momentum', # (opt) str,    电流参数迭代方法,  (sgd, gd, momentum, or adam)  
    'step_size_coil':       4e-6,       # (lrc) float,  参数coil_arg, 迭代步长, 为0则不优化                      
    'step_size_fr':         1e-5,       # (lrfr)float,  参数fr, 迭代步长, 为0则不优化
    'step_size_I':          1,          # (lrfr)float,  参数I, 迭代步长, 为0则不优化   
    'momentum_mass':            0.9,        # (mom) float,  梯度下降的动量参数
    'axis_resolution':          10,         # (res) int,    Resolution of the axis, multiplies NZ                        
    'var':                      0.999,      # adam优化方法的参数
    'eps':                      1e-8,       # adam优化方法的参数
    
# 线圈

    # 线圈参数
    'number_coils':             18,         # (nc)  int,    线圈总数                    
    'number_field_periods':     3,          # (nfp) int,    线圈周期数                     
    'stellarator_symmetry':     1,          # (ss)  int,    仿星器对称，1:对称，0:非对称                     
    'number_independent_coils': 3,          # (nic) int,    独立线圈数(半周期线圈数), (nc=nfp*(ss+1)*nic)                     
    'number_segments':          210,         # (ns)  int,    每个线圈分段数                     
     

    # 线圈读取       
    'coil_case':                'fourier',  #       str,    线圈表示方法, 'spline' or 'fourier' or 'spline_local'
    'init_coil_option':         'coil',     #       str,    初始线圈参数的来源, 'spline' or 'coil' or 'fourier' or 'circle'
    'circle_coil_radius':       1.0,        #       float,  生成初始的线圈半径   
    'coil_file_type':           'npy',      #       str,    初始线圈文件类型, 'npy' or 'makegrid', 后续可以再加
    'init_coil_file':                       #       str,    初始线圈文件名
            'initfiles/qas/coils_3.npy',       

    # Fourier表示
    'number_fourier_coils':        6,          # (nfc) int,    表示线圈的fourier分量数
                     
    # Bspline表示
    'number_control_points':    67,         # (ncp) int,    每个线圈控制点数,为输入线圈坐标点数+2，默认有一个坐标点闭合                   
    'spline_k':                 3,          # (k)   int,    Bspline阶数,默认为3阶

    # Bspline局部优化
    'optimize_location_nic':    [0,1],      #       list,   局部优化的线圈位置, 由列表给出进行局部优化的线圈是第几个, 第一个线圈从0开始   
    'optimize_location_ns':                 #       list,   局部优化的线圈位置, 由列表给出每个进行局部优化的线圈的具体分段, 
                [[[12, 23]], [[17, 26]]],               
        # 3阶列表，第一阶表示第几个线圈, 第二阶表示一个线圈中分成几段, 第三阶为每一段的起始与末尾点的位置
        # 此处第三阶的位置是实际的坐标位置, 不是控制点对应的节点区间, 每一项都为int
        # 同线圈不同段间距应大于3, 否则连在一起

    # 有限截面参数
    'length_normal':            [0.35 for i in range(3)],       # (ln)  list,  有限截面下每个线圈的法向间隔的长度                   
    'length_binormal':          [0.35 for i in range(3)],       # (lb)  list,  有限截面下每个线圈的副法向间隔的长度                    
    'number_normal':            3,          # (nn)  int,    有限截面下的法向线圈数量                     
    'number_binormal':          3,          # (nb)  int,    有限截面下的副法向线圈数量                    
                     
    # 旋转角参数
    'init_fr_case':             0,          #       int,    初始fr给出方法, 0：自动生成各项为0, 1：读取文件
    'init_fr_file':                         #       str,    给出变量fr的初始值文件
            'results_f/circle/s1_fr.npy',
    'number_rotate':            0,          # (nr)  int,    描述线圈绕组组的半旋转数的整数,通常设为0                    
    'number_fourier_rotate':    6,          # (nfr) int,    每个线圈的旋转的傅里叶分量的个数                  
   
# 电流

    # 电流初始
    'current_independent':      0,          #       int,    每个独立线圈是否拥有独立电流, 0:否, 1:是
    'current_I':                [1.71e7],      #       list,   线圈初始电流数值         

    # 电流参数优化
    'I_optimize':               1,          #       int,    是否优化线圈电流, 0为否, 1为是
        # 通过设置迭代步长是否为0来控制电流优化
    

# 磁面
    
    # 磁面参数
    'number_theta':             20,         # (nt)  int,    磁面上\theta(极向)的网格点数                    
    'number_zeta':              150,        # (nz)  int,    磁面上\zeta(环向)的网格点数              
    'surface_case':             1,          #       int,    磁面数据来源, 0:直接读取文件, 1:计算vmec文件生成
    
    # 计算磁面           
    'surface_vmec_file':                    #       str,    磁面数据的vmec文件
            'initfiles/qas/plasma.original',

    
    # 读取磁面数据
    'surface_r_file':                       #       str,    磁面坐标文件
            'initfiles/w7x/highres_r_surf.npy',
    'surface_nn_file':                      #       str,    磁面法向文件
            'initfiles/w7x/highres_nn_surf.npy',
    'surface_sg_file':                      #       str,    磁面面积文件
            'initfiles/w7x/highres_sg_surf.npy',

# 背景磁场

    'Bn_extern':                 0,          #       int,    背景磁场设置, 0:无, 1:boundary文件
    'Bn_extern_file':                        #       str,    读取对应的文件
            'initfiles/ncsx_c09r00/c09r00.boundary',

    

# LTS/HTS材料

    'material':             'REBCO_LT',    # str,    材料类型, REBCO_LT, NbTi, Nb3Sn    
    'HTS_signle_width':         4e-3,       # (sw)  float,  HTS材料单根宽度, 不包括相邻间隙
    'HTS_signle_thickness':     5e-5,       # (st)  float,  HTS材料单层结构厚度, 不包括相邻间隙
    'HTS_I_thickness':          1.2e-6,     #       float,  HTS材料导电层厚度
    'HTS_sec_area':             4.8e-9,     #       float,  HTS材料截面积（厚度*宽度或pi*(w/2)**2）
    'HTS_temperature':          4.2,        # (T)   float,  HTS材料温度, 单位K
    'HTS_I_percent':            0.6,        #       float,  线圈电流与超导临界电流的比例
    'HTS_structural_percent':   0.2,       #       float,  超导线缆与结构材料的比例

# loss function 目标和权重

    'weight_bnormal':           1,          # (wb)  float,  法向磁场分量, 一般设为1
    'weight_length':            0,          # (wl)  float,  单根线圈平均长度 
    'weight_curvature':         0,          # (wc)  float,  曲率 
    'weight_curvature_max':     0,          # (wcm) float,  最大曲率
    'weight_torsion':           0,          # (wt)  float,  扭转 
    'weight_torsion_max':       0,          # (wtm) float,  最大扭转
    'weight_distance_coil_coil':    0,      # (wdcc)float,  线圈间距 
    'weight_distance_coil_surface': 0,      # (wdcs)float,  线圈与磁面距离 
    'weight_HTS_strain':            0,          #       float,  应变量

    #  target 不为0则采取差值平方的loss
    'target_length_mean':            0,          #       float,  目标长度, 
    'target_curvature_max':     0,          #       float,  目标最大曲率
    'target_torsion_max':       0,          #       float,  目标最大扭转
    'target_distance_coil_coil':    10,      #       float,  目标最大线圈间距
    'target_distance_coil_surface': 10,      #       float,  目标最大线圈与磁面距离
    'target_HTS_strain':            0,          #       float,  目标最大应变

# 画图

    # 画图选项
    'plot_coil':                2,          #       int,    是否画线圈, 0:不画, 1:画线圈点集, 2:画有限截面
    'plot_loss':                0,          #       int,    是否画迭代曲线, 0：不画, 1：画
    'plot_poincare':            0,          #       int,    是否画poincare图, 0：不画, 1：画
    
    # 画线圈
    'number_points':            500,        # (nps) int,    画线圈时的散点数, 建议不少于线圈段数

    # 画poincare图
    'poincare_number':          25,         # (pn)      int,    画poincare图时的磁面圈数                         
    'poincare_phi0':            0,          # (phi0)float,  画poincare图时的环向坐标
    'number_iter':              400,        # (niter) int,  画poincare图时的磁力线追踪周期数 
    'number_step':              1,          # (nstep) int,  画poincare图时的每个周期的追踪步数
                                
# 程序输出

    # 输出选项,  0：不保存, 1：保存, 
    'save_npy' :                0,          #       int,    保存npy文件, 仅限被优化参数和loss值
    'save_hdf5' :               1,          #       int,    保存hdf5文件, 包含所有参数(大部分)
    'save_makegrid' :           0,          #       int,    保存线圈makegrid文件

    # 输出地址
    'out_hdf5':                             #       str,    hdf5, 输出参数
        'results/qas/hdf5.h5',        
    'out_coil_makegrid':                    #       str,    makegrid , 输出线圈
        'results/w7x/fmf5/makegrid',                
    'save_loss':                            #       str,    npy, 输出损失函数值(lossvals)
        'results/w7x/fmf5/loss.npy',         
    'save_coil_arg':                        #       str,    npy, 输出优化线圈参数(coil_arg)
        'results/w7x/fmf5/coil_arg.npy',
    'save_fr':                              #       str,    npy, 输出优化旋转参数(fr)
        'results/w7x/fmf5/fr.npy'
    
}



with open('initfiles/init_args.json', 'w') as f:
    json.dump(args, f, indent=4)


# main.main()

