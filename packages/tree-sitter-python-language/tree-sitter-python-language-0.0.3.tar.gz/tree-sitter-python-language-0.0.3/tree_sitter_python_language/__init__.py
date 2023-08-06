from functools import lru_cache
from pathlib import Path

from tree_sitter import Language

_PACKAGE = Path(__file__).parent

_BUILD_INPUT = _PACKAGE / 'vendor' / 'tree-sitter-python'
_BUILD_OUTPUT = _PACKAGE / 'python-language.so'
_TREE_SITTER_ZIP_URL = 'https://github.com/tree-sitter/tree-sitter-python/archive/{ref}.zip'

@lru_cache
def py_language() -> Language:
    return Language(build_python_language(rebuild=False), 'python')


def build_python_language(rebuild: bool = False) -> Path:
    """compile the python language into a useable .so file"""
    assert _BUILD_INPUT.exists(), 'the language files must be downloaded'

    if _BUILD_OUTPUT.exists() and rebuild:
        _BUILD_OUTPUT.unlink()
    
    if not _BUILD_OUTPUT.exists():
        build_successful = Language.build_library(str(_BUILD_OUTPUT), [str(_BUILD_INPUT)])
        assert build_successful, 'python tree-parser language failed to build'

    return _BUILD_OUTPUT


def fetch_python_language_zip(ref: str = 'refs/head/master') -> None:
    """
    Download and extract the python language repo
    ref: git ref to download, e.g. 'refs/head/master' or a git sha
    """
    import zipfile
    from io import BytesIO

    import requests

    response = requests.get(_TREE_SITTER_ZIP_URL.format(ref=ref))

    # extracting the zip file contents but remove the top level dirname
    with zipfile.ZipFile(BytesIO(response.content)) as zip:
        for zip_info in zip.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zip_info.filename = '/'.join(zip_info.filename.split('/')[1:])
            zip.extract(zip_info, _BUILD_INPUT)


def fetch_and_build_python_language() -> Language:
    fetch_python_language_zip()
    build_python_language()
    return py_language()
