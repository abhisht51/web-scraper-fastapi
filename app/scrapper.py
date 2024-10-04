from bs4 import BeautifulSoup as Soup
from typing import Any
import requests
import os
import time

from .logger import Logger

logger = Logger("Atlys Scrapper: ")

URL = "https://dentalstall.com/shop/page"
public_folder = os.path.join(os.getcwd(), "public", "images")


def pages(page: str, proxy_string: str = None, save_img: bool = False) -> dict[Any]:
    products = []
    proxy = {}
    html = None
    # check for valid url?
    if proxy_string:
        proxy = {"https": proxy_string}  # assumed https proxy only

    MAX_RETRIES = 3
    RETRY_DELAY = 3  # seconds
    retries = 0

    while retries < MAX_RETRIES:
        try:
            url_to_fetch = f"{URL}/{page}/"
            logger.info(f"Fetching from page {url_to_fetch}")
            response = requests.get(f"{url_to_fetch}", proxies=proxy)
            if response.status_code == 200:
                html = response
                break
            else:
                raise Exception(
                    f"Failed to fetch webpage. Status code: {response.status_code}"
                )
        except Exception as e:
            retries += 1
            if retries < MAX_RETRIES:
                logger.info(
                    f"Retry {retries}/{MAX_RETRIES} for fetching webpage after error: {e}"
                )
                time.sleep(RETRY_DELAY)
            else:
                logger.error(
                    f"Failed to fetch webpage after {MAX_RETRIES} retries: {URL}/{page}"
                )

    # page = requests.get(f"{URL}/{page}", proxies=proxy)
    soup = Soup(html.content, "html.parser")
    product_containers = soup.find_all("div", class_="product-inner clearfix")

    if not os.path.exists(public_folder):
        os.makedirs(public_folder)

    for product in product_containers:
        title_tag = product.find("h2", class_="woo-loop-product__title")
        product_title = title_tag.text.strip() if title_tag else ""

        price_tag = product.find("span", class_="woocommerce-Price-amount amount")
        product_price = (
            float(price_tag.text.replace("₹", "").replace(",", "").strip())
            if price_tag
            else 0
        )

        image_tag = product.find("img", class_="attachment-woocommerce_thumbnail")
        img_src = image_tag["data-lazy-src"] if image_tag else ""

        if img_src:
            img_name = os.path.basename(img_src)
            path_to_image = os.path.join(public_folder, img_name)

            if save_img:
                # Download and save the image if flag is true
                response = requests.get(img_src)
                if response.status_code == 200:
                    with open(path_to_image, "wb") as img_file:
                        img_file.write(response.content)

            products.append(
                {
                    "product_title": product_title,
                    "product_price": product_price,
                    "path_to_image": path_to_image,
                }
            )

    return products
