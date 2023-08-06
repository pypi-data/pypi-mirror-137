from sqlalchemy import create_engine as _create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from ..local import get_free_port

DRIVERS = {
    "mariadb": "mysql+pymysql",
    "mysql": "mysql+pymysql",
    "postgresql": "postgresql+psycopg2",
}


def create_engine(conf: dict, use_tunnel: bool = False, drivers: dict = DRIVERS) -> Engine:
    """Create engine using conf from aws secrets manager.

    Args:
        conf (dict): username, password, engine, host, port, dbname
        use_tunnel (bool, optional): [description]. Defaults to False.

    Returns:
        Engine: [description]
    """

    # set driver
    _conf = conf.copy()
    db_engine = _conf.pop("engine")
    if db_engine is not None:
        _conf["drivername"] = DRIVERS.get(db_engine)
    else:
        _conf["drivername"] = db_engine

    # rename dbname -> database
    _conf["database"] = _conf.pop("dbname")

    # if use ssh tunnel
    if use_tunnel:
        _conf["host"] = "127.0.0.1"
        _conf["port"] = get_free_port()

    # generate database url
    db_url = URL.create(**_conf)

    return _create_engine(db_url)
