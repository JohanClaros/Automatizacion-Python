from datetime import datetime, timedelta
 
def restar_hora(hora1,hora2):
    formato = "%H:%M:%S"
    lista = hora2.split(":")
    hora=int(lista[0])
    minuto=int(lista[1])
    segundo=int(lista[2])
    h1 = datetime.strptime(hora1, formato)
    dh = timedelta(hours=hora) 
    dm = timedelta(minutes=minuto)          
    ds = timedelta(seconds=segundo) 
    resultado1 =h1 - ds
    resultado2 = resultado1 - dm
    resultado = resultado2 - dh
    resultado=resultado.strftime(formato)
    return str(resultado)
 
print(restar_hora("04:30:50","04:29:30"))