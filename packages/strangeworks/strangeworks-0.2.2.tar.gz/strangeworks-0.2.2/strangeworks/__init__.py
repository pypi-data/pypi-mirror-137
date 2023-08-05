"""Strangeworks SDK"""

from strangeworks.annealing.annealing import Annealing
from .auth import auth
from .VERSION import VERSION as __version__
from .client import Client


# SUBMODULES = [
#     "blueqat",
#     "braket",
#     "cirq",
#     "dwave",
#     "forest",
#     "pennylane",
#     "qiskit",
#     "tket",
# ]
# PUBLIC_METHODS = ["store_config", "print", "json", "plot", "qasm_diagram", "histogram"]

client = Client()  # instantiate a client on import by default

# strangeworks.(public method)
authenticate = client.authenticate
login = auth.Login
annealing = client.annealing
rest_client = client.rest_client

# override system print on staging and production
# ENV = os.getenv("ENV")
# if ENV in ["staging", "production"]:
#    builtins.print = client._print_log

# User's should explicity import submodules like 'import strangeworks.qiskit'.
# But if they don't, provide suggestion for importing submodules and using public
# methods. And dynamically import submodule if AttributeError would be raised.
# def __getattr__(name):
#     if name in SUBMODULES:
#         suggestion = f"You must 'import {__name__}.{name}' in your code.\n"
#         sys.stderr.write(suggestion)
#         warning = rd.error("warning", suggestion)
#         client._post_result_data(warning)
#         return importlib.import_module(f"strangeworks.{name}")
#     else:
#         suggestion = (
#             f"The strangeworks submodules available to import like "
#             f"'import strangeworks.qiskit' are: "
#             f"{SUBMODULES}.\n"
#             f"The strangeworks public methods available to use like "
#             f"'strangeworks.print(\"hello world\")' are: "
#             f"{PUBLIC_METHODS}.\n"
#         )
#         sys.stderr.write(suggestion)
#         raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
