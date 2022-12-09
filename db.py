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
      self.config = toml.load(f)["db"]
    
  def _saveDb(self, db) -> None:
    db.set_index("id", inplace=True)
    db.to_csv(self.dbFilename)

  def _confirmDbExists(self) -> None:
    # If the database doesn't exist, make it
    self.dbFilename = self.config["dbFilename"] + ".csv"
    if not os.path.exists(self.dbFilename):
      colNames = self.config["colNames"]
      df = pd.DataFrame(columns=colNames)
      df.set_index("id", inplace=True)
      self._saveDb(df)

  def _getDb(self) -> pd.DataFrame:
    # Load the database from the csv file
    df = pd.read_csv(self.dbFilename, na_filter=False)
    return df

  def getId(self, id : str) -> pd.DataFrame:
    db = self._getDb()
    db = db[db.id==id]
    return db
  
  def changeStatus(self, id : str, newStatus : str) -> pd.DataFrame:
    db = self._getDb()
    # Find which row the ID is at
    rowNo = df[df["id"] == id].index.values[0]
    db.at[rowNo, 'status'] = newStatus
    self._saveDb(db)
    return self.getId(id)

  def getPartsString(self) -> str:
    db = self._getDb()
    partsDf = db[ db.dataType == "equipment"]
    partsDf = partsDf[["alias","longDesc","statusDesc"]]
    parts = partsDf.values.tolist()
    retVal = []
    for row in parts:
      retVal.append( " | ".join(row))
    return "\n".join(retVal)
    
    
    

if __name__ == "__main__":
  db = Database()
  df = db.getId("R3")
  print(df.head())
  #print(df)
  df = db.changeStatus("R3", "R0")
  print(df)
  df = db.changeStatus("R3", "")
  print(df)
  parts = db.getPartsString()
  print(parts)
