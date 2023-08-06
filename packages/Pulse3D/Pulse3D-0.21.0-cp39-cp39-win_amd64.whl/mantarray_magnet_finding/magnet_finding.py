# -*- coding: utf-8 -*-
"""More accurate estimation of magnet positions."""
from typing import Any
from typing import Dict

from labware_domain_models import LabwareDefinition
from nptyping import NDArray
from numba import njit
import numpy as np
from scipy.optimize import least_squares

# Kevin (12/1/21): Sensor locations relative to origin
SENSOR_DISTANCES_FROM_CENTER_POINT = np.asarray([[-2.25, 2.25, 0], [2.25, 2.25, 0], [0, -2.25, 0]])

ADJACENT_WELL_DISTANCE_MM = 19.5
WELL_VERTICAL_SPACING = np.asarray([0, -ADJACENT_WELL_DISTANCE_MM, 0])
WELL_HORIZONTAL_SPACING = np.asarray([ADJACENT_WELL_DISTANCE_MM, 0, 0])
WELLS_PER_COL = 4

# Kevin (12/1/21): Used for calculating magnet's dipole moment
MAGNET_VOLUME = np.pi * (0.75 / 2.0) ** 2
# Kevin (12/1/21): This is part of the dipole model
DIPOLE_MODEL_FACTOR = 4 * np.pi

NUM_PARAMS = 6

TWENTY_FOUR_WELL_PLATE = LabwareDefinition(row_count=4, column_count=6)

TISSUE_SENSOR_READINGS = "tissue_sensor_readings"


@njit(fastmath=True)  # type: ignore
def objective_function_ls(
    pos: NDArray[(1, Any), float],
    b_meas: NDArray[(1, Any), float],
    manta: NDArray[(72, 3), float],
    num_active_wells: int,
) -> NDArray[
    (Any,), float
]:  # pragma: no cover  # Tanner (1/9/22): codecov cannot cover functions compiled with numba
    xpos, ypos, zpos, theta, phi, remn = pos.reshape(NUM_PARAMS, num_active_wells)

    fields = np.zeros((len(manta), 3))

    for magnet in range(0, num_active_wells):
        st = np.sin(theta[magnet])
        sph = np.sin(phi[magnet])
        ct = np.cos(theta[magnet])
        cph = np.cos(phi[magnet])
        m = MAGNET_VOLUME * remn[magnet] * np.array([[st * cph], [st * sph], [ct]])  # moment vectors

        r = -np.asarray([xpos[magnet], ypos[magnet], zpos[magnet]]) + manta  # radii to moment
        rAbs = np.sqrt(np.sum(r ** 2, axis=1))

        # simulate fields at sensors using dipole model for each magnet
        fields_from_magnet = (
            np.transpose(3 * r * np.dot(r, m)) / rAbs ** 5 - m / rAbs ** 3
        ) / DIPOLE_MODEL_FACTOR

        fields += np.transpose(fields_from_magnet)

    return fields.reshape((1, 3 * r.shape[0]))[0] - b_meas


def get_positions(data: NDArray[(24, 3, 3, Any), float]) -> Dict[str, NDArray[(1, Any), float]]:
    """Run least squares optimizer on instrument data to get magnet positions.

    Initial guess is set to be TODO

    Assumes 3 active sensors for each well, that all active wells have magnets, and that all magnets have the well beneath them active

    Args:
        data: an array indexed as [well, sensor, axis, timepoint]. Data
            should be the difference of the data with plate on the instrument
            and empty plate calibration data.
    """
    # Tanner (12/3/21): hardcoding these for now. Could be made constants if appropriate
    num_sensors = 3
    num_axes = 3

    # Tanner (12/2/21): Every well/sensor/axis will always be active as of now
    num_active_wells = 24
    active_wells = list(range(num_active_wells))

    # Kevin (12/1/21): Manta gives the locations of all active sensors on all arrays with respect to a common point
    # computing the locations of each centrally located point about which each array is to be distributed,
    # for the purpose of offsetting the values in triad by the correct well spacing
    # The values in "triad" and "manta" relate to layout of the board itself so they don't change at all so long as the board doesn't
    triad = SENSOR_DISTANCES_FROM_CENTER_POINT.copy()
    manta = np.empty((triad.shape[0] * num_active_wells, triad.shape[1]))
    for well_idx in range(0, num_active_wells):
        well_slice = slice(well_idx * triad.shape[0], (well_idx + 1) * triad.shape[0])
        manta[well_slice, :] = (
            triad
            + well_idx % WELLS_PER_COL * WELL_VERTICAL_SPACING
            + (well_idx // WELLS_PER_COL) * WELL_HORIZONTAL_SPACING
        )

    # Kevin (12/1/21): Initial guess is dependent on where the plate sits relative to the sensors
    initial_guess_values = {"X": 0, "Y": 1, "Z": -5, "THETA": 90 / 360 * 2 * np.pi, "PHI": 0, "REMN": -575}
    # Kevin (12/1/21): Each magnet has its own positional coordinates and other characteristics depending on where it's located in the consumable. Every magnet
    # position is referenced with respect to the center of the array beneath well A1, so the positions need to be adjusted to account for that, e.g. the magnet in
    # A2 has the x/y coordinate (19.5, 0), so guess is processed in the below loop to produce that value. prev_guess contains the guesses for each magnet at each position
    prev_guess = [
        initial_guess_values["X"] + ADJACENT_WELL_DISTANCE_MM * (well_idx // WELLS_PER_COL)
        for well_idx in active_wells
    ]
    prev_guess.extend(
        [
            initial_guess_values["Y"] - ADJACENT_WELL_DISTANCE_MM * (well_idx % WELLS_PER_COL)
            for well_idx in active_wells
        ]
    )
    for param in list(initial_guess_values.keys())[2:]:
        prev_guess.extend([initial_guess_values[param]] * num_active_wells)

    params = tuple(initial_guess_values.keys())
    estimations = {param: np.empty((data.shape[-1], num_active_wells)) for param in params}

    b_meas = np.empty(num_active_wells * 9)

    # Tanner (12/8/21): should probably add some sort of logging eventually

    # Kevin (12/1/21): Run the algorithm on each time index. The algorithm uses its previous outputs as its initial guess for all datapoints but the first one
    for data_idx in range(0, data.shape[-1]):
        # Kevin (12/1/21): This sorts the data from processData into something that the algorithm can operate on; it shouldn't be necessary if you combine this method and processData
        for mi_idx, well_idx in enumerate(active_wells):
            # Kevin (12/1/21): rearrange sensor readings as a 1d vector
            b_meas[mi_idx * 9 : (mi_idx + 1) * 9] = data[well_idx, :, :, data_idx].reshape(
                (1, num_sensors * num_axes)
            )

        res = least_squares(
            objective_function_ls,
            prev_guess,
            args=(b_meas, manta, num_active_wells),
            method="trf",
            ftol=1e-2,
            verbose=0,
        )

        # Tanner (12/2/21): set the start of all subsequent loops as the estimation from the first loop
        if data_idx == 0:
            prev_guess = np.asarray(res.x)  # type: ignore

        outputs = np.asarray(res.x).reshape(NUM_PARAMS, num_active_wells)
        for i, param in enumerate(params):
            estimations[param][data_idx, :] = outputs[i]

    # Kevin (12/1/21): I've gotten some strange results from downsampling; I'm not sure why that is necessarily, could be aliasing,
    # could be that the guesses for successive runs need to be really close together to get good accuracy.
    # For large files, you may be able to use the 1D approximation after running the algorithm once or twice "priming"
    return estimations
