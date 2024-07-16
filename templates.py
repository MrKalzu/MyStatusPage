base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="{refresh}">
    <style>
        body {{
            background-color: #2e2e2e; /* Dark gray background color */
            color: #ffffff; /* White text color for better readability */
        }}
        .server {{
            display: flex;
            flex-direction: row;
            padding: 20px;
            width: 100%; /* Ensures the parent div takes full width */
            box-sizing: border-box; /* Includes padding and border in the element's total width and height */
        }}
        .server-content {{
            width: 70%; /* 70% width for server content */
        }}
        .connection {{
            padding: 20px;
            border: 2px solid gray;
            width: 20%; /* 30% width for connection div */
            box-sizing: border-box; /* Includes padding and border in the element's total width and height */
        }}
    </style>
    <title>Server Status</title>
</head>
<body>
    {server_statuses}
</body>
</html>
"""


server_status_template = """
<!-- {server} {status} -->
<div class="server" style="padding: 20px; border: 2px solid {color}; background-color: {bg_color}; color: {text_color};">
    <div class="server-content">
        <h2>Server: {server}</h2>
        <h3>Status: {status}</h3>
        <p>Last Ping: {last_ping}</p>
    </div>
    {connection_statuses}
</div>
"""

connection_status_template = """
<div class="connection" style="padding: 20px; border: 2px solid {color}; background-color: {bg_color}; color: {text_color};">
    <h2>Connection: {connection}</h2>
    <h3>Status: {status}</h3>
    <p>Last Ping: {last_ping}</p>
</div>
"""
