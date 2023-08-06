from dataclasses import dataclass


@dataclass
class WorkingDir:

    path: str

    @property
    def get_path(self) -> str:
        return self.path
