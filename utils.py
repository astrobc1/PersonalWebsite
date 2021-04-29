# Base Python libraries
import os

# Import numpy and pandas
import numpy as np
import pandas as pd

# Import pychell orbits module
import pychell.orbits as pco

# Streamlit
import streamlit as st
import streamlit.components.v1 as components

def write_map_result(rvprob:pco.RVProblem, comps:dict, map_result:dict):
    st.markdown('# MAP Results')
    pbest = map_result["pbest"]
    for par in pbest.values():
        st.text(repr(par))
    st.markdown('## Function calls: ' + str(map_result['fcalls']))
    st.markdown('## ln(L): ' + str(-1 * map_result['fbest']))
    st.markdown('## Red Chi 2: ' + str(rvprob.obj.compute_redchi2(pbest, include_white_error=True, include_kernel_error=False)))

    # Full RV plot
    st.markdown('## Full RV Plot')
    fig = rvprob.plot_full_rvs(pars=pbest, n_model_pts=5000)
    comps["fig_rvs_full_map"] = st.plotly_chart(fig)

    # Phased rv plot
    st.markdown('## Planets')
    planet_figs = rvprob.plot_phased_rvs_all(pars=pbest)
    for i, planet_index in enumerate(rvprob.planets_dict):
        name = "figplanet_" + str(planet_index) + "_map"
        comps[name] = st.plotly_chart(planet_figs[i])

def write_mcmc_result(rvprob:pco.RVProblem, comps:dict, mcmc_result:dict):
    st.markdown('# MCMC Results')
    pbest = mcmc_result["pmed"]
    for par in pbest.values():
        st.text(repr(par))
    st.markdown('## ln(L): ' + str(mcmc_result['lnL']))
    st.markdown('## Red Chi 2: ' + str(rvprob.obj.compute_redchi2(pbest, include_white_error=True, include_kernel_error=False)))

    # Full RV plot
    st.markdown('## Full RV Plot')
    fig = rvprob.plot_full_rvs(pars=pbest, n_model_pts=5000)
    comps["fig_rvs_full_map"] = st.plotly_chart(fig)

    # Phased rv plot
    st.markdown('## Planets')
    planet_figs = rvprob.plot_phased_rvs_all(pars=pbest)
    for i, planet_index in enumerate(rvprob.planets_dict):
        name = "figplanet_" + str(planet_index) + "_map"
        comps[name] = st.plotly_chart(planet_figs[i])
        
    # Corner plot
    st.markdown('## Corner Plot')
    corner_plot = rvprob.corner_plot(mcmc_result=mcmc_result)
    comps["corner_plot"] = st.pyplot(corner_plot)
    
def write_mc_result(rvprob:pco.RVProblem, comps:dict, mc_result:dict):
    st.markdown('# Model Comparison')
    df = pd.DataFrame()
    n_models = len(mc_result)
    df["Planets"] = [""]*n_models
    df["ln \u2112"] = [1.0]*n_models
    df["\u0394 AICc"] = [1.0]*n_models
    df["\u0394 BIC"] = [1.0]*n_models
    df["N free"] = [1.0]*n_models
    df["Red. \u03C7 Sq."] = [1.0]*n_models
    for i in range(n_models):
        s = ""
        for planet_index in mc_result[i]["planets_dict"]:
            s += mc_result[i]["planets_dict"][planet_index]["label"] + ", "
        if len(s) > 0:
            s = s[0:-2]
        df["Planets"][i] = s
        df["ln \u2112"][i] = mc_result[i]["lnL"]
        df["\u0394 AICc"][i] = mc_result[i]["delta_aicc"]
        df["\u0394 BIC"][i] = mc_result[i]["delta_bic"]
        df["N free"][i] = mc_result[i]["pbest"].num_varied()
        df["Red. \u03C7 Sq."][i] = mc_result[i]["redchi2"]
    st.table(df)


def write_actions(rvprob:pco.RVProblem, comps:dict):
    
    st.markdown('## Actions')
    comps["map_button"] = st.button(label='MAP')
    comps["mcmc_button"] = st.button(label='MCMC')
    comps["mc_button"] = st.button(label='Model Comparison')
    comps["per_search_button"] = st.button('Period Search')
    
    # Period search options
    st.markdown('## Period Search Options:')
    st.markdown('### Periodogram Type:')
    comps["persearch_kind_input"] = st.radio(label="", options=["GLS", "Brute Force"])
    
    # period search inputs
    pgcols = st.beta_columns(2)
    comps["persearch_min_input"] = pgcols[0].text_input(label='Period min', value=1.1)
    comps["persearch_max_input"] = pgcols[1].text_input(label='Period max', value=100)
    
def action_dispatch(rvprob:pco.RVProblem, comps:dict):
    
    # MAP fit
    if comps["map_button"]:
        map_result = rvprob.mapfit()
        write_map_result(rvprob, comps, map_result)
    elif comps["mcmc_button"]:
        mcmc_result = rvprob.mcmc()
        write_mcmc_result(rvprob, comps, mcmc_result)
    elif comps["mc_button"]:
        mc_result = rvprob.model_comparison()
        write_mc_result(rvprob, comps, mc_result)
    elif comps["per_search_button"]:
        pass
    
def write_data_selector(data:pco.CompositeRVData, comps:dict):
    
    st.markdown("## RV Data")
    for _data in data.values():
        comps[_data.label] = st.checkbox(label=f"{_data.label} {[len(_data.t)]}", value=True)
        
    for _data in data.values():
        instname = _data.label
        if not comps[instname]:
            del data[instname]