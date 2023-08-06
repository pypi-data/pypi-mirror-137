# Latest Indonesia Earthquake
This package will get the latest earthquake from Indonesia Meteorological, Climatological, and Geophysical Agency (BMKG). 

## HOW IT WORK
This package will scrape from [BMKG](https://www.bmkg.go.id ) to get latest earthquake happened in Indonesia

This package will use BeautifulSoup4 and Requests  to produce output in the form of JSON that is ready to be used in web or mobile application.

## HOW TO USE 
```
import latestearthquake

if __name__ == '__main__':
    gempa_di_indonesia = latestearthquake.GempaTerkini('https://bmkg.go.id')
    print(f'Aplikasi utama menggunakan package yang memiliki deskripsi {gempa_di_indonesia.description}')
    gempa_di_indonesia.tampilkan_keterangan()
    gempa_di_indonesia.run()
```

# Author
Christian Yurianja