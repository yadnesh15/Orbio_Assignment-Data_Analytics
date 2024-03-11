# Prepared By Yadnesh Kolhe
# March 08,2024 Friday
# Task1:Scrape the below mentioned amazon URLs with python libraries and output save into the Json format

import requests
from bs4 import BeautifulSoup
import os
import re

def scrape_amazon_product(url,lst):
    ##### Send an HTTP GET request to the Amazon product page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product information
        product_title = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
        name = re.compile(r'([\S\d\w\s]+?TV)').search(product_title).group(1)

        product_price = soup.find('span', {"class": "a-price-whole"}).get_text(strip=True)
        # product_price = soup.find('span', {"class": "a-offscreen"}).get_text(strip=True)

        rating = soup.find('span', {"class": "a-icon-alt"}).get_text(strip=True)

        no_of_rating = soup.find('span', {"id": "acrCustomerReviewText"}).get_text(strip=True)

        product_description = soup.find('div', {'id': 'productOverview_feature_div'}).get_text(strip=True)
        image_url = soup.find('div', {'id': 'imgTagWrapperId'}).find('img')['src']

        brandname, screen_size, supported_internetservices, display_technology, product_dimension, \
            resolution, refresh_rate, special_feature, model_name, included_components = data_extraction(product_description)

        product_info = {"name":name,
                        "model-number":product_title,
                        "rating":rating,
                        "no-of-rating":no_of_rating,
                        "image":image_url,
                        "price":product_price,
                        "additional-information":
                            {"brand-name":brandname,
                             "screen-size":screen_size,
                             "supported-internet-services":supported_internetservices,
                             "display-technology":display_technology,
                             "resolution":resolution,
                             "refresh-rate":refresh_rate,
                             "special-features": special_feature,
                             "model-name":model_name,
                             "included-components":included_components
                            }
                        }

    else:
        print("Failed to access to data. Status code:", response.status_code)

    return product_info

def data_extraction(prod_desc):

    # test = """
    # Screen Size40 InchesBrandHisenseSupported Internet ServicesGoogle TVDisplay TechnologyLCDProduct
    # Dimensions3.3"D x 35.4"W x 20.3"HResolution1080pRefresh Rate60 HzSpecial FeatureGame Mode,
    # FlatModel NameA4 SeriesIncluded ComponentsStand, TV, Remote Control, Power CableSee more
    # """

    # patterns matching
    screen_size_pattern = re.compile(r'Screen Size(\d+ Inches)')
    # brand = re.compile(r'Brand(\w+)')
    # brand = re.compile(r'Brand(\w+)(?=\b)')
    brand = re.compile(r'Brand(\w+)\s*Supported')
    supported_internet_services = re.compile(r'Services([\w\s]+)Display')
    display_technology = re.compile(r'Technology([\w\s]+)Product')
    product_dimension = re.compile(r'Dimensions([\s\S]+?)Resolution')
    resolution = re.compile(r'Resolution([\s\S]+?)Refresh')
    refresh_rate = re.compile(r'Rate([\s\S]+?)Special')
    special_feature = re.compile(r'Feature([\s\S]+?)Model')
    model_name_pattern = re.compile(r'Model Name([\s\S]+?)Included')
    included_components = re.compile(r'Included Components(.+?)See more')


    brandname = brand.search(prod_desc).group(1) if brand.search(prod_desc).group(1) else "not available"
    screen_size = screen_size_pattern.search(prod_desc).group(1) if screen_size_pattern.search(prod_desc).group(1)  else "not available"
    supported_internetservices = supported_internet_services.search(prod_desc).group(1) if supported_internet_services.search(prod_desc).group(1) else "not available"
    display_technology = display_technology.search(prod_desc).group(1) if display_technology.search(prod_desc).group(1) else "not available"
    product_dimension = product_dimension.search(prod_desc).group(1) if product_dimension.search(prod_desc).group(1) else "not available"
    resolution = resolution.search(prod_desc).group(1) if resolution.search(prod_desc).group(1) else "not available"
    refresh_rate = refresh_rate.search(prod_desc).group(1) if refresh_rate.search(prod_desc).group(1) else "not available"
    special_feature = special_feature.search(prod_desc).group(1) if special_feature.search(prod_desc).group(1) else "not available"
    model_name = model_name_pattern.search(prod_desc).group(1) if model_name_pattern.search(prod_desc).group(1) else "not available"
    included_components = included_components.search(prod_desc).group(1) if included_components.search(prod_desc).group(1) else "not available"

    return brandname,screen_size,supported_internetservices,display_technology,product_dimension,\
        resolution, refresh_rate,special_feature,model_name,included_components


if __name__ == "__main__":
    urls = [
        # "https://www.amazon.com/gp/bestsellers/electronics/172659"
        "https://www.amazon.com/dp/B0C7VBWHLQ/",
        "https://www.amazon.com/dp/B0BCH68K6M/",
        "https://www.amazon.com/dp/B0C9VWK5H5/",
        "https://www.amazon.com/dp/B0C1J4MPBB/"
    ]

    lst= []
    for url in urls:
        data = scrape_amazon_product(url,lst)
        lst.append(data)

    import json
    with open("data.json", 'w') as json_file:
        json.dump(lst, json_file, indent=4)

