#!/usr/bin/env python
# coding: utf-8
"""
StoneSoup Plugin
================
"""

# %%
# PyEHM includes implementations of `Stone Soup <https://stonesoup.readthedocs.io/en/v0.1b6/index.html>`_ compatible
# Joint Probabilistic Data Association (JPDA) `DataAssociator
# <https://stonesoup.readthedocs.io/en/v0.1b6/stonesoup.dataassociator.html>`_ classes. These are provided under the
# :class:`~.JPDAWithEHM` :class:`~.JPDAWithEHM2` classes, which implement the :class:`~.EHM` and :class:`~.EHM2`
# algorithms, respectively, and can be used as drop-in replacements to the
# :class:`stonesoup.dataassociator.probability.JPDA` data associator.
#
# In this example, we will showcase how the above classes can be utilised using PyEHM's published entry points to
# Stone Soup, and will compare their performance to :class:`stonesoup.dataassociator.probability.JPDA`. It should be
# noted that the code used below is a modified version of the Stone Soup
# `JPDA tutorial <https://stonesoup.readthedocs.io/en/v0.1b6/auto_tutorials/08_JPDATutorial.html>`_

# %%
# Simulate ground truth
# ---------------------
# We simulate three targets moving in the positive x, y cartesian plane (intersecting approximately half-way through
# their transition).

# We then add truth detections with clutter at each time-step.
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import uniform

from stonesoup.models.transition.linear import CombinedLinearGaussianTransitionModel, ConstantVelocity
from stonesoup.types.groundtruth import GroundTruthPath, GroundTruthState
from stonesoup.types.detection import TrueDetection
from stonesoup.types.detection import Clutter
from stonesoup.models.measurement.linear import LinearGaussian


np.random.seed(1991)

truths = set()

start_time = datetime.now()
transition_model = CombinedLinearGaussianTransitionModel([ConstantVelocity(0.005),
                                                          ConstantVelocity(0.005)])

truth = GroundTruthPath([GroundTruthState([0, 1, 0, 1], timestamp=start_time)])
for k in range(1, 21):
    truth.append(GroundTruthState(
        transition_model.function(truth[k-1], noise=True, time_interval=timedelta(seconds=1)),
        timestamp=start_time+timedelta(seconds=k)))
truths.add(truth)

truth = GroundTruthPath([GroundTruthState([0, 1, 20, -1], timestamp=start_time)])
for k in range(1, 21):
    truth.append(GroundTruthState(
        transition_model.function(truth[k-1], noise=True, time_interval=timedelta(seconds=1)),
        timestamp=start_time+timedelta(seconds=k)))
truths.add(truth)

truth = GroundTruthPath([GroundTruthState([10, 0, 0, 1], timestamp=start_time)])
for k in range(1, 21):
    truth.append(GroundTruthState(
        transition_model.function(truth[k-1], noise=True, time_interval=timedelta(seconds=1)),
        timestamp=start_time+timedelta(seconds=k)))
truths.add(truth)

# Generate measurements.
all_measurements = []

measurement_model = LinearGaussian(
    ndim_state=4,
    mapping=(0, 2),
    noise_covar=np.array([[0.75, 0],
                          [0, 0.75]])
    )

prob_detect = 0.9  # 90% chance of detection.

for k in range(20):
    measurement_set = set()

    for truth in truths:
        # Generate actual detection from the state with a 10% chance that no detection is received.
        if np.random.rand() <= prob_detect:
            measurement = measurement_model.function(truth[k], noise=True)
            measurement_set.add(TrueDetection(state_vector=measurement,
                                              groundtruth_path=truth,
                                              timestamp=truth[k].timestamp))

        # Generate clutter at this time-step
        truth_x = truth[k].state_vector[0]
        truth_y = truth[k].state_vector[2]
        for _ in range(np.random.randint(10)):
            x = uniform.rvs(truth_x - 10, 20)
            y = uniform.rvs(truth_y - 10, 20)
            measurement_set.add(Clutter(np.array([[x], [y]]), timestamp=truth[k].timestamp))
    all_measurements.append(measurement_set)


# %%
# Tracking components
# -------------------
# In order to compare the 3 data associators noted above, we will be constructing a set of 3 multi-target trackers,
# each of which will make use of a different data associator. Therefore, we now proceed to define the tracking
# components that will constitute the building blocks of the multi-target trackers.

# %%
# Predictor and Updater
# ~~~~~~~~~~~~~~~~~~~~~
# All 3 multi-target trackers will make use of the same pair of predictor and updater:


from stonesoup.predictor.kalman import KalmanPredictor
predictor = KalmanPredictor(transition_model)


from stonesoup.updater.kalman import KalmanUpdater
updater = KalmanUpdater(measurement_model)


# %%
# Hypothesiser
# ~~~~~~~~~~~~
# Similarly, the same hypothesiser will be used by all trackers:


from stonesoup.hypothesiser.probability import PDAHypothesiser
hypothesiser = PDAHypothesiser(predictor=predictor,
                               updater=updater,
                               clutter_spatial_density=0.125,
                               prob_detect=prob_detect)


# %%
# Metrics
# ~~~~~~~
# Below we define some metrics that will enable us to evaluate and compare the tracking performance of the various
# multi-target trackers. More specifically, we will be using the OSPA metric as our basis for comparison:

from stonesoup.metricgenerator.manager import SimpleManager
from stonesoup.metricgenerator.ospametric import OSPAMetric
from stonesoup.measures import Euclidean

ospa_generator = OSPAMetric(c=10, p=1, measure=Euclidean([0, 2]))

# Metric manager for standard JPDA tracker
metric_manager_jpda = SimpleManager([ospa_generator])

# Metric manager for JPDA with EHM tracker
metric_manager_jpda_ehm = SimpleManager([ospa_generator])

# Metric manager for JPDA with EHM2 tracker
metric_manager_jpda_ehm2 = SimpleManager([ospa_generator])


# %%
# Priors
# ~~~~~~
# We assume that the initial positions of the targets are known in advance. Hence, below we define the set of priors
# and initial tracks that will used by each of the trackers


from stonesoup.types.state import GaussianState
from stonesoup.types.track import Track

prior1 = GaussianState([[0], [1], [0], [1]], np.diag([1.5, 0.5, 1.5, 0.5]), timestamp=start_time)
prior2 = GaussianState([[0], [1], [20], [-1]], np.diag([1.5, 0.5, 1.5, 0.5]), timestamp=start_time)
prior3 = GaussianState([[10], [0], [0], [1]], np.diag([1.5, 0.5, 1.5, 0.5]), timestamp=start_time)
priors = {prior1, prior2, prior3}

# %%
# Data Associators
# ~~~~~~~~~~~~~~~~
# We now define the different data associators that we wish to compare:

# Standard JPDA
from stonesoup.dataassociator.probability import JPDA
jpda = JPDA(hypothesiser=hypothesiser)

# JPDA with EHM
from stonesoup.plugins.pyehm import JPDAWithEHM
jpda_ehm = JPDAWithEHM(hypothesiser=hypothesiser)

# JPDA with EHM2
from stonesoup.plugins.pyehm import JPDAWithEHM2
jpda_ehm2 = JPDAWithEHM2(hypothesiser=hypothesiser)



# %%
# Running the trackers
# --------------------
# Below we define a helper function that runs a given tracker configuration, based on the data associator that we wish
# use. This is essentially equivalent to the :class:`stonesoup.tracker.simple.MultiTargetMixtureTracker` recursion, but
# without the track initiation and deletion:


from stonesoup.types.array import StateVectors
from stonesoup.functions import gm_reduce_single
from stonesoup.types.update import GaussianStateUpdate


def run_tracker(data_associator, metric_manager):
    # Track priors
    tracks = {Track([prior]) for prior in priors}

    s = datetime.now()
    for n, measurements in enumerate(all_measurements):
        hypotheses = data_associator.associate(tracks,
                                               measurements,
                                               start_time + timedelta(seconds=n))

        # Loop through each track, performing the association step with weights adjusted according to
        # JPDA.
        for track in tracks:
            track_hypotheses = hypotheses[track]

            posterior_states = []
            posterior_state_weights = []
            for hypothesis in track_hypotheses:
                if not hypothesis:
                    posterior_states.append(hypothesis.prediction)
                else:
                    posterior_state = updater.update(hypothesis)
                    posterior_states.append(posterior_state)
                posterior_state_weights.append(hypothesis.probability)

            means = StateVectors([state.state_vector for state in posterior_states])
            covars = np.stack([state.covar for state in posterior_states], axis=2)
            weights = np.asarray(posterior_state_weights)

            # Reduce mixture of states to one posterior estimate Gaussian.
            post_mean, post_covar = gm_reduce_single(means, covars, weights)

            # Add a Gaussian state approximation to the track.
            track.append(GaussianStateUpdate(
                post_mean, post_covar,
                track_hypotheses,
                track_hypotheses[0].measurement.timestamp))

        metric_manager.add_data(
            truths, tracks, measurements,
            overwrite=False,  # Don't overwrite, instead add above as additional data
        )
    dt = datetime.now() - s
    return tracks, dt

# %%
# Standard JPDA tracker
# ~~~~~~~~~~~~~~~~~~~~~

tracks_jpda, diff_jpda = run_tracker(jpda, metric_manager_jpda)


# %%
# JPDA with EHM tracker
# ~~~~~~~~~~~~~~~~~~~~~

tracks_jpda_ehm, diff_jpda_ehm = run_tracker(jpda_ehm, metric_manager_jpda_ehm)


# %%
# JPDA with EHM2 tracker
# ~~~~~~~~~~~~~~~~~~~~~~

tracks_jpda_ehm2, diff_jpda_ehm2 = run_tracker(jpda_ehm2, metric_manager_jpda_ehm2)

# %%
# Plot the resulting tracks
# -------------------------
multi_fig = plt.figure(figsize=(10, 12))
ax1 = multi_fig.add_subplot(3, 1, 1)
ax1.set_xlabel("$x$")
ax1.set_ylabel("$y$")
ax1.set_ylim(-2, 25)
ax1.set_xlim(-2, 25)
ax1.set_title("Standard JPDA")

ax2 = multi_fig.add_subplot(3, 1, 2)
ax2.set_xlabel("$x$")
ax2.set_ylabel("$y$")
ax2.set_ylim(-2, 25)
ax2.set_xlim(-2, 25)
ax2.set_title("JPDA with EHM")

ax3 = multi_fig.add_subplot(3, 1, 3)
ax3.set_xlabel("$x$")
ax3.set_ylabel("$y$")
ax3.set_ylim(-2, 25)
ax3.set_xlim(-2, 25)
ax3.set_title("JPDA with EHM2")

axes = [ax1, ax2, ax3]

# Plot ground truth.
for truth in truths:
    for ax in axes:
        ax.plot([state.state_vector[0] for state in truth],
                 [state.state_vector[2] for state in truth],
                 linestyle="--",)

# Plot measurements.
for set_ in all_measurements:
    for ax in axes:
        # Plot actual detections.
        ax.scatter([state.state_vector[0] for state in set_ if isinstance(state, TrueDetection)],
                    [state.state_vector[1] for state in set_ if isinstance(state, TrueDetection)],
                    color='g')
        # Plot clutter.
        ax.scatter([state.state_vector[0] for state in set_ if isinstance(state, Clutter)],
                    [state.state_vector[1] for state in set_ if isinstance(state, Clutter)],
                    color='y',
                    marker='2')

tracks_all = [tracks_jpda, tracks_jpda_ehm, tracks_jpda_ehm2]

for ax, tracks in zip(axes, tracks_all):

    for track in tracks:
        # Plot track.
        ax.plot([state.state_vector[0, 0] for state in track[1:]],  # Skip plotting the prior
                 [state.state_vector[2, 0] for state in track[1:]],
                 marker=".")

    # Plot ellipses representing the gaussian estimate state at each update.
    from matplotlib.patches import Ellipse
    for track in tracks:
        for state in track[1:]:  # Skip the prior
            w, v = np.linalg.eig(measurement_model.matrix()@state.covar@measurement_model.matrix().T)
            max_ind = np.argmax(w)
            min_ind = np.argmin(w)
            orient = np.arctan2(v[1, max_ind], v[0, max_ind])
            ellipse = Ellipse(xy=state.state_vector[(0, 2), 0],
                              width=2*np.sqrt(w[max_ind]),
                              height=2*np.sqrt(w[min_ind]),
                              angle=np.rad2deg(orient),
                              alpha=0.2)
            ax.add_artist(ellipse)
multi_fig.tight_layout()

# %%
# Comparison
# ----------
#
# Tracking Performance
# ~~~~~~~~~~~~~~~~~~~~
#
# First, we will compare the tracking performance of the trackers in terms of the generated OSPA metrics. Below we
# proceed to plot the respective metric for each tracker:

# Metrics for standard JPDA
metrics_jpda = metric_manager_jpda.generate_metrics()
ospa_metric_jpda = {metric for metric in metrics_jpda if metric.title == "OSPA distances"}.pop()

# Metrics for JPDA with EHM
metrics_jpda_ehm = metric_manager_jpda_ehm.generate_metrics()
ospa_metric_jpda_ehm = {metric for metric in metrics_jpda_ehm if metric.title == "OSPA distances"}.pop()

# Metrics for JPDA with EHM
metrics_jpda_ehm2 = metric_manager_jpda_ehm2.generate_metrics()
ospa_metric_jpda_ehm2 = {metric for metric in metrics_jpda_ehm2 if metric.title == "OSPA distances"}.pop()

# Plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot([i.timestamp for i in ospa_metric_jpda.value], [i.value for i in ospa_metric_jpda.value], 'x-', label='Standard JPDA')
ax.plot([i.timestamp for i in ospa_metric_jpda_ehm.value], [i.value for i in ospa_metric_jpda_ehm.value], '*--', label='JPDA with EHM')
ax.plot([i.timestamp for i in ospa_metric_jpda_ehm2.value], [i.value for i in ospa_metric_jpda_ehm2.value], '+--', label='JPDA with EHM2')

ax.set_ylabel("OSPA distance")
ax.tick_params(labelbottom=False)
_ = ax.set_xlabel("Time")
ax.legend()

# %%
# As we can see, the calculated OSPA is identical for the 3 trackers. This is to be expected, since the
# joint association probabilities produced by the :class:`~.EHM` and :class:`~.EHM2` algorithms (used by the
# :class:`~.JPDAWithEHM` and :class:`~.JPDAWithEHM2` classes, respectively) should be identical to
# the standard JPDA (see :ref:`sphx_glr_auto_examples_ehm_vs_ehm2_vs_jpda.py` for more details).

# %%
# Computation times
# ~~~~~~~~~~~~~~~~~

y = ['Standard JPDA', 'JPDA with EHM', 'JPDA with EHM2']
y_pos = [i for i, _ in enumerate(y)]
x = [diff_jpda.total_seconds(), diff_jpda_ehm.total_seconds(), diff_jpda_ehm2.total_seconds()]

# Plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.barh(y_pos, x, tick_label=y)
for i, v in enumerate(x):
    if i == 0:
        ax.text(v - 3, i, str(np.around(v, 2)), color='white')
    else:
        ax.text(v + 1, i, str(np.around(v, 2)))
ax.set_ylabel('Tracker')
ax.set_xlabel('Time (s)')
fig.tight_layout()




