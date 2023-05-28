# CDC Event Schema

## Example Event

```json
{
	"payload" : {
		"before" : null,
		"after" : {
			"_id": {
				"$oid" : "645fe9eaf4790c34c8fcc2ed"
			},
			"description" : "buy milk",
			"creation_timestamp" : {
				"$date" : 1684007402978
			},
			"due_date" : {
				"$date" : 1684266602978
			},
			"completed" : false
		}
	}
}
```

## JSON Schema Definition

```json
{
	"$schema": "https://json-schema.org/draft/2020-12/schema",
	"$id": "https://example.com/product.schema.json",
	"type" : "object",
	"properties" : {
		"payload" : {
			"type" : "object",
			"properties" : {
				"before" : {
					"oneOf" : [{ "type" : "null" }, { "$ref" : "#/$defs/todoItem" }]
				},
				"after" : {
					"oneOf" : [{ "type" : "null" }, { "$ref" : "#/$defs/todoItem" }]
				}
			},
			"required" : ["before", "after"]
		}
	},
	"required" : ["payload"],
   "$defs" : {
	  "todoItem" : {
		  "title": "TodoItem",
		  "description": "An item in a todo checklist",
	  	  "type" : "object",
		  "properties" : {
			  "_id" : {
				  "type" : "object",
				  "properties" : {
					  "$oid" : {
						  "type" : "string"
					  }
				  }
			  },
			  "description" : {
				  "type" : "string"
			  },
			  "creation_timestamp" : {
				  "type" : "object",
				  "properties" : {
					  "$date" : {
						  "type" : "integer"
					  }
				  }
			  },
			  "due_date" : {
			  		"anyOf" : [
						{
							"type" : "object",
							"properties" : {
								"$date" : {
									"type" : "integer"
								}
							}
						},
						{
							"type" : "null"
						}
					]
			  },
			  "completed" : {
				  "type" : "boolean"
			  }
		  },
		  "required" : ["_id", "description", "creation_timestamp", "completed"]
	  }
  }
}
```
