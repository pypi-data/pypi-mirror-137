# Earthquake in Indonesia
General Information about latest earthquake **especially in Indonesia.**

## The work-flow
Package scrape from [[bmkg]](https://www.bmkg.go.id/).

*This package using **beautifulSoup4 and request**, 
from JSON can be used on mobile & web applications*

## Step to use
```
import dataoflatestearthquakeindonesia

if __name__ == '__main__':
    earthquake_in_indonesia = dataoflatestearthquakeindonesia.Dataoflatestearthquakeindonesia('https://bmkg.go.id')
    print(f'Main application of package using description{earthquake_in_indonesia.description}')
    dataoflatestearthquakeindonesia.show_data()
    earthquake_in_indonesia.run()
```

## Author
Idea by **Eko S Wibowo as a coach of rwid**

tried project to learning python -**gustus**

