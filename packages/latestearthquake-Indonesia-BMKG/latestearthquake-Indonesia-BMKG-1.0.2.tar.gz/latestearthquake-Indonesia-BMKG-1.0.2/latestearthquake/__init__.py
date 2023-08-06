import requests
from bs4 import BeautifulSoup
"""
Method = fungsi
Field / Attribute = variabel 
Constructor = method yang dipanggil pertama kali saat objek diciptakan.
              Gunakan untuk mendeklarasikan semua field pada class ini.
Contohnya:

def __init__(self, url, description):
        self.description = description
        self.result = None
        self.url = url
"""

class Bencana:
    def __init__(self, url, description):
        self.description = description
        self.result = None
        self.url = url

    def tampilkan_keterangan(self):
        print(self.description)

    def scraping_data(self):
        print('scraping_data Not Yet Implemented')

    def show_data(self):
        print('show_data Not Yet Implemented')

    def run(self):
        self.scraping_data()
        self.show_data()


class BanjirTerkini(Bencana):
    def __init__(self, url):
        super(BanjirTerkini, self).__init__(url, 'NOT YET IMPLEMENTED, but it should return last flood in Indonesia')

    def tampilkan_keterangan(self):
        print(f'UNDER CONSTRUCTION {self.description} ')

class GempaTerkini(Bencana):
    def __init__(self, url):
        super(GempaTerkini, self).__init__(url, 'To get the latest earthquake in Indonesia from bmkg.go.id')

    # Extract data from Website
    def scraping_data(self):
        try:
            content = requests.get(self.url)
        except Exception:
            return None

        if content.status_code == 200:
            # Get and assign Date and Time data
            soup = BeautifulSoup(content.text, 'html.parser') #1. INSTATIATION = INSTANSIASI = PENCIPTAAN OBJEK DARI CLASS
            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            date = result[0]
            time = result[1]

            # Get and assign magnitude, depth, ls, bt, location, and perceived data
            result = soup.find('div', {'class', 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')

            i = 0
            magnitude = None
            depth = None
            ls = None
            bt = None
            location = None
            perceived = None

            for res in result:
                if i == 1:
                    magnitude = res.text
                elif i == 2:
                    depth = res.text
                elif i == 3:
                    coordinate = res.text.split(' - ')
                    ls = coordinate[0]
                    bt = coordinate[1]
                elif i == 4:
                    location = res.text
                elif i == 5:
                    perceived = res.text
                i = i + 1

            output = dict()
            output['date'] = date
            output['time'] = time
            output['magnitude'] = magnitude
            output['depth'] = depth
            output['coordinate'] = {'ls': ls, 'bt': bt}
            output['location'] = location
            output['perceived'] = perceived
            self.result = output
        else:
            return None

    # Show the data from extraction

    def show_data(self):
        if self.result is None:
            print('Latest earthquake data is not found')
            return
        print('Latest earthquake based on BMKG')
        print(f"Date: {self.result['date']}")
        print(f"Time: {self.result['time']}")
        print(f"Magnitude: {self.result['magnitude']}")
        print(f"Depth: {self.result['depth']}")
        print(f"Coordinate: LS={self.result['coordinate']['ls']}, BT={self. result['coordinate']['bt']}")
        print(f"Location: {self.result['location']}")
        print(f"Perceived: {self.result['perceived']}")

if __name__ == '__main__':
    gempa_di_indonesia = GempaTerkini('https://bmkg.go.id')
    gempa_di_indonesia.tampilkan_keterangan()
    gempa_di_indonesia.run()

    banjir_di_indonesia = BanjirTerkini('NOT YET')
    banjir_di_indonesia.tampilkan_keterangan()
    banjir_di_indonesia.run()

    daftar_bencana = [gempa_di_indonesia, banjir_di_indonesia]
    print('\nSemua bencana yang ada')
    for bencana in daftar_bencana:
        bencana.tampilkan_keterangan()

    # gempa_di_dunia = GempaTerkini('https://bmkg.go.id')
    # print('\nDeskripsi class GempaTerkini', gempa_di_dunia.description)
    # gempa_di_dunia.run()

    # gempa_di_indonesia.data_extraction()
    # gempa_di_indonesia.show_data()