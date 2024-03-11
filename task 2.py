# Prepared By Yadnesh Kolhe
# March 10,2024 Sunday
# Task2: Go to the website given below and retrieve the details first 50 products.
# Create dashboards in Power BI. Use brands as a slicer.

from bs4 import BeautifulSoup
import openpyxl
import re
import requests

def main():
    # Url
    # url = "https://www.amazon.com/gp/bestsellers/electronics/172659"
    # from above amazon url data save in the "Amazon.html" file
    with open('Amazon.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')

    # Find all divs from html file
    divs = soup.find_all('div', class_='a-cardui _cDEzb_grid-cell_1uMOS expandableGrid p13n-grid-content')
    # divs = soup.find_all('div', class_='a-link-normal')

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    headers = ['brandname',	'product_name',	'product_price','product_no_of_reviews',
               'product_rating','screen_size','resolution',	'product_dimension',
               'refresh_rate','special_feature','model_name','included_components']

    sheet.append(headers)

    for div in divs:
        # Name
        product_name = div.find('div', class_="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
        product_name = product_name.text.strip() if product_name else " "

        # product price
        product_price = div.find('span', class_='a-size-base')
        product_price = product_price.text.strip() if product_price else " "
        product_price = float(product_price.replace("$", "").replace(",",""))

        # product number of reviews
        product_no_of_reviews = div.find('span', class_='a-size-small')
        product_no_of_reviews = product_no_of_reviews.text.strip() if product_no_of_reviews else " "
        product_no_of_reviews = int(product_no_of_reviews.replace(",", ""))

        # Product ratings
        product_rating = div.find('span', class_='a-icon-alt')
        product_rating = product_rating.text.strip() if product_rating else " "
        product_rating = float(product_rating[:3])

        # find the product link
        href_link = div.find('div', class_='p13n-sc-uncoverable-faceout').find('a', class_='a-link-normal')['href']

        response = requests.get(href_link)

        if response.status_code < 500:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            product_info = soup.find('div', class_='celwidget', id='productOverview_feature_div').get_text(strip=True)

            brandname, screen_size, supported_internetservices, display_technology, product_dimension, \
                resolution, refresh_rate, special_feature, model_name, included_components = data_extraction(product_info)

            # Dump in to the excel file
            sheet.append([brandname, product_name, product_price, product_no_of_reviews, product_rating, screen_size,
                          resolution, product_dimension, refresh_rate, special_feature, model_name, included_components ])

        else:
            print("Failed to access to data. Status code:", response.status_code)

    # Save the Excel file
    workbook.save('Top50_TVs_data.xlsx')


def data_extraction(prod_desc):
    screen_size_pattern = re.compile(r'Screen Size(\d+ Inches)')
    brand = re.compile(r'Brand(\w+)\s*Supported')
    supported_internet_services = re.compile(r'Services([\w\s]+?)Display')
    display_technology = re.compile(r'Technology([\w\s]+)Product')
    product_dimension = re.compile(r'Dimensions([\s\S]+?)Resolution')
    resolution = re.compile(r'Resolution([\s\S]+?)Refresh')
    refresh_rate = re.compile(r'Rate([\s\S]+?)Special')
    special_feature = re.compile(r'Feature([\s\S]+?)Model')
    model_name_pattern = re.compile(r'Model Name([\s\S]+?)Included')
    included_components = re.compile(r'Included Components(.+?)See more')

    brandname = brand.search(prod_desc).group(1) if brand.search(prod_desc) else "not available"
    screen_size = screen_size_pattern.search(prod_desc).group(1) if screen_size_pattern.search(prod_desc) else "not available"
    supported_internetservices = supported_internet_services.search(prod_desc).group(1) if supported_internet_services.search(prod_desc) else "not available"
    display_technology = display_technology.search(prod_desc).group(1) if display_technology.search(prod_desc) else "not available"
    product_dimension = product_dimension.search(prod_desc).group(1) if product_dimension.search(prod_desc) else "not available"
    resolution = resolution.search(prod_desc).group(1) if resolution.search(prod_desc) else "not available"
    refresh_rate = refresh_rate.search(prod_desc).group(1) if refresh_rate.search(prod_desc) else "not available"
    special_feature = special_feature.search(prod_desc).group(1) if special_feature.search(prod_desc) else "not available"
    model_name = model_name_pattern.search(prod_desc).group(1) if model_name_pattern.search(prod_desc) else "not available"
    included_components = included_components.search(prod_desc).group(1) if included_components.search(prod_desc) else "not available"

    return brandname, screen_size, supported_internetservices, display_technology, product_dimension, \
        resolution, refresh_rate, special_feature, model_name, included_components


if __name__ == '__main__':
    main()