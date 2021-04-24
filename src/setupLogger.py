import logging
from datetime import date

logfile_level = logging.INFO
shell_level = logging.DEBUG


def setup(announcement=None):

    # Setup Shell Logger
    logger = logging.getLogger()
    logging.basicConfig(level=shell_level, format="[%(levelname)s]: %(message)s")

    # Setup File Logger
    today = date.today()
    fh = logging.FileHandler("logs/" + today.strftime("%d-%m-%Y") + ".log")
    fh.setLevel(logfile_level)
    logger.addHandler(fh)

    if announcement != None:
        formatterHeader = logging.Formatter("%(message)s")
        fh.setFormatter(formatterHeader)
        logger.info(
            "\n============================================================================\n============================================================================"
        )
        formatterHeader = logging.Formatter("[%(asctime)s|RUNNING]:\t%(message)s")
        fh.setFormatter(formatterHeader)
        logger.info(announcement)

    formatterFile = logging.Formatter(
        "[%(asctime)s|%(levelname)s|%(name)s]:\t%(message)s"
    )
    fh.setFormatter(formatterFile)