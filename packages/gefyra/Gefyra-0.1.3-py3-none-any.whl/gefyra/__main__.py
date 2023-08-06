#!/usr/bin/env python3
import argparse
import logging
import sys

from gefyra.api import (
    bridge,
    down,
    run,
    up,
    unbridge,
    unbridge_all,
    list_interceptrequests,
)
from gefyra.local.check import probe_nsenter, probe_kubernetes, probe_docker

console = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter("[%(levelname)s] %(name)s %(message)s")
formatter = logging.Formatter("[%(levelname)s] %(message)s")
console.setFormatter(formatter)

logger = logging.getLogger("gefyra")


parser = argparse.ArgumentParser(description="Gefyra Client")
action = parser.add_subparsers(dest="action", help="the action to be performed")
parser.add_argument("-d", "--debug", action="store_true", help="add debug output")

up_parser = action.add_parser("up")
run_parser = action.add_parser("run")
run_parser.add_argument(
    "-i", "--image", help="the docker image to run in Gefyra", required=True
)
run_parser.add_argument(
    "-N", "--name", help="the name of the container running in Gefyra", required=True
)
run_parser.add_argument(
    "-n",
    "--namespace",
    help="the namespace for this container to run in",
    default="default",
)
run_parser.add_argument(
    "--env",
    action="append",
    help="set or override environment variables in the form ENV=value, allowed multiple times",
    required=False,
)
run_parser.add_argument(
    "--env-from",
    help="copy the environment from the container in the notation 'Pod/Container'",
    required=False,
)
bridge_parser = action.add_parser("bridge")
bridge_parser.add_argument(
    "-N", "--name", help="the name of the container running in Gefyra", required=True
)
bridge_parser.add_argument(
    "-C",
    "--container-name",
    help="the name for the locally running container",
    required=True,
)
bridge_parser.add_argument(
    "-I", "--bridge-name", help="the name of the bridge", required=False
)
bridge_parser.add_argument(
    "-p", "--port", help="the port to send the traffic to", required=True
)
bridge_parser.add_argument(
    "-n",
    "--namespace",
    help="the namespace for this container to run in",
    default="default",
)
intercept_flags = [
    {"name": "deployment"},
    {"name": "statefulset"},
    {"name": "pod"},
    {"name": "container"},
    {"name": "container-port"},
]
for flag in intercept_flags:
    bridge_parser.add_argument(f"--{flag['name']}")

down_parser = action.add_parser("down")
unbridge_parser = action.add_parser("unbridge")
unbridge_parser.add_argument("-N", "--name", help="the name of the intercept request")
unbridge_parser.add_argument(
    "-A", "--all", help="removes all current intercept requests", action="store_true"
)
list_parser = action.add_parser("list")
list_parser.add_argument(
    "--containers", help="list all containers running in Gefyra", action="store_true"
)
list_parser.add_argument(
    "--bridges", help="list all active bridges in Gefyra", action="store_true"
)
check_parser = action.add_parser("check")


def get_intercept_kwargs(parser_args):
    kwargs = {}
    for flag in intercept_flags:
        _f = flag["name"].replace("-", "_")
        if getattr(parser_args, _f):
            kwargs[_f] = getattr(parser_args, _f)
    return kwargs


def main():
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(console)
    if args.action == "up":
        up()
    elif args.action == "run":
        run(
            image=args.image,
            name=args.name,
            namespace=args.namespace,
            env_from=args.env_from,
            env=args.env,
        )
    elif args.action == "bridge":
        bridge(
            args.name,
            args.port,
            container_name=args.container_name,
            namespace=args.namespace,
            bridge_name=args.bridge_name,
            **get_intercept_kwargs(args),
        )
    elif args.action == "unbridge":
        if args.name:
            unbridge(args.name)
        elif args.all:
            unbridge_all()
    elif args.action == "list":
        if args.containers:
            pass
        elif args.bridges:
            ireqs = list_interceptrequests()
            if ireqs:
                for ireq in ireqs:
                    print(ireq)
            else:
                logger.info("No active bridges found")
    elif args.action == "down":
        down()
    elif args.action == "check":
        probe_nsenter()
        probe_docker()
        probe_kubernetes()
    else:
        logger.error(
            f"action must be one of [up, run, bridge, unbridge, list, down, check], got {args.action}"
        )


if __name__ == "__main__":  # noqa
    main()
