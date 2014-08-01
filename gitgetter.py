#!/usr/bin/env python


import subprocess

"""
Adapted from:
    https://github.com/paulrademacher/gitjson/

The MIT License (MIT)

Copyright (c) 2014 Paul Rademacher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

class NotAGitRepo(Exception):
    pass

class UnknownGitError(Exception):
    pass

def git_log():

    START_OF_COMMIT = "@@@@@@@@@@"

    args = ["log",
            "--pretty=tformat:" + START_OF_COMMIT + "%n%h%n%aN%n%aE%n%at%n%ai%n%p%n%t%n%s",
            "--date=local",
            "--numstat"]

    # @ksikka improved error handling
    p = subprocess.Popen(["git"] + args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, err = p.communicate()
    retcode = p.wait()
    if retcode != 0:
        if retcode == 128 and 'fatal: Not a git repository (or any of the parent directories): .git' in err:
            raise NotAGitRepo
        else:
            raise UnknownGitError

    # Step through output, parsing each commit.
    commits = []
    lines = output.split("\n")

    i = 0
    while i < len(lines):
        if not lines[i]:
            # End of log.
            break

        i += 1  # Skip the START_OF_COMMIT marker.

        sha = lines[i]
        name = lines[i+1]
        email = lines[i+2]
        date = lines[i+3]
        date_iso = lines[i+4]
        parents = lines[i+5].split(" ")
        tree = lines[i+6]
        subject = lines[i+7]
        i += 8

        files = []

        # If there is a numstat, process it.
        if lines[i] != START_OF_COMMIT:
            i += 1  # Skip blank line before numstat.

            # Read the numstat.
            while i < len(lines) and lines[i] and \
                    (lines[i][0].isdigit() or lines[i][0] == '-'):
                fields = lines[i].split("\t")
                files.append({'ins': fields[0], 'del': fields[1], 'path': fields[2]})
                i += 1

        # @ksikka reduced complexity
        commit = {}
        commit['sha'] = sha
        commit['name'] = name
        commit['email'] = email
        commit['date'] = date
        commit['date_iso'] = date_iso
        commit['subject'] = subject
        commit['files'] = files
        commit['parents'] = parents
        commit['tree'] = tree

        commits.append(commit)

    return commits

if __name__ == '__main__':
    print git_log()
