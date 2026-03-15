import json
import logging
from boto3.dynamodb.conditions import Key
from app.aws.session import dynamodb, dynamodb_client, is_mock_mode, service_available
from app.config import Config
from app.utils.mock_services import mock_registry_lookup
from app.utils.serialization import to_json_compatible


logger = logging.getLogger(__name__)
_LOCAL_DB = {
    Config.REGISTRY_TABLE: [],
    Config.ANALYSIS_RESULTS_TABLE: [],
    Config.APPEALS_TABLE: [],
    Config.TRANSLATIONS_TABLE: [],
    Config.AUDIT_LOGS_TABLE: [],
}


def _table_name(logical_name: str) -> str:
    return {
        "InstitutionalRegistry": Config.REGISTRY_TABLE,
        "AnalysisResults": Config.ANALYSIS_RESULTS_TABLE,
        "Appeals": Config.APPEALS_TABLE,
        "Translations": Config.TRANSLATIONS_TABLE,
        "AuditLogs": Config.AUDIT_LOGS_TABLE,
    }.get(logical_name, logical_name)


def get_table(table_name: str):
    if not service_available("dynamodb") or dynamodb is None:
        logger.warning(json.dumps({
            "event": "dynamodb_mock_fallback",
            "table": _table_name(table_name),
            "reason": "service_unavailable",
        }))
        return None
    try:
        return dynamodb.Table(_table_name(table_name))
    except Exception as error:
        logger.warning(json.dumps({
            "event": "dynamodb_table_init_failed",
            "table": _table_name(table_name),
            "error": str(error),
        }))
        return None


def put_item(table_name: str, item: dict):
    table = get_table(table_name)
    if table:
        try:
            table.put_item(Item=item)
            return True
        except Exception as error:
            logger.warning(json.dumps({
                "event": "dynamodb_put_fallback",
                "table": _table_name(table_name),
                "error": str(error),
            }))
    _LOCAL_DB[_table_name(table_name)].append(item)
    return True


def get_item(table_name: str, key: dict):
    table = get_table(table_name)
    if table:
        try:
            response = table.get_item(Key=key)
            item = response.get("Item")
            return to_json_compatible(item) if item else None
        except Exception as error:
            logger.warning(json.dumps({
                "event": "dynamodb_get_fallback",
                "table": _table_name(table_name),
                "error": str(error),
            }))
    for record in _LOCAL_DB[_table_name(table_name)]:
        if all(record.get(k) == v for k, v in key.items()):
            return to_json_compatible(record)
    return None


def describe_table(table_name: str):
    if not service_available("dynamodb_client") or dynamodb_client is None:
        return None
    try:
        response = dynamodb_client.describe_table(TableName=_table_name(table_name))
        return to_json_compatible(response["Table"])
    except Exception as error:
        logger.warning(json.dumps({
            "event": "dynamodb_describe_failed",
            "table": _table_name(table_name),
            "error": str(error),
        }))
        return None


def _query_index(table, attribute_name: str, value: str, index_name: str):
    if not value:
        return []
    response = table.query(
        IndexName=index_name,
        KeyConditionExpression=Key(attribute_name).eq(value),
        Limit=25,
    )
    return response.get("Items", [])


def _query_candidates(table, attribute_name: str, values: list[str], index_name: str):
    results = []
    seen = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        results.extend(_query_index(table, attribute_name, value, index_name))
    return results


def query_registry(entity_name: str = None, domain: str = None):
    table = get_table("InstitutionalRegistry")
    original_domain = (domain or "").strip()
    normalized_domain = original_domain.lower()
    original_entity = (entity_name or "").strip()
    normalized_entity = original_entity.lower()

    if table:
        try:
            results = []
            if normalized_domain:
                results.extend(
                    _query_candidates(
                        table,
                        Config.REGISTRY_DOMAIN_ATTRIBUTE,
                        [original_domain, normalized_domain],
                        Config.REGISTRY_DOMAIN_INDEX_NAME,
                    )
                )
            if normalized_entity:
                results.extend(
                    _query_candidates(
                        table,
                        Config.REGISTRY_ENTITY_ATTRIBUTE,
                        [original_entity, normalized_entity],
                        Config.REGISTRY_ENTITY_INDEX_NAME,
                    )
                )

            deduped = []
            seen = set()
            for item in results:
                marker = item.get("registry_id") or f"{item.get('entity_name')}::{item.get('domain')}"
                if marker not in seen:
                    seen.add(marker)
                    deduped.append(to_json_compatible(item))
            return deduped
        except Exception as error:
            logger.warning(json.dumps({
                "event": "registry_query_fallback",
                "domain": normalized_domain,
                "entity_name": normalized_entity,
                "error": str(error),
            }))

    if Config.ALLOW_MOCK_FALLBACK or is_mock_mode():
        mock_result = mock_registry_lookup(normalized_domain, entity_name or normalized_entity)
        return [mock_result] if mock_result else []
    return []
