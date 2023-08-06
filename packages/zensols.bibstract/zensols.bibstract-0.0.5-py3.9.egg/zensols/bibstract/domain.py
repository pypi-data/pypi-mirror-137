"""Domain and utility classes.

"""
__author__ = 'Paul Landes'

from typing import Set, Dict, List, Tuple
from dataclasses import dataclass, field
import logging
import sys
from itertools import chain
from io import TextIOBase
import re
from zensols.persist import persisted
from zensols.config import Writable, ConfigFactory
from zensols.introspect import ClassImporter, ClassInspector, Class
from zensols.cli import ApplicationError

logger = logging.getLogger(__name__)


class BibstractError(ApplicationError):
    """Application level error."""
    pass


@dataclass
class RegexFileParser(object):
    """Finds all instances of the citation references in a file.

    """
    REF_REGEX = re.compile(r'\{([a-zA-Z0-9,-]+?)\}')
    """The default regular expression used to find citation references in sty and
    tex files (i.e. ``\\cite`` commands).

    """

    MULTI_REF_REGEX = re.compile(r'\s*,\s*')
    """The regular expression used to find comma separated lists of citations
    commands (i.e. ``\\cite``).

    """

    pattern: re.Pattern = field(default=REF_REGEX)
    """The regular expression pattern used to find the references."""

    collector: Set[str] = field(default_factory=lambda: set())
    """The set to add found references."""

    def find(self, fileobj: TextIOBase):
        for line in fileobj.readlines():
            refs = self.pattern.findall(line)
            refs = chain.from_iterable(
                map(lambda r: re.split(self.MULTI_REF_REGEX, r), refs))
            self.collector.update(refs)


@dataclass
class Converter(object):
    """A base class to convert fields of a BibTex entry (which is of type ``dict``)
    to another field.

    Subclasses should override :meth:`_convert`.

    """
    ENTRY_TYPE = 'ENTRYTYPE'

    name: str = field()
    """The name of the converter."""

    def convert(self, entry: Dict[str, str]) -> Dict[str, str]:
        """Convert and return a new entry.

        :param entry: the source data to transform

        :return: a new instance of a ``dict`` with the transformed data
        """
        entry = dict(entry)
        self._convert(entry)
        return entry

    def _convert(self, entry: Dict[str, str]):
        """The templated method subclasses should extend.  The default base class
        implementation is to return what's given as an identity mapping.

        """
        return entry

    def __str__(self) -> str:
        return f'converter: {self.name}'


@dataclass
class DestructiveConverter(Converter):
    """A converter that can optionally remove or modify entries.

    """
    destructive: bool = field(default=False)
    """If true, remove the original field if converting from one key to another in
    the Bibtex entry.

    """


@dataclass
class ConverterLibrary(Writable):
    config_factory: ConfigFactory = field()
    """The configuration factory used to create the converters."""

    converter_class_names: List[str] = field()
    """The list of converter class names currently available."""

    converter_names: List[str] = field(default=None)
    """A list of converter names used to convert to BibTex entries."""

    def __post_init__(self):
        self.converter_names = list(filter(
            lambda x: x != 'identity', self.converter_names))
        self._unregistered = {}

    def _create_converter(self, name: str) -> Converter:
        conv = self.config_factory(f'{name}_converter')
        conv.name = name
        return conv

    @property
    @persisted('_converters')
    def converters(self) -> Tuple[Converter]:
        return tuple(map(self._create_converter, self.converter_names))

    @property
    @persisted('_by_name')
    def converters_by_name(self) -> Dict[str, Converter]:
        convs = self.converters
        return {c.name: c for c in convs}

    def __getitem__(self, key: str):
        conv = self.converters_by_name.get(key)
        if conv is None:
            conv = self._unregistered.get(key)
            if conv is None:
                conv = self._create_converter(key)
                self._unregistered[key] = conv
        if conv is None:
            raise BibstractError(f'No such converter: {key}')
        return conv

    def write(self, depth: int = 0, writer: TextIOBase = sys.stdout,
              markdown_depth: int = 1):
        for cname in self.converter_class_names:
            cls = ClassImporter(cname).get_class()
            inspector = ClassInspector(cls)
            mcls: Class = inspector.get_class()
            header = '#' * markdown_depth
            self._write_line(f'{header} Converter {cls.NAME}', depth, writer)
            writer.write('\n')
            self._write_line(mcls.doc.text, depth, writer)
            writer.write('\n\n')
