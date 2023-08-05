VALIDATE_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "storages": {
            "items": {
                "additionalProperties": false,
                "nullable": true,
                "properties": {
                    "balance": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "max_limit": {
                                "format": "double",
                                "maximum": 10000000,
                                "minimum": 0.1,
                                "type": "number"
                            },
                            "min_limit": {
                                "format": "double",
                                "maximum": 10000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "start_amount": {
                                "format": "double",
                                "maximum": 10000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "start_amount",
                            "min_limit",
                            "max_limit"
                        ],
                        "type": "object"
                    },
                    "forecast": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "date": {
                                    "format": "date",
                                    "nullable": false,
                                    "type": "string"
                                },
                                "delta": {
                                    "format": "double",
                                    "maximum": 10000000,
                                    "minimum": -10000000,
                                    "type": "number"
                                },
                                "time_index": {
                                    "format": "int32",
                                    "maximum": 31,
                                    "minimum": 0,
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "time_index",
                                "delta"
                            ],
                            "type": "object"
                        },
                        "maxLength": 1000,
                        "minLength": 0,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "restricted_time_indexes": {
                        "items": {
                            "format": "int32",
                            "maximum": 31,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "maxLength": 1000,
                        "minLength": 0,
                        "type": "array"
                    },
                    "tariff": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "storage_cost": {
                                "format": "double",
                                "maximum": 10000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "transfer_cost": {
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "transfer_cost",
                            "storage_cost"
                        ],
                        "type": "object"
                    }
                },
                "required": [
                    "key",
                    "balance",
                    "forecast",
                    "tariff"
                ],
                "type": "object"
            },
            "maxItems": 10000,
            "minItems": 1,
            "nullable": false,
            "type": "array"
        }
    },
    "required": [
        "storages"
    ],
    "type": "object"
}'''