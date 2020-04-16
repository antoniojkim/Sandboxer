
import os
import pathlib

import argparse
import subprocess
from shutil import copyfile

from datetime import datetime


curr_dir = os.getcwd()
sandbox_dir = os.path.join(curr_dir, ".sandbox")
file_dir = pathlib.Path(__file__).parent.absolute()
template_dir = os.path.join(file_dir, ".templates")

if not os.path.isdir(sandbox_dir):
    os.mkdir(sandbox_dir)


def create(args):
    if args.name is None:
        raise NameError("Name required to create new sandbox")

    name = args.name
    new_sandbox_dir = os.path.join(sandbox_dir, name)
    if os.path.isfile(new_sandbox_dir):
        if args.force:
            name = f"{name}__{datetime.now().strftime('%Y-%m-%d__%H-%M-%S')}"
            new_sandbox_dir = os.path.join(sandbox_dir, name)
        else:
            raise ValueError(f"{name} sandbox already exists!")

    os.mkdir(new_sandbox_dir)

    for template in os.listdir(template_dir):
        copyfile(os.path.join(template_dir, template),
                 os.path.join(new_sandbox_dir, template))

    with open(os.path.join(sandbox_dir, ".info"), "w") as file:
        file.write(name)


def build(args):
    if args.name is not None:
        recent_sandbox_dir = os.path.join(sandbox_dir, args.name)
    else:
        with open(os.path.join(sandbox_dir, ".info")) as file:
            sandbox = file.read()
            recent_sandbox_dir = os.path.join(sandbox_dir, sandbox)

    os.chdir(recent_sandbox_dir)

    if args.lang == "c++":
        make = subprocess.Popen("make", shell=True)
        make.communicate()
        if make.returncode == 0:
            run = subprocess.Popen("./sandbox", shell=True)
            run.communicate()

    elif args.lang == "python":
        run = subprocess.Popen(f"python -u sandbox.py", shell=True)
        run.communicate()

    os.chdir(curr_dir)


def clean(args):
    for sandbox in os.listdir(sandbox_dir):
        if os.path.isdir(sandbox) and sandbox not in (".sandbox", ".templates"):
            for sandbox_file in os.listdir(os.path.join(sandbox_dir, sandbox)):
                if os.path.isfile(os.path.join(template_dir, sandbox_file)):
                    with open(os.listdir(os.path.join(sandbox_dir, sandbox, sandbox_file))) as file:
                        sandbox_contents = file.read()

                    with open(os.listdir(os.path.join(template_dir, sandbox, sandbox_file))) as file:
                        template_contents = file.read()

                    if sandbox_contents.strip() == template_contents.strip():
                        os.remove(os.listdir(os.path.join(sandbox_dir, sandbox, sandbox_file)))                


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name",
                        default=None,
                        nargs='?',
                        help="name of sandbox")
    parser.add_argument('--lang',
                        default='c++',
                        nargs='?',
                        choices=['c++', 'python', 'py'],
                        help='sandbox language (default: %(default)s)')
    parser.add_argument('--force', '-f',
                        action="store_true",
                        help='Forces sandbox action')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--create", action="store_true")
    group.add_argument("--build", action="store_true")
    group.add_argument("--clean", action="store_true")

    args = parser.parse_args()

    if args.lang is None:
        args.lang = "c++"
    elif args.land == "py":
        args.lang = "python"

    if args.create:
        create(args)
    elif args.build:
        build(args)
    elif args.clean:
        clean(args)


if __name__ == "__main__":
    main()
