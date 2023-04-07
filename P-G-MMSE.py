import json
import numpy as np
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
parser.add_argument('-s', '--data-source', type=str, default='data/L100N4K40p100-homo')
parser.add_argument('-n', '--running-number', type=int)
parser.add_argument('-w', '--workers', type=int, default=5)
parser.add_argument('--schema', action='append', type=str)
parser.add_argument('--sample', type=int, default=50)
parser.add_argument('-t', '--threshold', type=float)


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    if args.sample > args.user_num * args.running_number:
        args.sample = args.user_num * args.running_number
    p = args.power
    with open('schema.json') as f:
        schemas = json.load(f)
    SE_collection = {'J-MMSE': [], "L-MMSE": []}
    SE_collection.update({'G-MMSE ({})'.format(s): [] for s in args.schema})
    truncated_list = {s: [] for s in args.schema}
    channels = Channels(args.data_source, args.workers)
    for running_idx in range(args.running_number):
        H, Hhat, C, Epsilon = channels.next()
        print('running {}-th instance...'.format(running_idx))
        if running_idx > 0:
            V_J_MMSE = J_MMSE(Hhat, C, Epsilon, p)
            SE_collection['J-MMSE'].extend(get_se(H, V_J_MMSE, C, p))
            group_list = [i for i in range(0, args.ap_num, args.antenna)][1:]
            V_G_MMSE = G_MMSE(Hhat, C, Epsilon, p, group_list)
            SE_collection['L-MMSE'].extend(get_se(H, V_G_MMSE, C, p))
        for schema in args.schema:
            print('schema {}...'.format(schema))
            group_list = schemas[schema]['group-list']
            V_G_MMSE = G_MMSE(Hhat, C, Epsilon, p, group_list)
            if 'fusing' in schemas[schema]:
                if schemas[schema]['fusing'] == 'LC':
                    He = get_he(Hhat, V_G_MMSE, group_list)
                    Re = get_epsilon(He)
                    Z = get_lc_z(He, Re, p, V_G_MMSE, group_list)
                elif schemas[schema]['fusing'] == 'IPS':
                    Z = get_z(Hhat, C, Epsilon, p, group_list, V_G_MMSE)
                # truncate Z using threshold
                # get truncating list at the first instance
                if running_idx == 0:
                    truncated_num = [0 for _ in range(len(group_list)-1)]
                    truncated_list[schema] = [[] for _ in range(len(group_list)-1)]
                    for g in range(len(group_list)-1):
                        Zi = Z[g*args.user_num:(g+1)*args.user_num]
                        for k in range(args.user_num):
                            if np.abs(Zi[k, k]) < args.threshold:
                                Zi[:, k] = 0
                                truncated_num[g] += 1
                                truncated_list[schema][g].append(k)
                    print('truncated number: {}'.format(truncated_num))
                # apply truncating strategy
                else:
                    for g in range(len(group_list)-1):
                        Zi = Z[g*args.user_num:(g+1)*args.user_num]
                        for k in truncated_list[schema][g]:
                            Zi[:, k] = 0
                    V_G_MMSE = fuse(V_G_MMSE, Z, group_list)
            if running_idx > 0:
                SE_collection['G-MMSE ({})'.format(schema)].extend(get_se(H, V_G_MMSE, C, p))
    for schema in SE_collection:
        SE_collection[schema].sort()
        SE_collection[schema] = SE_collection[schema][::int(len(SE_collection[schema])/args.sample)]
    cdf_plot(SE_collection)
    print('done.')
