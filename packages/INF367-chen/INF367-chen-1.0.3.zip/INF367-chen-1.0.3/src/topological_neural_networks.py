import copy

import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

"""Implementation of different topological neural networks"""


class SelfOrganizingMap(object):
    """Self organizing maps"""

    def __init__(self, length: int = 7, width: int = 9, random_state: int = 0):
        self._length = length
        self._width = width
        # Use initial random weights on fixed random state
        self._random_generator = np.random.RandomState(random_state)
        # Have to wait with proper initialization
        self._self_organizing_map = nx.grid_2d_graph(self._length, self._width)
        self._learning_rate = None
        self._neighbour_learning_rate = None

    def get_som(self):
        """Getter for testing/validation"""
        return self._self_organizing_map

    def _find_bmu_for_point(self, sample):
        # Euclidean distance between the rows/points in the training date and the centroids
        dist = [np.square(sample - attributes["vector"]).sum(axis=1) for node, attributes in
                self._self_organizing_map.nodes(data=True)]
        dist_as_array = np.array(dist).reshape(self._length, self._width)
        # Getting coordinates of the best matching unit
        bmu_x, bmu_y = np.argwhere(dist_as_array == np.min(dist_as_array))[0]
        return bmu_x, bmu_y

    def fit(self, training_data=None, learning_rate=0.5, learning_rate_decay=0.0001, neighbour_learning_rate=0.95,
            number_of_epochs=1000):
        """Fit SOM on training data"""
        self._learning_rate = learning_rate
        self._neighbour_learning_rate = neighbour_learning_rate
        assert training_data is not None
        # Initialize the SOM around the mean of the training data
        random_indices_sample = self._random_generator.choice(range(training_data.shape[0]),
                                                              (self._length, self._width))
        init_data = training_data[random_indices_sample]
        for idx, (node, attributes) in enumerate(self._self_organizing_map.nodes(data=True)):
            attributes["vector"] = init_data[node]
        for epoch in range(number_of_epochs):
            print(f"Epoch {epoch} started...")
            # This shuffle fix was super for the performance of the SOM! We now do not always iterate in the same
            # way over the data points, which caused a bias in the direction of the last part of the training set
            self._random_generator.shuffle(training_data)
            for idx, sample in enumerate(training_data):
                bmu_x, bmu_y = self._find_bmu_for_point(training_data[idx].reshape(1, -1))
                # move the bmu
                self._self_organizing_map.nodes[(bmu_x, bmu_y)]["vector"] += self._learning_rate * (
                        sample - self._self_organizing_map.nodes[(bmu_x, bmu_y)]["vector"])
                # move the neighbours
                for neighbour_node in self._self_organizing_map.neighbors((bmu_x, bmu_y)):
                    self._self_organizing_map.nodes[neighbour_node][
                        "vector"] += np.multiply(np.multiply(self._learning_rate, self._neighbour_learning_rate), (
                            sample - self._self_organizing_map.nodes[neighbour_node]["vector"]))
                    # Update rates
            self._learning_rate = self._learning_rate * np.exp(-epoch * learning_rate_decay)
            print(f"{self._learning_rate=}")
        print('Fitting finished\n')

    def transform(self, testing_data):
        """Compute euclidean distance from new points and centers, give out label!"""
        test_labels = []
        for point in testing_data:
            bmu_x, bmu_y = self._find_bmu_for_point(point)
            test_labels.append(np.array(bmu_x, bmu_y))
        return test_labels


class NeuralGas(object):
    """Growing Neural Gas"""

    def __init__(self):
        pass

    def fit(self, training_data, k, number_of_epochs, epsilon_start, epsilon_end,
            lambda_start, lambda_end, rand_seed):
        # we retrieve the sample size and the dimension/features
        n_samples, n_features = np.shape(training_data)
        # Set seed in the beginning (I think that is the same as when I fix the RandomState)
        np.random.seed(rand_seed)
        # randomly initialize codebook_vectors
        codebook_vectors = np.array(4 * np.random.rand(k, n_features) - 2)

        # with yield we can return values without stopping the functions workflow, here we return the initialisation
        yield copy.deepcopy(codebook_vectors)
        for epoch in range(number_of_epochs):

            # This kind of slowing down the learning rate is much more elegant, since we can stop at a certain value
            learning_rate = epsilon_start * (epsilon_end / epsilon_start) ** (epoch / number_of_epochs)
            neighborhood_radius = lambda_start * (lambda_end / lambda_start) ** (epoch / number_of_epochs)

            print('Starting epoch t={} [learning rate={:.3f}, neighborhood radius = {:.3f}]...'.format(epoch,
                                                                                                       learning_rate,
                                                                                                       neighborhood_radius))

            # Either permutation or shuffle
            indexes = np.random.permutation(n_samples)

            # iterate through all indexes in the index array
            for index in indexes:
                sample = training_data[index]

                # Neural Gas learning rule is soft-competition, meaning that closer points will be moved more, but not
                # just the winner
                list_closest = np.argsort(np.linalg.norm(codebook_vectors - sample, axis=1))
                for rank, closest in enumerate(list_closest, 0):
                    # This one was tricky, I had to transpose the sample
                    # to match the dimensions (we multiply point-wise)
                    codebook_vectors[closest] += learning_rate * np.exp(-rank / neighborhood_radius) * (
                            np.transpose(sample) - codebook_vectors[closest])

            # Convenience return for testing
            yield copy.deepcopy(codebook_vectors)

        print('Fitting finished\n')

    def transform(self):
        raise NotImplementedError


class GrowingNeuralGas(object):
    """Growing Neural Gas"""

    def __init__(self):
        self.node_number = 0
        self._graph = nx.Graph()
        np.random.seed(0)
        self.training_data = None

    def get_graph(self):
        return self._graph

    def get_next_node_number(self):
        self.node_number += 1
        return self.node_number - 1

    def fit(self, training_data, learning_rate_alpha=0.1, number_of_epochs: int = 25,
            number_of_steps_before_node_insertion=100, error_decay_beta=0.1, error_decay_gamma=0.1,
            age_threshold=50):
        self.training_data = training_data
        # Get the number of samples and their dimension
        n_samples, n_features = np.shape(self.training_data)
        # Add the two initial nodes
        w_one = 5 * np.random.rand(1, n_features) - 2.5
        w_two = 5 * np.random.rand(1, n_features) - 2.5
        # Initialize GNG with two connected nodes (edge age 0) with random weight vectors and errors 0
        self._graph.add_node(self.get_next_node_number(), vector=w_one, error=0)
        self._graph.add_node(self.get_next_node_number(), vector=w_two, error=0)
        # Adding initial edge
        # 0. epoch
        yield copy.deepcopy(self._graph)
        for epoch in range(number_of_epochs):
            print(f"Begin epoch {epoch}/{number_of_epochs}")
            # Either permutation or shuffle
            indexes = np.random.permutation(n_samples)
            running_steps = 0
            # iterate through all indexes in the index array
            for index in indexes:
                sample = training_data[index]
                # find two nearest vectors
                vec_1, vec_2 = self.find_the_two_closest_weight_vectors(sample)
                # add error, note that the Error in the pseudocode of the paper is SQUARED!
                self._graph.nodes[vec_1]['error'] += np.linalg.norm(sample - self._graph.nodes[vec_1]['vector']) ** 2
                # Update weights of vec_1 and vec_2, following the lecture slides, not the paper!!!
                # print(self._graph.nodes[vec_1]['vector'])
                self._graph.nodes[vec_1]['vector'] = np.add(self._graph.nodes[vec_1]['vector'],
                                                            learning_rate_alpha * np.subtract(sample,
                                                                                              self._graph.nodes[vec_1][
                                                                                                  'vector']))
                self._graph.nodes[vec_2]['vector'] = np.add(self._graph.nodes[vec_2]['vector'],
                                                            learning_rate_alpha * np.subtract(sample,
                                                                                              self._graph.nodes[
                                                                                                  vec_2]['vector']))
                # print(movement_vec_1)
                # print(self._graph.nodes[vec_1]['vector'])
                # Increment age from all neighbour-edges of vec_1,
                # nbunch as argument allows filtering by the node in the graph (can be empty!)
                for node_1, neighbour_of_node_1, attributes in self._graph.edges(data=True, nbunch=[vec_1]):
                    # In the 0. epoch, we will not get here, since the graph has no edges yet
                    # add_edge is idempotent and will just overwrite the existing edge (updating)
                    self._graph.add_edge(node_1, neighbour_of_node_1, age=attributes['age'] + 1)
                # add edge between vec_1 and vec_2, set age to 0
                self._graph.add_edge(vec_1, vec_2, age=0)
                # delete nodes without edges, and edges that are too old
                self.kill_old_edges(age_threshold)
                self.kill_single_nodes()
                # Every m steps
                running_steps += 1
                if running_steps % number_of_steps_before_node_insertion == 0:
                    # Find node with largest error
                    biggest_error_node, max_error = 0, 0
                    for node, attributes in self._graph.nodes(data=True):
                        if attributes["error"] > max_error:
                            biggest_error_node = node
                            max_error = attributes["error"]
                    # Getting the neighbour with the highest error
                    neighbour_error_dict = {}
                    for neighbour in self._graph.neighbors(biggest_error_node):
                        neighbour_error_dict[neighbour] = (self._graph.nodes[neighbour]['error'])
                    # Get the neighbour with the biggest error
                    (biggest_error_neighbour_node, biggest_error_neighbour_error) = \
                        list(sorted(neighbour_error_dict.items(), key=lambda x: x[1], reverse=True))[0]  # type: ignore
                    # Update error of the two vectors
                    self._graph.nodes[biggest_error_node]['error'] *= error_decay_beta
                    self._graph.nodes[biggest_error_neighbour_node]['error'] *= error_decay_beta
                    # Delete edge between them
                    self._graph.remove_edge(biggest_error_node, biggest_error_neighbour_node)
                    # Add new node
                    new_node = (self._graph.nodes[biggest_error_node]["vector"] +
                                self._graph.nodes[biggest_error_neighbour_node]["vector"]) * 0.5
                    new_node_number = self.get_next_node_number()
                    self._graph.add_node(new_node_number,
                                         vector=new_node,
                                         error=self._graph.nodes[biggest_error_node]['error'])
                    # Add edges
                    self._graph.add_edge(new_node_number, biggest_error_node, age=0)
                    self._graph.add_edge(new_node_number, biggest_error_neighbour_node, age=0)

                for node, attributes in self._graph.nodes(data=True):
                    attributes["error"] = attributes["error"] * error_decay_gamma
                yield copy.deepcopy(self._graph)
                # Limiting the number of nodes???
                # if len(self._graph.nodes) > training_data.shape[0] * 0.25:
                #     return
        print('Fitting finished\n')

    def transform(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def find_the_two_closest_weight_vectors(self, sample):
        # Get a ranking of which weight vectors are closest.
        all_graph_weight_vectors = {node_number: attributes['vector'].flatten() for node_number, attributes in
                                    self._graph.nodes(data=True)}
        distances = {k: np.linalg.norm(v - sample) for k, v in all_graph_weight_vectors.items()}
        list_closest = list(sorted(distances.items(), key=lambda x: x[1]))[:2]  # type: ignore

        # return the nearest and second closest point as dict
        return list_closest[0][0], list_closest[1][0]

    def kill_single_nodes(self):
        to_be_deleted = []
        for node in self._graph.nodes:
            if self._graph.degree(node) == 0:
                to_be_deleted.append(node)
        for node in to_be_deleted:
            self._graph.remove_node(node)

    def kill_old_edges(self, age_threshold):
        to_be_deleted = []
        for node_1, neighbour_of_node_1, attributes in self._graph.edges(data=True):
            if attributes['age'] > age_threshold:
                to_be_deleted.append((node_1, neighbour_of_node_1))
        for node, other_node in to_be_deleted:
            self._graph.remove_edge(node, other_node)


class GenerativeGaussianGraphs(object):
    """Generative Gaussian Graphs"""

    def __init__(self):
        raise NotImplementedError

    def fit(self, number_of_components_k=4, pruning_threshold_epsilon=0.01):
        # Step 1: Random initialization
        # Step 2: Standard GMM with k centers
        # Step 2: Delaunay graph
        # Step 2: Standard GMM with k centers
        # Step 2: Standard GMM with k centers
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError


def draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test, traces_offset=0):
    training_and_test_traces = [
        [moon_train_coord, label_train, '0', 'Train', 'square', 'blue'],
        [moon_train_coord, label_train, '1', 'Train', 'circle', 'red'],
        [moon_test_coord, label_test, '0', 'Test', 'square-dot', 'blue'],
        [moon_test_coord, label_test, '1', 'Test', 'circle-dot', 'red'],
    ]

    # Plotly has the nice ability to just "add" traces to an existing plot which
    # we have defined as training_and_test_traces
    for _moon_coord, _moon_label, _iterating_label, _split, _marker, _color in training_and_test_traces:
        fig.add_trace(
            go.Scatter(
                x=_moon_coord[_moon_label == _iterating_label, 0],
                y=_moon_coord[_moon_label == _iterating_label, 1],
                name=f'{_split} Split, Label {_iterating_label}',
                mode='markers', marker=dict(symbol=_marker, color=_color, opacity=0.5)
            ))
    fig.update_traces(
        marker_size=11, marker_line_width=1.2,
    )


def visualize_self_organizing_maps():
    som = SelfOrganizingMap()
    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    som.fit(moon_train_coord)

    edge_x = []
    edge_y = []
    for edge in som.get_som().edges():
        x0, y0 = som.get_som().nodes[edge[0]]['vector'].flatten().tolist()
        x1, y1 = som.get_som().nodes[edge[1]]['vector'].flatten().tolist()
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for node in som.get_som().nodes():
        x, y = som.get_som().nodes[node]['vector'].flatten().tolist()
        node_x.append(x)
        node_y.append(y)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        name="Edges",
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name="Nodes",
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(som.get_som().adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='SOM on the two moons',
                        titlefont_size=16,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Author: I-Hao Chen",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01)
                    ))
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.show()
    fig.write_image("som_final.png")


def visualize_neural_gas():
    # hyperparameters for neural gas
    k = 25
    number_of_epochs = 50
    epsilon_start = 1
    epsilon_end = 0.001
    lambda_start = 15
    lambda_end = 0.001

    # seed
    rand_seed = 0

    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    ng = NeuralGas()
    results = np.array(list(ng.fit(moon_train_coord, k, number_of_epochs, epsilon_start, epsilon_end,
                                   lambda_start, lambda_end, rand_seed)))
    # We want to visualize the algorithm with an animation, so we need pandas and DataFrames to do so
    col_names = ['epoch', 'cluster_label', 'coordinates']
    # Creates our index for MultiIndex later
    index = pd.MultiIndex.from_product([range(s) for s in results.shape], names=col_names)
    # Creates a series with all the values and holding on to the correct epoch via the Multiindex
    df = pd.DataFrame({'results_list': results.flatten()}, index=index)['results_list']
    df = df.unstack(level='coordinates').swaplevel().sort_index()
    df.columns = ['x', 'y']
    df.index.names = ['cluster_label', 'epoch']
    df = df.reset_index()
    fig = px.scatter(df, x="x", y="y", animation_frame="epoch", animation_group="cluster_label",
                     color="cluster_label", hover_name="cluster_label", range_x=[-2.5, 2.5], range_y=[-2.5, 2.5],
                     title="Neural Gas on the two moons")
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    fig.show()


def visualize_growing_neural_gas():
    moon_coord, moon_label = make_moons(n_samples=250, noise=0.02, random_state=0)
    # Load and split data with a method from scikit-learn
    moon_train_coord, moon_test_coord, label_train, label_test = train_test_split(
        moon_coord, moon_label.astype(str), test_size=0.25, random_state=0)
    gng = GrowingNeuralGas()
    results = list(gng.fit(moon_train_coord))
    print(f"{len(results)} steps in total trained!")
    edge_x = []
    edge_y = []
    for edge in gng.get_graph().edges():
        x0, y0 = gng.get_graph().nodes[edge[0]]['vector'].flatten().tolist()
        x1, y1 = gng.get_graph().nodes[edge[1]]['vector'].flatten().tolist()
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for node in gng.get_graph().nodes():
        x, y = gng.get_graph().nodes[node]['vector'].flatten().tolist()
        node_x.append(x)
        node_y.append(y)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name="Edges")
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name="Nodes",
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(gng.get_graph().adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='GNG on the two moons',
                        titlefont_size=16,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Author: I-Hao Chen",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01)
                    ))
    draw_moons(fig, moon_train_coord, moon_test_coord, label_train, label_test)
    fig.show()
    fig.write_image("gng_final.png")


if __name__ == "__main__":
    visualize_self_organizing_maps()
