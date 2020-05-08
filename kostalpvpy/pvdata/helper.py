from datetime import datetime, timedelta

from kostalpvpy.pvdata.models import PVData

from sqlalchemy import func


def get_current_values():
    """
    :return: the current photovoltaic values from the system
    """
    return PVData.query.order_by(PVData.id.desc()).first()


def get_max_energy_last_seven_days():
    """
    :return: the maximum energy produced in the last seven days
    """
    return (PVData.query.whith_entities(func.max(PVData.daily_energy).label('max_daily_energy'))
            .filter(PVData.created_at >= (datetime.now() - timedelta(days=7))).first().max_daily_energy)


def get_last_year_energy():
    current_year = datetime.now().year
    return (PVData.query.whith_entities(PVData.total_energy)
            .filter(func.strftime('%Y', PVData.created_at) == str(current_year - 1))
            .order_by(PVData.id.desc()).first())
