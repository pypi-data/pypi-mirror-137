ACTUALIZE_TASK_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "facts": {
            "additionalProperties": false,
            "properties": {
                "order_facts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "demand_facts": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "demand_key": {
                                            "maxLength": 1024,
                                            "minLength": 1,
                                            "type": "string"
                                        },
                                        "time": {
                                            "format": "date-time",
                                            "type": "string"
                                        },
                                        "type": {
                                            "enum": [
                                                "DONE",
                                                "CANCEL"
                                            ],
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "type",
                                        "time",
                                        "demand_key"
                                    ],
                                    "type": "object"
                                },
                                "type": "array"
                            },
                            "order_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "time": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "type": {
                                "enum": [
                                    "DONE",
                                    "CANCEL",
                                    "PROGRESS"
                                ],
                                "type": "string"
                            }
                        },
                        "required": [
                            "type",
                            "time",
                            "order_key"
                        ],
                        "type": "object"
                    },
                    "type": "array"
                },
                "performer_facts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "performer_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            },
                            "position": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "latitude": {
                                        "format": "double",
                                        "maximum": 90,
                                        "minimum": -90,
                                        "type": "number"
                                    },
                                    "longitude": {
                                        "format": "double",
                                        "maximum": 180,
                                        "minimum": -180,
                                        "type": "number"
                                    },
                                    "time": {
                                        "format": "date-time",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "latitude",
                                    "longitude",
                                    "time"
                                ],
                                "type": "object"
                            },
                            "time": {
                                "format": "date-time",
                                "type": "string"
                            }
                        },
                        "required": [
                            "time",
                            "performer_key",
                            "position"
                        ],
                        "type": "object"
                    },
                    "type": "array"
                },
                "transport_facts": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "position": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "latitude": {
                                        "format": "double",
                                        "maximum": 90,
                                        "minimum": -90,
                                        "type": "number"
                                    },
                                    "longitude": {
                                        "format": "double",
                                        "maximum": 180,
                                        "minimum": -180,
                                        "type": "number"
                                    },
                                    "time": {
                                        "format": "date-time",
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "latitude",
                                    "longitude",
                                    "time"
                                ],
                                "type": "object"
                            },
                            "time": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "transport_key": {
                                "maxLength": 1024,
                                "minLength": 1,
                                "type": "string"
                            }
                        },
                        "required": [
                            "time",
                            "transport_key",
                            "position"
                        ],
                        "type": "object"
                    },
                    "type": "array"
                }
            },
            "type": "object"
        },
        "hardlinks": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "links": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "entity_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "type": {
                                    "enum": [
                                        "ORDER",
                                        "SHIFT"
                                    ],
                                    "nullable": false,
                                    "type": "string"
                                }
                            },
                            "required": [
                                "type",
                                "entity_key"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 2,
                        "type": "array"
                    }
                },
                "required": [
                    "key",
                    "links"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "locations": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "attributes": {
                        "default": [],
                        "items": {
                            "maxLength": 10000,
                            "minLength": 0,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "load_windows": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": false,
                            "properties": {
                                "gates_count": {
                                    "default": 0,
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
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
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 0,
                        "type": "array"
                    },
                    "location": {
                        "additionalProperties": false,
                        "properties": {
                            "arrival_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "departure_duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 1440,
                                "minimum": 0,
                                "type": "integer"
                            },
                            "latitude": {
                                "format": "double",
                                "maximum": 90,
                                "minimum": -90,
                                "type": "number"
                            },
                            "longitude": {
                                "format": "double",
                                "maximum": 180,
                                "minimum": -180,
                                "type": "number"
                            }
                        },
                        "required": [
                            "latitude",
                            "longitude"
                        ],
                        "type": "object"
                    },
                    "transport_restrictions": {
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    }
                },
                "required": [
                    "key",
                    "location"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "orders": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "attributes": {
                        "default": [],
                        "items": {
                            "maxLength": 10000,
                            "minLength": 0,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "cargos": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "capacity": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "capacity_x": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_y": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_z": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "mass": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "volume": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        }
                                    },
                                    "type": "object"
                                },
                                "cargo_features": {
                                    "default": [],
                                    "items": {
                                        "maxLength": 256,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "cargo_restrictions": {
                                    "default": [],
                                    "items": {
                                        "maxLength": 256,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "height": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "length": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "max_storage_time": {
                                    "default": 43800,
                                    "format": "int32",
                                    "maximum": 43800,
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "restrictions": {
                                    "items": {
                                        "maxLength": 256,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "maxItems": 100,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "rotation": {
                                    "default": [],
                                    "items": {
                                        "default": "ALL",
                                        "enum": [
                                            "ALL",
                                            "YAW",
                                            "PITCH",
                                            "ROLL"
                                        ],
                                        "nullable": false,
                                        "type": "string"
                                    },
                                    "maxItems": 4,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "width": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                }
                            },
                            "required": [
                                "key"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array"
                    },
                    "demands": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": false,
                            "properties": {
                                "attributes": {
                                    "default": [],
                                    "items": {
                                        "maxLength": 10000,
                                        "minLength": 0,
                                        "type": "string"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "demand_type": {
                                    "enum": [
                                        "PICKUP",
                                        "DROP",
                                        "WORK"
                                    ],
                                    "nullable": false,
                                    "type": "string"
                                },
                                "key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "possible_events": {
                                    "items": {
                                        "additionalProperties": false,
                                        "nullable": false,
                                        "properties": {
                                            "duration": {
                                                "default": 0,
                                                "format": "int32",
                                                "maximum": 525600,
                                                "minimum": 0,
                                                "type": "integer"
                                            },
                                            "key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            },
                                            "location_key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            },
                                            "reward": {
                                                "default": 1000.1,
                                                "format": "double",
                                                "maximum": 1000000,
                                                "minimum": 0,
                                                "type": "number"
                                            },
                                            "soft_time_window": {
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
                                            "location_key",
                                            "time_window"
                                        ],
                                        "type": "object"
                                    },
                                    "maxItems": 500,
                                    "minItems": 1,
                                    "type": "array"
                                },
                                "precedence_in_order": {
                                    "default": 0,
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "precedence_in_trip": {
                                    "default": 0,
                                    "format": "int32",
                                    "maximum": 9000,
                                    "minimum": 0,
                                    "type": "integer"
                                },
                                "target_cargos": {
                                    "items": {
                                        "maxLength": 1024,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                }
                            },
                            "required": [
                                "key",
                                "demand_type",
                                "possible_events"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 1,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "order_features": {
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "order_restrictions": {
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "performer_blacklist": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "performer_restrictions": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    }
                },
                "required": [
                    "key",
                    "demands"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "performers": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "attributes": {
                        "default": [],
                        "items": {
                            "maxLength": 10000,
                            "minLength": 0,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "max_work_shifts": {
                        "default": 31,
                        "format": "int32",
                        "maximum": 31,
                        "minimum": 1,
                        "type": "integer"
                    },
                    "own_transport_type": {
                        "default": "CAR",
                        "enum": [
                            "CAR",
                            "TRUCK",
                            "CAR_GT",
                            "TUK_TUK",
                            "BICYCLE",
                            "PEDESTRIAN",
                            "PUBLIC_TRANSPORT"
                        ],
                        "nullable": false,
                        "type": "string"
                    },
                    "performer_features": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "transport_restrictions": {
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    }
                },
                "required": [
                    "key"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "settings": {
            "additionalProperties": false,
            "nullable": false,
            "properties": {
                "current_time": {
                    "format": "date-time",
                    "type": "string"
                },
                "ferry_crossing": {
                    "default": true,
                    "type": "boolean"
                },
                "geo_provider": {
                    "maxLength": 256,
                    "minLength": 1,
                    "type": "string"
                },
                "result_timezone": {
                    "default": 0,
                    "format": "int32",
                    "maximum": 12,
                    "minimum": -12,
                    "type": "integer"
                },
                "toll_roads": {
                    "default": true,
                    "type": "boolean"
                }
            },
            "type": "object"
        },
        "shifts": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "attributes": {
                        "default": [],
                        "items": {
                            "maxLength": 10000,
                            "minLength": 0,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "availability_time": {
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
                    },
                    "finish_location_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "max_locations": {
                        "default": 0,
                        "format": "int32",
                        "maximum": 1000,
                        "minimum": 0,
                        "type": "integer"
                    },
                    "max_stops": {
                        "default": 0,
                        "format": "int32",
                        "maximum": 1000,
                        "minimum": 0,
                        "type": "integer"
                    },
                    "resource_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "shift_type": {
                        "enum": [
                            "PERFORMER",
                            "TRANSPORT"
                        ],
                        "nullable": false,
                        "type": "string"
                    },
                    "start_location_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "tariff": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "constraints": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": false,
                                    "properties": {
                                        "cost_per_unit": {
                                            "default": 0.001,
                                            "format": "double",
                                            "maximum": 10000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "stage_length": {
                                            "default": 100000000,
                                            "format": "int32",
                                            "maximum": 100000000,
                                            "minimum": 1,
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "stage_length",
                                        "cost_per_unit"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 100,
                                "minItems": 1,
                                "type": "array"
                            },
                            "cost_per_shift": {
                                "default": 0.001,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "max_penalty_cost": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "cost_per_shift",
                            "constraints"
                        ],
                        "type": "object"
                    },
                    "work_and_rest_rules": {
                        "additionalProperties": false,
                        "nullable": false,
                        "properties": {
                            "first_break": {
                                "additionalProperties": false,
                                "nullable": false,
                                "properties": {
                                    "duration": {
                                        "default": 0,
                                        "format": "int32",
                                        "maximum": 43800,
                                        "minimum": 1,
                                        "type": "integer"
                                    },
                                    "max_work_duration_sum": {
                                        "default": 0,
                                        "format": "int32",
                                        "maximum": 43800,
                                        "minimum": 1,
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "max_work_duration_sum",
                                    "duration"
                                ],
                                "type": "object"
                            }
                        },
                        "required": [
                            "first_break"
                        ],
                        "type": "object"
                    },
                    "working_time": {
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
                    "key",
                    "shift_type",
                    "resource_key",
                    "availability_time",
                    "working_time"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "transports": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "attributes": {
                        "default": [],
                        "items": {
                            "maxLength": 10000,
                            "minLength": 0,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "boxes": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": true,
                            "properties": {
                                "capacity": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "capacity_x": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_y": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_z": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "mass": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "volume": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        }
                                    },
                                    "type": "object"
                                },
                                "features": {
                                    "items": {
                                        "maxLength": 256,
                                        "minLength": 1,
                                        "type": "string"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "height": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "length": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                },
                                "max_size": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "capacity_x": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_y": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "capacity_z": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "mass": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "volume": {
                                            "default": 0,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        }
                                    },
                                    "type": "object"
                                },
                                "width": {
                                    "default": 0,
                                    "format": "double",
                                    "maximum": 1000000,
                                    "minimum": 0,
                                    "type": "number"
                                }
                            },
                            "required": [
                                "key"
                            ],
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 1,
                        "type": "array"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "max_boxes": {
                        "default": 0,
                        "format": "int32",
                        "maximum": 100,
                        "minimum": 0,
                        "type": "integer"
                    },
                    "max_capacity": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "capacity_x": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "capacity_y": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "capacity_z": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "mass": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            },
                            "volume": {
                                "default": 0,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "type": "object"
                    },
                    "performer_restrictions": {
                        "default": [],
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "transport_features": {
                        "items": {
                            "maxLength": 256,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "transport_type": {
                        "default": "CAR",
                        "enum": [
                            "CAR",
                            "TRUCK",
                            "CAR_GT",
                            "TUK_TUK",
                            "BICYCLE",
                            "PEDESTRIAN",
                            "PUBLIC_TRANSPORT"
                        ],
                        "nullable": false,
                        "type": "string"
                    }
                },
                "required": [
                    "key"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 1,
            "type": "array"
        },
        "trips": {
            "items": {
                "additionalProperties": false,
                "nullable": false,
                "properties": {
                    "actions": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": false,
                            "properties": {
                                "attributes": {
                                    "default": [],
                                    "items": {
                                        "maxLength": 10000,
                                        "minLength": 0,
                                        "type": "string"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array",
                                    "uniqueItems": true
                                },
                                "cargo_placements": {
                                    "items": {
                                        "additionalProperties": false,
                                        "properties": {
                                            "box_key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            },
                                            "cargo_key": {
                                                "maxLength": 1024,
                                                "minLength": 1,
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "box_key",
                                            "cargo_key"
                                        ],
                                        "type": "object"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 0,
                                    "type": "array"
                                },
                                "demand_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "event_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "location_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "order_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "todolist": {
                                    "items": {
                                        "additionalProperties": false,
                                        "nullable": false,
                                        "properties": {
                                            "job_time": {
                                                "format": "date-time",
                                                "type": "string"
                                            },
                                            "job_type": {
                                                "enum": [
                                                    "LOCATION_ARRIVAL",
                                                    "READY_TO_WORK",
                                                    "START_WORK",
                                                    "FINISH_WORK",
                                                    "LOCATION_DEPARTURE",
                                                    "BREAK"
                                                ],
                                                "nullable": false,
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "job_type",
                                            "job_time"
                                        ],
                                        "type": "object"
                                    },
                                    "maxItems": 1000,
                                    "minItems": 1,
                                    "type": "array"
                                }
                            },
                            "required": [
                                "order_key",
                                "demand_key",
                                "location_key"
                            ],
                            "type": "object"
                        },
                        "maxItems": 1000,
                        "minItems": 1,
                        "type": "array"
                    },
                    "assigned_shifts": {
                        "items": {
                            "additionalProperties": false,
                            "nullable": false,
                            "properties": {
                                "shift_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "shift_time": {
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
                                "shift_key",
                                "shift_time"
                            ],
                            "type": "object"
                        },
                        "maxItems": 2,
                        "minItems": 2,
                        "type": "array"
                    },
                    "attributes": {
                        "default": [],
                        "items": {
                            "maxLength": 10000,
                            "minLength": 0,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "finish_location_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "start_location_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "waitlist": {
                        "items": {
                            "maxLength": 1024,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 1000,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    }
                },
                "required": [
                    "key",
                    "assigned_shifts"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        }
    },
    "required": [
        "locations",
        "orders",
        "performers",
        "transports",
        "shifts",
        "trips"
    ],
    "type": "object"
}'''