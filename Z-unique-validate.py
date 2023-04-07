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
parser.add_argument('-s', '--data-source', type=str, default='data/L100N4K40p100-hete')
parser.add_argument('-n', '--running-number', type=int, default=10)
parser.add_argument('-w', '--workers', type=int, default=5)
# parser.add_argument('--schema', action='append', type=str, default=['2uniform-lc', '2uniform-ips']) # 3.522809857823992e-10
# parser.add_argument('--schema', action='append', type=str, default=['4uniform-lc', '4uniform-ips']) # 3.979573463807364e-10
parser.add_argument('--schema', action='append', type=str, default=['2uniform-lc', '2uniform-ips']) # 3.1452873173148075e-10
parser.add_argument('--sample', type=int, default=50)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.sample > args.user_num * args.running_number:
        args.sample = args.user_num * args.running_number
    p = args.power
    with open('schema.json') as f:
        schemas = json.load(f)
    mse = []
    channels = Channels(args.data_source, args.workers)
    for running_idx in range(args.running_number):
        H, Hhat, C, Epsilon = channels.next()
        print('running {}-th instance...'.format(running_idx))
        for schema in args.schema:
            print('schema {}...'.format(schema))
            group_list = schemas[schema]['group-list']
            V_G_MMSE = G_MMSE(Hhat, C, Epsilon, p, group_list)
            if 'fusing' in schemas[schema]:
                if schemas[schema]['fusing'] == 'LC':
                    He = get_he(Hhat, V_G_MMSE, group_list)
                    Re = get_epsilon(He)
                    Z_LC = get_lc_z(He, Re, p, V_G_MMSE, C, group_list)
                elif schemas[schema]['fusing'] == 'IPS':
                    Z_IPS = get_z(Hhat, C, Epsilon, p, group_list, V_G_MMSE)
        mse.append(np.sum(np.abs(Z_LC-Z_IPS))/np.sum(np.abs(Z_IPS)))
    print(np.mean(mse))
    print('done.')
