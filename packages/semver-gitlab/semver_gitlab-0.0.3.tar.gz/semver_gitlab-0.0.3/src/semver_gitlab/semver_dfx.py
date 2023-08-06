#!/usr/bin/env python3
import os
import sys
import semver
import gitlab
import subprocess

from semver_gitlab import constants


def get_gitlab_object(token):
    # private token authentication (GitLab.com)
    gl = gitlab.Gitlab(private_token=token)
    # in on-prem, use url
    # gl = gitlab.Gitlab(url='https://gitlab.com', private_token=gitlab_private_token)
    gl.auth()
    return gl


def get_project(gl, project_id):
    project = gl.projects.get(project_id)
    return project


# retrieve the merge requests until the last release tag commit at master branch
def get_merge_requests(project, merge_commit_sha, target_branch):
    merge_requests = project.mergerequests.list(state='merged', ordered_by='merged_at')

    results = []
    try:
        for mr in merge_requests:
            if mr.merge_commit_sha == merge_commit_sha:
                break
            if mr.target_branch == target_branch:
                results.append(mr)
    except StopIteration:
        raise Exception(f"There are no merge request found!")

    return results


def get_project_merge_request_labels(merge_request):
    labels = merge_request.labels
    return labels


def get_next_bump(merge_requests):
    result = constants.PATCH_BUMP_LABEL
    for mr in merge_requests:
        if constants.MAJOR_BUMP_LABEL in mr.labels:
            result = constants.MAJOR_BUMP_LABEL
            break
        elif constants.MINOR_BUMP_LABEL in mr.labels:
            result = constants.MINOR_BUMP_LABEL

    return result


def get_project_tags(project):
    tags = project.tags.list(ordered_by='updated')
    return tags


def verify_env_var_presence(name):
    if name not in os.environ:
        raise Exception(f"Expected the following environment variable to be set: {name}")


def get_base_version(version):
    version_dict = semver.parse(version)

    major = str(version_dict["major"])
    minor = str(version_dict["minor"])
    patch = str(version_dict["patch"])

    version = major + '.' + minor + '.' + patch

    return version


def bump_prerelease(version):
    version_dict = semver.parse(version)

    major = str(version_dict["major"])
    minor = str(version_dict["minor"])
    patch = str(version_dict["patch"])
    prerelease = str(version_dict["prerelease"])

    try:
        # Get the prerelease number
        splitted_prerelease = prerelease.split(".")
        if (splitted_prerelease[0] != "alpha"):
            raise Exception(f"Not alpha found so setting alpha to version 1!")
        prerelease = int(splitted_prerelease[-1])
        prerelease = prerelease + 1
        prerelease = str(prerelease)
        prerelease = "alpha" + "." + prerelease
    except:
        # print("well, it WASN'T defined after all!")
        prerelease = "alpha.1"

    new_version = major + '.' + minor + '.' + patch + '-' + prerelease

    return new_version


def get_latest_tags(project):
    tags = get_project_tags(project)
    # TODO Handle hardcoded versions
    version = {constants.BRANCH_DEVELOP: "0.0.0",
               constants.BRANCH_RELEASE: "0.0.0",
               constants.BRANCH_MASTER: "0.0.0"}
    sha = {constants.BRANCH_DEVELOP: "",
           constants.BRANCH_RELEASE: "",
           constants.BRANCH_MASTER: ""}
    for x in tags:
        tag = x.name
        target = x.target
        if constants.PRE_RELEASE_TAG_DEVELOP in tag:
            comparison_result = semver.compare(tag, version[constants.BRANCH_DEVELOP])
            if comparison_result == 1:
                version[constants.BRANCH_DEVELOP] = tag
                sha[constants.BRANCH_DEVELOP] = target
        elif constants.PRE_RELEASE_TAG_RELEASE in tag:
            comparison_result = semver.compare(tag, version[constants.BRANCH_RELEASE])
            if comparison_result == 1:
                version[constants.BRANCH_RELEASE] = tag
                sha[constants.BRANCH_RELEASE] = target
        else:
            comparison_result = semver.compare(tag, version[constants.BRANCH_MASTER])
            if comparison_result == 1:
                version[constants.BRANCH_MASTER] = tag
                sha[constants.BRANCH_MASTER] = target

    return version, sha


def git(*args):
    return subprocess.check_output(["git"] + list(args))


def calculate_new_version(args):
    gl = get_gitlab_object(args.token)
    project = get_project(gl, args.project)
    version, sha = get_latest_tags(project)

    if constants.BRANCH_MASTER == args.branch:
        return get_base_version(version[constants.BRANCH_DEVELOP])

    # Increase alpha
    next_dev_version = bump_prerelease(version[constants.BRANCH_DEVELOP])

    merge_requests = get_merge_requests(project, sha[constants.BRANCH_MASTER], args.branch)
    # Check if development different then master
    if len(merge_requests) == 0:
        return next_dev_version

    next_bump = get_next_bump(merge_requests)

    next_master_version = ""

    if next_bump == constants.MAJOR_BUMP_LABEL:
        next_master_version = semver.bump_major(version[constants.BRANCH_MASTER])
    elif next_bump == constants.MINOR_BUMP_LABEL:
        next_master_version = semver.bump_minor(version[constants.BRANCH_MASTER])
    else:
        next_master_version = semver.bump_patch(version[constants.BRANCH_MASTER])

    # Add alpha to master
    next_master_version = bump_prerelease(next_master_version)

    comparison_result = semver.compare(next_dev_version, next_master_version)
    if comparison_result == 1:
        return next_dev_version
    elif comparison_result == -1:
        return next_master_version

    raise Exception(
        f"Comparison result occurred between new_dev_version and new_master_version, They can not be equal!")


def verify_args(args):
    if not args.token:
        raise ValueError("GitLab Access Token is missing")
    if not args.branch:
        raise ValueError("Target branch is missing")
    if not args.project:
        raise ValueError("Gitlab Project ID is missing")

    return args


def init(args):
    args = verify_args(args)

    version = calculate_new_version(args)
    print(version)

    return 0