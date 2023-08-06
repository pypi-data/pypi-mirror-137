# Copyright Contributors to the Testing Farm project.
# SPDX-License-Identifier: Apache-2.0
"""
The module provides schemes of test requests
"""
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    Field,
    HttpUrl,
    validator,
)

from ..database import RequestStateType
from ..errors import UnprocessableEntityError


class ArtifactTypes(str, Enum):
    """
    Artifact type represents an artifact type which was built by a specific instance of a build system.
    """

    FEDORA_KOJI_BUILD = 'fedora-koji-build'
    BODHI_UPDATE = 'bodhi-update'
    FEDORA_COPR_BUILD = 'fedora-copr-build'
    PACKAGE = 'package'
    REPOSITORY = 'repository'


class Architectures(str, Enum):
    """
    Force the given architecture of the test environment to provision.
    """

    X86_64 = 'x86_64'
    S390X = 's390x'
    AARCH64 = 'aarch64'
    PPC64LE = 'ppc64le'


class NoteLevels(str, Enum):
    """
    Level of the note.
    """

    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


class TestStageResults(str, Enum):
    """
    Result of the test stage.
    """

    PASSED = 'passed'
    FAILED = 'failed'
    SKIPPED = 'skipped'


class TestStates(str, Enum):
    """
    State of the request
    """

    NEW = 'new'
    QUEUED = 'queued'
    RUNNING = 'running'
    ERROR = 'error'
    COMPLETE = 'complete'


class TestOverallResults(str, Enum):
    """
    Overall result of testing the request. Special value `unknown` means that result could not be determined.
    The overall result `error` was added because some test frameworks recognize this state
    themselves, e.g. tmt.
    """

    PASSED = 'passed'
    FAILED = 'failed'
    SKIPPED = 'skipped'
    UNKNOWN = 'unknown'
    ERROR = 'error'


class TestFMF(BaseModel):
    """
    Run all plans according to the TMT/FMF definition.
    Unique remote identifier of the FMF metadata as
    described in [documentation](https://fmf.readthedocs.io/en/latest/concept.html#identifiers).
    """

    url: HttpUrl = Field(
        ...,
        description=(
            'Git repository containing the metadata tree. Use any format acceptable by the git clone command.'
        ),
    )
    ref: Optional[str] = Field(
        'master',
        description=(
            'Branch, tag or commit specifying the desired git revision. '
            'This is used to perform a git checkout in the repository.'
        ),
    )
    path: Optional[str] = Field(
        '.',
        description=(
            'Path to the metadata tree root. '
            'Should be relative to the git repository root provided in the `url` parameter.'
        ),
    )
    name: Optional[str] = Field('/', description=('Node name as defined by the hierarchy in the metadata tree.'))


class TestSTI(BaseModel):
    """
    Run STI tests from the given GIT repository.
    """

    url: HttpUrl = Field(
        ...,
        description=('Git repository containing the STI tests. Use any format acceptable by the git clone command.'),
    )
    ref: str = Field(
        ...,
        description=(
            'Branch, tag or commit specifying the desired git revision. '
            'This is used to perform a git checkout in the repository.'
        ),
    )
    playbooks: Optional[List[str]] = Field(
        ['tests/tests*.yml'],
        description=(
            'Playbooks to run from the given repositories. Globbing is supported. '
            'By default standard `tests/tests*.yml` is used.'
        ),
    )
    extra_variables: Optional[List[Dict[str, str]]] = Field(
        None,
        description=(
            'A mapping of Ansible extra variable names to values, which will be passed to `ansible-playbook`.'
        ),
    )


class TestScript(BaseModel):
    """
    Run given scripts from the given GIT repository in the default shell.
    """

    url: HttpUrl = Field(
        ..., description=('Git repository containing the scripts. Use any format acceptable by the git clone command.')
    )
    ref: str = Field(
        ...,
        description=(
            'Branch, tag or commit specifying the desired git revision. '
            'This is used to perform a git checkout in the repository.'
        ),
    )
    script: List[str] = Field(
        ...,
        description=(
            'Scripts to run. Script is a command executed from the root of the cloned directory om the given '
            'test environment. More commands can be specified. Each command is asserted on return code 0.'
        ),
    )


class Test(BaseModel):
    """
    Details about the test to run. Only one test type can be specified.
    If the user needs to run multiple tests, it should do it in separate requests.
    """

    fmf: Optional[TestFMF] = Field(
        None,
    )
    script: Optional[TestScript] = Field(
        None,
    )
    sti: Optional[TestSTI] = Field(
        None,
    )


class Artifact(BaseModel):
    """
    Additional artifact to install in the test environment.
    """

    id: str = Field(
        ...,
        description=(
            'Unique identifier of the artifact. Value depends on the type of the artifact.\n\n'
            '* fedora-koji-build - use task ID of the koji build task, e.g. 43054146\n'
            '* bodhi-update - use the bodhi update identifier, e.g. FEDORA-2020-6cdec13e90\n'
            '* fedora-copr-build - use the copr build-id:chroot-name, e.g. 1784470:fedora-32-x86_64\n'
            '* package - use any identifier which the package manager '
            'understands, e.g. openssh, openssh-8.2p1-73.f33, etc.\n'
            '* repository - baseurl of an RPM repository to install packages from, e.g. https://my.repo/repository\n'
        ),
    )
    type: ArtifactTypes = Field(
        ...,
    )
    packages: Optional[List[str]] = Field(
        None,
        description=(
            'List of packages to install, if applicable to the artifact. '
            'By default all packages from the artifact are installed. '
            'Use any identifier which the package manager understands, e.g. openssh, openssh-8.2p1-73.f33, etc.'
        ),
    )


class EnvironmentSettings(BaseModel):
    """
    Various environment settings or tweaks.
    """

    reboot: bool = Field(
        False,
        description=(
            'In some cases the users would like to reboot the system after artifacts installation. '
            'To instruct Testing Farm to attempt a restart and run tests after a successful boot, '
            'set this setting to `true`. Defaults to `false`, no restart is done by default.'
        ),
    )


class Tmt(BaseModel):
    """
    Special environment settings for `tmt` tool.
    """

    context: Dict[str, str] = Field(
        ...,
        description=(
            'A mapping of tmt context variable names to values. For more information about tmt context '
            'see [documentation](https://tmt.readthedocs.io/en/latest/spec/context.html).'
        ),
    )


class Os(BaseModel):
    """
    Identifies the operating system used for the test environment.
    """

    compose: str = Field(
        ...,
        description=(
            'Specify the compose of the operating system by its ID. Let Testing Farm choose the best '
            'infrastructure pool for execution. Both specific IDs and symbolic names can be specified. '
            'Symbolic names are translated to specific IDs according to the following logic:\n'
            '* Fedora - translates to latest stable Fedora image\n'
            '* Fedora-Rawhide - translates to latest Fedora Rawhide image\n'
            '* Fedora-XY - translates to latest available Fedora XY image\n'
            '* Fedora-Rawhide-20200402.n.0 - a concrete Fedora Rawide image\n\n'
            'Please note by default the translation of the ID is done only to VM images, '
            'if you want to run the test in container, specify the pool type to `container`.'
        ),
    )


class EnvironmentRequested(BaseModel):
    """
    Requested test environment to provision.
    """

    arch: Architectures = Field(
        ...,
    )
    os: Optional[Os] = Field(
        None,
    )
    pool: Optional[str] = Field(
        None,
        description=(
            'Name of the infrastructure pool to use. If not chosen, Testing Farm will choose the most suitable pool.'
        ),
    )
    variables: Optional[Dict[Any, Any]] = Field(
        None,
        description=(
            'A mapping of environment variable names to values, which will be exported in the test environment.'
        ),
    )
    artifacts: Optional[List[Artifact]] = Field(
        None, description=('Additional artifacts to install in the test environment.')
    )
    settings: Optional[EnvironmentSettings] = Field(
        None,
    )
    tmt: Optional[Tmt] = Field(
        None,
    )


class EnvironmentProvisioned(BaseModel):
    """
    Provisioned test environment.
    """

    arch: Architectures = Field(
        ...,
    )
    os: Optional[Os] = Field(
        None,
    )
    pool: Optional[str] = Field(
        None,
        description=(
            'Name of the infrastructure pool to use. If not chosen, Testing Farm will choose the most suitable pool.'
        ),
    )


class Note(BaseModel):
    """
    Note produced by Testing Farm related.
    """

    level: NoteLevels = Field(...)
    message: str = Field(...)


class Stage(BaseModel):
    """
    Stage of the test request with various details.
    """

    name: str = Field(..., description=('Name of the stage.'))
    result: TestStageResults = Field(
        ...,
    )
    log: HttpUrl = Field(
        ..., description=('URL to a stage specific log. Can point also to an artifact directory with various logs.')
    )
    notes: Optional[List[Note]] = Field(
        None, description=('Notes produced by Testing Farm related to this concrete stage')
    )


class Webhook(BaseModel):
    """
    Notification webhook.
    """

    url: HttpUrl = Field(
        ...,
        description=(
            'Post to given webhook URL in case of the request has changed. The purpose of the webhook is to inform '
            'our users about request changes and mitigates the need of periodic polling for request updates. '
            'The body of the request contains the `request_id` and an optional authentication `token`. '
            'In case of unsuccessful request, the request is retried few times.'
        ),
    )
    token: Optional[str] = Field(
        '',
        description=(
            'Optional token to send in the body under key `token` when posting to the webhook URL. '
            'Provides means of authentication to the service accepting the webhook.'
        ),
    )


class Notification(BaseModel):
    """
    Request update notification settings.
    """

    webhook: Optional[Webhook] = Field(
        None,
    )


class Result(BaseModel):
    """
    Result related properties.
    """

    summary: Optional[str] = Field(
        None,
        description=(
            'Human readable summary of the test request. In case of error state contains the error message. '
            'In case of skipped results, contains the reason of the skipping. In case of passed or failed results '
            'in contains a human readable interpretation of the test results, e.g. 1 plans from 3 failed.'
        ),
    )
    overall: TestOverallResults = Field(
        ...,
    )
    xunit: HttpUrl = Field(..., description=('A URL link to test results in XUnit format.'))


class Run(BaseModel):
    """
    Details of the request run.
    """

    console: HttpUrl = Field(
        ..., description=('URL of a plain-text log from Testing Farm, which can be followed for progress.')
    )
    stages: List[Stage] = Field([], description=('Stages of the test request with various details.'))
    artifacts: str = Field(..., description=('URL to the root of produced artifacts from the test request.'))


class Request(BaseModel):
    """
    Test request schema. Should be the same as database model
    """

    id: uuid.UUID = Field(
        ...,
        description=(
            'A unique identification of the request. Uses UUID format as defined in '
            '[RFC 4122](https://tools.ietf.org/html/rfc4122). Generated by Testing Farm.'
        ),
    )
    user_id: uuid.UUID = Field(..., description=('ID of the user created the test request.'))
    generation: int = Field(0, description=('TODO:'))
    state: RequestStateType = Field(
        ...,
    )
    notes: Optional[List[Note]] = Field(None, description=('Notes produced by Testing Farm.'))
    environment_requested: Optional[List[EnvironmentRequested]] = Field(
        None, description=('List of requested test environments.')
    )
    environment_provisioned: Optional[List[EnvironmentProvisioned]] = Field(
        None, description=('List of provisioned test environments.')
    )
    test: Test = Field(
        ...,
    )
    result: Optional[Result] = Field(
        None,
    )
    run: Optional[Run] = Field(
        ...,
    )
    notification: Optional[Notification] = Field(
        None,
    )

    queued_time: Optional[timedelta] = Field(..., description=('The duration of the request in the queue in seconds.'))
    run_time: Optional[timedelta] = Field(..., description=('The duration of the runtime in seconds.'))

    created: datetime = Field(..., description=('Date/time of creation of the request in RFC 3339 format.'))
    updated: datetime = Field(..., description=('Date/time of last update of the request in RFC 3339 format.'))

    @validator('test')
    def test_one_of(cls: Any, v: Any) -> Any:  # pylint: disable=invalid-name,no-self-argument,no-self-use
        """
        Validate `test` has only one section.
        """
        counter = 0
        for key in v.__dict__.keys():
            if v.__dict__[key] is not None:
                counter += 1
        if counter > 1:
            raise UnprocessableEntityError(message='Test section has more than one type.')
        if counter < 1:
            raise UnprocessableEntityError(message='Test section is empty or test type is wrong.')
        return v

    class Config:
        """
        https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
        """

        orm_mode = True


class RequestCreateIn(BaseModel):
    """
    Create test request API request.
    """

    api_key: str = Field(..., description=('An unique identifier used to authenticate a client.'))
    test: Test = Field(
        ...,
    )
    environments: Optional[List[EnvironmentRequested]] = Field(
        None, description=('List of requested test environments.')
    )
    notification: Optional[Notification] = Field(
        None,
    )

    @validator('test')
    def test_one_of(cls: Any, v: Any) -> Any:  # pylint: disable=invalid-name,no-self-argument,no-self-use
        """
        Validate `test` has only one section.
        """
        counter = 0
        for key in v.__dict__.keys():
            if v.__dict__[key] is not None:
                counter += 1
        if counter > 1:
            raise UnprocessableEntityError(message='Test section has more than one type.')
        if counter < 1:
            raise UnprocessableEntityError(message='Test section is empty or test type is wrong.')
        return v


class RequestCreateOut(BaseModel):
    """
    Create test request API response.
    """

    id: uuid.UUID = Field(
        ...,
        description=(
            'A unique identification of the request. Uses UUID format as defined in '
            '[RFC 4122](https://tools.ietf.org/html/rfc4122). Generated by Testing Farm.'
        ),
    )
    test: Test = Field(
        ...,
    )
    # state: RequestStateType = Field(  # TODO: uncomment once database migrated
    state: str = Field(
        # RequestStateType.NEW,
        RequestStateType.NEW.name.lower(),
    )
    environments: Optional[List[EnvironmentRequested]] = Field(
        None, description=('List of requested test environments.')
    )
    notification: Optional[Notification] = Field(
        None,
    )
    created: datetime = Field(..., description=('Date/time of creation of the request in RFC 3339 format.'))
    updated: datetime = Field(..., description=('Date/time of last update of the request in RFC 3339 format.'))


class RequestGetIn(BaseModel):
    """
    Get test request API request.
    """

    request_id: uuid.UUID = Field(..., description=('Provide request_id you are interested in.'))


class RequestGetUpdateOut(BaseModel):
    """
    Get test request API response.
    """

    user_id: uuid.UUID = Field(..., description=('ID of the user created the test request.'))
    test: Test = Field(
        ...,
    )
    # state: RequestStateType = Field(  # TODO: uncomment once database migrated
    state: str = Field(
        ...,
    )
    environments: Optional[List[EnvironmentRequested]] = Field(
        None, description=('List of requested test environments.')
    )
    notes: Optional[List[Note]] = Field(None, description=('Notes produced by Testing Farm.'))
    result: Optional[Result] = Field(
        None,
    )
    run: Optional[Run] = Field(
        ...,
    )

    queued_time: Optional[timedelta] = Field(..., description=('The duration of the request in the queue in seconds.'))
    run_time: Optional[timedelta] = Field(..., description=('The duration of the runtime in seconds.'))

    created: datetime = Field(..., description=('Date/time of creation of the request in RFC 3339 format.'))
    updated: datetime = Field(..., description=('Date/time of last update of the request in RFC 3339 format.'))


class RequestUpdateIn(BaseModel):
    """
    Update test request API request.
    """

    api_key: str = Field(..., description=('An unique identifier used to authenticate a client.'))
    state: Optional[RequestStateType] = Field(
        None,
    )
    notes: Optional[List[Note]] = Field(None, description=('Notes produced by Testing Farm.'))
    environment_provisioned: Optional[List[EnvironmentProvisioned]] = Field(
        None, description=('List of provisioned test environments.')
    )
    result: Optional[Result] = Field(
        None,
    )
    run: Optional[Run] = Field(
        None,
    )
