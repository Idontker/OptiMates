import logging
from datetime import date

log_level = logging.DEBUG

# BUG: logfile wird ausgeschrieben


def setup(announcement=None):
    # der logger gibt hier den root Logger, welcher per Default auf stdout ausgibt
    # jeder haendler, den ich hinzufüge, kann aber nur auf einer höheren Ebene wie er selbst printen
    # daher scheitert mein Loggging

    # Setup Shell Logger
    logger = logging.getLogger()
    logging.basicConfig(level=log_level, format="[%(levelname)s]: %(message)s")

    # Setup File Logger
    today = date.today()
    fh = logging.FileHandler("logs/" + today.strftime("%d-%m-%Y") + ".log")
    fh.setLevel(log_level)
    logger.addHandler(fh)

    if announcement != None:
        formatterHeader = logging.Formatter("%(message)s")
        fh.setFormatter(formatterHeader)
        logger.info(
            "\n============================================================================ " +
            "\n============================================================================"
        )
        formatterHeader = logging.Formatter(
            "[%(asctime)s|RUNNING]:\t%(message)s")
        fh.setFormatter(formatterHeader)
        logger.info(announcement)

    formatterFile = logging.Formatter(
        "[%(asctime)s|%(levelname)s|%(name)s]:\t%(message)s"
    )
    fh.setFormatter(formatterFile)
