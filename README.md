# Python + Flask + wfastcgi + MiniConda + IIS + Swagger

![logo do projeto](docs/logo.png)

Aplicação em python de exemplo rodando em um contêiner Docker configurado sob o IIS por meio  Wfastcgi.

Aplicação conta com a geração de log e a disponibilização de um serviço a fim de verificar o status do aplicativo.

A aplicação conta também com o uso do Swagger a fim de dispobilizar informações (documentação) das APIs da aplicação.


# Criação da Imagem Docker

Para criação da imagem e execução, favor executar o seguinte comando na raiz do projeto:

    docker-compose build
    docker-compose up -d

Antes de realizar a criação do contêiner, configure o volume para uma pasta em sua máquina.

# Acesso à documentação da aplicação (Swagger)

Com o container em execução, acesse o seguinte endereço:

    http://<endereço ip>:8001


# Acesso ao serviço de exempo

Com o container em execução, acesse o seguinte endereço:

    http://<endereço ip>:8001/app/status
    