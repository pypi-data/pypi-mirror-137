# Copyright (c) 2021, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a pandas extension to tabular chemical structures."""


import logging
import re
from pathlib import Path
from typing import Iterable, Union

import pandas as pd
from pandas.api.extensions import register_dataframe_accessor

from .structure import Structure
from .structure_identifier import StructureIdentifier


logger = logging.getLogger(__name__)


@register_dataframe_accessor("cheminfo")
class StructuresTable:
    """Define a cheminformatics extension for tabular chemical structures."""

    def __init__(self, data_frame: pd.DataFrame) -> None:
        """Validate and initialize the cheminformatics extension."""
        self._columns = ["inchikey", "inchi", "smiles"]
        self._inchikey_pattern = re.compile(r"[A-Z]{14}-[A-Z]{10}-[A-Z]")
        # Match the proton sublayer until the next layer or until the end of the string.
        self._proton_layer_pattern = re.compile(r"/p.*?(/|$)")
        self._validate(data_frame)
        self._df = data_frame

    @classmethod
    def make_from_file(cls, structures: Path, delimiter: str = "\t") -> pd.DataFrame:
        """Extract and transform chemical structures from the given tabular file."""
        assert structures.is_file(), f"'{structures}' was not found."
        logger.info("Extract chemical structures.")
        raw = pd.read_csv(structures, sep=delimiter)
        logger.info(f"Found {len(raw):n} entries.")
        logger.info("Transform chemical structures.")
        logger.debug("Ignore rows with missing InChIs.")
        result = raw.loc[raw["inchi"].notnull(), :].cheminfo.neutralize_protonation()
        logger.info(f"Maintained {len(result):n} entries.")
        assert len(result["inchikey"].unique()) == len(
            result
        ), "InChIKeys are not unique even though they *should* be."
        return result

    def _validate(self, df: pd.DataFrame) -> None:
        self._validate_headers(df)
        self._validate_dtypes(df)
        self._validate_inchikey(df)
        self._validate_inchi(df)

    def _validate_headers(self, df: pd.DataFrame) -> None:
        assert set(self._columns).issubset(df.columns), (
            "The pandas.DataFrame must contain the columns with headers inchikey, "
            "inchi, and smiles."
        )

    def _validate_dtypes(self, df: pd.DataFrame) -> None:
        for col in self._columns:
            assert isinstance(
                df[col].dtype, (pd.StringDtype, object)
            ), f"The {col} column must contain strings, not {df[col].dtype}."

    def _validate_inchikey(self, df: pd.DataFrame) -> None:
        mask = df["inchikey"].str.fullmatch(self._inchikey_pattern, na=False)
        num_invalid = (~mask).sum()
        assert (
            num_invalid == 0
        ), f"{num_invalid:n} ({num_invalid / len(mask):.2%}) InChIKeys are invalid."

    def _validate_inchi(self, df: pd.DataFrame) -> None:
        mask = df["inchi"].str.startswith("InChI=1")
        num_invalid = (~mask).sum()
        assert (
            num_invalid == 0
        ), f"{num_invalid:n} ({num_invalid / len(mask):.2%}) InChIs are invalid."

    def neutralize_protonation(self, inplace: bool = False) -> pd.DataFrame:
        """
        Neutralize protonation on both the InChIKey and InChI columns.

        Parameters
        ----------
        inplace
            Whether or not the table should be overwritten (default False).

        Returns
        -------
        pandas.DataFrame
            The transformed data frame which is deduplicated by InChIKey and InChI.

        """
        if inplace:
            result = self._df
        else:
            result = self._df.copy()
        result.loc[:, "inchikey"] = self._df["inchikey"].str[:-1] + "N"
        result.loc[:, "inchi"] = self._df["inchi"].str.replace(
            pat=self._proton_layer_pattern, repl=r"\g<1>", n=1
        )
        return result.drop_duplicates(["inchikey", "inchi"], inplace=inplace)

    def iter_structures(self) -> Iterable[Structure]:
        """Iterate over chemical structures in the table."""
        return (
            Structure(
                identifier=StructureIdentifier(inchikey=row.inchikey, inchi=row.inchi),
                smiles=None if pd.isnull(row.smiles) else row.smiles,
            )
            for row in self._df.itertuples(index=False)
        )
