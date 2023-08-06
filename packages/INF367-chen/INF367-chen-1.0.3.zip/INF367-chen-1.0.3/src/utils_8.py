import numpy as np
from IPython.display import HTML
from matplotlib import animation
from matplotlib import pyplot as plt
from numpy import zeros
from sklearn.metrics.pairwise import euclidean_distances


def load_data(filepath):
    with np.load(filepath) as f:
        print(f.keys)
        samples = f['samples']
        return (samples)


def plot_codebook(samples, codebook_vectors, k, *args):
    # function plotCodebook(samples, codebook_vectors)
    # function plotCodebook(samples, codebook_vectors, x)
    #
    # plots datasets points X colored according to codebook affiliation
    #
    # input parameters:
    # samples:  datasets points (n_samples x n_features-matrix)
    # codebook_vectors:  codebook (k x n_features-matrix)
    #
    # optional:
    # x:  single datasets point to highlight
    #

    if len(args) == 0:
        x = []
    else:
        x = args[0]
        assert len(x) == 2, 'the point to be highlighted needs to be a 2, vector'

    # get datasets dimesionality
    n_features = samples.shape[1]
    assert n_features == 2

    # get codebook_vector for every sample
    if k == 1:
        codebook_vector_num = zeros(len(samples))
    else:
        dist = euclidean_distances(samples, codebook_vectors)
        codebook_vector_num = np.argmin(dist, 1)

    cmap = plt.get_cmap('tab20')

    # plot all samples belonging to one codebook_vector with one color
    for index in range(k):
        plt.plot(samples[codebook_vector_num == index, 0],
                 samples[codebook_vector_num == index, 1],
                 marker='o', linestyle='', color=cmap(index))

    # plot codebook_vectors
    plt.plot(codebook_vectors[:, 0], codebook_vectors[:, 1], 'o', markerfacecolor='g', markeredgecolor='k')

    # plot single datasets point
    if len(args) == 0:
        x = []
    else:
        x = args[0]
        assert len(x) == 2, 'the point to be highlighted needs to be a 2, vector'
        plt.plot(x[0], x[1], 'o', markerfacecolor='r', markeredgecolor='k')

    plt.axis('scaled')


class Animation:
    def __init__(self, samples, k):
        self.samples = samples
        # self.codebook_vectors = codebook_vectors
        self.k = k
        self.fig, self.ax = plt.subplots()
        plt.close()

    def init_func(self):
        # self.ax.xlim((-7, 7))
        # self.ax.ylim((-7, 7))
        self.ax.set_xlim([-9, 9])
        self.ax.set_ylim([-9, 9])
        # self.ax.axis('scaled')
        self.plot_liste = []
        cmap = plt.get_cmap('tab20')
        for index in range(self.k):
            plot_cluster, = self.ax.plot([], [], marker='*', linestyle='', color=cmap(index))
            self.plot_liste.append(plot_cluster)

        self.plot_codebooks, = self.ax.plot([], [], 'o', markerfacecolor='g', markeredgecolor='k')
        self.plot_sample, = self.ax.plot([], [], 'o', markerfacecolor='r', markeredgecolor='k')
        #
        return (self.plot_liste, self.plot_codebooks,)

    def func(self, t):
        codebook_vectors, sample = t

        if not len(sample) == 0:
            self.plot_sample.set_data(sample[0], sample[1], )

        if self.k == 1:
            codebook_vector_num = zeros(len(self.samples))
        else:
            dist = euclidean_distances(self.samples, codebook_vectors)
            codebook_vector_num = np.argmin(dist, 1)

        for index in range(self.k):
            self.plot_liste[index].set_data(self.samples[codebook_vector_num == index, 0],
                                            self.samples[codebook_vector_num == index, 1], )

        self.plot_codebooks.set_data(codebook_vectors[:, 0], codebook_vectors[:, 1], )
        #
        return (self.plot_liste, self.plot_codebooks,)

    def play(self, frames):
        anim = animation.FuncAnimation(self.fig,
                                       func=self.func,
                                       frames=frames,
                                       init_func=self.init_func,
                                       blit=False)
        return HTML(anim.to_jshtml(default_mode='once'))
