import pandas as pd
import os
import toml
import numpy as np
import time
from datetime import datetime


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

    def _saveDb(self, db, filename: str = "") -> None:
        """
        > It takes a dataframe, sets the index to the column named "id", and then saves the dataframe to a
        csv file

        :param db: The dataframe to save
        :param filename: The name of the file to save the database to
        :type filename: str
        """
        if not filename:
            filename = self.dbFilename
        db.set_index("id", inplace=True)
        db.to_csv(filename)

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

    def _getDb(self, filename: str = "") -> pd.DataFrame:
        """
        `_getDb()` loads the database from the csv file

        :param filename: The name of the file to load the database from
        :type filename: str
        :return: A dataframe
        """
        if not filename:
            filename = self.dbFilename
        # Load the database from the csv file
        df = pd.read_csv(filename, na_filter=False)
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
        def _timestampToDate(row):
            # If it's not borrowed, ignore the timestamp
            if not row["name_borrower"]:
                return ""
            # If the timestamp is blank, ignore it
            timestamp = row["timestamp"]
            if not timestamp:
                return ""
            dt_obj = datetime.fromtimestamp(float(timestamp))
            timeStr = dt_obj.strftime('%d-%b-%Y')
            return timeStr
        # Get the equipment from the database
        db = self._getDb()
        partsDf = db[db.dataType == "equipment"]
        # Make a copy of the original database and join the username of the person who borrowed the equipment
        df3 = db.copy()[["id", "name"]]
        df3.rename({"id": "status"}, inplace=True, axis=1)
        partsWBorrow = partsDf.join(
            df3.set_index("status"),
            on="status",
            rsuffix="_borrower",
            how="left",
        )
        partsWBorrow = partsWBorrow.replace(np.nan, "")
        # Get the borrowed date
        partsWBorrow["returnDate"] = partsWBorrow.apply(lambda row: _timestampToDate(row), axis=1)
        partsShort = partsWBorrow[["name", "name_borrower", "returnDate"]]
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
        allParts = self.getParts()
        db = self._getDb()
        user = db[db.id == id]
        userDict = user.to_dict('records')
        if not userDict:
            return []
        firstMatchuser = userDict[0]
        firstMatchuser["name"]
        uName = firstMatchuser["name"]
        borrowedParts = [part for part in allParts if part[1] == uName]
        return borrowedParts

    def getOverdueEquipment(self) -> list:
        db = self._getDb()
        equipmentDf = db[db.dataType == "equipment"]
        borrowedEquipment = equipmentDf[equipmentDf.status != ""]
        weekAgo = time.time() - 60 * 60 * 24 * 7
        overdueEquipment = borrowedEquipment[
            borrowedEquipment.timestamp.astype(float) < weekAgo
        ]
        return overdueEquipment.to_dict("records")

    def appendDb(self, filename) -> None:
        """
        It reads the current database, reads the new database, combines them, removes duplicates, and saves
        the new database

        :param filename: The name of the file to be appended to the database
        """
        df1 = self._getDb()
        df2 = self._getDb(filename)
        df = pd.concat([df1, df2])
        df = df[~df.id.duplicated(keep="first")]
        self._saveDb(df)

    def exportDb(self, filename: str) -> None:
        """
        > It gets the database, saves it to a file, and returns nothing

        :param filename: The name of the file to export the database to
        :type filename: str
        """
        db = self._getDb()
        self._saveDb(db, filename)


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
