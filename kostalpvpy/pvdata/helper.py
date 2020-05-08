from datetime import datetime, timedelta

from sqlalchemy import func

from kostalpvpy.pvdata.models import PVData
from kostalpvpy.extensions import db


def get_current_values():
    """
    :return: the current photovoltaic values from the system
    """
    return PVData.query.order_by(PVData.id.desc()).first()


def get_max_energy_last_seven_days():
    """
    :return: the maximum energy produced in the last seven days
    """
    return (PVData.query.with_entities(func.max(PVData.daily_energy).label('max_daily_energy'))
            .filter(PVData.created_at >= (datetime.now() - timedelta(days=7))).first().max_daily_energy)


def get_last_year_energy():
    current_year = datetime.now().year
    return (PVData.query.with_entities(PVData.total_energy)
            .filter(func.strftime('%Y', PVData.created_at) == str(current_year - 1))
            .order_by(PVData.id.desc()).first())


def get_table_data():
    last_30_days = datetime.now() - timedelta(days=30)
    data = db.engine.execute(
        """SELECT
            Strftime('%Y-%m-%d', created_at) AS created_at,
            Max(daily_energy) AS daily_energy,
            Max(total_energy) AS total_energy,
            Max(current_power) AS max_output
           FROM pvdata
           WHERE Strftime('%Y-%m-%d', created_at) > ?
           GROUP BY Strftime('%Y-%m-%d', created_at)
           ORDER BY created_at DESC""", last_30_days)
    return data
