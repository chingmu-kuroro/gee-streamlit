import streamlit as st
import ee
import geemap.foliumap as geemap
from oauth2client.service_account import ServiceAccountCredentials
import json

st.set_page_config(layout="wide")
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")

# 讀取 Streamlit Secret 中的 GEE 憑證
gee_json = st.secrets["GEE_SERVICE_ACCOUNT"]

# 轉為憑證物件
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    gee_json,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# 初始化 Earth Engine
ee.Initialize(credentials)

# 地理區域
point = ee.Geometry.Point([121.56, 25.03])

# 擷取 Landsat NDVI
image = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2") \
    .filterBounds(point) \
    .filterDate("2022-01-01", "2022-12-31") \
    .median()

ndvi = image.normalizedDifference(["SR_B5", "SR_B4"]).rename("NDVI")

# 顯示地圖
Map = geemap.Map(center=[25.03, 121.56], zoom=10)
Map.addLayer(ndvi, {"min": 0, "max": 1, "palette": ["white", "green"]}, "NDVI")
Map.to_streamlit(height=600)
