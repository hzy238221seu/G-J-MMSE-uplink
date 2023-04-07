import numpy as np
from scipy.linalg import sqrtm


def get_z(Hhat, C, Epsilon, p, group_list, V_G_MMSE):
    if group_list[0] != 0:
        group_list.insert(0, 0)
    if group_list[-1] != Hhat.shape[0]:
        group_list.append(Hhat.shape[0])
    Z = np.zeros(((len(group_list)-1)*Hhat.shape[1], Hhat.shape[1]), dtype=Hhat.dtype)
    for i in range(len(group_list)-1):
        Y_plus = np.eye(group_list[i+1]-group_list[i])+p*C[group_list[i]:group_list[i+1], group_list[i]:group_list[i+1]]+p*Epsilon[group_list[i]:group_list[i+1], group_list[i]:group_list[i+1]]
        C_rd = np.zeros((Hhat.shape[0]-(group_list[i+1]-group_list[i]), Hhat.shape[0]-(group_list[i+1]-group_list[i])), dtype=Hhat.dtype)
        C_rd[:group_list[i], :group_list[i]] = C[:group_list[i], :group_list[i]]
        C_rd[group_list[i]:, group_list[i]:] = C[group_list[i+1]:, group_list[i+1]:]
        Epsilon_rd = np.zeros(C_rd.shape, dtype=C_rd.dtype)
        Epsilon_rd[:group_list[i], :group_list[i]] = Epsilon[:group_list[i], :group_list[i]]
        Epsilon_rd[:group_list[i], group_list[i]:] = Epsilon[:group_list[i], group_list[i+1]:]
        Epsilon_rd[group_list[i]:, group_list[i]:] = Epsilon[group_list[i+1]:, group_list[i+1]:]
        Epsilon_rd[group_list[i]:, :group_list[i]:] = Epsilon[group_list[i+1]:, :group_list[i]]
        Y_rd = np.eye(Hhat.shape[0]-(group_list[i+1]-group_list[i]))+p*C_rd+p*Epsilon_rd
        inverse_core1 = Y_rd
        V_G1 = V_G_MMSE[group_list[i]:group_list[i+1]]
        Hhat_rd = np.concatenate((Hhat[:group_list[i]], Hhat[group_list[i+1]:]), 0)
        for ka in range(Hhat.shape[1]):
            for kb in range(Hhat.shape[1]):
                inverse_core1 -= ((np.conjugate(V_G1[:, ka:ka+1]).T@Y_plus@V_G1[:, kb:kb+1])[0, 0]*Hhat_rd[:, ka:ka+1]@np.conjugate(Hhat_rd[:, kb:kb+1]).T)
        inverse_core1 = np.linalg.inv(inverse_core1)
        Yc = inverse_core1
        F1 = np.zeros((Hhat.shape[1], Hhat.shape[1]), dtype=Yc.dtype)
        for ka in range(Hhat.shape[1]):
            for kb in range(Hhat.shape[1]):
                F1[ka:ka+1] += ((np.conjugate(Hhat_rd[:, ka:ka+1]).T@Yc@Hhat_rd[:, kb:kb+1])[0,0]*np.conjugate(V_G1[:, kb:kb+1]).T@Hhat[group_list[i]:group_list[i+1]])
        complementary1 = p*F1
        complementary2 = p*np.conjugate(Hhat_rd).T@Yc@Hhat_rd
        Z[i*Hhat.shape[1]:(i+1)*Hhat.shape[1]] = complementary1 - complementary2 + np.eye(Hhat.shape[1])
    return Z


def get_lc_z(He, Re, p, V_G_MMSE, C, group_list):
    if group_list[0] != 0:
        group_list.insert(0, 0)
    if group_list[-1] != V_G_MMSE.shape[0]:
        group_list.append(V_G_MMSE.shape[0])
    Ce = np.zeros((He.shape[0], He.shape[0]), dtype=He.dtype)
    Eye = np.zeros((He.shape[0], He.shape[0]), dtype=He.dtype)
    for g in range(len(group_list)-1):
        Eye[g*He.shape[1]:(g+1)*He.shape[1], g*He.shape[1]:(g+1)*He.shape[1]] = np.conjugate(V_G_MMSE[group_list[g]:group_list[g+1]]).T@V_G_MMSE[group_list[g]:group_list[g+1]]
        Ce[g*He.shape[1]:(g+1)*He.shape[1], g*He.shape[1]:(g+1)*He.shape[1]] = np.conjugate(V_G_MMSE[group_list[g]:group_list[g+1]]).T@C[group_list[g]:group_list[g+1], group_list[g]:group_list[g+1]]@V_G_MMSE[group_list[g]:group_list[g+1]]
    return p*np.linalg.inv(p*(Re+Ce)+Eye)@He


def get_lc_z_approach(He, Re, p, V_G_MMSE, C, group_list):
    if group_list[0] != 0:
        group_list.insert(0, 0)
    if group_list[-1] != V_G_MMSE.shape[0]:
        group_list.append(V_G_MMSE.shape[0])
    Ce = np.zeros((He.shape[0], He.shape[0]), dtype=He.dtype)
    Eye = np.zeros((He.shape[0], He.shape[0]), dtype=He.dtype)
    for g in range(len(group_list)-1):
        Eye[g*He.shape[1]:(g+1)*He.shape[1], g*He.shape[1]:(g+1)*He.shape[1]] = np.conjugate(V_G_MMSE[group_list[g]:group_list[g+1]]).T@V_G_MMSE[group_list[g]:group_list[g+1]]
        Ce[g*He.shape[1]:(g+1)*He.shape[1], g*He.shape[1]:(g+1)*He.shape[1]] = np.conjugate(V_G_MMSE[group_list[g]:group_list[g+1]]).T@C[group_list[g]:group_list[g+1], group_list[g]:group_list[g+1]]@V_G_MMSE[group_list[g]:group_list[g+1]]
    return p*np.linalg.inv(p*(Re)+Eye)@He


def fuse(V_G_MMSE, Z, group_list):
    if group_list[0] != 0:
        group_list.insert(0, 0)
    if group_list[-1] != V_G_MMSE.shape[0]:
        group_list.append(V_G_MMSE.shape[0])
    K = Z.shape[1]
    for g in range(len(group_list)-1):
        V_G_MMSE[group_list[g]:group_list[g+1]] = V_G_MMSE[group_list[g]:group_list[g+1]]@Z[g*K:(g+1)*K]
    return V_G_MMSE
