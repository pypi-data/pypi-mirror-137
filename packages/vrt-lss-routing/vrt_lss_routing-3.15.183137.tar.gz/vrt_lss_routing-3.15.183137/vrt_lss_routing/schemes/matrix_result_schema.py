MATRIX_RESULT_SCHEMA = '''{
    "additionalProperties": false,
    "properties": {
        "matrix": {
            "additionalProperties": false,
            "nullable": true,
            "properties": {
                "distances": {
                    "items": {
                        "items": {
                            "format": "int64",
                            "maximum": 10000000,
                            "minimum": -1,
                            "type": "integer"
                        },
                        "maxItems": 9000,
                        "minItems": 2,
                        "type": "array",
                        "uniqueItems": false
                    },
                    "maxItems": 9000,
                    "minItems": 2,
                    "type": "array",
                    "uniqueItems": false
                },
                "durations": {
                    "items": {
                        "items": {
                            "format": "int64",
                            "maximum": 10000000,
                            "minimum": -1,
                            "type": "integer"
                        },
                        "maxItems": 9000,
                        "minItems": 2,
                        "type": "array",
                        "uniqueItems": false
                    },
                    "maxItems": 9000,
                    "minItems": 2,
                    "type": "array",
                    "uniqueItems": false
                },
                "waypoints": {
                    "items": {
                        "additionalProperties": false,
                        "nullable": true,
                        "properties": {
                            "duration": {
                                "default": 0,
                                "format": "int32",
                                "maximum": 43800,
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
                            },
                            "name": {
                                "maxLength": 1024,
                                "minLength": 0,
                                "type": "string"
                            }
                        },
                        "required": [
                            "latitude",
                            "longitude"
                        ],
                        "type": "object"
                    },
                    "maxItems": 9000,
                    "minItems": 2,
                    "type": "array",
                    "uniqueItems": false
                }
            },
            "required": [
                "waypoints",
                "distances",
                "durations"
            ],
            "type": "object"
        },
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
        }
    },
    "required": [
        "matrix"
    ],
    "type": "object"
}'''