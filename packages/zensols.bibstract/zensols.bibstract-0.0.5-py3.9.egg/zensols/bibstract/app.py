"""This utility extracts Bib(La)Tex references (a.k.a *markers*) from a
(La)Tex.

"""
__author__ = 'Paul Landes'

from typing import Dict
from dataclasses import dataclass, field
import logging
from pathlib import Path
from zensols.config import ConfigFactory
from . import Extractor, ConverterLibrary

logger = logging.getLogger(__name__)


@dataclass
class Exporter(object):
    """This utility extracts Bib(La)Tex references from a (La)Tex.

    """
    CLI_META = {'mnemonic_excludes': {'get_extractor'},
                'mnemonic_overrides': {'print_bibtex_ids': 'showbib',
                                       'print_texfile_refs': 'showtex',
                                       'print_extracted_ids': 'showextract',
                                       'print_entry': 'entry'},
                'option_includes': {}}

    config_factory: ConfigFactory = field()
    """The configuration factory used to create this instance."""

    converter_library: ConverterLibrary = field()
    """The converter library used to print what's available."""

    log_name: str = field()
    """The name of the package logger."""

    def get_extractor(self, texpath: Path = None) -> Extractor:
        return self.config_factory.new_instance('extractor', texpath=texpath)

    def _set_log_level_info(self):
        logging.getLogger(self.log_name).setLevel(logging.INFO)

    def converters(self):
        """List converters and their information."""
        self.converter_library.write()

    def print_bibtex_ids(self):
        """Print BibTex citation keys."""
        extractor = self.get_extractor()
        extractor.print_bibtex_ids()

    def print_texfile_refs(self, texpath: Path):
        """Print citation references.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        """
        extractor = self.get_extractor(texpath)
        extractor.print_texfile_refs()

    def print_extracted_ids(self, texpath: Path):
        """Print BibTex export citation keys.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        """
        extractor = self.get_extractor(texpath)
        extractor.print_extracted_ids()

    def print_entry(self, citation_key: str):
        """Print a single BibTex entry as it would be given in the output.

        :param citation_key: the citation key of entry to print out

        """
        extractor = self.get_extractor()
        entry: Dict[str, Dict[str, str]] = extractor.get_entry(citation_key)
        extractor.write_entry(entry)

    def export(self, texpath: Path):
        """Export the derived BibTex file.

        :param texpath: either a file or directory to recursively scan for
                        files with LaTex citation references

        """
        self._set_log_level_info()
        extractor = self.get_extractor(texpath)
        extractor.extract()
