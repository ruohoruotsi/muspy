"""Datasets built from music21 corpus."""
from pathlib import Path
from typing import Union

from ..datasets import Dataset, MusicDataset
from ..inputs import read
from ..music import Music

try:
    from music21 import corpus

    HAS_MUSIC21 = True
except ImportError:
    HAS_MUSIC21 = False

_NAME = "Music21 Corpus Dataset"
_DESCRIPTION = """\
Dataset automatically created from a music21 corpus.
"""
_HOMEPAGE = "https://web.mit.edu/music21/doc/about/referenceCorpus.html"
_CITATION = """\
@inproceedings{cuthbert2010music21,
  author={Cuthbert, Michael Scott and Ariza, Christopher},
  title={Music21: A Toolkit for Computer-Aided Musicology and Symbolic Music \
Data},
  booktitle={Proceedings of the 18th International Society for Music \
Information Retrieval Conference (ISMIR)},
  year={2010}
}
"""


class Music21Dataset(Dataset):
    """A class of datasets containing files in music21 corpus.

    Parameters
    ----------
    composer : str
        Name of a composer or a collection.
    extensions : list of str
        File extensions of desired files.

    Notes
    -----
    Please refer to the music21 corpus reference page for a full list [1].

    [1] https://web.mit.edu/music21/doc/about/referenceCorpus.html

    """

    @classmethod
    def _converter(cls, filename: str) -> Music:
        return read(filename)

    def __init__(self, composer, extensions):
        if not HAS_MUSIC21:
            raise ImportError("Optional package music21 is required.")
        self.composer = composer
        self.filenames = corpus.getComposer(composer, extensions)

    def __repr__(self) -> str:
        return "{}(composer={})".format(type(self).__name__, self.composer)

    def __getitem__(self, index) -> Music:
        return self._converter(str(self.filenames[index]))

    def __len__(self) -> int:
        return len(self.filenames)

    def convert(
        self,
        root: Union[str, Path],
        kind: str = "json",
        n_jobs: int = 1,
        ignore_exceptions: bool = False,
    ) -> "MusicDataset":
        """Convert and save the Music objects; return a MusicDataset instance.

        Parameters
        ----------
        root : str or Path
            Root directory to save the data.
        kind : {'json', 'yaml'}, optional
            File format to save the data. Defaults to 'json'.
        n_jobs : int, optional
            Maximum number of concurrently running jobs in multiprocessing. If
            equal to 1, disable multiprocessing. Defaults to 1.
        ignore_exceptions : bool, optional
            Whether to ignore errors and skip failed conversions. This can be
            helpful if some of the source files is known to be corrupted.
            Defaults to False.

        """
        self.save(root, kind, n_jobs, ignore_exceptions)
        return MusicDataset(root, kind)