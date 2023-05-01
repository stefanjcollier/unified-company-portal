from typing import Type
from functools import reduce
import operator
from typing import Sequence
from pydantic import BaseModel

from app.companies.models.unified_models import UnifiedCompany, UnifiedRelatedPerson, UnifiedRelatedCompany, \
    UnifiedNameEntity
from app.lib.dict import dict_without_blanks


def consolidate_companies(companies: Sequence[UnifiedCompany]) -> UnifiedCompany:
    """
    Consolidate a list of company models for the same company into a single model,
     enriching it with data from all providers. Attempting a best effort to consolidate related people and companies.
    """
    leaf_data = _squash_models(companies)

    related_people_arrays = _flatten_lists([company.related_people for company in companies])
    leaf_data['related_people'] = consolidate_named_entities(related_people_arrays, UnifiedRelatedPerson)

    related_companies_arrays = _flatten_lists([company.related_companies for company in companies])
    leaf_data['related_companies'] = consolidate_named_entities(related_companies_arrays, UnifiedRelatedCompany)

    return UnifiedCompany.parse_obj(leaf_data)


def consolidate_named_entities(
        entities: list[UnifiedNameEntity],
        klass: Type[UnifiedRelatedPerson | UnifiedRelatedCompany]
) -> list[UnifiedRelatedPerson]:
    """
    Consolidate a list of people to a distinct list of people; where data from multiple providers for a single person
    creates a more supplemented record.

    :param entities: the entities that could contain identical people from differing providers
    :param klass: the model of the entities
    :return: a list of :model: instances
    """
    groups_of_same_entities = _group_named_entities(entities)
    list_of_entity_data_dicts = map(_squash_models, groups_of_same_entities)
    return list(map(klass.parse_obj, list_of_entity_data_dicts))


def _group_named_entities(entities: list[UnifiedNameEntity]) -> list[list[UnifiedNameEntity]]:
    """ Create a list of lists where each sublist contains data for the same named entity """
    result = {}
    for entity in entities:
        key = entity.name
        result.setdefault(key, [])
        result[key].append(entity)

    return list(result.values())


def _squash_models(models: Sequence[BaseModel]) -> dict:
    """ Create a single dict containing the last non-None value for each model """
    leaf_datas = map(dict_without_blanks, map(_extract_leaf_data, models))
    return reduce(operator.__or__, leaf_datas)


def _extract_leaf_data(model: BaseModel) -> dict:
    """ Convert the model to a dict and only keep non-list key-values"""
    return {key: value for key, value in model.dict().items() if not isinstance(value, list)}


def _flatten_lists(list_of_lists: list[list]) -> list:
    """ Turn a list of lists into a list of all the items """
    return [element for sublist in list_of_lists for element in sublist]
