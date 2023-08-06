# -*- coding: utf-8 -*-
"""CCURE class file."""

from bits.mssql import MSSQL
from .update import Update


class CCURE(MSSQL):
    """CCURE class."""

    def __init__(self, server, user, password, database, verbose=False):
        """Initialize an CCURE class instance."""
        MSSQL.__init__(self, server, user, password, database, verbose)
        self.verbose = verbose

    def get_credentials(self):
        """Return a list of all Credentials in CCURE."""
        return self.get_table("Credential")

    def get_personnel(self):
        """Return a list of all Personnel in CCURE."""
        return self.get_table("Personnel")

    def get_personnel_types(self):
        """Return a list of all Personnel Types in CCURE."""
        return self.get_table("PersonnelType")

    def get_images(self):
        """REturn a list of all Photos in CCURE."""
        return self.get_table("Images")

    def get_table(self, table):
        """Return a list of all rows in the given table."""
        query = f"SELECT * FROM Access.{table};"
        self.cursor.execute(query)
        return list(self.cursor.fetchall())

    def update(
        self,
        credentials_path="credentials.csv",
        newpersonnel_path="newpersonnel.csv",
        personnel_path="personnel.csv",
    ):
        """Return an Update object for CCURE."""
        return Update(
            ccure=self,
            credentials_path=credentials_path,
            newpersonnel_path=newpersonnel_path,
            personnel_path=personnel_path,
        )
