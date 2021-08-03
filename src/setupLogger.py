import logging
from datetime import date

shell_level = logging.DEBUG
logfile_level = logging.DEBUG

# BUG: logfile wird ausgeschrieben


def setup(announcement=None):

    # der logger gibt hier den root Logger, welcher per Default auf stdout ausgibt
    # jeder haendler, den ich hinzufüge, kann aber nur auf einer höheren Ebene wie er selbst printen
    # daher scheitert mein Loggging

    # Idee ist: hieraus eine schnittstelle bauen, welcher jeweils 2 unabhänge Logger triggered 
    # dann muss aber in jeder Klasse das "import logging" ausgetauscht werden durch "from setupLogger import myLogger"


    # Setup Shell Logger
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s]: %(message)s")

    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(shell_level)
    # logger.addHandler(stream_handler)

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


    logger.setLevel(shell_level)