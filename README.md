# Python + Flask + wfastcgi + MiniConda + IIS + Swagger
![logo do projeto](docs/logo.png)
Aplicação em python de exemplo rodando em um contêiner Docker configurado sob o IIS por meio  WFastCGI.

Aplicação conta com a geração de log e a disponibilização de um serviço a fim de verificar o status do aplicativo e todas as configurações do IIS/AppPool para rodar modelos analíticos com bibliotecas suportados pelo Python/Conda/PIP/R.

A aplicação conta também com o uso do Swagger a fim de dispobilizar informações (documentação) das APIs REST da aplicação.

# Pré-requisitos da máquina de desenvolvimento
	
	Windows 10 Pro/Enterprise (Home Edition não suportado pela Microsoft) ou Windows Server 2019 Version 1803
	Instalação do Docker conforme procedimento microsoft
		https://docs.microsoft.com/en-us/virtualization/windowscontainers/quick-start/set-up-environment?tabs=Windows-10
	

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
    