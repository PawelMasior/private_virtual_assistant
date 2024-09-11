### Table: `chat_completions`

| Column Name     | Type       | Not Null | Default Value       | Primary Key |
| --------------- | ---------- | -------- | ------------------- | ----------- |
| `id`            | `INTEGER`  | False    | `None`              | True        |
| `invocation_id` | `TEXT`     | False    | `None`              | False       |
| `client_id`     | `INTEGER`  | False    | `None`              | False       |
| `wrapper_id`    | `INTEGER`  | False    | `None`              | False       |
| `session_id`    | `TEXT`     | False    | `None`              | False       |
| `source_name`   | `TEXT`     | False    | `None`              | False       |
| `request`       | `TEXT`     | False    | `None`              | False       |
| `response`      | `TEXT`     | False    | `None`              | False       |
| `is_cached`     | `INEGER`   | False    | `None`              | False       |
| `cost`          | `REAL`     | False    | `None`              | False       |
| `start_time`    | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |
| `end_time`      | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |

### Table: `agents`

| Column Name  | Type       | Not Null | Default Value       | Primary Key |
| ------------ | ---------- | -------- | ------------------- | ----------- |
| `id`         | `INTEGER`  | False    | `None`              | True        |
| `agent_id`   | `INTEGER`  | False    | `None`              | False       |
| `wrapper_id` | `INTEGER`  | False    | `None`              | False       |
| `session_id` | `TEXT`     | False    | `None`              | False       |
| `name`       | `TEXT`     | False    | `None`              | False       |
| `class`      | `TEXT`     | False    | `None`              | False       |
| `init_args`  | `TEXT`     | False    | `None`              | False       |
| `timestamp`  | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |

### Table: `oai_wrappers`

| Column Name  | Type       | Not Null | Default Value       | Primary Key |
| ------------ | ---------- | -------- | ------------------- | ----------- |
| `id`         | `INTEGER`  | False    | `None`              | True        |
| `wrapper_id` | `INTEGER`  | False    | `None`              | False       |
| `session_id` | `TEXT`     | False    | `None`              | False       |
| `init_args`  | `TEXT`     | False    | `None`              | False       |
| `timestamp`  | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |

### Table: `oai_clients`

| Column Name  | Type       | Not Null | Default Value       | Primary Key |
| ------------ | ---------- | -------- | ------------------- | ----------- |
| `id`         | `INTEGER`  | False    | `None`              | True        |
| `client_id`  | `INTEGER`  | False    | `None`              | False       |
| `wrapper_id` | `INTEGER`  | False    | `None`              | False       |
| `session_id` | `TEXT`     | False    | `None`              | False       |
| `class`      | `TEXT`     | False    | `None`              | False       |
| `init_args`  | `TEXT`     | False    | `None`              | False       |
| `timestamp`  | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |

### Table: `version`

| Column Name      | Type      | Not Null | Default Value | Primary Key |
| ---------------- | --------- | -------- | ------------- | ----------- |
| `id`             | `INTEGER` | False    | `None`        | True        |
| `version_number` | `INTEGER` | True     | `None`        | False       |

### Table: `events`

| Column Name        | Type       | Not Null | Default Value       | Primary Key |
| ------------------ | ---------- | -------- | ------------------- | ----------- |
| `event_name`       | `TEXT`     | False    | `None`              | False       |
| `source_id`        | `INTEGER`  | False    | `None`              | False       |
| `source_name`      | `TEXT`     | False    | `None`              | False       |
| `agent_module`     | `TEXT`     | False    | `NULL`              | False       |
| `agent_class_name` | `TEXT`     | False    | `NULL`              | False       |
| `id`               | `INTEGER`  | False    | `None`              | True        |
| `json_state`       | `TEXT`     | False    | `None`              | False       |
| `timestamp`        | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |

### Table: `function_calls`

| Column Name     | Type       | Not Null | Default Value       | Primary Key |
| --------------- | ---------- | -------- | ------------------- | ----------- |
| `source_id`     | `INTEGER`  | False    | `None`              | False       |
| `source_name`   | `TEXT`     | False    | `None`              | False       |
| `function_name` | `TEXT`     | False    | `None`              | False       |
| `args`          | `TEXT`     | False    | `NULL`              | False       |
| `returns`       | `TEXT`     | False    | `NULL`              | False       |
| `timestamp`     | `DATETIME` | False    | `CURRENT_TIMESTAMP` | False       |
