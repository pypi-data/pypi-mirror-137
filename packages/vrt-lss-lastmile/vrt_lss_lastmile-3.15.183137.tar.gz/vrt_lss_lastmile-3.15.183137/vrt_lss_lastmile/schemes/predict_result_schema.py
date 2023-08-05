PREDICT_RESULT_SCHEMA = '''{
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
        "windows": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "cost": {
                        "format": "double",
                        "minimum": 0,
                        "type": "number"
                    },
                    "time_window": {
                        "additionalProperties": false,
                        "properties": {
                            "from": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "to": {
                                "format": "date-time",
                                "type": "string"
                            }
                        },
                        "required": [
                            "from",
                            "to"
                        ],
                        "type": "object"
                    }
                },
                "required": [
                    "time_window",
                    "cost"
                ],
                "type": "object"
            },
            "type": "array"
        }
    },
    "type": "object"
}'''