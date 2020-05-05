from flask import Blueprint, render_template

from kostalpvpy.pvdata.models import PVData

bp_home = Blueprint("home", __name__)


@bp_home.route("/")
def home():
    return render_template("home/home.html", pvdata=None)


@bp_home.route("/test2")
def test():
    return render_template("home/sample_solar.html")
