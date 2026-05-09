from dotenv import load_dotenv
import os
import psycopg2

def definir_tamanho_calendario(mes):
    match mes:
        case 