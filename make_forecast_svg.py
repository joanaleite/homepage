"""
Draw forecast.svg: the AirPassengers series and an ARIMA fan chart.
Requirements: pip install statsforecast matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
from statsforecast.utils import AirPassengersDF as df

# 1. Fit the model and forecast 36 months with 50/80/95% intervals
sf = StatsForecast(models=[AutoARIMA(season_length=12)], freq=pd.infer_freq(df["ds"]))
fc = sf.forecast(df=df, h=36, level=[50, 80, 95])

# 2. Time indices: the forecast starts at the last observation, so the fan joins the data
y = df["y"].to_numpy()
t_obs = np.arange(len(y))
t_fc = np.arange(len(y) - 1, len(y) + 36)
last = y[-1]

# 3. Smooth curves: interpolate every line on a fine time grid (monotone, no overshoot)
t_obs_fine = np.linspace(t_obs[0], t_obs[-1], 2000)
t_fc_fine = np.linspace(t_fc[0], t_fc[-1], 600)
smooth_fc = {
    col: PchipInterpolator(t_fc, np.r_[last, fc[col]])(t_fc_fine)
    for col in fc.columns
    if col.startswith("AutoARIMA")
}

# 4. Draw: no axes, transparent background, the site's colours
fig, ax = plt.subplots(figsize=(12, 3.6))
green, ink = "#2f6b4f", "#1c1f1d"

for level, alpha in [(95, 0.10), (80, 0.16), (50, 0.26)]:  # widest band first
    ax.fill_between(
        t_fc_fine,
        smooth_fc[f"AutoARIMA-lo-{level}"],
        smooth_fc[f"AutoARIMA-hi-{level}"],
        color=green,
        alpha=alpha,
        lw=0,
    )

ax.plot(
    t_fc_fine, smooth_fc["AutoARIMA"], color=green, lw=0.8, ls=(0, (4, 4))
)  # point forecast
ax.plot(
    t_obs_fine, PchipInterpolator(t_obs, y)(t_obs_fine), color=ink, lw=0.8
)  # observed

ax.set_xlim(0, t_fc[-1])
ax.axis("off")
fig.savefig("forecast.svg", transparent=True, bbox_inches="tight", pad_inches=0)
print("forecast.svg written")
