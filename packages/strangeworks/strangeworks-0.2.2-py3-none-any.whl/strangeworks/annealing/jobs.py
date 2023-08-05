from strangeworks.annealing.backends import Backend
from strangeworks.errors.error import StrangeworksError
from strangeworks.rest_client.rest_client import StrangeworksRestClient
import datetime, json, time


class Job:

    COMPLETED = "completed"
    QUEUED = "queued"
    RUNNING = "running"
    FAILED = "failed"
    CANCELLED = "cancelled"
    CREATED = "created"

    __terminal_states = [COMPLETED, FAILED, CANCELLED]

    def __init__(
        self,
        id: str = None,
        remote_id: str = None,
        backend: Backend = None,
        rest_client: StrangeworksRestClient = None,
        wait_timeout: int = None,
        status: str = None,
        results: dict = {},
        slug: str = None,
    ):
        self.__id = id
        self.__remote_id = remote_id
        self.__backend = backend
        self.__rest_client = rest_client
        self.__wait_timeout = wait_timeout
        self.__status = status
        self.__results = results
        self.__slug = slug

    @classmethod
    def from_json(
        cls,
        job: dict = {},
        backend: Backend = None,
        rest_client: StrangeworksRestClient = None,
    ) -> "Job":
        id = job.get("id", "")
        remote_id = job.get("remot_id", "")
        return cls(id=id, remote_id=remote_id, backend=backend, rest_client=rest_client)

    def results(self):
        """
        waits for job completion. on error raises excetion with error.
        otherwise accepts and formats results for utilization
        """
        self.__wait_for_result()
        return self.__results

    # assumes your Job.Status is in a JOB_FINAL_STATE
    def __wait_for_result(self):
        wait = 5
        result = None
        start_time = datetime.datetime.now()
        while self.__status not in self.__terminal_states:
            response = self.__rest_client.get(f"/jobs/{self.__id}?include=result_data")
            if "status" in response:
                self.__status = response["status"]
                if self.__status == self.COMPLETED and "sdkResult" in response:
                    sdk_results = response["sdkResult"]
                    if "data" in sdk_results:
                        self.__results = json.loads(sdk_results["data"])
            time.sleep(wait)
            if self.__wait_timeout is not None and (
                (datetime.datetime.now().second - start_time.second)
                > self.__wait_timeout
            ):
                raise StrangeworksError.timeout(
                    message=f"timeout attempting to fetch results after {self.__wait_timeout}"
                )

        if self.__status == self.FAILED:
            raise StrangeworksError(
                f"Unable to get a result from an errored job {self.__slug()}"
            )

        if self.__status == self.CANCELLED:
            raise StrangeworksError(
                f"Unable to get a result from a cancelled job {self.__slug()}"
            )
