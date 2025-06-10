import streamlit as st
import folium
from streamlit_folium import st_folium

# 관광지 정보 데이터
tourist_spots = {
    "에펠탑": {
        "location": [48.8584, 2.2945],
        "description": """
**에펠탑 (Tour Eiffel)**  
프랑스 파리의 상징인 에펠탑은 1889년 파리 만국박람회를 기념하기 위해 건설되었습니다.  
높이는 약 330미터이며, 야경이 특히 아름다워 많은 관광객이 찾습니다.  
3층 전망대까지 올라가면 파리 시내를 한눈에 조망할 수 있습니다.
"""
    },
    "루브르 박물관": {
        "location": [48.8606, 2.3376],
        "description": """
**루브르 박물관 (Musée du Louvre)**  
세계에서 가장 유명한 미술관 중 하나로, 모나리자를 비롯한 수많은 예술작품이 전시되어 있습니다.  
과거 왕궁이었던 건물을 개조한 곳으로, 유럽 예술의 정수를 느낄 수 있습니다.
"""
    },
    "몽생미셸": {
        "location": [48.6361, -1.5115],
        "description": """
**몽생미셸 (Mont-Saint-Michel)**  
바다 위 섬에 세워진 중세 수도원으로, 밀물과 썰물에 따라 육지와 섬이 되는 신비로운 장소입니다.  
프랑스 북서부 노르망디 지방에 위치하며, 유네스코 세계유산으로 지정되어 있습니다.
"""
    },
    "베르사유 궁전": {
        "location": [48.8049, 2.1204],
        "description": """
**베르사유 궁전 (Château de Versailles)**  
프랑스 절대왕정의 상징으로, 루이 14세가 건축한 호화로운 궁전입니다.  
웅장한 정원과 거울의 방, 수많은 조각상과 분수로 유명합니다.
"""
    }
}

# Streamlit 앱 구성
st.set_page_config(page_title="프랑스 관광지 가이드", layout="wide")
st.title("🇫🇷 프랑스의 주요 관광지 가이드")
st.write("프랑스를 여행하며 꼭 가봐야 할 명소들을 소개합니다!")

# 관광지 선택
spot_names = list(tourist_spots.keys())
selected_spot = st.sidebar.selectbox("관광지를 선택하세요", spot_names)

# 관광지 정보 가져오기
info = tourist_spots[selected_spot]
lat, lon = info["location"]
description = info["description"]

# Folium 지도 생성
m = folium.Map(location=[lat, lon], zoom_start=6)
folium.Marker([lat, lon], tooltip=selected_spot, popup=selected_spot, icon=folium.Icon(color='blue')).add_to(m)

# 지도 출력
st.subheader(f"📍 {selected_spot}")
st.markdown(description)
st_folium(m, width=700, height=500)
