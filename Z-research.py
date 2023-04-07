import json
import numpy as np
import matplotlib.pyplot as plt
from combining import J_MMSE, G_MMSE, get_epsilon
from evaluating import get_se, cdf_plot, get_he
from fusing import get_lc_z, get_z, fuse
from data import Channels
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-K', '--user_num', type=int, default=40)
parser.add_argument('-L', '--ap_num', type=int, default=100)
parser.add_argument('-N', '--antenna', type=int, default=4)
parser.add_argument('-p', '--power', type=float, default=100)
parser.add_argument('-s', '--data-source', type=str, default='data')
parser.add_argument('-n', '--running-number', type=int)
parser.add_argument('-w', '--workers', type=int, default=5)
parser.add_argument('--schema', action='append', type=str)


if __name__ == '__main__':
    args = parser.parse_args()
    p = args.power
    with open('schema.json') as f:
        schemas = json.load(f)
    channels = Channels(args.data_source, args.workers)
    Zdiag = []
    for running_idx in range(args.running_number):
        H, Hhat, C, Epsilon = channels.next()
        schema = args.schema[0]
        print('running {}-th instance...'.format(running_idx))
        print('schema {}...'.format(schema))
        group_list = schemas[schema]['group-list']
        V_G_MMSE = G_MMSE(Hhat, C, Epsilon, p, group_list)
        He = get_he(Hhat, V_G_MMSE, group_list)
        Re = get_epsilon(He)
        Z = get_z(Hhat, C, Epsilon, p, group_list, V_G_MMSE)
        Zdiag.extend(np.concatenate([np.expand_dims(np.diag(Z[args.user_num*ii:args.user_num*(ii+1)]), 0) for ii in range(len(group_list)-1)], 0).tolist())
    plt.matshow(np.abs(np.array(Zdiag)))
    plt.show()
    print('done.')
