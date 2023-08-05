from strangeworks.annealing.backends import Backend
from strangeworks.annealing.jobs import Job
from strangeworks.errors.error import StrangeworksError
from strangeworks.rest_client.rest_client import StrangeworksRestClient
from typing import Dict, Tuple
import uuid


class Annealing:
    """
    Annealing client for direct access to annealing machines.
    """

    # TODO: replace this w/ annealing service url, currently only aws is supported
    __base_url = "/plugins/aws"

    def __init__(
        self,
        rest_client: StrangeworksRestClient = None,
        result_id: str = None,
        problem_path: str = None,
        backend: str = "",
        backends: list = [],
    ):
        self.__rest_client = rest_client
        if self.__rest_client is None:
            raise StrangeworksError.invalid_argument(
                message="must include rest_client when initializing Annealing class, try using the default Annealing client: strangeworks.annealing...",
            )
        self.__backend = backend
        self.__problem_path = problem_path
        self.__result_id = result_id
        self.__backends = backends

    def _new_client(self, rest_client: StrangeworksRestClient = None):
        self.__rest_client = rest_client

    def get_backends(self, selected_backend: str = None, pprint: bool = False):
        """
        Fetches available annealing backends for a user,
        stores backends for quick access,
        allow user to select a backend for immediate use,
        and pretty print backend name
        """
        response = self.__rest_client.get(f"{self.__base_url}/backends/annealing")
        for backend_name in response:
            self.__backends.append(backend_name)
            if selected_backend is not None and selected_backend == backend_name:
                self.__backend = backend_name
            # pprint backends if user sets option to true
            if pprint:
                print("=" * 50)
                print(f"Backend name: {backend_name}")
                print(f"Backend provider: AWS Braket")

    def select_backend(self, selected_backend: str = None):
        if selected_backend not in self.__backends:
            raise StrangeworksError.invalid_argument(
                f"Backend {selected_backend} not available"
            )
        self.__backend = selected_backend

    def upload_problem(file_path: str = ""):
        """Uploads a qubo file to Strangeworks to allow for larger problems to be defined"""
        raise StrangeworksError.not_implemented()

    def run(
        self,
        quadratic: Dict[Tuple[int, int], float] = None,
        linear: Dict[int, float] = None,
        problem_type: str = None,
        problem_path: str = None,
        shots: int = 1,
        backend: str = None,
    ) -> Job:
        """Low level annealing executor. Assumes user has already embedded problem to device target"""

        if backend is None:
            backend = self.__backend

        # create a new result for each job unless the user specifies a result in the client
        result_id = (
            self.__result_id if self.__result_id is not None else str(uuid.uuid4())
        )
        payload = {
            "target": self.__backend,
            "result_id": result_id,
            "shots": shots,
        }

        if problem_type is not None:
            payload["problem_type"] = problem_type

        # TODO: Allow uploading for problems
        problem_exists = False
        if problem_path is not None or self.__problem_path is not None:
            problem_exists = True
            raise StrangeworksError.not_implemented()

        # convert quadratic for serialization
        if quadratic is not None and linear is not None:
            nq = {}
            for v in quadratic:
                k = ",".join(map(str, v))
                nq[k] = quadratic[v]
            qb = {}
            qb["quadratic"] = nq
            qb["linear"] = linear
            payload["qubo"] = qb
            problem_exists = True

        # raise an exception if user has not provided a problem to solve
        if not problem_exists:
            raise StrangeworksError.invalid_argument(
                "must include problem to execute on annealing device"
            )

        # post to the correct plugin and return a job
        response = self.__rest_client.post(
            url=f"{self.__base_url}/run-annealing-job",
            json=payload,
            expected_response=200,
        )
        return Job.from_json(
            job=response, backend=self.__backend, rest_client=self.__rest_client
        )

    def __is_valid_uuid(self, value):
        if len(value) != 36:
            return False
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False
