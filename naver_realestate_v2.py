import streamlit as st
import requests
import pandas as pd

# Streamlit page setup
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")
st.title("Real Estate Listings from Pages 1 to 10")
st.markdown("This page fetches and displays real estate listings from pages 1 to 10 using the Naver Real Estate API.")

# Define the cookies and headers as provided

cookies = {
    "NNB": st.secrets["NNB"],
    "ASID": st.secrets["ASID"],
    "__gads": st.secrets["gads"],
    "__gpi": st.secrets["gpi"],
    "_ga": st.secrets["ga"],
    "_ga_8P4PY65YZ2": st.secrets["ga_8P4PY65YZ2"],
    "NFS": st.secrets["NFS"],
    "NID_JKL": st.secrets["NID_JKL"],
    "NAC": st.secrets["NAC"],
    "page_uid": st.secrets["page_uid"],
    "NID_AUT": st.secrets["NID_AUT"],
    "_fwb": st.secrets["fwb"],
    "NACT": st.secrets["NACT"],
    "NID_SES": st.secrets["NID_SES"],
    "SRT30": st.secrets["SRT30"],
    "SRT5": st.secrets["SRT5"],
    "REALESTATE": st.secrets["REALESTATE"]
}


headers = {
    "accept": st.secrets["accept"],
    "language": st.secrets["language"],
    "authorization": st.secrets["authorization"],
    "priority": st.secrets["priority"],
    "referer": st.secrets["referer"],
    "sec-ch-ua": st.secrets["sec_ch_ua"],
    "sec-ch-ua-mobile": st.secrets["sec_ch_ua_mobile"],
    "sec-ch-ua-platform": st.secrets["sec_ch_ua_platform"],
    "sec-fetch-dest": st.secrets["sec_fetch_dest"],
    "sec-fetch-mode": st.secrets["sec_fetch_mode"],
    "sec-fetch-site": st.secrets["sec_fetch_site"],
    "user-agent": st.secrets["user_agent"]
}




# Function to get data from the API for pages 1 to 10
@st.cache_data
def fetch_all_data():
    all_articles = []
    for page in range(1, 11):
        try:
            # Make the request for the specific page
            url = f'https://new.land.naver.com/api/articles/complex/228?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=228&buildingNos=&areaNos=&type=list&order=dateDesc'
            response = requests.get(url, cookies=cookies, headers=headers)

            # Verify response is valid JSON
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])
                all_articles.extend(articles)
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")

    return all_articles

# Fetch data for all pages
data = fetch_all_data()

# Transform data into a DataFrame if data is available
if data:
    df = pd.DataFrame(data)
    # Select columns to display
    df_display = df[["articleNo", "articleName", "realEstateTypeName", "tradeTypeName", "floorInfo",
                     "dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", "articleFeatureDesc",
                     "tagList", "buildingName", "sameAddrMaxPrc", "sameAddrMinPrc", "realtorName"]]

    # Display the table in Streamlit with a clean, readable layout
    st.write("### Real Estate Listings - Pages 1 to 10")
    st.dataframe(df_display)
else:
    st.write("No data available.")
    