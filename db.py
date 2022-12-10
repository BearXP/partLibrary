import pandas as pd
import os
import toml
import numpy as np

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
    df_ids = db.to_dict(orient='records')
    # Id there is a match, return it
    if df_ids:
      return df_ids[0]
    # If there is not a match, don't return it
    return df_ids
  
  def changeStatus(self, id : str, newStatus : str) -> pd.DataFrame:
    db = self._getDb()
    # Find which row the ID is at
    rowNo = db[db["id"] == id].index.values[0]
    db.at[rowNo, 'status'] = newStatus
    self._saveDb(db)
    return self.getId(id)
  
  def getParts(self) -> list:
    db = self._getDb()
    partsDf = db[ db.dataType == "equipment"]
    df3 = db.copy()[["id", "name"]]
    df3.rename({"id" : "status"}, inplace=True, axis=1)
    partsWBorrow = partsDf.join(df3.set_index('status'), on="status", rsuffix="_borrower", how="left", )
    partsShort = partsWBorrow[["name","name_borrower"]]
    partsShort = partsShort.replace(np.nan, '')
    parts = partsShort.values.tolist()
    return parts
  
  def getBorrowedEquipment(self, id : str) -> list:
    db = self._getDb()
    equipmentDf = db[ db.dataType == "equipment"]
    borrowed = equipmentDf[ equipmentDf.status == id]
    df3 = db.copy()[["id", "name"]]
    df3.rename({"id" : "status"}, inplace=True, axis=1)
    partsWBorrow = borrowed.join(df3.set_index('status'), on="status", rsuffix="_borrower", how="left", )
    partsShort = partsWBorrow[["name","name_borrower"]]
    partsShort = partsShort.replace(np.nan, '')
    parts = partsShort.values.tolist()
    return parts


  def getPartsString(self) -> str:
    parts = self.getParts()
    retVal = []
    for row in parts:
      retVal.append( f"{row[0]:<20}|{row[1]:>10}")
      #retVal.append( " | ".join(row))
    return "\n".join(retVal)
    
    
    

if __name__ == "__main__":
  db = Database()
  # df = db.getId("R3")
  # print(df.head())
  # #print(df)
  # df = db.changeStatus("R3", "R0")
  # print(df)
  # df = db.changeStatus("R3", "")
  # print(df)
  parts = db.getPartsString()
  print("     Equipment Name | Borrowed By")
  print(parts)
  print("------------")
  parts = db.getBorrowedEquipment("U0")
  print(parts)
