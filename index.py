# Base Python libraries
import os

# Import numpy
import numpy as np

# Import pychell orbits module
import pychell.orbits as pco

# Streamlit
import streamlit as st
import streamlit.components.v1 as components
import utils

page = st.sidebar.radio(label="Navigation", options=["Home", "Research", "Hobbies", "pychell Demo"])

link_python = "[Python](https://www.python.org/)"
link_julia = "[Julia](https://julialang.org/)"
link_ishell = "[iSHELL](http://irtfweb.ifa.hawaii.edu/~ishell/)"
link_github = "[GitHub](https://github.com/astrobc1)"
link_cv = "[CV](https://drive.google.com/file/d/1a_GyRiSXR_x3HZBnm3-jMWzSI53Z_Y3f/view?usp=sharing)"
#st.markdown(link_python, unsafe_allow_html=True)

if page == "Home":
    
    "## Bryson Cale"
    "### Physics Ph.D. Candidate"
    "### @ George Mason University, graduating August 2021"
    col1, col2 = st.beta_columns(2)
    col1.image("images/me.jpg", width=300)
    col2.markdown("### Links")
    col2.markdown(link_github, unsafe_allow_html=True)
    col2.markdown(link_cv, unsafe_allow_html=True)
    
elif page == "Research":
    
    "I primarily search for exoplanets with the radial-velocity (RV) technique. Planets do not orbit a stationary star, but rather the star+planet(s) orbit about the center of mass of the system. As the star moves about the center of mass, changes to its spectrum can be measured via Doppler Spectroscopy. Significant periods in the velicity correspond to the period (effective year) for the candidate perturber, and the relative amplitude of the velocity change will can be used to measure the mass of the object. Searching for planets around M dwarfs in particular provides a potential shortcut to finding habitable zone worlds, and is a primary science case for my Ph.D thesis."
    
    "I primarily use the iSHELL spectrograph on the NASA Infrared Telescope Facility, which utilizes near-infrared wavelengths to perform the Doppler measurements. I also use the following visible wavelength facilities - CHIRON, MINERVA, MINERVA-Australis, and PARVI. I develop codes to delicately compute these velocities from the raw spectral data these facilities provide."
    
    "## Codes I\'ve developed:"
    
    col1, col2 = st.beta_columns(2)
    
    #col1.image("images/pychell_logo.png", width=300)
    st.write(
    """
    <div>
        <a href="https://github.com/astrobc1/pychell">
            <img src="images/pychell_logo.png" />
        </a>
    </div>
    """,
    allow_unsafe_html=True)
    
    col1.write("1. Pychell is a package to process high resolution echelle spectra and generate precise radial velocities. Pychell makes use of the optimize package.")
    col2.image("images/opt_logo.png", width=300)
    col2.write("2. Optimize is a suite for generic Bayesian inference and optimization routines. Included is a Robust iterative Nelder Mead algorithm for high dimensional parameter spaces, so long as enough of the initial guesses are accurate (frequently tested in ~ 50 dimensions).")
    st.image("images/spec.png", use_column_width=True)
    
elif page == "Hobbies":
    
    "In my free time I -- "
    "Play tennis!"
    st.image("images/tennis.png", use_column_width=True)
    
    "2. Programming in either Python or Julia. I like to explore fractal geometry in the complex plane."
    st.image("images/juliaset.png", use_column_width=True)
    
    "3. Cook endless amounts of Italian food."
    
elif page == "pychell Demo":
    
    #################################
    #### Required for any RV run ####
    #################################
    
    # Path to input rv file and outputs for outputs
    output_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    fname = 'kelt24_example/kelt24_rvs.txt'

    # The name of the star for plots
    star_name = 'KELT-24'

    # Mass and uncertainty of star for mass determination (solar units)
    mstar = 1.460
    mstar_unc = [0.059, 0.055] # -, +

    # All data in one dictionary from a radvel formatted csv file
    data = pco.CompositeRVData.from_radvel_file(fname)
    
    # Stores streamlit state
    comps = {}
    
    # Choose which data to use here.
    # Data object is automatically updated according to the check boxes through streamlit magic.
    utils.write_data_selector(data, comps)

    # Init parameters and planets dictionary
    pars = pco.Parameters()
    planets_dict = {}

    # Used later to set initial values
    jitter_dict = {"TRES": 0, "SONG": 50}

    # Define parameters for planet 1
    # Other bases are available, this fits for P, TC, ECC, W, K.
    planets_dict[1] = {"label": "b", "basis": pco.TCOrbitBasis(1)}

    # Values from Rodriguez et al. 2019 for KELT-24 b
    # Given the extremely precise values for P and TC from the multiple transits, there is no reason to fit for P and TC here.
    # We will still fit for P and TC for demonstrative purposes.
    per1 = 5.5514926
    per1_unc = 0.0000081
    tc1 =  2457147.0529
    tc1_unc = 0.002
    ecc1 = 0.077
    ecc1_unc = 0.024
    w1 = 55 * np.pi / 180
    w1_unc = 15 * np.pi / 180

    # Period
    pars["per1"] = pco.Parameter(value=per1, vary=True)
    pars["per1"].add_prior(pco.Gaussian(per1, per1_unc))

    # Time of conjunction
    pars["tc1"] = pco.Parameter(value=tc1, vary=True)
    pars["tc1"].add_prior(pco.Gaussian(tc1, tc1_unc))

    # Eccentricity
    pars["ecc1"] = pco.Parameter(value=ecc1, vary=True)
    pars["ecc1"].add_prior(pco.Uniform(1E-10, 1))
    pars["ecc1"].add_prior(pco.Gaussian(ecc1, ecc1_unc))

    # Angle of periastron
    pars["w1"] = pco.Parameter(value=w1, vary=True)
    pars["w1"].add_prior(pco.Gaussian(w1, w1_unc))

    # RV semi-amplitude
    pars["k1"] = pco.Parameter(value=462, vary=True)
    pars["k1"].add_prior(pco.Positive())

    # Per instrument zero points
    # Additional small offset is to avoid cases where the median is already subtracted off.
    for instname in data:
        data[instname].y += 300
        pname = "gamma_" + instname
        pars[pname] = pco.Parameter(value=np.nanmedian(data[instname].rv) + np.pi, vary=True)
        pars[pname].add_prior(pco.Uniform(pars[pname].value - 200, pars[pname].value + 200))
        
    # Linear and quadratic trends, fix at zero
    pars["gamma_dot"] = pco.Parameter(value=0, vary=False)
    pars["gamma_ddot"] = pco.Parameter(value=0, vary=False)

    # Per-instrument jitter (only fit for SONG jitter, TRES jitter is typically sufficient.)
    for instname in data:
        pname = "jitter_" + instname
        pars[pname] = pco.Parameter(value=jitter_dict[instname], vary=jitter_dict[instname] > 0)
        if pars[pname].vary:
            pars[pname].add_prior(pco.Uniform(1E-10, 100))

    # Initiate a composite likelihood object
    likes = pco.RVPosterior()

    # Define a single kernel and model, add to likelihoods
    kernel = pco.WhiteNoise(data=data)
    model = pco.RVModel(planets_dict=planets_dict, data=data, p0=pars)
    likes["rvs"] = pco.RVLikelihood(data=data, model=model, kernel=kernel)

    # Define max like optimizer (iterative Nelder-Mead) and emcee MCMC sampler
    optimizer = pco.NelderMead(obj=likes)
    sampler = pco.AffInv(obj=likes, options=None)

    # Construct a top-level RV "problem"
    rvprob = pco.RVProblem(output_path=output_path, star_name=star_name, p0=pars, optimizer=optimizer, sampler=sampler, data=data, obj=likes, mstar=mstar, mstar_unc=mstar_unc, tag="EXAMPLE")

    ##########################################
    #### Remaining Streamlit interactions ####
    ##########################################
    
    # Actions to perform
    utils.write_actions(rvprob, comps)
    
    # With inputs all set, perform the desired action
    utils.action_dispatch(rvprob, comps)