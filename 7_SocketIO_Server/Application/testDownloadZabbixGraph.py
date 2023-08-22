
ULR_LOGIN = 'http://157.65.24.169/index.php?name=Admin&password=zabbix&enter=Sign%20in'
URL_GRAPH = 'http://157.65.24.169/chart.php?from=2023-06-25%2000%3A51%3A00&to=2023-06-25%2003%3A34%3A00&itemids%5B0%5D=44379&type=0&profileIdx=web.item.graph.filter&profileIdx2=44379&width=1082&height=300'

image_filename = "downloaded_image.png"

import requests.sessions as sessions

def download_image(url, filename):
    with sessions.Session() as session:
      session.request(method="get", url=ULR_LOGIN)
      response = session.request(method="get", url=URL_GRAPH)
    
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")


download_image(URL_GRAPH, image_filename)

