from __future__ import annotations


import functools
import re
from typing import Any, Optional, TypedDict

import pycountry
import ckan.plugins.toolkit as tk
from . import utils

_swap_case = re.compile("(?<=[a-z])(?=[A-Z])")

CONFIG_LANGUAGES = "ckanext.iso19115.metadata.supported_languages"
DEFAULT_LANGUAGES = "eng"


def get_helpers():
    return {
        "iso19115_implementation_as_options": implementations,
        "iso19115_codelist_as_options": codelist,
        "iso19115_languages": languages,
    }


class AnnotatedOption(TypedDict):
    value: str
    label: str
    annotation: Optional[str]


def languages(field: dict[str, Any]):
    return _get_languages()


@functools.lru_cache(1)
def _get_languages() -> list[AnnotatedOption]:
    supported = tk.aslist(tk.config.get(CONFIG_LANGUAGES, DEFAULT_LANGUAGES))
    languages = (
        map(pycountry.languages.lookup, supported)
        if supported
        else pycountry.languages
    )

    return [
        AnnotatedOption(value=l.alpha_3, label=l.name, annotation=None)
        for l in languages
    ]


@functools.lru_cache()
def _get_implementations(el: str) -> list[AnnotatedOption]:
    from ckanext.iso19115.utils import get_builder

    base = get_builder(el)
    options = []
    for impl in base.implementations():
        name = impl.name(False)
        if not name:
            continue
        label = _swap_case.sub(" ", name.split(":")[-1].replace("_", " "))
        options.append(
            AnnotatedOption(
                value=name, label=label, annotation=impl.annotation()
            )
        )

    return options


def implementations(field: dict[str, Any]):
    return _get_implementations(field["iso19115_source"])


@functools.lru_cache()
def _get_codelist(name: str) -> list[AnnotatedOption]:
    return [
        AnnotatedOption(
            value=code.name,
            label=_swap_case.sub(" ", code.name).capitalize(),
            annotation=code.definition,
        )
        for code in utils.codelist_options(name)
    ]


def codelist(field: dict[str, Any]):
    return _get_codelist(field["iso19115_source"])
