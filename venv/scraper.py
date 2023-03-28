import requests
import lxml.html as html
# módulo para crear una carpeta
import os
# módulo para traer la fecha de hoy
import datetime

HOME_URL = 'https://terrenos.com.ec/propiedades/en/pichincha/'

XPATH_LINK_TO_PUBLICATION = '//h2[@class="h5 mb-0 Property__item--list__title"]/a/@href'
XPATH_TITLE = '//div[@class="Properties__title mb-4"]/h1/text()'
XPATH_LOCATION_TITLE = '//div[@class="Properties__title mb-4"]/h2/text()'
XPATH_HEADER = '//div[@class="row Properties__info justify-content-start"]/div[@class="col-6 col-md-3 col text-center"]/h4/small/text()'
XPATH_PRICE_AREA_M2 = '//div[@class="row Properties__info justify-content-start"]/div[@class="col-6 col-md-3 col text-center"]/h4/strong/text()'
XPATH_CODE = '//div[@class="row Properties__info justify-content-start"]/div[@class="col-6 col-md-3 col text-center text-md-right align-self-end"]/h4/strong/text()'
XPATH_TABLE = '//table[@class="table table-hover Properties__Features"]/tbody/tr/td/text()'
XPATH_LATITUDE = '//div[@class="card shadow--lg"]/div/@data-lat'
XPATH_LONGITUDE = '//div[@class="card shadow--lg"]/div/@data-lng'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                # para remplazar y dejar sin textos adicionales
                title = title.replace('\"','')
                location_title = parsed.xpath(XPATH_LOCATION_TITLE)[0]
                header = parsed.xpath(XPATH_HEADER)
                price_area_m2 = parsed.xpath(XPATH_PRICE_AREA_M2)
                code = parsed.xpath(XPATH_CODE)[0]
                table = parsed.xpath(XPATH_TABLE)
                latitude = parsed.xpath(XPATH_LATITUDE)[0]
                longitude = parsed.xpath(XPATH_LONGITUDE)[0]

            except IndexError:
                return
            
            # guardar en un archivo, formato y contenido
            with open(f'{today}/{code}.txt', 'w', encoding= 'utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(location_title)
                f.write('\n\n')
                header_str = ','.join(header)
                f.write(header_str)
                f.write('\n\n')
                price_area_m2_str = ' / '.join(price_area_m2)
                f.write(price_area_m2_str)
                f.write('\n\n')
                f.write(code)
                f.write('\n\n')
                f.write(' '.join(table))
                f.write('\n\n')
                f.write(latitude)
                f.write('\n\n')
                f.write(longitude)
                f.write('\n\n')

        else:
            raise ValueError(f'Error:{response.status_code}')
    except ValueError as ve:
        print(ve)


# Hacer que si sale algún error se prevea
def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # decode es un metodo que permite transformar caracteres especiales
            home = response.content.decode('utf-8')
            # Toma el conenido de html en home y lo transforma en un documento para hacer xpath 
            parsed = html.fromstring(home)
            links_to_publication = parsed.xpath(XPATH_LINK_TO_PUBLICATION)
            # print(links_to_publication)

            # dar formato al momento en el que se extraen los datos
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_publication:
                parse_notice(link, today)
                
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()