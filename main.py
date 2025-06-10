import streamlit as st
import folium
from streamlit_folium import st_folium

# 도시별 관광지 데이터
cities = {
    "파리": {
        "에펠탑": {
            "location": [48.8584, 2.2945],
            "description": """
**에펠탑 (Tour Eiffel)**  
프랑스 파리의 상징이자 대표 관광지로, 야경이 아름답고 전망대에서는 파리 전경을 감상할 수 있습니다.
"""
        },
        "루브르 박물관": {
            "location": [48.8606, 2.3376],
            "description": """
**루브르 박물관 (Musée du Louvre)**  
모나리자와 밀로의 비너스를 비롯한 세계적 명화를 감상할 수 있는 세계 최대 규모의 미술관입니다.
"""
        },
        "베르사유 궁전": {
            "location": [48.8049, 2.1204],
            "description": """
**베르사유 궁전 (Château de Versailles)**  
프랑스 왕실의 호화로운 궁전으로, 아름다운 정원과 거울의 방이 유명합니다.
"""
        }
    },
    "노르망디": {
        "몽생미셸": {
            "location": [48.6361, -1.5115],
            "description": """
**몽생미셸 (Mont-Saint-Michel)**  
바다 위에 떠 있는 듯한 수도원 섬으로, 유네스코 세계유산에 등재되어 있습니다.  
밀물과 썰물의 차이로 인한 변화가 매우 신비롭습니다.
"""
        }
    }
}

# Streamlit 앱 구성
st.set_page_config(page_title="프랑스 관광지 가이드", layout="wide")
st.title("🇫🇷 도시별 프랑스 관광지 가이드")
st.write("프랑스 주요 도시별 관광지를 친절하게 안내해드립니다.")

# 사이드바에서 도시 선택
city_names = list(cities.keys())
selected_city = st.sidebar.selectbox("도시를 선택하세요", city_names)

# 선택한 도시의 관광지 목록
spots_in_city = list(cities[selected_city].keys())
selected_spot = st.sidebar.selectbox("관광지를 선택하세요", spots_in_city)

# 관광지 정보
spot_info = cities[selected_city][selected_spot]
lat, lon = spot_info["location"]
description = spot_info["description"]

# 관광지 정보 출력
st.subheader(f"📍 {selected_spot} ({selected_city})")
st.markdown(description)

# 지도 출력
m = folium.Map(location=[lat, lon], zoom_start=6)
folium.Marker([lat, lon], tooltip=selected_spot, popup=selected_spot,
              icon=folium.Icon(color='blue')).add_to(m)
st_folium(m, width=700, height=500)
