from flask import Blueprint, render_template

from kostalpvpy.pvdata.helper import (get_current_values, get_last_year_energy, get_max_energy_last_seven_days)

bp_home = Blueprint("home", __name__)


@bp_home.route("/")
def home():
    # photovoltaic data
    pv = get_current_values()
    daily_energy = pv.daily_energy
    total_energy = pv.total_energy

    max_daily_energy_last_seven_days = get_max_energy_last_seven_days()

    last_year_energy = get_last_year_energy()
    current_year_energy = total_energy

    if hasattr(last_year_energy, "total_energy"):
        current_year_energy = total_energy - last_year_energy.total_energy

    return render_template("home/home.html",
                           daily_energy=daily_energy,
                           max_daily_energy_last_seven_days=max_daily_energy_last_seven_days,
                           current_year_energy=current_year_energy,
                           total_energy=total_energy)
