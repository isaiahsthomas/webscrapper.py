import requests
import pandas as pd

def get_json_response(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def extract_details_from_json(json_response):
    properties = json_response['cat1']['searchResults']['listResults']
    
    addresses = [prop.get('address', None) for prop in properties]
    prices = [prop.get('price', None) for prop in properties]
    beds = [prop.get('beds', None) for prop in properties]
    baths = [prop.get('baths', None) for prop in properties]
    area = [prop.get('area', None) for prop in properties]
    links = [f"https://www.zillow.com{prop.get('detailUrl', '')}" for prop in properties]
    
    data = {
        'Address': addresses, 
        'Price': prices, 
        'Beds': beds, 
        'Baths': baths, 
        'Area (sqft)': area, 
        'Links': links
    }
    df = pd.DataFrame(data)
    return df

def main():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    url = "https://www.zillow.com/search/GetSearchPageState.htm"
    
    params = {
        "searchQueryState": """{"pagination":{},"usersSearchTerm":"Pembroke Pines, FL","mapBounds":{"west":-80.43885391088867,"east":-80.21672408911132,"south":25.90498558277996,"north":26.148088598786437},"regionSelection":[{"regionId":19892,"regionType":6}],"isMapVisible":true,"filterState":{"sortSelection":{"value":"globalrelevanceex"},"isAllHomes":{"value":true}},"isListVisible":true,"mapZoom":12}""",
        "wants": """{"cat1":["listResults","mapResults"],"cat2":["total"]}""",
        "requestId": "3"
    }
    
    dfs = []
    
    for page in range(1, 11):
        params["searchQueryState"] = params["searchQueryState"].rsplit("}", 1)[0] + f', "pagination": {{"currentPage": {page}}}}}'
        json_response = get_json_response(url, headers, params)
        df = extract_details_from_json(json_response)
        dfs.append(df)
    
    final_df = pd.concat(dfs, ignore_index=True)
    print(final_df)

if __name__ == "__main__":
    main()

