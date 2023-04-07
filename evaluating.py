import numpy as np
import matplotlib.pyplot as plt


def get_se(H, V, C, p, group_list=None):
    if group_list is None:
        Combined = p*(np.abs(np.conjugate(V.T)@H)**2)
        Signal = np.eye(Combined.shape[-1]) * Combined
        IS = np.sum(Combined - Signal, -1)
        Signal = np.sum(Signal, -1)
        C_plus = p*C + np.eye(C.shape[0])
        IN = np.sum((np.conjugate(V.T)@C_plus@V) * np.eye(V.shape[1]), -1)
    else:
        Signal = np.zeros((H.shape[1],), dtype=H.dtype)
        IS = np.copy(Signal)
        IN = np.copy(Signal)
        if group_list[0] != 0:
            group_list.insert(0, 0)
        if group_list[-1] != len(H):
            group_list.append(len(H))
        for g in range(len(group_list)-1):
            Hg = H[group_list[g]:group_list[g+1]]
            Vg = V[group_list[g]:group_list[g+1]]
            Cg = C[group_list[g]:group_list[g+1], group_list[g]:group_list[g+1]]
            Combinedg = p*(np.abs(np.conjugate(Vg.T)@Hg)**2)
            Signalg = np.eye(Combinedg.shape[-1]) * Combinedg
            ISg = np.sum(Combinedg - Signalg, -1)
            Signalg = np.sum(Signalg, -1)
            C_plusg = p*Cg + np.eye(Cg.shape[0])
            INg = np.sum((np.conjugate(Vg.T)@C_plusg@Vg) * np.eye(Vg.shape[1]), -1)
            Signal += Signalg
            IS += ISg
            IN += INg
    return np.log2(1+Signal / (IS + IN + 1e-5)).real 


def get_he(H, V, slice_list=None):
    if slice_list is None:
        return np.conjugate(V.T)@H
    if slice_list[0] != 0:
        slice_list.insert(0, 0)
    if slice_list[-1] != H.shape[0]:
        slice_list.append(H.shape[0])
    return np.concatenate([np.conjugate(V.T[:, slice_list[i]:slice_list[i+1]])@H[slice_list[i]:slice_list[i+1]] for i in range(len(slice_list)-1)], 0)


def cdf_plot(se_collection):
    marker = ['D', '+', 'o', '^', '|', '*', 'h']
    for i, schema in enumerate(se_collection):
        plt.plot(se_collection[schema], np.linspace(0, 1, len(se_collection[schema])), marker[i%len(marker)], label=schema)
    plt.grid()
    plt.legend()
    plt.xlabel('SE (bit/s/Hz)')
    plt.ylabel('CDF')
    plt.show()
