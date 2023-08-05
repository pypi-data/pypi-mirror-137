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
                            "job_facts": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
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
                                        },
                                        "time": {
                                            "format": "date-time",
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "time",
                                        "job_type"
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
                }
            },
            "type": "object"
        },
        "orders": {
            "items": {
                "additionalProperties": false,
                "properties": {
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
                        "minItems": 1,
                        "type": "array"
                    },
                    "cost": {
                        "additionalProperties": false,
                        "properties": {
                            "penalty": {
                                "additionalProperties": false,
                                "properties": {
                                    "max_value": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "period": {
                                        "default": 60,
                                        "format": "int32",
                                        "maximum": 1440,
                                        "minimum": 1,
                                        "type": "integer"
                                    },
                                    "start_time": {
                                        "format": "date-time",
                                        "type": "string"
                                    },
                                    "value": {
                                        "default": 0,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    }
                                },
                                "required": [
                                    "start_time",
                                    "period",
                                    "value",
                                    "max_value"
                                ],
                                "type": "object"
                            },
                            "reward": {
                                "default": 1000.1,
                                "format": "double",
                                "maximum": 1000000,
                                "minimum": 0,
                                "type": "number"
                            }
                        },
                        "required": [
                            "reward"
                        ],
                        "type": "object"
                    },
                    "customer": {
                        "additionalProperties": false,
                        "properties": {
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
                            "time_windows": {
                                "items": {
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
                                "maxItems": 100,
                                "minItems": 1,
                                "type": "array"
                            }
                        },
                        "required": [
                            "location",
                            "time_windows"
                        ],
                        "type": "object"
                    },
                    "customer_duration": {
                        "default": 0,
                        "format": "double",
                        "maximum": 43800,
                        "minimum": 0,
                        "type": "number"
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
                    },
                    "type": {
                        "default": "DROP",
                        "enum": [
                            "DROP",
                            "PICKUP"
                        ],
                        "nullable": false,
                        "type": "string"
                    },
                    "warehouse_duration": {
                        "default": 0,
                        "format": "double",
                        "maximum": 43800,
                        "minimum": 0,
                        "type": "number"
                    },
                    "warehouse_keys": {
                        "items": {
                            "maxLength": 1024,
                            "minLength": 1,
                            "type": "string"
                        },
                        "maxItems": 100,
                        "minItems": 1,
                        "type": "array"
                    }
                },
                "required": [
                    "key",
                    "warehouse_keys",
                    "customer",
                    "cargos"
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
                "properties": {
                    "box": {
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
                    "count": {
                        "default": 1,
                        "format": "int32",
                        "maximum": 5000,
                        "minimum": 1,
                        "type": "integer"
                    },
                    "features": {
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
                    "finish_location": {
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
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "shifts": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
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
                                "availability_time",
                                "working_time"
                            ],
                            "type": "object"
                        },
                        "maxItems": 100,
                        "minItems": 1,
                        "type": "array"
                    },
                    "start_location": {
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
                    "tariff": {
                        "additionalProperties": false,
                        "properties": {
                            "basic": {
                                "additionalProperties": false,
                                "nullable": true,
                                "properties": {
                                    "cost_per_meter": {
                                        "default": 0.001,
                                        "format": "double",
                                        "maximum": 10000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "cost_per_minute": {
                                        "default": 0.001,
                                        "format": "double",
                                        "maximum": 10000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "cost_per_shift": {
                                        "default": 0.001,
                                        "format": "double",
                                        "maximum": 1000000,
                                        "minimum": 0,
                                        "type": "number"
                                    },
                                    "max_length": {
                                        "default": 100000000,
                                        "format": "int32",
                                        "maximum": 100000000,
                                        "minimum": 1,
                                        "type": "integer"
                                    },
                                    "max_time": {
                                        "default": 43800,
                                        "format": "int32",
                                        "maximum": 43800,
                                        "minimum": 1,
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "cost_per_shift",
                                    "cost_per_meter",
                                    "max_length",
                                    "cost_per_minute",
                                    "max_time"
                                ],
                                "type": "object"
                            },
                            "extra": {
                                "items": {
                                    "additionalProperties": false,
                                    "nullable": true,
                                    "properties": {
                                        "cost_per_meter": {
                                            "default": 0.001,
                                            "format": "double",
                                            "maximum": 10000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "cost_per_minute": {
                                            "default": 0.001,
                                            "format": "double",
                                            "maximum": 10000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "cost_per_shift": {
                                            "default": 0.001,
                                            "format": "double",
                                            "maximum": 1000000,
                                            "minimum": 0,
                                            "type": "number"
                                        },
                                        "max_length": {
                                            "default": 100000000,
                                            "format": "int32",
                                            "maximum": 100000000,
                                            "minimum": 1,
                                            "type": "integer"
                                        },
                                        "max_time": {
                                            "default": 43800,
                                            "format": "int32",
                                            "maximum": 43800,
                                            "minimum": 1,
                                            "type": "integer"
                                        }
                                    },
                                    "required": [
                                        "cost_per_shift",
                                        "cost_per_meter",
                                        "max_length",
                                        "cost_per_minute",
                                        "max_time"
                                    ],
                                    "type": "object"
                                },
                                "maxItems": 10,
                                "minItems": 0,
                                "type": "array"
                            }
                        },
                        "required": [
                            "basic"
                        ],
                        "type": "object"
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
                    "key",
                    "shifts"
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
        "trips": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "actions": {
                        "items": {
                            "additionalProperties": false,
                            "properties": {
                                "location_time": {
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
                                "order_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                },
                                "order_time": {
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
                                "warehouse_key": {
                                    "maxLength": 1024,
                                    "minLength": 1,
                                    "type": "string"
                                }
                            },
                            "required": [
                                "order_key",
                                "order_time",
                                "location_time"
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
                    "performer_key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
                    },
                    "trip_time": {
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
                    "performer_key",
                    "trip_time"
                ],
                "type": "object"
            },
            "maxItems": 9000,
            "minItems": 0,
            "type": "array"
        },
        "warehouses": {
            "items": {
                "additionalProperties": false,
                "properties": {
                    "key": {
                        "maxLength": 1024,
                        "minLength": 1,
                        "type": "string"
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
                    "work_windows": {
                        "items": {
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
                        "maxItems": 100,
                        "minItems": 0,
                        "type": "array"
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
        }
    },
    "required": [
        "warehouses",
        "orders",
        "performers",
        "trips"
    ],
    "type": "object"
}'''