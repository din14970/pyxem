# -*- coding: utf-8 -*-
# Copyright 2018 The pyXem developers
#
# This file is part of pyXem.
#
# pyXem is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyXem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyXem.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import pytest
from pyxem.signals.diffraction_simulation import DiffractionSimulation
from pyxem.signals.diffraction_simulation import ProfileSimulation
from pyxem.generators.diffraction_generator import DiffractionGenerator
from pyxem import ElectronDiffraction
import pymatgen as pmg


@pytest.fixture
def coords_intensity_simulation():
    return DiffractionSimulation(coordinates = np.asarray([[0.3,1.2,0]]),
                                 intensities = np.ones(1))

@pytest.mark.xfail(raises=ValueError)
def test_wrong_calibration_setting():
    DiffractionSimulation(coordinates = np.asarray([[0.3,1.2,0]]),
                          intensities = np.ones(1),
                          calibration = [1,2,5])

@pytest.fixture
def get_signal():
    size  = 144
    sigma = 0.03
    max_r = 1.5
    return coords_intensity_simulation().as_signal(size,sigma,max_r)

def test_typing():
    assert type(get_signal()) is ElectronDiffraction

def test_correct_quadrant_np():
    A = get_signal().data
    assert (np.sum(A[:72,:72]) == 0)
    assert (np.sum(A[72:,:72]) == 0)
    assert (np.sum(A[:72,72:]) == 0)
    assert (np.sum(A[72:,72:])  > 0)

def test_correct_quadrant_hs():
    S = get_signal()
    assert (np.sum(S.isig[:72,:72].data) == 0)
    assert (np.sum(S.isig[72:,:72].data) == 0)
    assert (np.sum(S.isig[:72,72:].data) == 0)
    assert (np.sum(S.isig[72:,72:].data)  > 0)

# Test Profile Simulation

@pytest.fixture(params=[
    (300, 0.02, None),
])
def diffraction_calculator(request):
    return DiffractionGenerator(*request.param)

@pytest.fixture
def profile_simulation():
    return ProfileSimulation(magnitudes=[0.31891931643691351,
                                         0.52079306292509475,
                                         0.6106839974876449,
                                         0.73651261277849378,
                                         0.80259601243613932,
                                         0.9020400452156796,
                                         0.95675794931074043,
                                         1.0415861258501895,
                                         1.0893168446141808,
                                         1.1645286909108374,
                                         1.2074090451670043,
                                         1.2756772657476541],
                             intensities = np.array([100.,
                                                     99.34619104,
                                                     64.1846346,
                                                     18.57137199,
                                                     28.84307971,
                                                     41.31084268,
                                                     23.42104951,
                                                     13.996264,
                                                     24.87559364,
                                                     20.85636003,
                                                     9.46737774,
                                                     5.43222307]),
                             hkls = [{(1, 1, 1): 8},
                                     {(2, 2, 0): 12},
                                     {(3, 1, 1): 24},
                                     {(4, 0, 0): 6},
                                     {(3, 3, 1): 24},
                                     {(4, 2, 2): 24},
                                     {(3, 3, 3): 8, (5, 1, 1): 24},
                                     {(4, 4, 0): 12},
                                     {(5, 3, 1): 48},
                                     {(6, 2, 0): 24},
                                     {(5, 3, 3): 24},
                                     {(4, 4, 4): 8}])

def test_plot_profile_simulation(profile_simulation):
    profile_simulation.get_plot(g_max=1)
