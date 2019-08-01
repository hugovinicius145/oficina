Projeto em Desenvolvimento para Gerenciar uma Oficina de Moto.

Para Instalar O Projeto:

    Python 3 Instalado.

    Instalar Driver MySql:
       sudo apt-get install python3-dev libmysqlclient-dev

    Criar Database 'oficina'.

    Criar arquivo de configuração do MySql:
        sudo nano /etc/mysql/oficina.cnf

        Arquivo /etc/mysql/oficina.cnf:
        
            !includedir /etc/mysql/conf.d/
            !includedir /etc/mysql/mysql.conf.d/
            [client]
            database = oficina
            user = [nome-usuario]
            password = [senha]
            default-character-set = utf8


    Reiniciar Serviço MySql:
       sudo systemctl daemon-reload

    Instalar o PIP:
        sudo apt install python3-pip

    Criar Ambiente Virtual:
	    python3 -m venv venv

    Ativar o Ambiente Virtual:
	    source venv/bin/activate
    
    Instalar as dependências do projeto:
        pip install -r requirements.txt

    Criar um super usuario de admin:
	    python manage.py createsuperuser

    Validar as configurções de Models:
        python manage.py makemigrations

    Criar as tabelas no banco:
        python manage.py migrate

    Executar a Aplicação:
	    python manage.py runserver
