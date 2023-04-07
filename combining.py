import numpy as np


def J_MMSE(Hhat, C, Epsilon, p):
    inv = np.linalg.inv(np.eye(Epsilon.shape[0])+p*C+p*Epsilon)
    return p*inv@Hhat


def G_MMSE(Hhat_full, C_full, Epsilon_full, p, group_list):
    if group_list[0] != 0:
        group_list.insert(0, 0)
    if group_list[-1] != Hhat_full.shape[0]:
        group_list.append(Hhat_full.shape[0])
    combining = np.zeros(Hhat_full.shape, dtype=Hhat_full.dtype)
    for i in range(len(group_list)-1):
        Hhat = Hhat_full[group_list[i]:group_list[i+1]]
        C = C_full[group_list[i]:group_list[i+1], group_list[i]:group_list[i+1]]
        Epsilon = Epsilon_full[group_list[i]:group_list[i+1], group_list[i]:group_list[i+1]]
        combining[group_list[i]:group_list[i+1], :] = J_MMSE(Hhat, C, Epsilon, p)
    return combining


def get_epsilon(Hhat):
    if len(Hhat.shape) == 2:
        return Hhat@np.conjugate(np.transpose(Hhat))
    return Hhat@np.conjugate(np.transpose(Hhat, (0, 2, 1)))
