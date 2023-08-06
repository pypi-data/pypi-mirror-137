import click, os, sys, traceback
from typing import Tuple
from klee.internal import log, Structure, __version__
from klee import plans, test

@click.group()
@click.version_option(__version__)
def cli():
    pass
# Common Args
def shared_args(fn):
    click.argument('targets', nargs=-1)(fn)
    click.option('-p', '--plan_type', default='default', type =
        click.Choice([*plans.Options], case_sensitive=False))(fn)
    click.option('-c', '--claims-dir', default='test_claims', help='suggested location: test_claims')(fn)
    click.option('-o', '--output-dir', default='test_cases', help="suggested location: test_cases")(fn)
def test_args(fn):
    shared_args(fn)
    click.option('--pytest', default = "-vvv", help="arguments to send to pytest")(fn)
# Legacy/JSON output
@shared_args
@cli.command('build')
def BuildCommand(targets, plan_type, claims_dir, output_dir):
    require_engine_folder()
    structure = Structure(os.getcwd(), claims_dir, output_dir)
    structure.json_enabled = True; structure.register_instance()
    _echo('Building', targets)

    @error_logging
    def _logic():
        build_sys = plans.Options[plan_type.lower()](structure)
        build_sys.build_node_labels(targets)
# Run Tests Locally
@test_args
@click.option('-ld', '--local_defense', is_flag=True)
@cli.command('test')
def ExecLocalTest(targets, plan_type, claims_dir, output_dir, pytest, local_defense):
    require_engine_folder()
    structure = Structure(os.getcwd(), claims_dir, output_dir)
    structure.register_instance()

    if local_defense:
        os.environ['RIALTIC_LOCAL_DEFENSE'] = 'TRUE'

    _echo('Running tests for', targets)
    if not test.PyTestUtility.env_vars_present():
        print("aborting...")
        sys.exit(1)

    @error_logging
    def _logic():
        build_sys = plans.Options[plan_type.lower()](structure)
        test_cases = build_sys.build_node_labels(targets)

        args = [x.strip() for x in pytest.split(',')]
        return test.LocalTest(args).invoke_cases(test_cases)
# Run Tests Remotely
@test_args
@cli.command('smoke')
def ExecSmokeTest(targets, plan_type, claims_dir, output_dir, pytest):
    require_engine_folder()
    structure = Structure(os.getcwd(), claims_dir, output_dir)
    structure.register_instance(); _echo('Running smoke tests for', targets)

    @error_logging
    def _logic():
        build_sys = plans.Options[plan_type.lower()](structure)
        test_cases = build_sys.build_node_labels(targets)

        args = [x.strip() for x in pytest.split(',')]
        return test.SmokeTest(args).invoke_cases(test_cases)
# Helper Functions
def require_engine_folder():
    if not os.path.exists('oim-engine.json'):
        print("This utility may only be run from within an engine's root directory.")
        sys.exit(1)

def _echo(what, targets = None):
    if targets is None:
        message = f'cli: {what}\n'
    else:
        message = f'cli: {what} {",".join(targets) or "all"} targets\n'
    click.echo(message); log.info(message)

def error_logging(closure):
    try:
        code = closure()
    except:
        log.critical(traceback.format_exc())
        code = 1
    if code is not None:
        sys.exit(code)
# Utils Commands
@cli.command('sync-pipenv')
def ExecSyncPipenv():
    from klee.utils.sync_pipenv import ForceWrite
    require_engine_folder()
    structure = Structure(os.getcwd(), 'test_claims', 'test_cases')
    structure.register_instance()

    _echo('Using experimental sync-pipenv flow')
    ForceWrite(structure)

@cli.command('v1-redeploy')
@click.argument('targets', nargs=-1)
def ExecV1Redeploy(targets: Tuple[str]):
    from klee.utils.v1_redeploy import run
    if not targets:
        path = os.path.abspath(os.getcwd())
        targets = (path.split('/')[-1], )

    for target in targets:
        try:
            run(target)
        except:
            log.critical(traceback.format_exc())
