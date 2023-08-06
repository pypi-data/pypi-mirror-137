import io
import json

import pytest
from django.core.management import call_command

from django_dataclasses.management.commands.openapi_export import reformat_path


def test_openapi_export(client):
    stdout = io.StringIO()
    call_command("openapi_export", stdout=stdout)
    stdout.seek(0)

    assert json.loads(stdout.read()) == {
        "info": {"title": "Backend", "version": "1.0.0"},
        "openapi": "3.0.2",
        "components": {
            "responses": {
                "error": {
                    "content": {"text/plain": {"schema": {"$ref": "#/components/schemas/text"}}},
                    "description": "An error message in plain-text",
                }
            },
            "schemas": {
                "MyViewRequest": {
                    "description": "MyViewRequest(a: str, b: int)",
                    "properties": {"a": {"type": "string"}, "b": {"type": "integer"}},
                    "required": ["a", "b"],
                    "type": "object",
                    "x-module-name": "test_project.views",
                },
                "MyViewResponse": {
                    "description": "MyViewResponse OpenAPI description",
                    "properties": {
                        "c": {"$ref": "#/components/schemas/NestedThing"},
                        "d": {"type": "integer"},
                    },
                    "required": ["c", "d"],
                    "type": "object",
                    "x-module-name": "test_project.views",
                },
                "NestedThing": {
                    "description": "NestedThing(e: List[datetime.datetime])",
                    "properties": {
                        "e": {"items": {"format": "date-time", "type": "string"}, "type": "array"}
                    },
                    "required": ["e"],
                    "type": "object",
                    "x-module-name": "test_project.views",
                },
                "text": {"type": "string"},
                "IterableObject": {
                    "description": "An object that is returned as part of a list",
                    "properties": {"a": {"type": "integer"}},
                    "required": ["a"],
                    "type": "object",
                    "x-module-name": "test_project.views",
                },
                "Iterable[IterableObject]": {
                    "description": "An Iterable of IterableObject items.",
                    "properties": {
                        "count": {"type": "integer"},
                        "items": {
                            "items": {"$ref": "#/components/schemas/IterableObject"},
                            "type": "array",
                        },
                        "page": {"type": "integer"},
                    },
                    "required": ["items", "page", "count"],
                    "type": "object",
                    "x-module-name": "django_dataclasses.iterable",
                },
            },
        },
        "paths": {
            "/test_get/{item}": {
                "parameters": [
                    {"in": "path", "name": "item", "required": True, "schema": {"type": "integer"}}
                ],
                "get": {
                    "description": "no body",
                    "operationId": "other_view",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/MyViewResponse"}
                                }
                            },
                            "description": "MyViewResponse OpenAPI description",
                        },
                        "4XX": {"$ref": "#/components/responses/error"},
                        "5XX": {"$ref": "#/components/responses/error"},
                    },
                },
            },
            "/test_iterable/": {
                "get": {
                    "description": "Wraps result into a list of items",
                    "operationId": "iterable_view",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Iterable[IterableObject]"
                                    }
                                }
                            },
                            "description": "An Iterable of IterableObject items.",
                        },
                        "4XX": {"$ref": "#/components/responses/error"},
                        "5XX": {"$ref": "#/components/responses/error"},
                    },
                }
            },
            "/test_paginator/": {
                "parameters": [
                    {
                        "in": "query",
                        "name": "page",
                        "required": False,
                        "schema": {"type": "string"},
                    },
                    {
                        "in": "query",
                        "name": "page_size",
                        "required": False,
                        "schema": {"type": "string"},
                    },
                ],
                "get": {
                    "description": "Wraps result into a paginated list of items",
                    "operationId": "paginator_view",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Iterable[IterableObject]"
                                    }
                                }
                            },
                            "description": "An Iterable of IterableObject items.",
                        },
                        "4XX": {"$ref": "#/components/responses/error"},
                        "5XX": {"$ref": "#/components/responses/error"},
                    },
                },
            },
            "/test_post/": {
                "post": {
                    "operationId": "my_view",
                    "description": "my_view OpenAPI description",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MyViewRequest"}
                            }
                        },
                        "description": "MyViewRequest(a: str, b: int)",
                    },
                    "responses": {
                        "201": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/MyViewResponse"}
                                }
                            },
                            "description": "MyViewResponse OpenAPI description",
                        },
                        "4XX": {"$ref": "#/components/responses/error"},
                        "5XX": {"$ref": "#/components/responses/error"},
                    },
                }
            },
        },
    }


@pytest.mark.parametrize(
    "input_, new_path, parameters",
    [
        ("some_path/", "/some_path/", []),
        (
            "<parameter>/",
            "/{parameter}/",
            [{"in": "path", "name": "parameter", "required": True, "schema": {"type": "string"}}],
        ),
        (
            "<int:parameter>/",
            "/{parameter}/",
            [{"in": "path", "name": "parameter", "required": True, "schema": {"type": "integer"}}],
        ),
        (
            "<int:parameter>/<other>",
            "/{parameter}/{other}",
            [
                {
                    "in": "path",
                    "name": "parameter",
                    "required": True,
                    "schema": {"type": "integer"},
                },
                {"in": "path", "name": "other", "required": True, "schema": {"type": "string"}},
            ],
        ),
    ],
)
def test_api_path(input_, new_path, parameters):
    actual_path, actual_parameters = reformat_path(input_)
    assert actual_path == new_path
    assert actual_parameters == parameters
