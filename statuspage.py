import json
import time
import os
from templates import base_template, server_status_template, connection_status_template

class Statuspage:
    def __init__(self, settings, db,  logger) -> None:
        self.settings = settings
        self.db = db
        self.logger = logger
        self.html_file = os.path.join(settings['web_dir'], settings['status_page_file'])
        self.update_interval = int(settings['update_interval'])
        self.failure_interval = int(settings['failure_interval'])

        # Check if the web_dir exists, create it if it doesn't
        os.makedirs(os.path.dirname(self.html_file), exist_ok=True)

    def update_status(self):
        """Update the status HTML page based on the latest ping data."""
        rows = self.db.get_server_statuses()
        self.logger.debug(f"Server statuses: {rows}")
    
        server_statuses = ""
        current_time = time.time()
        current_server = None
        server_data = {}
    
        for row in rows:
            server, last_ping_time, connection, last_update = row
            if server not in server_data:
                server_data[server] = {
                    'last_ping': last_ping_time,
                    'connections': []
                }
            if last_update is not None:
                server_data[server]['connections'].append((connection, last_update))
    
        for server, data in server_data.items():
            last_ping_time = data['last_ping']
            if current_time - last_ping_time < self.failure_interval:
                status = "UP"
                color = "#28a745"
                bg_color = "#1c3b1a"
                text_color = "#c3e6cb"
            else:
                status = "DOWN"
                color = "#dc3545"
                bg_color = "#441a1f"
                text_color = "#f5c6cb"
    
            last_ping = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_ping_time))
    
            connection_statuses = ""
            for connection, last_update in data['connections']:
                if last_update == 0:  # Connection is down
                    conn_status = "DOWN"
                    conn_color = "#dc3545"
                    conn_bg_color = "#441a1f"
                    conn_text_color = "#f5c6cb"
                    last_connection_ping = "N/A"
                else:
                    if current_time - last_update < self.failure_interval:
                        conn_status = "UP"
                        conn_color = "#28a745"
                        conn_bg_color = "#1c3b1a"
                        conn_text_color = "#c3e6cb"
                    else:
                        conn_status = "DOWN"
                        conn_color = "#dc3545"
                        conn_bg_color = "#441a1f"
                        conn_text_color = "#f5c6cb"
                    last_connection_ping = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update))
    
                connection_statuses += connection_status_template.format(
                    connection=connection,
                    status=conn_status,
                    last_ping=last_connection_ping,
                    color=conn_color,
                    bg_color=conn_bg_color,
                    text_color=conn_text_color
                )
    
            server_statuses += server_status_template.format(
                server=server,
                status=status,
                last_ping=last_ping,
                connection_statuses=connection_statuses,
                color=color,
                bg_color=bg_color,
                text_color=text_color
            )
    
        with open(self.html_file, "w") as f:
            f.write(base_template.format(
                refresh=self.update_interval,
                server_statuses=server_statuses
            ))
