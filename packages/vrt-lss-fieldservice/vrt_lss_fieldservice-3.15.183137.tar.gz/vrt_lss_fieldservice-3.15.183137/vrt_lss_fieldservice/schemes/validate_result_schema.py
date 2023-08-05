VALIDATE_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "tracedata": {
            "additionalProperties": false,
            "properties": {
                "client": {
                    "maxLength": 256,
                    "minLength": 2,
                    "type": "string"
                },
                "code": {
                    "maxLength": 256,
                    "minLength": 3,
                    "type": "string"
                },
                "method": {
                    "enum": [
                        "PLAN",
                        "REPLAN",
                        "ACTUALIZE",
                        "CONVERT",
                        "ANALYTICS",
                        "PREDICT",
                        "VALIDATE",
                        "ROUTE",
                        "MATRIX",
                        "CLUSTER"
                    ],
                    "type": "string"
                },
                "server": {
                    "maxLength": 256,
                    "minLength": 2,
                    "type": "string"
                },
                "service": {
                    "enum": [
                        "LASTMILE",
                        "DELIVERY",
                        "FIELDSERVICE",
                        "MERCHANDISER",
                        "ROUTING",
                        "CLUSTERING",
                        "ACCOUNT",
                        "STOCK",
                        "ADMIN"
                    ],
                    "type": "string"
                },
                "time": {
                    "format": "date-time",
                    "type": "string"
                }
            },
            "required": [
                "code"
            ],
            "type": "object"
        },
        "validations": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "entity_key": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "entity_type": {
                        "maxLength": 1024,
                        "type": "string"
                    },
                    "info": {
                        "type": "string"
                    },
                    "type": {
                        "enum": [
                            "info",
                            "warning",
                            "error"
                        ],
                        "nullable": false,
                        "type": "string"
                    }
                },
                "required": [
                    "type",
                    "info"
                ],
                "type": "object"
            },
            "type": "array"
        }
    },
    "type": "object"
}'''