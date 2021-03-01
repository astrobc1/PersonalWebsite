import streamlit as st

page = st.sidebar.radio(label="Navigation", options=["Home", "Research", "Hobbies"])

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
    
    col1.image("images/pychell_logo.png", width=300)
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
    
    
    
    