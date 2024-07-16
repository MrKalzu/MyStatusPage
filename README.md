# Statuspage Generator

A Python script that generates a simple statuspage HTML file. The HTML file can be served with any HTTP server, such as nginx.

## Features

- Generates a status page for multiple servers
- Runs as a daemon process
- Configurable via INI file
- Uses only Python 3 standard libraries

## Installation

1. Clone the repository:

 - git clone https://github.com/MrKalzu/statuspage-generator

2. Go to the directory:

cd statuspage-generator

3. Copy the example configuration file:

cp examples/example.config.ini config.ini

4. Edit the configuration file to suit your needs:

vim config.ini

## Usage

To start the service:

- Foreground mode: `python3 service.py`
- Daemon mode: `python3 service.py start`

Other daemon commands:
- Stop the service: `python3 service.py stop`
- Restart the service: `python3 service.py restart`

## Configuration

The `config.ini` file controls the behavior of the Statuspage Generator. Here are the main configuration options:

- `listen`: IP address to bind to (default: 0.0.0.0)
- `port`: Port to listen on (default: 8080)
- `web_dir`: Directory to store the generated HTML file
- `status_page_file`: Name of the generated HTML file
- `database_file`: Path to the SQLite database file
- `failure_interval`: Time (in seconds) before a server is considered down
- `update_interval`: Frequency (in seconds) of status page updates
- `log_file`: Path to the log file
- `log_level`: Logging level (INFO, ERROR, or DEBUG)
- `stdout_logs`: Whether to print logs to stdout
- `pid_file`: Path to the PID file for daemon mode

The `[Servers]` section lists the servers to monitor and their access tokens.

For a full example, see `examples/example.config.ini`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]

## Acknowledgements

Most of the stuff in this repository was generated using ChatGPT and Claude.ai.
