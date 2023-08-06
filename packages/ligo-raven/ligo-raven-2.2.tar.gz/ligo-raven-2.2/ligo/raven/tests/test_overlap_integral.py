from unittest.mock import call, patch
import unittest.mock as mock
import pytest
from math import isclose

import os
import sys
import healpy as hp
import numpy as np
from numpy import deg2rad as rads
import pytest
from scipy import integrate

from ligo.skymap import io, distance
from astropy.coordinates import ICRS, SkyCoord
from astropy import units as u
from astropy_healpix import HEALPix, nside_to_level, pixel_resolution_to_nside

from ligo.raven.search import skymap_overlap_integral


### Functions to create/combine sky maps ###
############################################


def from_cone(ra, dec, error):
    """ Create a gaussian sky map centered on the given ra, dec
    with width determined by 1-sigma error radius. """ 
    center = SkyCoord(ra * u.deg, dec * u.deg)
    radius = error * u.deg

    # Determine resolution such that there are at least
    # 4 pixels across the error radius.
    hpx = HEALPix(pixel_resolution_to_nside(radius / 4, round='up'),
                  'ring', frame=ICRS())
    nside = hpx.nside
    npix2 = hp.nside2npix(nside)
    ipix = np.arange(npix2)

    # Evaluate Gaussian.
    distance = hpx.healpix_to_skycoord(ipix).separation(center)
    probdensity = np.exp(-0.5 * np.square(distance / radius).to_value(
        u.dimensionless_unscaled))
    probdensity /= probdensity.sum() * hpx.pixel_area.to_value(u.steradian)
    
    return probdensity, nside

    
def make_skymap(nside, skymap_type, hemi=(1,0,0), ra=0, dec=0, error=10):
    
    npix2 = hp.nside2npix(nside)
    
    if skymap_type == 'hemi':
        m1 = np.zeros(npix2)
        disc_idx = hp.query_disc(nside, hemi, np.pi / 2)
        m1[disc_idx] = 1   
    elif skymap_type =='allsky':
        m1 = np.full(npix2 ,1.)
    elif skymap_type =='cone':
        m1, nside = from_cone(ra, dec, error)
    else:
        raise AssertionError
        
    m1 /= m1.sum()
    return m1, nside


### Functions to calculate overlap integrals by numerical integration ###
#########################################################################


def angdist(alpha, delta, alpha0=0, delta0=0):
    return np.arccos(np.cos(delta)*np.cos(delta0)+np.sin(delta)*np.sin(delta0)*np.cos(alpha-alpha0))


def gaussian_probdensity(alpha, delta, alpha0, delta0, omega0):
    return np.exp(-.5*(angdist(alpha, delta, alpha0=alpha0, delta0=delta0)/omega0)**2.0)


def gaussian_probdensity_integrand(alpha, delta, alpha0, delta0, omega0):    
    return gaussian_probdensity(alpha, delta, alpha0, delta0, omega0)*np.sin(delta)


def gaussian_overlap_integrand(alpha, delta, alpha0, delta0, omega0, alpha00, delta00, omega00):
    return (gaussian_probdensity(alpha, delta, alpha0, delta0, omega0) * 
    gaussian_probdensity(alpha, delta, alpha00, delta00, omega00) * np.sin(delta))


def gaussian_overlap_integral(alpha0, alpha00, delta0, delta00, omega0, omega00):    
    numerator = 4 * np.pi*integrate.nquad(gaussian_overlap_integrand,[[0, 2*np.pi], [0, np.pi]], args=(alpha0,delta0,omega0,alpha00,delta00,omega00))[0]
    denominator = (integrate.nquad(gaussian_probdensity_integrand,[[0, 2*np.pi], [0, np.pi]], args=(alpha0,delta0,omega0))[0] * 
                   integrate.nquad(gaussian_probdensity_integrand,[[0, 2*np.pi], [0, np.pi]], args=(alpha00,delta00,omega00))[0])
    
    answer = numerator/denominator
    return answer


### Start tests ###
###################

@pytest.mark.parametrize(
    'test_type',
     ['no-overlap-hemi','allsky','allsky-hemi','same-hemi','concentric-gaussians',
      'noncoincident-gaussians','gaussian-hemi'])
def test_overlap_integrals(test_type):
    
    # generate a sky map
    if test_type == 'no-overlap-hemi':
        m1, nside1 = make_skymap(32, 'hemi', hemi=(1,0,0))
        m2, nside2 = make_skymap(64, 'hemi', hemi=(-1,0,0))
        expected_overlap = 0.00236
    elif test_type == 'allsky':
        m1, nside1 = make_skymap(16, 'allsky')
        m2, nside2 = make_skymap(16, 'allsky')
        expected_overlap = 1
    elif test_type == 'allsky-hemi':
        m1, nside1 = make_skymap(32, 'allsky')
        m2, nside2 = make_skymap(64, 'hemi', hemi=(0,1,0))
        expected_overlap = 1
    elif test_type == 'same-hemi':
        m1, nside1 = make_skymap(64, 'hemi', hemi=(1,0,0))
        m2, nside2 = make_skymap(32, 'hemi', hemi=(1,0,0))
        expected_overlap = 2
    elif test_type == 'concentric-gaussians':
        ra1, ra2, dec1, dec2, error1, error2 = 180, 180, 0, 0, 10, 5
        m1, nside1 = make_skymap(16, 'cone', ra=ra1, dec=dec1, error=error1)
        m2, nside2 = make_skymap(16, 'cone', ra=ra1, dec=dec2, error=error2)
        expected_overlap = gaussian_overlap_integral(rads(ra1), rads(ra2), rads(dec1)+np.pi/2,
                                            rads(dec2)+np.pi/2, rads(error1), rads(error2))
    elif test_type == 'noncoincident-gaussians':
        ra1, ra2, dec1, dec2, error1, error2 = 180, 0, 0, 45, 10, 5
        m1, nside1 = make_skymap(16, 'cone', ra=ra1, dec=dec1, error=error1)
        m2, nside2 = make_skymap(16, 'cone', ra=ra2, dec=dec2, error=error2)
        expected_overlap = gaussian_overlap_integral(rads(ra1), rads(ra2), rads(dec1)+np.pi/2,
                                            rads(dec2)+np.pi/2, rads(error1), rads(error2))    
    elif test_type == 'gaussian-hemi':
        ra1, dec1, error1 = 270, 0, 1
        m1, nside1 = make_skymap(16, 'cone', ra=ra1, dec=dec1, error=error1)
        m2, nside2 = make_skymap(32, 'hemi', hemi=(0,-1,0))
        expected_overlap = 2
    
    # calculate spatial overlap integral and compare to expected value
    assert isclose(skymap_overlap_integral(m1, m2), expected_overlap, rel_tol=.1)
