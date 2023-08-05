import importlib
import inspect
import logging
import os
import shutil
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type, Union

import pytorch_lightning as pl
from pytorch_lightning.plugins import TorchCheckpointIO

METADATA_KEY: str = "metadata"

pylogger = logging.getLogger(__name__)


_METADATA_MODULE_KEY = f"{METADATA_KEY}_module"
_METADATA_CLASS_KEY = f"{METADATA_KEY}_class"


def _normalize_path(path: Union[Path, str]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    return (path.parent / path.stem.split(".")[0]).with_suffix(".ckpt.zip")


class NNCheckpointIO(TorchCheckpointIO):
    def __init__(self, jailing_dir: Optional[str] = None):
        self.jailing_dir = jailing_dir

    @classmethod
    def load(cls, path: Path, map_location: Optional[Callable] = lambda storage, loc: storage):
        return cls().load_checkpoint(path=str(path), map_location=map_location)

    def save_checkpoint(self, checkpoint: Dict[str, Any], path, storage_options: Optional[Any] = None) -> None:
        checkpoint_dir: Path = _normalize_path(path=path)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)

            if METADATA_KEY in checkpoint:
                metadata = checkpoint[METADATA_KEY]

                metadata_path: Path = tmp_dir / METADATA_KEY
                metadata_path.mkdir(exist_ok=True, parents=True)
                metadata.save(dst_path=metadata_path)

                checkpoint[_METADATA_MODULE_KEY] = inspect.getmodule(metadata).__name__
                checkpoint[_METADATA_CLASS_KEY] = type(metadata).__name__

                del checkpoint[METADATA_KEY]

            super().save_checkpoint(
                checkpoint=checkpoint, path=tmp_dir / "checkpoint.ckpt", storage_options=storage_options
            )

            compress_checkpoint(src_dir=tmp_dir, dst_file=checkpoint_dir)

    def load_checkpoint(self, path, map_location: Optional[Callable] = lambda storage, loc: storage) -> Dict[str, Any]:
        # load_checkpoint called from Trainer/Callbacks
        with extract_checkpoint(ckpt_file=Path(path)) as ckpt_dir:
            checkpoint = super().load_checkpoint(path=ckpt_dir / "checkpoint.ckpt", map_location=map_location)

            if _METADATA_MODULE_KEY in checkpoint:
                metadata_path: Path = ckpt_dir / METADATA_KEY
                if metadata_path.exists():
                    metadata_module = importlib.import_module(checkpoint[_METADATA_MODULE_KEY])
                    metadata = getattr(metadata_module, checkpoint[_METADATA_CLASS_KEY]).load(src_path=metadata_path)
                    checkpoint[METADATA_KEY] = metadata
                    del checkpoint[_METADATA_MODULE_KEY]
                    del checkpoint[_METADATA_CLASS_KEY]
                else:
                    raise FileNotFoundError(
                        "This checkpoint is corrupted. It appears data info is required but missing."
                    )

            return checkpoint

    def remove_checkpoint(self, path) -> None:
        if self.jailing_dir is None or path.startswith(self.jailing_dir):
            _normalize_path(path).unlink()
            pylogger.debug(f"Removing checkpoint from {path}")
        else:
            pylogger.debug(
                "Ignoring checkpoint deletion since it pertains to another run: "
                "https://github.com/PyTorchLightning/pytorch-lightning/issues/11379"
            )


def compress_checkpoint(src_dir: Path, dst_file: Path, delete_dir: bool = True):

    with zipfile.ZipFile(_normalize_path(dst_file), "w") as zip_file:
        for folder, subfolders, files in os.walk(src_dir):
            folder: Path = Path(folder)
            for file in files:
                zip_file.write(
                    folder / file,
                    os.path.relpath(os.path.join(folder, file), src_dir),
                    compress_type=zipfile.ZIP_DEFLATED,
                )

    if delete_dir:
        pylogger.debug(f"Deleting the checkpoint folder: '{src_dir}'")
        shutil.rmtree(path=src_dir, ignore_errors=True)


@contextmanager
def extract_checkpoint(ckpt_file: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp_dir:
        pylogger.debug(f"Extracting archive file '{ckpt_file}' to temp dir '{tmp_dir}'")
        with zipfile.ZipFile(_normalize_path(ckpt_file), "r") as compressed_ckpt:
            compressed_ckpt.extractall(tmp_dir)
        yield Path(tmp_dir)


def load_model(module_class: Type[pl.LightningModule], checkpoint_path: Path):
    checkpoint = NNCheckpointIO.load(path=checkpoint_path)

    model = module_class._load_model_state(checkpoint=checkpoint, metadata=checkpoint["metadata"])
    return model
