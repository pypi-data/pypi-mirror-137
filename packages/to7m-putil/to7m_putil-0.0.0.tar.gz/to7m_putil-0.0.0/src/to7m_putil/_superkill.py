#!/usr/bin/env python3


import sys, os, signal, argparse
from psutil import process_iter
from fnmatch import fnmatch
from time import sleep
from shlex import quote


def gather_processes(patterns, current_pid):
    matches = []
    for process in process_iter(['pid', 'cmdline']):
        if process.info['cmdline'] and process.info['pid'] != current_pid:
            process_command = " ".join(process.info['cmdline'])
            pattern = 0
            match_found = False
            while pattern < len(patterns) and match_found is False:
                if fnmatch(process_command, patterns[pattern]):
                    matches.append((process.info['pid'], process_command))
                    match_found = True
                pattern += 1
    return matches


def stringify_processes(processes):
    strings = [str(process) for process in processes]
    return "\n".join(strings)


def convert_attempts_string_to_list(attempts_string):
    waits_for_methods = attempts_string.split(",")
    methods_dict = {"TERM": signal.SIGTERM, "INT": signal.SIGINT,
                    "HUP": signal.SIGHUP, "KILL": signal.SIGKILL}
    attempt_tasks = []
    for method in range(len(waits_for_methods)):
        method_and_waits = waits_for_methods[method].split(":")
        if method_and_waits[0] not in methods_dict:
            raise SystemExit(f"invalid method: {method_and_waits[0]}")
        if len(method_and_waits) < 2:
            raise SystemExit(
                      f"wait time not provided: {method_and_waits[method]}")
        for wait in range(1, len(method_and_waits)):
            try:
                wait = float(method_and_waits[wait])
            except:
                raise SystemExit(f"invalid number: {wait}")
            attempt_tasks.append((methods_dict[method_and_waits[0]],
                                  wait))
    return attempt_tasks


def convert_attempts_list_to_text(attempts_list):
    text_list = []
    for attempt in attempts_list:
        if attempt[1] == 1:
            time_unit = "second"
        else:
            time_unit = "seconds"
        text_list.append(f"wait on signal {attempt[0]}"
                         + f" for {attempt[1]} {time_unit}")
    return ",\nthen ".join(text_list)


def kill_procedure(verbose, attempts_string, loop, patterns, current_pid):
    attempts_list = convert_attempts_string_to_list(attempts_string)
    if verbose:
        print(convert_attempts_list_to_text(attempts_list))
    remaining_matches = gather_processes(patterns, current_pid)
    if not remaining_matches:
        if verbose:
            print("no matches found")
        return
    for attempt in attempts_list:
        method, wait = attempt
        if verbose:
            print(f"attempting signal {method}"
                  + " to kill the following processes:")
            print(stringify_processes(remaining_matches))
        for process in remaining_matches:
            try:
                os.kill(process[0], method)
            except:
                if verbose:
                    print(f"process {process} not found"
                          + ";\nmust have died from something else")
        if verbose:
            if wait == 1:
                time_unit = "second"
            else:
                time_unit = "seconds"
            print(f"waiting {wait} {time_unit}")
        sleep(wait)
        remaining_matches = gather_processes(patterns, current_pid)
        if not remaining_matches:
            if verbose:
                print("all matches successfully killed")
            return
    if loop:
        method, wait = attempts_list[-1]
        if verbose:
            if wait == 1:
                time_unit = "second"
            else:
                time_unit = "seconds"
        while remaining_matches:
            if verbose:
                print(f"attempting signal {method} on loop"
                    + " to kill the following processes:")
                print(stringify_processes(remaining_matches))
            for process in remaining_matches:
                try:
                    os.kill(process[0], method)
                except:
                    if verbose:
                        print(f"process {process} not found"
                              + ";\nmust have died from something else")
            if verbose:
                print(f"waiting {wait} {time_unit}")
            sleep(wait)
            remaining_matches = gather_processes(patterns, current_pid)
            if not remaining_matches:
                if verbose:
                    print("all matches successfully killed")
                return
    else:
        if verbose:
            print("failed to kill the following processes:")
            processes_list = gather_processes(patterns, current_pid)
            print(f"{stringify_processes(processes_list)}")


def superkill(
        patterns=[], predecessor=False,
        list_mode=False, verbose=False, loop=False,
        attempts_string="TERM:0:0.01:0.1:0.3:1,INT:0.1:1,HUP:1,KILL:1,KILL:3"):
    patterns = [patterns] if type(patterns) is str else patterns

    if predecessor:
        patterns.append(f"*{quote(sys.argv[0])}*")

    current_pid = os.getpid()
    if list_mode:
        if patterns:
            if verbose:
                print(f"searching for the following patterns: {patterns}")
        else:
            patterns = ["*"]
        processes_string = stringify_processes(gather_processes(patterns,
                                                                current_pid))
        if processes_string:
            print(processes_string)
    else:
        if patterns:
            kill_procedure(
                verbose, attempts_string, loop, patterns, current_pid)
        else:
            print("at least one pattern must be provided")
