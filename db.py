import pandas as pd
import os
import toml
import numpy as np
import time


class Database:
    def __init__(self):
        """
        It loads the config file, and then confirms that the database exists
        """
        self._loadConfig()
        self._confirmDbExists()

    def _loadConfig(self) -> None:
        """
        > Load the config settings

        And here's a longer description of the function:

        > Load the config settings from the config.toml file
        """
        # Load the config settings
        with open("config.toml", "r") as f:
            self.config = toml.load(f)["db"]

    def _saveDb(self, db) -> None:
        """
        It takes a dataframe, sets the index to the column named "id", and then saves the dataframe to a csv
        file
        @param db - The dataframe to save
        """
        db.set_index("id", inplace=True)
        db.to_csv(self.dbFilename)

    def _confirmDbExists(self) -> None:
        """
        If the database doesn't exist, make it
        """
        # If the database doesn't exist, make it
        self.dbFilename = self.config["dbFilename"] + ".csv"
        if not os.path.exists(self.dbFilename):
            colNames = self.config["colNames"]
            df = pd.DataFrame(columns=colNames)
            df.set_index("id", inplace=True)
            self._saveDb(df)

    def _getDb(self) -> pd.DataFrame:
        """
        > Load the database from the csv file

        The function is a member of the class `Database` and is named `_getDb`. It returns a Pandas
        DataFrame
        @returns A dataframe
        """
        # Load the database from the csv file
        df = pd.read_csv(self.dbFilename, na_filter=False)
        return df

    def getId(self, id: str) -> pd.DataFrame:
        """
        `getId` returns a single row from the database, if it exists, or an empty list if it doesn't.
        @param {str} id - The id of the record you want to get
        @returns A dictionary
        """
        db = self._getDb()
        db = db[db.id == id]
        df_ids = db.to_dict(orient="records")
        # Id there is a match, return it
        if df_ids:
            return df_ids[0]
        # If there is not a match, don't return it
        return df_ids

    def changeStatus(self, id: str, newStatus: str) -> pd.DataFrame:
        """
        It finds the row in the database that has the ID that was passed in, changes the status to the new
        status that was passed in, and then returns the row that was changed
        @param {str} id - The ID of the row to change
        @param {str} newStatus - The new status of the ID.
        @returns A dataframe with the row of the ID
        """
        db = self._getDb()
        # Find which row the ID is at
        rowNo = db[db["id"] == id].index.values[0]
        db.at[rowNo, "status"] = newStatus
        db.at[rowNo, "timestamp"] = time.time()
        self._saveDb(db)
        return self.getId(id)

    def getParts(self) -> list:
        """
        It takes a dataframe, filters it to only include rows where the dataType column is equal to
        "equipment", then joins that dataframe with another dataframe that only includes the id and name
        columns, renames the id column to status, and joins the two dataframes on the status column
        @returns A list of lists.
        """
        db = self._getDb()
        partsDf = db[db.dataType == "equipment"]
        df3 = db.copy()[["id", "name"]]
        df3.rename({"id": "status"}, inplace=True, axis=1)
        partsWBorrow = partsDf.join(
            df3.set_index("status"),
            on="status",
            rsuffix="_borrower",
            how="left",
        )
        partsShort = partsWBorrow[["name", "name_borrower"]]
        partsShort = partsShort.replace(np.nan, "")
        parts = partsShort.values.tolist()
        return parts

    def getBorrowedEquipment(self, id: str) -> list:
        """
        It takes an id, finds all the equipment with that id as the status, joins the equipment with the
        people table to get the name of the person who borrowed the equipment, and returns a list of the
        equipment and the name of the person who borrowed it
        @param {str} id - the id of the person who borrowed the equipment
        @returns A list of lists. Each list contains the name of the equipment and the name of the person
        who borrowed it.
        """
        db = self._getDb()
        equipmentDf = db[db.dataType == "equipment"]
        borrowed = equipmentDf[equipmentDf.status == id]
        df3 = db.copy()[["id", "name"]]
        df3.rename({"id": "status"}, inplace=True, axis=1)
        partsWBorrow = borrowed.join(
            df3.set_index("status"),
            on="status",
            rsuffix="_borrower",
            how="left",
        )
        partsShort = partsWBorrow[["name", "name_borrower"]]
        partsShort = partsShort.replace(np.nan, "")
        parts = partsShort.values.tolist()
        return parts


if __name__ == "__main__":
    db = Database()
    df = db.getId("E3")
    print(df)
    # print(df)
    df = db.changeStatus("E3", "U0")
    print(df)
    df = db.changeStatus("E3", "")
    print(df)
    print("------------")
    parts = db.getBorrowedEquipment("U0")
    print(parts)
