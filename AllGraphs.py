#!/usr/bin/env python
from all_graph_in_folder import openfile,graph,decrease_ratio
from test_finding_function import decrease
import os

if __name__ == '__main__':
    folder = '/Users/apple/Downloads/Second Desktop/大四/毕业论文参考文献/yzw毕设上半学期数据/TGA Data/第二批'
    os.chdir(folder)

    count = 1
    for file in os.listdir(folder):
        if file == '.DS_Store':
            continue
        basename = os.path.basename(file)
        basename_list = list(basename)
        t = openfile(file)
        x_axis, y_axis = t

        baseline = decrease(x_axis, y_axis, file)
        new_y_axis = [(i - baseline) / baseline * 100 for i in y_axis]
        graph(x_axis, new_y_axis, basename_list, count)
        print('='*30)

        count += 1
