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
    id=value[0]
    value=value.replace(",",".")
    flaglat=False
    flaglong=False
    lat=""
    long=""
    for char in value:
        if(char == ">"):
            flaglat=True
        if(char!=">" and flaglat==True and char !="/"):
            lat+=char
        if(char=="/"):
            flaglat=False
            flaglong=True
        if(char!="/" and flaglong==True):
            long+=char
    return int(id),float(lat),float(long)

def hora_evento(request):
    hora_evento=request.POST.get("hour_event")
    counter=0
    string_hora=hora_evento[0]+hora_evento[1]
    int_hora=int(string_hora)
    if(int_hora==0):
        intervalo_horas=[int_hora,int_hora+1,int_hora+2]
    elif(int_hora ==23):
        intervalo_horas=[int_hora-2,int_hora-1,int_hora]
    else:
         intervalo_horas=[int_hora-1,int_hora,int_hora+1]
    return intervalo_horas

def avaliacao_condicao_climatica(city_info,intervalo):
    '''
    Retorna uma lista contendo características da condição climática
    '''
    '''
    cityinfo
    [0]->Temperatura
    [1]->Umidade relativa
    [2]->Temperatura aparente
    [3]->Probabilidade de chuva
    [4]->Chuva
    [5]->Cobertura por nuvens
    [6]->Velocidade do vento
    
    '''
    city_info_inter=[]
    for register in city_info:
        city_info_inter.append([register[intervalo[0]],register[intervalo[1]],register[intervalo[2]]])
    i=0
    '''
    if temperatura0 and umidade1 and temperatura_aparente2 and probabilidade_de_chuva3 and chuva4 and cobertura_por_nuvens5
    '''
    while i<=2:
        
        #Dia ensolarado
       
        if (city_info_inter[0][i]>=25 and city_info_inter[0][i]<=35)and(city_info_inter[1][i]<30)\
            and city_info_inter[2][i]<=(city_info_inter[0][i]*1.2)and city_info_inter[3][i]<10\
            and city_info_inter[4][i]<2 and city_info_inter[5][i]<=15  :
            return ["light_green-c","sunny","Dia ensolarado","Vá na praia, mas passe protetor solar!!!"]
        
        #Mormaço
       
        elif (city_info_inter[0][i]>=25 and city_info_inter[0][i]<=30)and(city_info_inter[1][i]>70 and city_info_inter[1][i]<90)\
            and city_info_inter[2][i]>(city_info_inter[0][i])and (city_info_inter[3][i]>=20 and city_info_inter[3][i]<=40)\
            and city_info_inter[4][i]<2 and city_info_inter[5][i]>=80:
              return ["rain-c","cloudy","Mormaço","Cuidado redobrado com a pele, passe protetor solar!!!"]
                                                                                                         
       
       #Abafado
        
        elif (city_info_inter[0][i]>=30)and(city_info_inter[1][i]>65)\
            and city_info_inter[2][i]>(city_info_inter[0][i])and (city_info_inter[3][i]>60 and city_info_inter[3][i]<80)\
            and city_info_inter[4][i]<5 and city_info_inter[5][i]>=60 :
              return ["blue-c","sunny","Dia abafado","Quente e sem chuva, mas pode chover a qualquer momento!!!"]
        
        #Dia frio e chuvoso
       
        elif (city_info_inter[0][i]>=10 and city_info_inter[0][i]<=20)and(city_info_inter[1][i]>=90)\
            and city_info_inter[2][i]<(city_info_inter[0][i])and city_info_inter[3][i]>=90\
            and city_info_inter[4][i]>=5 and city_info_inter[5][i]>=90   :
              return ["rain-c","rain","Dia frio e chuvoso","Caso vá sair, leve um agasalho e um guarda-chuva!!!"]
        
        #Nevoeiro
        
        elif (city_info_inter[0][i]>=10 and city_info_inter[0][i]<=20)and(city_info_inter[1][i]>=90)\
            and city_info_inter[2][i]<=(city_info_inter[0][i])and city_info_inter[3][i]<20\
            and city_info_inter[4][i]<5 and city_info_inter[5][i]>=90  :
              return ["rain-c","cloudy","Nevoeiro","Se for dirigir, vá devagar e com atenção!!!"]
       
        #Dia Nublado
       
        elif (city_info_inter[0][i]>=18 and city_info_inter[0][i]<=25)and(city_info_inter[1][i]>=60 and city_info_inter[1][i]<=80)\
            and city_info_inter[2][i]<=(city_info_inter[0][i])and (city_info_inter[3][i]>=20 and city_info_inter[3][i]<=40)\
            and city_info_inter[4][i]<2 and city_info_inter[5][i]>=80  :
              return ["rain-c","cloudy","Dia nublado","Caso vá sair, leve um agasalho e um guarda-chuva!!!"]
        else:
            '''
            Parte mais simplificada, caso as condições anteriores não forem atendidas
            '''
            if(city_info_inter[0][i]>30 and city_info_inter[3][i]<10 and city_info_inter[4][i]<2 ):
              return ["light_green-c","sunny","Dia Quente e ensolarado","Aproveite o Sol, mas passe protetor solar!!!"]
            elif (city_info_inter[3][i]>80 and city_info_inter[4][i]>80 and city_info_inter[5][i]>80):
              return ["rain-c","rain","Dia de Chuva","Caso vá sair,leve um guarda-chuva!!!"]
            elif (city_info_inter[3][i]>40 and city_info_inter[4][i]>40 and city_info_inter[5][i]>40):
              return ["blue-c","cloudy","Dia nublado, com chance de chuva ","Caso vá sair,leve um guarda-chuva!!!"]
            elif(city_info_inter[0][i]<25 and city_info_inter[2][i]<25):
              return ["rain-c","cold","Dia frio","Caso vá sair, leve um agasalho!!!"]
        i+=1    

        '''
        cityinfo
        [0]->Temperatura
        [1]->Umidade relativa
        [2]->Temperatura aparente
        [3]->Probabilidade de chuva
        [4]->Chuva
        [5]->Cobertura por nuvens
        [6]->Velocidade do vento
        
        '''
def load_var_env():
    load_dotenv()
    HOST=os.getenv("HOST")
    USER=os.getenv("USER")
    PASSWORD=os.getenv("PASSWORD")
    DATABASE=os.getenv("DATABASE")
    port=5432
    return HOST,USER,PASSWORD,DATABASE,port