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
    
  def _saveDb(self, db) -> None:
    db.set_index("id", inplace=True)
    db.to_csv(self.dbFilename)

  def _confirmDbExists(self) -> None:
    # If the database doesn't exist, make it
    self.dbFilename = self.config["db"]["dbFilename"] + ".csv"
    if not os.path.exists(self.dbFilename):
      colNames = self.config["db"]["colNames"]
      df = pd.DataFrame(columns=colNames)
      df.set_index("id", inplace=True)
      self._saveDb(df)

  def _getDb(self) -> pd.DataFrame:
    # Load the database from the csv file
    df = pd.read_csv(self.dbFilename)
    return df

  def getId(self, id : int) -> pd.DataFrame:
    db = self._getDb()
    db = db[db.index==id]
    return db
  
  def changeStatus(self, id : int, newStatus : str) -> pd.DataFrame:
    db = self._getDb()
    db.at[id, 'status'] = newStatus
    statusStr = ""
    if newStatus:
      username = db.at[int(newStatus), "longDesc"]
      statusStr = f"Borrowed by {username}"
    db.at[id, 'statusDesc'] = statusStr
    self._saveDb(db)
    return db[db.index == id]

  def getPartsString(self) -> str:
    db = self._getDb()
    partsDf = db[ db.dataType == "part"]
    partsDf = partsDf[["alias","longDesc","statusDesc"]]
    parts = partsDf.values.tolist()
    retVal = []
    for row in parts:
      retVal.append( " | ".join(row))
    return "\n".join(retVal)
    
    
    

if __name__ == "__main__":
  db = Database()
  df = db.getId(3)
  print(df.head())
  #print(df)
  #df = db.changeStatus(3, "0")
  #print(df)
  parts = db.getPartsString()
  print(parts)
