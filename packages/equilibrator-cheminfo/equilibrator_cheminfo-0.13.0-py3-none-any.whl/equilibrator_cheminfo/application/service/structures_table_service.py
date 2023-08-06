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


"""Provide a service that coordinates the transformation of structures."""


import logging
import multiprocessing
from pathlib import Path
from typing import Type

import pandas as pd
from tqdm import tqdm

from equilibrator_cheminfo.domain.model import AbstractMolecularEntityRepository

from .abstract_molecular_entity_service import AbstractMolecularEntityService
from .create_molecular_entities_from_table_command import (
    CreateMolecularEntitiesFromTableCommand,
)


logger = logging.getLogger(__name__)


class StructuresTableService:
    """Define a service that coordinates the transformation of structures."""

    def __init__(
        self,
        *,
        molecular_entity_repository: AbstractMolecularEntityRepository,
        molecular_entity_service: Type[AbstractMolecularEntityService],
        **kwargs,
    ) -> None:
        """Initialize a structures table service with correct sub-service instances."""
        super().__init__(**kwargs)
        self._repo = molecular_entity_repository
        self._service = molecular_entity_service

    def transform(
        self, command: CreateMolecularEntitiesFromTableCommand, log_file: Path
    ) -> None:
        """Transform a structures table into a database of molecular entities."""
        if command.processes > 1:
            self._concurrently(
                self._filter_keys(command.structures), command, log_file=log_file
            )
        else:
            self._sequentially(
                self._filter_keys(command.structures), command, log_file=log_file
            )
        self._repo.log_summary()

    def _filter_keys(self, structures: pd.DataFrame) -> pd.DataFrame:
        """Filter the structures by known InChIKeys."""
        return structures.loc[
            ~structures["inchikey"].isin(self._repo.get_inchikeys()), :
        ]

    def _sequentially(
        self,
        structures: pd.DataFrame,
        command: CreateMolecularEntitiesFromTableCommand,
        log_file: Path,
    ) -> None:
        """Coordinate predictions on all structures sequentially and load results."""
        self._service.setup(
            command.minimum_ph,
            command.maximum_ph,
            command.fixed_ph,
            command.use_large_model,
            log_file,
        )
        for structure in tqdm(
            structures.cheminfo.iter_structures(),
            total=len(structures),
            desc="Molecular Entity",
            unit_scale=True,
        ):
            if (entity := self._service.run(structure)) is not None:
                self._repo.add(entity)

    def _concurrently(
        self,
        structures: pd.DataFrame,
        command: CreateMolecularEntitiesFromTableCommand,
        log_file: Path,
        batch_size: int = 1000,
    ) -> None:
        """Coordinate predictions on all structures concurrently and load results."""
        args = list(structures.cheminfo.iter_structures())
        chunk_size = min(max(len(args) // command.processes, 1), batch_size)
        with multiprocessing.get_context("spawn").Pool(
            processes=command.processes,
            initializer=self._service.setup,
            initargs=(
                command.minimum_ph,
                command.maximum_ph,
                command.fixed_ph,
                command.use_large_model,
                log_file,
            ),
        ) as pool:
            result_iter = pool.imap_unordered(
                self._service.run,
                args,
                chunksize=chunk_size,
            )
            for molecular_entity in (
                result
                for result in tqdm(
                    result_iter,
                    total=len(args),
                    desc="Molecular Entity",
                    unit_scale=True,
                )
                if result is not None
            ):
                self._repo.add(molecular_entity)
