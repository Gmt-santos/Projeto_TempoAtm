# Projeto TempoAtm ou MatWeather

## Descrição do projeto
<p>Um sistema que possibilite a criação de eventos, sua consulta, sua exclusão e sua edição, além de possibilitar uma consulta à condição climática do dia do evento em questão.</p>

## Tecnologias utilizadas
-Python;<br>
-Django;<br>
-PostgreSQL;<br>
-[API da OpenMeteo](https://open-meteo.com/);<br>
-HTML;<br>
-CSS;<br>
-JavaScript.

### Outras tecnologias e bibliotecas essenciais
-Psycopg;<br>
-Argon2.<br>

## Como executar na sua máquina
### 1-Instalar requisitos
```bash
python install -r requirements.txt
```
### 2-Ativar o servidor
```bash
python manage.py runserver
```
### 3- Abrir o link gerado(geralmente 'localhost' )
```bash
System check identified no issues (0 silenced).
May 24, 2026 - 07:42:27
Django version 6.0.3, using settings 'app_clima.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
### 4- Banco de dados
Crie um banco de dados com o exato script dado em [db_example.txt](https://github.com/Gmt-santos/Projeto_TempoAtm/blob/main/db_example.txt) e atente-se com a criação do arquivo .env com credenciais do seu servidor.
### 5- Precauções
Lembre-se de criar um arquivo 'local_settings.py' no formato:
```bash
SECRET_KEY = 'chave django'
DEBUG = True
ALLOWED_HOSTS = [HOSTS PERMITIDOS]
```
Com uma SECRET_KEY válida, por isso talvez seja necessário inicializar um app Django e sobrescrever ele com o ProjetoTempoAtm, atentando-se a deixar a SECRET_KEY intacta.

## Imagens
<img src="https://github.com/Gmt-santos/Projeto_TempoAtm/blob/main/static_files/media/images/example1_img.png?raw=true">
<img src="https://github.com/Gmt-santos/Projeto_TempoAtm/blob/main/static_files/media/images/example2_img.png?raw=true">