# coding: utf-8
# market environments
from dx import *

r = constant_short_rate('r', 0.02)

me_gbm = market_environment('gbm', dt.datetime(2014, 1, 1))
me_jd = market_environment('jd', dt.datetime(2014, 1, 1))
# geometric Brownian motion
me_gbm.add_constant('initial_value', 36.)
me_gbm.add_constant('volatility', 0.2) 
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('model', 'gbm')
# jump diffusion
me_jd.add_constant('initial_value', 36.)
me_jd.add_constant('volatility', 0.2)
me_jd.add_constant('lambda', 0.5)
    # probability for jump p.a.
me_jd.add_constant('mu', -0.75)
    # expected jump size [%]
me_jd.add_constant('delta', 0.1)
    # volatility of jump
me_jd.add_constant('currency', 'EUR')
me_jd.add_constant('model', 'jd')
# valuation environment
val_env = market_environment('val_env', dt.datetime(2014, 1, 1))
val_env.add_constant('paths', 5000)
val_env.add_constant('frequency', 'W')
val_env.add_curve('discount_curve', r)
val_env.add_constant('starting_date', dt.datetime(2014, 1, 1))
val_env.add_constant('final_date', dt.datetime(2014, 12, 31))
# add valuation environment to market environments
me_gbm.add_environment(val_env)
me_jd.add_environment(val_env)
underlyings = {
               'gbm' : me_gbm,
               'jd' : me_jd
               }
correlations = [
                ['gbm', 'jd', 0.75], 
                ]
gbm = geometric_brownian_motion('gbm_obj', me_gbm)
jd = jump_diffusion('jd_obj', me_jd)
me_max_call = market_environment('put', dt.datetime(2014, 1, 1))
me_max_call.add_constant('maturity', dt.datetime(2014, 12, 31))
me_max_call.add_constant('currency', 'EUR')
me_max_call.add_environment(val_env)
payoff_call = "np.maximum(np.maximum(maturity_value['gbm'], "
payoff_call += "maturity_value['jd']) - 34., 0)"
max_call = valuation_mcs_european_multi(
                        name='max_call',
                        val_env=me_max_call,
                        risk_factors=underlyings,
                        correlations=correlations,
                        payoff_func=payoff_call)
