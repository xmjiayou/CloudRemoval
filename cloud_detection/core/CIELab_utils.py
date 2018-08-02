# sRGB与CIE-L*ab色彩空间转换
# 常量
x_n = 95.05
y_n = 100.00
z_n = 108.89
sigma = 6/29
sigma2 = sigma**2
sigma3 = sigma**3
c = 4/29


def rgb_to_lab(rgb):
    return _xyz_to_lab(_rgb_to_xyz(rgb))


def lab_to_rgb(lab):
    return _xyz_to_rgb(_lab_to_xyz(lab))


def _rgb_to_xyz(rgb):
    r, g, b = map(lambda v: _gamma(v/255), rgb)
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) * 100
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) * 100
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) * 100
    xyz = (x, y, z)
    print(xyz)
    return xyz


def _xyz_to_rgb(xyz):
    x, y, z = map(lambda v: v/100, xyz)
    r = round(_gamma_inverse(x * 3.2406 + y * -1.5372 + z * -0.4986) * 255)
    g = round(_gamma_inverse(x * -0.9689 + y * 1.8758 + z * 0.0415) * 255)
    b = round(_gamma_inverse(x * 0.0557 + y * -0.2040 + z * 1.0570) * 255)
    rgb = (r, g, b)
    return rgb


def _xyz_to_lab(xyz):
    x, y, z = xyz
    l_ = 116 * _f(y/y_n) - 16
    a = 500 * (_f(x/x_n) - _f(y/y_n))
    b = 200 * (_f(y/y_n) - _f(z/z_n))
    lab = (l_, a, b)
    print(lab)
    return lab


def _lab_to_xyz(lab):
    l_, a, b = lab
    temp = (l_+16)/116
    x = x_n * _f_inverse(temp+a/500)
    y = y_n * _f_inverse(temp)
    z = z_n * _f_inverse(temp-b/200)
    xyz = (x, y, z)
    return xyz


def _f(t):
    return t**(1/3) if t > sigma3 else t/(3*sigma2)+c


def _f_inverse(t):
    return t**3 if t > sigma else 3*sigma2*(t-c)


def _gamma(t):
    return ((t+0.055)/1.055)**2.4 if t > 0.04045 else t/12.92


def _gamma_inverse(t):
    return 1.055*(t**(1/2.4))-0.055 if t > 0.0031308 else 12.92*t
