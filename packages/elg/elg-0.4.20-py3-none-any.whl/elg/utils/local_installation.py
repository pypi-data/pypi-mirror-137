DOCKER_COMPOSE = """\
version: "3.7"

services:
  
{LTSERVICES}

  restserver:
    image: registry.gitlab.com/european-language-grid/ilsp/elg-lt-service-execution-all:production-reactive
    command:
    - "--logging.level.elg.ltserviceexecution.api=WARN"
{LTSERVICES_URL}
    - "--elg.base.url=http://localhost:{EXPOSE_PORT}{EXECUTION_PATH}"
{EXPOSE_PORT_CONFIG}
    restart: always

{GUIS}

{FRONTEND}

"""

EXPOSE_PORT_CONFIG = """\
    ports:
    - "{EXPOSE_PORT}:8080"
"""

LTSERVICE = """\
  {LTSERVICE_NAME}:
    image: "{LTSERVICE_IMAGE}"
    restart: always\
"""

LTSERVICE_WITH_SIDECAR = """\
  {LTSERVICE_NAME}:
    image: "{LTSERVICE_IMAGE}"
    restart: always

  sidecar:
    image: "{SIDECAR_IMAGE}"
    network_mode: "service:{LTSERVICE_NAME}"
    depends_on:
      - {LTSERVICE_NAME}
"""

LTSERVICE_URL = (
    '    - "--elg.ltservices.staticServices.{LTSERVICE_NAME}=http://{LTSERVICE_NAME}:{LTSERVICE_PORT}{LTSERVICE_PATH}"'
)

GUI = """\
  {GUI_NAME}:
    image: "{GUI_IMAGE}"
    restart: always
"""

FRONTEND = """\
  frontend:
    image: "nginx:alpine"
    ports:
    - "{EXPOSE_PORT}:80"
    volumes:
    - type: bind
      source: ./nginx-conf
      target: /etc/nginx/templates
    restart: always
"""

DEFAULT_CONF_TEMPLATE = """\
log_format upstream_logging '[$time_local] $remote_addr - $remote_user - $server_name to: $upstream_addr: $request upstream_response_time $upstream_response_time msec $msec request_time $request_time';

server {{
    listen       80;
    server_name  localhost;

    location / {{
        alias /etc/nginx/conf.d/html/;
        index  index.html index.htm;
    }}

    location ~ \.json {{
        root /etc/nginx/templates/records;
    }}

    location /i18n/ {{
        proxy_pass https://live.european-language-grid.eu/i18n/;
    }}

    location /execution/ {{
        access_log /dev/stdout upstream_logging;
        proxy_pass http://restserver:8080/;
    }}

{GUIS}

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {{
        root   /usr/share/nginx/html;
    }}
}}
"""

GUI_CONF_TEMPLATE = """\
    location /{GUI_NAME}/ {{
          access_log /dev/stdout upstream_logging;
          proxy_pass http://{GUI_NAME}:{GUI_PORT}/;
      }}
"""

HTML_INDEX_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ELG Local Installation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Display:wght@600&display=swap" rel="stylesheet">
    <style>
      body {{
        font-family: 'Noto Sans Display', sans-serif;
        background-color: #f8f4ed;
        display: flex;
        flex-direction: column;
      }}
      body > * {{
        margin-inline: auto;
      }}
      h1,h2 {{
        font-weight: 600;
        width: 900px;
        text-align: center;
      }}
      h1 {{
        font-size: 32px;
        margin-bottom: 32px;
      }}
      h2 {{
        font-size: 24px;
      }}
      iframe {{
        margin-bottom: 32px;
        background-color: white;
      }}
    </style>
    
</head>
<body>
<h1>European Language Grid<br/>Local Installation</h1>
{IFRAMES}
<script>
{SCRIPTS}
</script>
</body>
</html>
"""

HTML_INDEX_IFRAME = """\
<h2>[{LTSERVICE_ID}] {LTSERVICE_FULL_NAME}</h2>
<iframe width="900" height="500" id="{LTSERVICE_NAME}" src="about:blank"></iframe>
"""

HTML_INDEX_SCRIPT = """\
window.addEventListener('message', function (e) {{
  document.getElementById('{LTSERVICE_NAME}').contentWindow.postMessage(JSON.stringify({{
    "StyleCss":" ",
    "ServiceUrl":window.location.origin+"/execution/async/process/{LTSERVICE_NAME}",
    "ApiRecordUrl":window.location.origin+"/{LTSERVICE_NAME}.json"
  }}), window.location.origin);
}}, false);

document.getElementById('{LTSERVICE_NAME}').src = '/{GUI_NAME}/{GUI_PATH}';
"""
