import streamlit as st
import folium
from streamlit_folium import st_folium

# 관광지 데이터
tourist_spots = [
    {
        "name": "에펠탑 (Eiffel Tower)",
        "location": [48.8584, 2.2945],
        "description": "에펠탑은 파리의 상징이자 세계에서 가장 유명한 랜드마크 중 하나입니다. 전망대에서는 파리 전경을 한눈에 감상할 수 있습니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg"
    },
    {
        "name": "루브르 박물관 (Louvre Museum)",
        "location": [48.8606, 2.3376],
        "description": "세계에서 가장 큰 미술관으로, 모나리자와 같은 걸작들이 전시되어 있습니다. 유리 피라미드가 입구에 있습니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Louvre_Museum_Wikimedia_Commons.jpg/640px-Louvre_Museum_Wikimedia_Commons.jpg"
    },
    {
        "name": "몽생미셸 (Mont Saint-Michel)",
        "location": [48.636, -1.5115],
        "description": "프랑스 북서부 해안에 위치한 작은 섬이자 수도원. 밀물과 썰물에 따라 섬이 되기도 하고 육지가 되기도 합니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Mont-Saint-Michel_vu_du_ciel.jpg"
    },
    {
        "name": "베르사유 궁전 (Palace of Versailles)",
        "location": [48.8049, 2.1204],
        "description": "루이 14세가 건설한 화려한 궁전으로 프랑스 절대왕정의 상징입니다. 정원과 거울의 방이 특히 유명합니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/32/Versailles_Palace%2C_Gardens%2C_and_Fountains.jpg"
    },
    {
        "name": "니스 해변 (Nice Beach)",
        "location": [43.6959, 7.2655],
        "description": "프랑스 리비에라에 위치한 지중해 해변으로, 푸른 바다와 아름다운 해안 산책로로 유명합니다.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e4/Nice_vue_promenade_des_Anglais.jpg"
    },
]

# Streamlit UI
st.title("🇫🇷 프랑스 주요 관광지 가이드")
st.markdown("프랑스의 아름다운 관광지를 지도와 함께 알아보세요!")

# 관광지 선택
spot_names = [spot["name"] for spot in tourist_spots]
selected_spot = st.selectbox("관광지를 선택하세요:", spot_names)

# 선택된 관광지 정보 표시
spot_info = next(spot for spot in tourist_spots if spot["name"] == selected_spot)
st.subheader(spot_info["name"])
st.image(spot_info["image"], use_column_width=True)
st.markdown(f"📍 **위치:** {spot_info['location'][0]}, {spot_info['location'][1]}")
st.write(spot_info["description"])

# Folium 지도 생성
m = folium.Map(location=spot_info["location"], zoom_start=6)
for spot in tourist_spots:
    folium.Marker(
        location=spot["location"],
        popup=folium.Popup(f"<b>{spot['name']}</b><br>{spot['description']}", max_width=300),
