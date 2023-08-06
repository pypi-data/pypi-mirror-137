<p align="center">
  <a  href="https://github.com/NoeCruzMW/zpy-flask-msc-docs"><img width="150" src="https://lh3.googleusercontent.com/a-/AOh14GjLO5qYYR5nQl5hgavUKz4Dv3LVzWDvGtV4xNam=s600-k-no-rp-mo" alt="Zurck'z"></a>
</p>
<p align="center">
    <em>ZDB Core, Layer for connect to mysql or oracle from python</em>
</p>
<p align="center"></p>

---

# ZPy Database Core

> Zurck'z Py

This package contains some helpers features for call function or stored procedures from python.

ZPy use the following packages:

- mysql-connector-python
- cx-Oracle

## Requirements

- Python 3.6+

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install py flask micro service core .

```bash
pip install zpy
pip install package_directory directory_to_install
```

## Features

Contains some helper features with specific integrations.

- Database
    - Only MySQL implementation
        - Functions executor
        - Stored Procedures executor
        - Autocommit is false by default
- Utils
    - funcs

## Roadmap

- ActiveRecord implementation
- Cluster

## Basic Usage

Basic Configuration

````python

config = {
    "user": "",
    "password": "",
    "database": "",
    "host": "",
    "port": 3306
}
````

With single datasource

```python
# Create database mediator with single datasource
db_manager = ZMediator.single(config, True)
# Open connection
db_conn = db_manager.default().new_connect()
try:
    # Execute function
    res = db_manager.default().exec("FN_GET_USER_BY_ID(%d)", list_params=[1], ret_type=DBTypes.cursor)
    print(res)
except Exception as e:
    logging.exception(e)
finally:
    # ⚠ Remember close opened connection
    db_conn.close()
```

Multiple Datasources

```python
# Define db mediator 
# Setup base configuration in ZMediator()
# The base configuration will be overwritten by add common values 
db_mngr = ZMediator(config, False)
.add_common("DB_NAME_1", "DB_USER", "DB_PASSWORD", True)  # Mark default ds
.add_common("DB_NAME_2", "DB_USER", "DB_PASSWORD")
.add_common("DB_NAME_3", "DB_USER", "DB_PASSWORD")

db_conn1 = db_mngr.default().new_connect()
db_conn2 = db_mngr.get("DB_NAME_1").new_connect()
db_conn3 = db_mngr.get("DB_NAME_3").new_connect()

try:
    # Execute function
    res = db_mngr.default().exec("FN_GET_USER_BY_ID(%d)", list_params=[1], ret_type=DBTypes.cursor)
    print(res)
    # Execute function
    res = db_mngr.get("DB_NAME_2").exec("FN_GET_USER_BY_ID(%d)", list_params=[1], ret_type=DBTypes.cursor)
    print(res)
    # Call sp
    res = db_mngr.get("DB_NAME_3").call("SP_GET_DATA", ret_type=DBTypes.cursor)
    print(res)
except Exception as e:
    logging.exception(e)
finally:
    # ⚠ Remember close opened connections
    db_conn1.close()
    db_conn2.close()
    db_conn3.close()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

[Noé Cruz](https://www.linkedin.com/in/zurckz/)
