import glob
from db import Database
import threading
import time
import logzero
import toml
import winsound


class Updater:
    def __init__(self):
        self.db = Database()
        self._loadConfig()

    def _loadConfig(self):
        with open("config.toml", "r") as f:
            allConfig = toml.load(f)
        self.config = allConfig["ExternalUpdater"]
        logzero.logfile(allConfig["gui"]["logFilename"])
        # logzero.loglevel(int(self.config["logLevel"]))

    def run(self):
        x = threading.Thread(target=self._thread)
        x.start()

    def _thread(self):
        logzero.logger.debug("Running background DB watcher")
        while True:
            # Check to see if the databse exists on the USB drive
            if self._externalDbExists():
                # Append the new items
                logzero.logger.info(
                    "USB Drive with database.csv detected. Updating Database..."
                )
                self.db.appendDb(self.config["EXTERNAL_DB_LOCATION"])
                logzero.logger.info("  > Exporting Database")
                self.db.exportDb(self.config["EXTERNAL_DB_LOCATION"])
                logzero.logger.info("  > Done")
                winsound.PlaySound(self.config["doneSfx"], winsound.SND_FILENAME)
                # Wait for the device to be removed
                while self._externalDbExists():
                    time.sleep(1)
            time.sleep(1)

    def _externalDbExists(self):
        files = glob.glob(self.config["EXTERNAL_DB_LOCATION"])
        return len(files) > 0


if __name__ == "__main__":
    up = Updater()
    up.run()
    while True:
        time.sleep(100)
