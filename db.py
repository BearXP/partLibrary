import pandas as pd
import os
import toml

class Database():
  def __init__(self):
    self._loadConfig()
    self._confirmDbExists()

  def _loadConfig(self) -> None:
    # Load the config settings
    with open("config.toml", "r") as f:
      self.config = toml.load(f)

  def _confirmDbExists(self) -> None:
    # If the database doesn't exist, make it
    self.dbFilename = self.config["db"]["dbFilename"] + ".csv"
    if not os.path.exists(self.dbFilename):
      colNames = self.config["db"]["colNames"]
      df = pd.DataFrame(columns=colNames)
      df.to_csv(self.dbFilename)

  def _getDb(self):
    # Load the database from the csv file
    df = pd.read_csv(self.dbFilename)
    return df

  def getId(self, id : int):
    db = self._getDb()
    db = db[db.id==id]
    return db

if __name__ == "__main__":
  db = Database()
  df = db.getId(3)
  print(df)
