from random import randint
import csv

def poblar(n, path, mes, email, deviceid):
    amb_lim_sup = 2
    amb_lim_inf = 0
    luz_lim_sup = 50
    luz_lim_inf = 25
    header = ['tmpambiente','humedad','luz','tmpagua','timestamp','email','deviceid']
    print(header)
    with open(path, mode='w') as fd:
        writer = csv.writer(fd)
        writer.writerow(header)
        for dia in range(1,n+1):  #dia
            if int(dia) < 10:
                dia = '0' + str(dia)
            for hora in range(24):  #hora
                row = []
                if hora < 12:
                    base = hora
                else:
                    base = 24 - hora
                tmpambiente = str(8 + base + randint(amb_lim_inf, amb_lim_sup))
                row.append(tmpambiente)
                humedad = str(25 + round(base/2) + randint(amb_lim_inf, amb_lim_sup))
                row.append(humedad)
                if hora > 7 and hora < 19:
                    luz_base = 20
                else:
                    luz_base = 1
                luz = str(10 + (luz_base*hora) + randint(luz_lim_inf, luz_lim_sup))
                row.append(luz)
                tmpagua = str(6 + base + randint(amb_lim_inf, amb_lim_sup))
                row.append(tmpagua)
                #2023-05-04 18:33:38 UTC
                if hora < 10:
                    hora = '0' + str(hora)
                timestamp = '2023-' + mes + '-' + str(dia) + ' ' + str(hora) + ':00:00'
                row.append(timestamp)
                row.append(email)
                row.append(deviceid)
                print(row)

                writer.writerow(row)

if __name__ == '__main__':
    #n días, destino, mes como '05'
    poblar(30, 'abril_htd2.csv', '04', 'rodrinoya.1@gmail.com', 'htd2')

