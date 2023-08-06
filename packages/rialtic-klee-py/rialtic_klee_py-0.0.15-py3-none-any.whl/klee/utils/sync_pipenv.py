from klee.internal import Structure, log
from klee import files
import os

def ForceWrite(_global: Structure):
    path = os.path.join(_global.root_dir, 'Pipfile')
    pipfile = files.read_lines(path)
    for ix, line in enumerate(pipfile):
        for key in _Dependencies:
            if key in line and not line.startswith('#'):
                pipfile[ix] = " = ".join((key, f'"{_Dependencies[key]}"'))
                log.info('replacing pipfile line: %s', line)
    files.save_lines(pipfile, path)

_Dependencies = {
    'rialtic-engine-lib-py': "~=1.11",
    'insight-engine-schema-python': "~=0.3",
    'rialtic-data-dev-py': "~=1.1",
    '"fhir.resources"': "~=6.2.0",

    'rialtic-klee-py': ">=0.0.14",
    'pytest': "~=6.2.5",
}
