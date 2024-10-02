from bs4 import BeautifulSoup as Soup
from typing import Any
import requests
import os

URL = "https://dentalstall.com/shop/page"
public_folder = os.path.join(os.getcwd(), "public", "images")


def pages(page: str, save_img: bool = False) -> dict[Any]:
    page = requests.get(f"{URL}/{page}")
    html = Soup(page.content, "html.parser")
    products = []

    product_containers = html.find_all("div", class_="product-inner clearfix")

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
