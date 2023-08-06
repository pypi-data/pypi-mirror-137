"""Extract BibTex references from a Tex file and add them from a master BibTex
file.

"""
__author__ = 'plandes'

from typing import Dict, Tuple, Iterable
from dataclasses import dataclass, field
import sys
import logging
import re
from pathlib import Path
from io import TextIOWrapper
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser
from zensols.persist import persisted
from . import BibstractError, RegexFileParser, Converter, ConverterLibrary

logger = logging.getLogger(__name__)


@dataclass
class Extractor(object):
    """Extracts references, parses the BibTex master source file, and extracts
    matching references from the LaTex file.

    """
    TEX_FILE_REGEX = re.compile(r'.+\.(?:tex|sty|cls)$')

    converter_library: ConverterLibrary = field()
    """The converter library used to print what's available."""

    master_bib: Path = field()
    """The path to the master BibTex file."""

    texpath: Path = field(default=None)
    """Either a file or directory to recursively scan for files with LaTex citation
    references.

    """
    @property
    def converters(self) -> Tuple[Converter]:
        return self.converter_library.converters

    @property
    @persisted('_database')
    def database(self) -> BibDatabase:
        """Return the BibTex Python object representation of master file.

        """
        logger.info(f'parsing master bibtex file: {self.master_bib}')
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        with open(self.master_bib) as f:
            return bibtexparser.load(f, parser)

    @property
    def bibtex_ids(self) -> iter:
        """Return all BibTex string IDs.  These could be BetterBibtex citation
        references.

        """
        return map(lambda e: e['ID'], self.database.entries)

    def _is_tex_file(self, path: Path) -> bool:
        """Return whether or not path is a file that might contain citation references.

        """
        return path.is_file() and \
            self.TEX_FILE_REGEX.match(path.name) is not None

    @property
    def tex_refs(self) -> set:
        """Return the set of parsed citation references.

        """
        parser = RegexFileParser()
        path = self.texpath
        logger.info(f'parsing references from Tex file: {path}')
        if path.is_file():
            paths = (path,)
        elif path.is_dir():
            paths = tuple(filter(self._is_tex_file, path.rglob('*')))
        else:
            raise BibstractError(f'No such file or directory: {path}')
        logger.debug(f'parsing references from Tex files: {paths}')
        for path in paths:
            with open(path) as f:
                parser.find(f)
        return parser.collector

    @property
    def extract_ids(self) -> set:
        """Return the set of BibTex references to be extracted.

        """
        bib = set(self.bibtex_ids)
        trefs = self.tex_refs
        return bib & trefs

    def print_bibtex_ids(self):
        logging.getLogger('bibtexparser').setLevel(logging.ERROR)
        for id in self.bibtex_ids:
            print(id)

    def print_texfile_refs(self):
        for ref in self.tex_refs:
            print(ref)

    def print_extracted_ids(self):
        for id in self.extract_ids:
            print(id)

    def _convert_dict(self, db: Dict[str, Dict[str, str]],
                      keys: Iterable[str]) -> Dict[str, str]:
        entries = {}
        for did in sorted(keys):
            entry = db[did]
            for conv in self.converters:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'applying {conv}')
                entry = conv.convert(entry)
            entries[did] = entry
        return entries

    @property
    @persisted('_entries', cache_global=True)
    def entries(self) -> Dict[str, Dict[str, str]]:
        """The BibTex entries parsed from the master bib file."""
        db = self.database.get_entry_dict()
        return self._convert_dict(db, db.keys())

    def _get_all_entries(self) -> Dict[str, Dict[str, str]]:
        return {}

    def get_entry(self, citation_key: str) -> Dict[str, Dict[str, str]]:
        entries = self._get_all_entries()
        entry: Dict[str, str] = entries.get(citation_key)
        if entry is None:
            db = self.database.get_entry_dict()
            entry = db[citation_key]
            converted = self._convert_dict(
                {citation_key: entry}, [citation_key])
            entry = converted[citation_key]
            entries[citation_key] = entry
        return entry

    @property
    @persisted('_extracted_entries')
    def extracted_entries(self) -> Dict[str, Dict[str, str]]:
        """The BibTex entries parsed from the master bib file."""
        db = self.database.get_entry_dict()
        return self._convert_dict(db, self.extract_ids)

    def extract(self, writer: TextIOWrapper = sys.stdout):
        """Extract the master source BibTex matching citation references from the LaTex
        file(s) and write them to ``writer``.

        :param writer: the BibTex entry data sink

        """
        bwriter = BibTexWriter()
        for bid, entry in self.extracted_entries.items():
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'extracting: {bid}: <{entry}>')
            if logger.isEnabledFor(logging.INFO):
                logger.info(f'writing entry {bid}')
            self.write_entry(entry, bwriter, writer)
        writer.flush()

    def write_entry(self, entry: Dict[str, str],
                    bwriter: BibTexWriter = None,
                    writer: TextIOWrapper = sys.stdout):
        bwriter = BibTexWriter() if bwriter is None else bwriter
        writer.write(bwriter._entry_to_bibtex(entry))
