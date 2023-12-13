insert_task_and_time = {
  "name": "insert_task_and_time",
  "description": "A function that takes in a task, start date, and end date and inserts it into the JSON from Notion API",
  "parameters": {
    "type": "object",
    "properties": {
      "task": {
        "type": "string",
        "description": "Task"
      },
      "start_date": {
        "type": "string",
        "description": "Start date of the task in ISO 8601 format"
      },
      "end_date": {
        "type": "string",
        "description": "End date of the task in ISO 8601 format"
      }
    },
    "required": [
      "task",
      "start_date",
      "end_date"
    ]
  }
}
