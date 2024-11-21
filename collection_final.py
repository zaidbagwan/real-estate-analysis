from bs4 import BeautifulSoup
import os
import pandas as pd


data = {
    "Society_Name": [],
    "Locality": [],
    "Price": [],
    "Average Price": [],
    "BHK Type": [],
    "Area": [],
    "Possession Status": [],
    "Furnishing": [],
    "Bathrooms": [],
    "Balcony": [],
}


base_dir = r"C:\Users\Zaid\OneDrive\Desktop\lotlite\MagicBricks\Magicbricks_final_final"

# Set to track unique entries (based on a key like society_name + locality + price)
unique_entries = set()

if not os.path.exists(base_dir):
    print(f"Directory not found: {base_dir}")
else:
    missing_society_names = []
    missing_avg_prices = []
    duplicate_entries_count = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    html_doc = f.read()
                    soup = BeautifulSoup(html_doc, "html.parser")

                    title = soup.find("div", class_="mb-srp__card__developer")
                    if title:
                        society_name = title.get_text(strip=True)
                    else:

                        society_name_tag = soup.find("div", {"data-summary": "society"})
                        society_name = (
                            society_name_tag.find(
                                "div", class_="mb-srp__card__summary--value"
                            ).get_text(strip=True)
                            if society_name_tag
                            else "N/A"
                        )

                    if society_name == "N/A":
                        missing_society_names.append(file_path)

                    avg_price_tag = soup.find("div", class_="mb-srp__card__price--size")
                    if avg_price_tag:
                        avg_price = avg_price_tag.get_text(strip=True)
                    else:

                        avg_price_alt = soup.find("div", {"data-summary": "avg-price"})
                        avg_price = (
                            avg_price_alt.get_text(strip=True)
                            if avg_price_alt
                            else "N/A"
                        )

                    if avg_price == "N/A":
                        missing_avg_prices.append(file_path)

                    locality_tag = soup.find("h2", class_="mb-srp__card--title")
                    locality = (
                        locality_tag.get_text(strip=True).split(" in ")[-1]
                        if locality_tag
                        else "N/A"
                    )

                    price_tag = soup.find("div", class_="mb-srp__card__price--amount")
                    price = price_tag.get_text(strip=True) if price_tag else "N/A"

                    bhk_tag = soup.find("h2", class_="mb-srp__card--title")
                    bhk_type = (
                        bhk_tag.get_text(strip=True).split("Flat")[0].strip()
                        if bhk_tag
                        else "N/A"
                    )

                    area_tag = soup.find(
                        "div", class_="mb-srp__card__summary__list"
                    ).find("div", class_="mb-srp__card__summary--value")
                    area = area_tag.get_text(strip=True) if area_tag else "N/A"

                    status_tag = soup.find("div", {"data-summary": "status"})
                    possession_status = (
                        status_tag.find(
                            "div", class_="mb-srp__card__summary--value"
                        ).get_text(strip=True)
                        if status_tag
                        else "N/A"
                    )

                    furnishing_tag = soup.find("div", {"data-summary": "furnishing"})
                    furnishing = (
                        furnishing_tag.find(
                            "div", class_="mb-srp__card__summary--value"
                        ).get_text(strip=True)
                        if furnishing_tag
                        else "N/A"
                    )

                    bathroom_tag = soup.find("div", {"data-summary": "bathroom"})
                    bathrooms = (
                        bathroom_tag.find(
                            "div", class_="mb-srp__card__summary--value"
                        ).get_text(strip=True)
                        if bathroom_tag
                        else "N/A"
                    )

                    balcony_tag = soup.find("div", {"data-summary": "balcony"})
                    balcony = (
                        balcony_tag.find(
                            "div", class_="mb-srp__card__summary--value"
                        ).get_text(strip=True)
                        if balcony_tag
                        else "N/A"
                    )

                    unique_key = (
                        society_name,
                        locality,
                        price,
                        avg_price,
                        bhk_type,
                        area,
                        possession_status,
                        furnishing,
                        bathrooms,
                        balcony,
                    )

                    if unique_key not in unique_entries:
                        unique_entries.add(unique_key)

                        data["Society_Name"].append(society_name)
                        data["Locality"].append(locality)
                        data["Price"].append(price)
                        data["Average Price"].append(avg_price)
                        data["BHK Type"].append(bhk_type)
                        data["Area"].append(area)
                        data["Possession Status"].append(possession_status)
                        data["Furnishing"].append(furnishing)
                        data["Bathrooms"].append(bathrooms)
                        data["Balcony"].append(balcony)

                    else:
                        duplicate_entries_count += 1

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    df = pd.DataFrame(data)

    csv_path = "magicbricks_new_data_final11.csv"
    try:
        df.to_csv(csv_path, index=False)
        print(f"CSV file created successfully: {csv_path}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

    if missing_society_names:
        print(f"Files missing society names: {len(missing_society_names)}")
    if missing_avg_prices:
        print(f"Files missing average prices: {len(missing_avg_prices)}")
    if duplicate_entries_count:
        print(f"Duplicate entries while scrapping: {duplicate_entries_count}")

    print(f"Scraped unique entries: {len(unique_entries)}")

    print(df)
