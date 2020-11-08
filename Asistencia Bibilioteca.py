from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

clientes= pd.read_csv('/Users/juanvecino/PycharmProjects/BiblotecaICAI/venv/clientes.csv',sep=';',encoding='utf8')
pagados= pd.read_csv('/Users/juanvecino/PycharmProjects/BiblotecaICAI/venv/pagados.csv',sep=';',encoding='utf8')

usuario = clientes['Usuario']
clave = clientes['Clave']
lista_pagados=[]

for pagar in pagados['Pagados']:
    lista_pagados.append(pagar)

for i in range(len(clientes)):
    #Medidas de seguridad
    if usuario[i] in lista_pagados:
        print('Continua..')
    else:
        quit()
    #Chrome driver GENERAL

    path = "/Users/juanvecino/Desktop/Selenium/chromedriver"
    driver = webdriver.Chrome(path)

    # Abrir Página

    driver.get('https://www.comillas.edu/es/biblioteca/20769')


    # Meterse dentro de la página

    pagina1 = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/a/img')
    pagina1.click()


    # Log_in


    try:

        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.NAME,"leid"))
        )
        element.send_keys(str(usuario[i]))
        log_in_contra = driver.find_element_by_id('lepass')
        log_in_contra.send_keys(str(clave[i]))
        conectar = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[2]/div/fieldset/form/a')
        conectar.click()
        #Reservar puesto
        reservar_web = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[3]/div[2]/a')
        reservar_web.click()

        #Sucursal
        sucursal = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div/form/div[3]/select/option[9]')
        sucursal.click()
        tipo_recurso = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div/form/div[4]/select/option[3]')
        tipo_recurso.click()
        #Alquilar Puesto
        solicitud = []
        puestos = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div/form/table')
        base= puestos.text
        menos = base.find('%')
        base=base[menos-4:]
        base = base.split('Solicitar')
        del base[-1]

        for bases in base:
            posi = bases.find('%')
            numero = int(bases[1:posi])
            solicitud.append(numero)
        posicion= solicitud.index(max(solicitud))

        element= driver.find_element_by_id(f'calDatepicker{posicion+1}')
        ActionChains(driver) \
            .key_down(Keys.COMMAND) \
            .click(element) \
            .key_up(Keys.CONTROL) \
            .perform()
        driver.switch_to.window(driver.window_handles[-1])

        #Maximizar pantalla
        driver.maximize_window()

        #Zoom
        driver.execute_script("document.body.style.zoom='100%'")

        #Escoger dia
        dia_ver = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/label[1]/span')
        dia_ver.click()

        siguiente_dia= driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[3]/button[3]')
        siguiente_dia.click()

    finally:
        print('Pimer proceso acabado')
    #Proceso de escoger una hora

    dia_semana = driver.find_element_by_xpath('//*[@id="calendar"]/div/div[2]/table/tbody/tr/td[2]')
    dia = dia_semana.text
    lista_semanas = []
    lista_semanas.append(dia)

    for dias in lista_semanas:
        final = dias.find('\n') 
        dia_semanal = str(dias[:final])

    horas= clientes[dia_semanal][i]
    horazas= horas.split('-')
    hora1 = horazas[0]
    hora2 = horazas[1]

    hora_1 = 0
    hora_1+= int(hora1[:2])
    if hora1[-2]=='3':
        hora_1+=0.5

    hora_2 = 0
    hora_2+= int(hora2[:2])
    if hora2[-2]=='3':
        hora_2+=0.5

    diferencia_horas= hora_2-hora_1

    #Subir/Bajar
    if hora_1<=14:
        subir=ActionChains(driver)
        subir.reset_actions()
        subir.move_by_offset(1787,127).click().perform()
    else:
        bajar = ActionChains(driver)
        bajar.reset_actions()
        bajar.move_by_offset(1787, 900).click().perform()

    #Saber que hora queremos
    incremento_horainicial=130 + ((hora_1-8)*2)*60
    hora_inicio= ActionChains(driver)
    hora_inicio.reset_actions()
    hora_inicio.move_by_offset(930,incremento_horainicial).click().perform()
    #Arrastrar
    incremento = ((diferencia_horas)*2 -1)*60
    arrastrar= ActionChains(driver)
    arrastrar.reset_actions()
    arrastrar.drag_and_drop_by_offset(driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/table/tbody/tr[2]/td[2]/div/div/div[3]'),0,incremento)\
        .perform()

    time.sleep(5)
    driver.quit()