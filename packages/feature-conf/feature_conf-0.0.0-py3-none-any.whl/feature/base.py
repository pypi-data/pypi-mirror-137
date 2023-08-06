from __future__ import annotations

import warnings
from dataclasses import Field
from functools import cached_property
from typing import ClassVar
from typing import Final
from typing import Mapping
from typing import TypeVar
from typing import cast
from typing import final

import immutables
from pydantic import BaseModel

from .references import ClassReference
from .sources import EnvVars
from .sources import Source

FeatureSelf = TypeVar("FeatureSelf", bound="Feature")


class Feature(BaseModel):
    enabled: ClassVar[bool] = True

    @classmethod
    def resolve(cls: type[FeatureSelf], prefix: str, source: Source) -> FeatureSelf:
        return cls.parse_obj(source.resolve_many(prefix, cls.__fields__.keys()))

    class Config:
        allow_mutation = False


@final
class DisabledFeature(Feature):
    enabled: ClassVar[bool] = False


disabled_feature: Final = DisabledFeature()


class UndefinedFeature(Warning):
    ...


class Config:
    _enabled_features_key: Final = "ENABLED_FEATURES"
    _enabled_features_separator: Final = "+"
    _initialized = False

    def __init__(self, spec: type, source: Source = EnvVars()) -> None:
        self._spec: Final = spec
        self._source: Final = source
        fields: Mapping[
            str, Field
        ] = spec.__dataclass_fields__  # type: ignore[attr-defined]
        feature_references: Final = immutables.Map(
            {
                feature_name: ClassReference(field.metadata["reference"], bound=Feature)
                for feature_name, field in fields.items()
            }
        )
        for feature_name, reference in feature_references.items():
            setattr(
                self,
                feature_name,
                reference.resolved.resolve(feature_name, source)
                if feature_name in self._enabled_features
                else disabled_feature,
            )
        self._initialized = True

    def __setattr__(self, key: str, value: object) -> None:
        if self._initialized:
            raise AttributeError(
                f"Cannot set attribute {key!r}, {self._spec.__qualname__!r} is frozen"
            )
        super().__setattr__(key, value)

    @cached_property
    def _enabled_features(self) -> frozenset[str]:
        env_value = self._source.resolve(self._enabled_features_key)
        if env_value is None:
            return frozenset()
        enabled_features = frozenset(
            feature_name.strip()
            for feature_name in env_value.split(self._enabled_features_separator)
        )
        if undefined_features := (
            enabled_features
            - self._spec.__dataclass_fields__.keys()  # type: ignore[attr-defined]
        ):
            warnings.warn(
                (
                    f"{self._enabled_features_key} contains features that are not "
                    f"defined: {undefined_features}"
                ),
                UndefinedFeature,
            )

        return enabled_features


S = TypeVar("S")


def load_spec(spec: type[S], source: Source = EnvVars()) -> S:
    return cast(S, Config(spec=spec, source=source))
