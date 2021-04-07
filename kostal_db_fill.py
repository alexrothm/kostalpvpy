from pikopy.piko import Piko
import sqlite3
import datetime
from astral import LocationInfo
from astral.sun import sun
from pytz import timezone
import os


def fill_with_sun(lat, lon, inverter):
    timezone_local = timezone('Europe/Berlin')
    now = datetime.datetime.now(timezone_local)
    city = LocationInfo("St", "GER", timezone_local, lat, lon)
    s = sun(city.observer, date=now, tzinfo=timezone_local)

    sunrise = s["dawn"]
    sunset = s["dusk"]

    if not sunrise <= now <= sunset:
        return city

    fill_db_with_piko(inverter)
    return s


def fill_db_with_piko(i: Piko):
    # if i.get_status() == "Aus":
    #     return None

    dc_1_u = i.get_string1_voltage()
    dc_1_i = i.get_string1_current()
    ac_1_u = i.get_l1_voltage()
    ac_1_p = i.get_l1_power()

    dc_2_u = i.get_string2_voltage()
    dc_2_i = i.get_string2_current()
    ac_2_u = i.get_l2_voltage()
    ac_2_p = i.get_l2_power()

    dc_3_u = i.get_string3_voltage()
    dc_3_i = i.get_string3_current()
    ac_3_u = i.get_l3_voltage()
    ac_3_p = i.get_l3_power()

    current_power = i.get_current_power()
    daily_energy = i.get_daily_energy()
    total_energy = i.get_total_energy()
    status = i.get_status()

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    database = os.path.join(PROJECT_ROOT, "app.db")

    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql_statement = [(datetime.datetime.now(),
                      dc_1_u, dc_1_i,
                      ac_1_u, ac_1_p,
                      dc_2_u, dc_2_i,
                      ac_2_u, ac_2_p,
                      dc_3_u, dc_3_i,
                      ac_3_u, ac_3_p,
                      current_power,
                      daily_energy,
                      total_energy,
                      status
                      )]

    c.executemany('INSERT INTO pvdata VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', sql_statement)
    conn.commit()
    c.close()

    return None


if __name__ == "__main__":
    inverter = Piko(host="http://192.168.178.78")
    fill_with_sun(52.005552, 6.919066, inverter)

