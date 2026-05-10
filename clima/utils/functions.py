from dotenv import load_dotenv
import os
import psycopg2
import datetime
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