import requests
from bs4 import BeautifulSoup


def extract_data():
    """
    Date: 24 August 2021
    Time: 12:05:52 WIB
    Magnitude: 4.0
    Depth: 40 km
    Location: LS=1.48  BT=134.01
    Main Earthquake Notes: Pusat gempa berada didarat 18 km barat laut ransiki
    Felt (Scale MMI): II-III Manokwari, II-III Ransiki
    :return:
    """
    try:
        content = requests.get('https://www.bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        date = result[0]
        time = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitude = None
        depth = None
        ls = None
        bt = None
        location = None
        felt = None

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
                felt = res.text
            i = i + 1

        result = dict()
        result['date'] = date
        result['time'] = time
        result['magnitude'] = magnitude
        result['depth'] = depth
        result['coordinate'] = {'ls': ls, 'bt': bt}
        result['location'] = location
        result['felt'] = felt
        return result
    else:
        return None

def show_data(result):
    if result is None:
        print("Latest Earthquake Not Found")
        return
    print('Latest Earthquake based on BMKG')
    print(f"date: {result['date']} ")
    print(f"time: {result['time']} ")
    print(f"magnitude: {result['magnitude']} ")
    print(f"depth: {result['depth']} ")
    print(f"location {result['location']} ")
    print(f"coordinate: LS={result['coordinate']['ls']}, BT={result['coordinate']['bt']} ")
    print(f"closest near: {result['felt']}")

if __name__ == '__main__':
    result = extract_data()
    show_data(result)