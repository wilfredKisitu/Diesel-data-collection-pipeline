# Project Structure

```
diesel/
├── DB/                         # SQLite database files
│   ├── diesel_data.db          # Local SQLite database
│   └── .gitkeep
├── dev/                        # Python virtual environment
├── devices/                    # Device communication modules
│   ├── __init__.py
│   ├── device_module.py        # Base DataReader abstract class
│   ├── device_types.py         # Device type definitions
│   ├── status_codes.py         # Status/error code constants
│   ├── serial_reader.py        # Serial port reader implementation
│   ├── modbus_reader.py        # Modbus reader implementation
│   ├── usb_serial_reader.py    # USB serial reader implementation
│   ├── usb_modbus_reader.py    # USB Modbus reader implementation
│   └── device.md               # Devices documentation
├── main/                       # Entry point scripts
│   ├── __init__.py
│   └── run_data_reader.py      # Main runner script
├── storage/                    # Storage backend modules
│   ├── __init__.py
│   ├── db_interface.py         # Abstract storage interface
│   ├── local/                  # Local storage implementations
│   │   └── sqlite_db.py        # SQLite storage implementation
│   └── cloud/                  # Cloud storage implementations
│       └── neon_db.py          # Neon (PostgreSQL) storage implementation
├── .env.local                  # Local environment variables
├── .gitignore
├── requirements.txt
└── struct.md                   # This file
```
