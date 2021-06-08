# Overview
---

Este projeto é um dashboard de investimento. 
Os dados são de planilhas excel, extraidos do site da XP e armazenados em um bucket S3 da AWS. 
O frontend é feito usando dash by Plotly. 

O Objetivo: 
- Verificar o balanço da carteira; 
- Visualizar a evolução dos ativos;
- Acompanhar quais estão performando bem e quais não;
- Ajudar na decisão de investimentos.

# Getting Started
---

This is an example of how to list things you need to use the software and hot to install them.

1. Clone the repo
2. Set python path
``` 
export $PTYHONPATH=app/src 
```

3. Install virtualenv and set virtualenv
``` 
pip install virtualenv
virtualenv env
source env/bin/activate
```

## Running App locally using docker

``` 
docker build -t <image_name>:<image_version> .
``` 

After application is build succesfully, image can by started with following command:

``` 
docker run -p 8051:8051 --rm  <docker_image_name>:<image_version>
Information about command options:
``` 

--rm removes the container after stopping it. There is always a fresh version of configuration and other features while running the app.
-v In the case of bind mounts, the first field is the path to the file or directory on the host machine. The second field is the path where the file or directory is mounted in the container.
-p maps a port from container to localhost
