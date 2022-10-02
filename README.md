# PONTO DE COLETA - SERVIDOR 
O servidor cria e recebe o payload do Raspberry para armazenar no banco de dados. 

Caso alguma porta esteja em uso, mate-a com: 
```console
sudo fuser -k <PORT>/tcp
```

## Deploy
Para fazer o os saber quais são as variáveis do ambiente:
```console
export $(cat config/.env | xargs) 
```
Para subir a database:
```console
sudo docker-compose up 
```
Para rodar o servidor:
```console
virtualenv venv --python=python3.9 
```
```console
source ./venv/bin/activate
```
```console
pip3 install -r requirements.txt
```
## Broker 
Caso queira criar um broker, instale mosquitto e o execute com:
```console
sudo mosquitto -c ./config/mosquitto.conf -v 
```
Não se esqueça de mudar o que vem depois de "listener" para seu ip!
### :)
Caso queira apagar o banco, rode:
```console
sudo docker volume rm $(sudo docker volume ls -q)
```

