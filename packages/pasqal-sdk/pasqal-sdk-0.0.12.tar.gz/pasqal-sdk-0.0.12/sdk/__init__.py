# Copyright 2020 Pasqal Cloud Services development team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sdk.batch import Batch
from sdk.client import Client
from sdk.endpoints import Endpoints
from sdk.job import Job


class SDK:
    _client: Client

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        endpoints: Endpoints = None,
        webhook: str = None,
    ):
        self._client = Client(client_id, client_secret, endpoints)
        self.batches = {}
        self.webhook = webhook

    def create_batch(
        self,
        serialized_sequence: str,
        emulator: bool = False,
    ) -> Batch:
        """Create a new batch and send it to the API.

        Args:
            serialized_sequence: Serialized pulser sequence.
            emulator: Whether to run the batch on an emulator.
              If set to false, the device_type will be set to the one
              stored in the serialized sequence

        Returns:
            Batch: The new batch that has been created in the database.
        """
        batch_rsp = self._client._send_batch(
            {
                "sequence_builder": serialized_sequence,
                "emulator": emulator,
                "webhook": self.webhook,
            }
        )
        batch = Batch(**batch_rsp, _client=self._client)
        self.batches[batch.id] = batch
        return batch

    def get_batch(self, id: int, load_results: bool = False) -> Batch:
        """Retrieve a batch's data and all its jobs.

        Args:
            id: Id of the batch.
            load_results: whether to load job results

        Returns:
            Batch: the batch stored in the PCS database.
        """

        batch_rsp = self._client._get_batch(id)
        batch = Batch(**batch_rsp, _client=self._client)

        job_rsp = self._client._get_jobs(id, fetch_results=load_results)
        for job in job_rsp:
            batch.jobs[job["id"]] = Job(**job)

        self.batches[batch.id] = batch
        return batch
