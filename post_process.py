import json
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_convert


def hue_rotate(angle):
    return np.array([
        [+0.213, +0.715, +0.072],
        [+0.213, +0.715, +0.072],
        [+0.213, +0.715, +0.072],
    ]) + math.cos(math.radians(angle)) * np.array([
        [+0.787, -0.715, -0.072],
        [-0.213, +0.285, -0.072],
        [-0.213, -0.715, +0.928],
    ]) + math.sin(math.radians(angle)) * np.array([
        [-0.213, -0.715, +0.928],
        [+0.143, +0.140, -0.283],
        [-0.787, +0.715, +0.072],
    ])


def brightness(percent):
    return np.eye(3) * (percent/100)


def saturate(percent):
    return np.array([
        [+0.213, +0.715, +0.072],
        [+0.213, +0.715, +0.072],
        [+0.213, +0.715, +0.072],
    ]) + (percent/100) * np.array([
        [+0.787, -0.715, -0.072],
        [-0.213, +0.285, -0.072],
        [-0.213, -0.715, +0.928],
    ])


def filter_color(rgb0, hsb):
    """
    param rgb0: [r,g,b]
    param hsb: {h,s,b}
    returns [r,g,b]
    """
    color = np.array(rgb0).reshape((3, 1))
    mh = hue_rotate(hsb['h'])
    ms = saturate(hsb['s'])
    mb = brightness(hsb['b'])

    color = np.clip(mh @ color, 0, 1)
    color = np.clip(ms @ color, 0, 1)
    color = np.clip(mb @ color, 0, 1)
    return list(color.reshape((3)))


def rgb2hex(rgb):
    r, g, b = rgb
    return (int(r*256) << 16) + (int(g*256) << 8) + int(b*256)


def avg_color(colors: list):
    return [sum([c[i] for c in colors])//len(colors) for i in range(3)]


original_colors = list(map(
    lambda c: [(c >> 16) / 255, (c >> 8) % 255 / 255, c % 255 / 255],
    [0xEBC8B1, 0xFFDCC2, 0xF3DAD1, 0xF2E0D0]))


def generate_plot(CSPACE: str, SEPERATE_IMG: str, save: bool = False):

    forms = json.load(open("forms.json"))

    # colors[#face][#answer] = [r,g,b]
    colors: list[list] = [[
        filter_color(original_colors[i],
                     form['colors'][i])
        for form in forms]
        for i in range(4)]

    color_groups = []
    if SEPERATE_IMG == 'each':
        color_groups = colors
    elif SEPERATE_IMG == 'total':
        color_groups = [colors[0]+colors[1]+colors[2]+colors[3]]
    elif SEPERATE_IMG == 'gender':
        color_groups = [colors[0]+colors[1], colors[2]+colors[3]]

    for i in range(len(color_groups)):
        fig = plt.figure(figsize=(5, 5))
        if len(CSPACE) == 3:
            ax = fig.add_subplot(projection='3d')
        elif CSPACE == 'CH':
            ax = fig.add_subplot(projection='polar')
        else:
            ax = fig.add_subplot(projection=None)

        # 设置坐标轴
        RGBs = color_groups[i]
        LABs = [cspace_convert(rgb, 'sRGB1', 'CIELab') for rgb in RGBs]
        LCHs = [cspace_convert(rgb, 'sRGB1', 'CIELCh') for rgb in RGBs]
        for k, v in {"RGB": RGBs, "LAB": LABs, "LCH": LCHs}.items():
            with open(f'result/{k}-{SEPERATE_IMG}-{i}-data.csv', 'w') as f:
                for c in list(v):
                    c = list(c)
                    f.write(",".join(map(str, c))+'\n')
            with open(f'result/{k}-{SEPERATE_IMG}-{i}-avg.txt', 'w') as f:
                f.write(f'{k}: {str(avg_color(v))}\n')

        if CSPACE == 'RGB':
            Rs = [c[0] for c in RGBs]
            Gs = [c[1] for c in RGBs]
            Bs = [c[2] for c in RGBs]
            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')
            ax.scatter(Rs, Gs, Bs, c=RGBs, marker='o')
        elif CSPACE == 'LAB':
            Ls = [c[0] for c in LABs]
            As = [c[1] for c in LABs]
            Bs = [c[2] for c in LABs]
            ax.set_xlabel('L')
            ax.set_ylabel('A')
            ax.set_zlabel('B')
            ax.scatter(Ls, As, Bs, c=RGBs, marker='o')
        elif CSPACE == 'AB':
            As = [c[1] for c in LABs]
            Bs = [c[2] for c in LABs]
            ax.set_xlabel('A')
            ax.set_ylabel('B')
            ax.scatter(As, Bs, c=RGBs, marker='o')
        elif CSPACE == 'CH':
            Cs = [c[1] for c in LCHs]
            Hs = [math.radians(c[2]) for c in LCHs]
            ax.scatter(Hs, Cs, c=RGBs, marker='o')

        if save:
            fig.savefig(f'result/{CSPACE}-{SEPERATE_IMG}-{i}.jpg', dpi=200)
            plt.close(fig)

    if not save:
        plt.show(block=True)


if __name__ == "__main__":
    for CSPACE in ['RGB', 'LAB', 'AB', 'CH']:
        for SEPERATE_IMG in ['each', 'total', 'gender']:
            naming = '{CSPACE}-{SEPERATE_IMG}-{i}'
            generate_plot(CSPACE, SEPERATE_IMG, save=True)
