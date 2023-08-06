from pathlib import Path
from typing import Any, Union

from tomlkit.exceptions import TOMLKitError
from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile as BaseTOMLFile

from andoya.core.exceptions import TOMLError


class TOMLFile(BaseTOMLFile):
    _path: Path

    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)
        super().__init__(path.as_posix())
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        """
        Whether the file exists.

        :return: True if the file exists, False otherwise.
        """
        return self._path.exists()

    def read(self) -> TOMLDocument:
        """
        Read the TOML file and return a TOMLDocument.

        :return: The TOMLDocument.
        """
        try:
            return super().read()
        except (ValueError, TOMLKitError) as e:
            raise TOMLError(f"Invalid TOML file {self.path.as_posix()}: {e}")

    def __getattr__(self, item: str) -> Any:
        return getattr(self._path, item)

    def __str__(self) -> str:
        return self._path.as_posix()
