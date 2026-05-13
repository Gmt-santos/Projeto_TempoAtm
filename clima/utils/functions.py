from dotenv import load_dotenv
import os
import psycopg2
import datetime as dt
import calendar as cal
def lista_de_dias(primeiro_dia,tamanho_mes):
    lista=[]
    i=1
    match primeiro_dia:
        case 1:
            lista.append("")
            lista.append("")
        case 2:
            lista.append("")
            lista.append("")
            lista.append("")
        case 3:
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
        case 4:
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
        case 5:
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")

        case 6:
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")
            lista.append("")


    while i<=tamanho_mes:
        lista.append(i)
        i+=1
    return lista

def coletar_primeirodia_mes(ano,mes):
    cal.setfirstweekday(6)
    tupla=cal.monthrange(ano,mes)
    return tupla

def string_mes(mes):
    match mes:
        case 1:
            return "Janeiro"
        case 2:
            return "Fevereiro"
        case 3:
            return "Março"
        case 4:
            return "Abril"
        case 5:
            return "Maio"
        case 6:
            return "Junho"
        case 7:
            return "Julho"
        case 8:
            return "Agosto"
        case 9:
            return "Setembro"
        case 10:
            return "Outubro"
        case 11:
            return "Novembro"
        case 12:
            return "Dezembro"

def mes_real():
    __obj=dt.date.today()
    return int(__obj.month)

def ano_real():
    __obj=dt.date.today()
    return int(__obj.year)

def retirar_id_lat_long(value:str):
    flaglat=False
    flaglong=False
    lat=""
    long=""
    for char in value:
        if(not flaglat and not flaglong):
            id=char
        if(flaglat and char !="/"):
            lat+=char
        if(char == ">"):
            flaglat=True
       
        if (char == "/"):
            flaglat=False
            flaglong=True

        if(flaglong and char !="/"):
            flaglong=True
    return int(id),int(lat),int(long)