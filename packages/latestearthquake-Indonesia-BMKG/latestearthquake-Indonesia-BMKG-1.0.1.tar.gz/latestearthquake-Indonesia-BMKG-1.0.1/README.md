# Latest Indonesia Earthquake
This package will get the latest earthquake from Indonesia Meteorological, Climatological, and Geophysical Agency (BMKG). 

## HOW IT WORK
This package will scrape from [BMKG](https://www.bmkg.go.id ) to get latest earthquake happened in Indonesia

This package will use BeautifulSoup4 and Requests  to produce output in the form of JSON that is ready to be used in web or mobile application.

## HOW TO USE 
```
import latestearthquake

if __name__ == '__main__':
    result = latestearthquake.data_extraction()
    latestearthquake.show_data(result)
```

# Author
Christian Yurianja