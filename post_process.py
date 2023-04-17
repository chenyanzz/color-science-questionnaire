import csv
import json
import math
import os

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
    return [sum([c[i] for c in colors])/len(colors) for i in range(3)]


def hex2rgb255(c):
    return [(c >> 16) / 255, ((c & 0xFF00) >> 8) % 255 / 255, (c & 0xFF) / 255]


original_colors = list(map(
    hex2rgb255,
    [0xEAC1B0, 0xF5C8AF, 0xE9CEC5, 0xEACFBD]))


def generate_plot(CSPACE: str, SEPERATE_IMG: str, TYPE: str, save: bool = False):

    colors = []
    folder = f'result-{TYPE}'
    try:
        os.mkdir(folder)
    except:
        pass

    # colors[#face][#answer] = [r,g,b]

    forms_ques = json.load(open("forms.json"))
    colors_ques: list[list] = [[
        filter_color(original_colors[i],
                     form['colors'][i])
        for form in forms_ques]
        for i in range(4)]

    forms_app = [[int(x) for x in row.split(',')[4:7]]
                 for row in open("app.csv").read().splitlines()]
    colors_app: list[list] = [[cspace_convert(
        color, 'CIELab', 'sRGB1') for color in forms_app[i::4]] for i in range(4)]

    if TYPE == 'app':
        colors = colors_app
    if TYPE == 'form':
        colors = colors_ques
    if TYPE == 'compare':
        colors = [a+b for (a, b) in zip(colors_app, colors_ques)]

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
            with open(f'{folder}/{k}-{SEPERATE_IMG}-{i}-data.csv', 'w') as f:
                for c in list(v):
                    c = list(c)
                    f.write(",".join(map(str, c))+'\n')
            with open(f'{folder}/{k}-{SEPERATE_IMG}-{i}-avg.txt', 'w') as f:
                f.write(f'{k}: {str(avg_color(v))}\n')

        # 坐标点上色
        n = 4 // len(color_groups)
        s = 10
        # blue: app, green: form
        pcs = RGBs if TYPE != 'compare' else [(0.46, 0.45, 0.97)] * len(
            colors_app[0])*n + [(0.55, 0.72, 0.44)]*len(colors_ques[0])*n

        if CSPACE == 'RGB':
            Rs = [c[0] for c in RGBs]
            Gs = [c[1] for c in RGBs]
            Bs = [c[2] for c in RGBs]
            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')
            ax.scatter(Rs, Gs, Bs, s=s, c=pcs, marker='o')
        elif CSPACE == 'LAB':
            Ls = [c[0] for c in LABs]
            As = [c[1] for c in LABs]
            Bs = [c[2] for c in LABs]
            ax.set_xlabel('L')
            ax.set_ylabel('A')
            ax.set_zlabel('B')
            ax.scatter(Ls, As, Bs, s=s, c=pcs, marker='o')
        elif CSPACE == 'AB':
            As = [c[1] for c in LABs]
            Bs = [c[2] for c in LABs]
            ax.set_xlabel('A')
            ax.set_ylabel('B')
            ax.scatter(As, Bs, s=s, c=pcs, marker='o')
        elif CSPACE == 'CH':
            Cs = [c[1] for c in LCHs]
            Hs = [math.radians(c[2]) for c in LCHs]
            ax.scatter(Hs, Cs, s=s, c=pcs, marker='o')

        if save:
            fig.savefig(f'{folder}/{CSPACE}-{SEPERATE_IMG}-{i}.jpg', dpi=300)
            plt.close(fig)

    if not save:
        plt.show(block=True)


if __name__ == "__main__":
    for CSPACE in ['RGB', 'LAB', 'AB', 'CH']:
        for SEPERATE_IMG in ['each', 'total', 'gender']:
            for TYPE in ['app', 'form', 'compare']:
                naming = f'{TYPE}-{CSPACE}-{SEPERATE_IMG}'
                print(f'generate_plot for "{naming}"')
                generate_plot(CSPACE, SEPERATE_IMG, TYPE, save=True)

# generate_plot('LAB', 'each', 'TYPE', save=True)

# def test_hsb(colorhex, h=0, s=100, b=100):
#     color = np.array(hex2rgb255(colorhex)).reshape((3, 1))
#     mh = hue_rotate(h)
#     ms = saturate(s)
#     mb = brightness(b)

#     color = np.clip(mh @ color, 0, 1)
#     color = np.clip(ms @ color, 0, 1)
#     color = np.clip(mb @ color, 0, 1)
#     print(hex(rgb2hex(color)))


# test_hsb(0xAA0000, b=120)
