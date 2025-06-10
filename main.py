import streamlit as st
import folium
from streamlit_folium import st_folium

# 도시별 관광지 데이터
# 각 관광지에 대한 설명을 더 자세하고 친절하게 작성했습니다.
cities = {
    "파리": {
        "에펠탑": {
            "location": [48.8584, 2.2945],
            "description": """
**✨ 파리의 상징, 에펠탑 (Tour Eiffel)**

환영합니다! 프랑스 파리 하면 가장 먼저 떠오르는, 빛나는 철골 구조물, 바로 에펠탑입니다. 밤이 되면 반짝이는 조명은 파리의 밤하늘을 더욱 로맨틱하게 만들어준답니다.

**놓치지 마세요!**
* **전망대:** 에펠탑에 올라 파리 시내를 한눈에 담아보세요. 특히 해 질 녘 노을과 야경은 정말 감동적이에요!
* **잔디밭 피크닉:** 에펠탑 아래 샹 드 마르스 공원에서 여유롭게 피크닉을 즐기며 에펠탑의 웅장함을 감상해보세요.
* **팁:** 미리 온라인으로 티켓을 예매하면 긴 줄을 피할 수 있어요!
"""
        },
        "루브르 박물관": {
            "location": [48.8606, 2.3376],
            "description": """
**🎨 세계 최대의 예술의 보고, 루브르 박물관 (Musée du Louvre)**

예술을 사랑하는 분이라면 절대 놓칠 수 없는 곳, 루브르 박물관입니다. 유리 피라미드를 통해 입장하면, 고대 문명부터 근세까지 수많은 걸작들이 여러분을 기다리고 있어요.

**꼭 봐야 할 작품!**
* **모나리자 (Mona Lisa):** 레오나르도 다빈치의 신비로운 미소를 직접 만나보세요.
* **밀로의 비너스 (Venus de Milo):** 완벽한 비율을 자랑하는 고대 그리스 조각상입니다.
* **사모트라케의 니케 (Winged Victory of Samothrace):** 박물관 중앙 계단에 우뚝 솟아 있는 승리의 여신상입니다.

**팁:** 박물관이 워낙 넓으니, 미리 보고 싶은 작품을 정해 동선을 짜는 것이 좋아요!
"""
        },
        "베르사유 궁전": {
            "location": [48.8049, 2.1204],
            "description": """
**👑 프랑스 왕실의 화려함, 베르사유 궁전 (Château de Versailles)**

파리 근교에 위치한 베르사유 궁전은 프랑스 절대 왕정의 상징이자, 화려함의 극치를 보여주는 곳입니다. 궁전 내부는 물론, 광대한 정원도 압도적인 아름다움을 자랑합니다.

**하이라이트!**
* **거울의 방 (Galerie des Glaces):** 화려한 샹들리에와 거울로 장식된 이 방은 눈부신 아름다움에 감탄을 자아내게 할 거예요.
* **정원 (Jardins de Versailles):** 섬세하게 가꿔진 넓은 정원을 산책하거나, 보트를 타는 등 다양한 방법으로 즐길 수 있습니다. 분수쇼도 놓치지 마세요!
* **트리아농 궁전 (Grand Trianon & Petit Trianon):** 마리 앙투아네트가 즐겨 찾던 작은 궁전들도 방문해보세요.
"""
        }
    },
    "노르망디": {
        "몽생미셸": {
            "location": [48.6361, -1.5115],
            "description": """
**🏰 신비로운 수도원 섬, 몽생미셸 (Mont-Saint-Michel)**

마치 동화 속에 들어온 듯한 착각을 불러일으키는 몽생미셸은 노르망디 해안에 위치한 수도원 섬입니다. 유네스코 세계유산으로 지정된 이곳은 밀물과 썰물의 차이가 만들어내는 장관으로 유명해요.

**특별한 경험!**
* **수도원 탐방:** 바다 위에 홀로 솟아 있는 수도원 내부를 탐방하며 중세 건축의 아름다움을 느껴보세요.
* **밀물과 썰물:** 방문 시기에 따라 몽생미셸이 섬이 되거나 육지와 연결되는 모습을 볼 수 있습니다. 썰물 때는 갯벌을 걷는 체험도 가능해요!
* **야경:** 밤이 되면 조명이 켜져 더욱 신비롭고 아름다운 모습을 감상할 수 있습니다.
"""
        }
    },
    "남프랑스 (코트다쥐르)": {
        "니스": {
            "location": [43.7000, 7.2661],
            "description": """
**☀️ 햇살 가득한 해변 도시, 니스 (Nice)**

지중해의 푸른 바다와 따뜻한 햇살이 반기는 니스에 오신 것을 환영합니다! '천사의 만'이라 불리는 아름다운 해변과 활기찬 구시가지가 매력적인 도시입니다.

**니스에서 즐길 거리!**
* **프롬나드 데 장글레 (Promenade des Anglais):** 니스의 상징인 해변 산책로를 따라 걸으며 지중해의 아름다움을 만끽해보세요. 자전거를 타거나 조깅을 하기에도 좋습니다.
* **구시가지 (Vieux Nice):** 좁은 골목길을 따라 아기자기한 상점과 레스토랑, 카페들이 즐비합니다. 신선한 해산물 요리도 꼭 맛보세요!
* **마세나 광장 (Place Masséna):** 니스의 중심 광장으로, 독특한 조형물과 아름다운 건축물들이 어우러져 있습니다.
"""
        },
        "칸": {
            "location": [43.5516, 7.0177],
            "description": """
**🎬 영화제의 도시, 칸 (Cannes)**

매년 5월, 세계적인 영화배우와 감독들이 모여드는 영화제의 도시, 칸입니다. 영화제가 아니더라도 고급스러운 분위기와 아름다운 해변을 즐길 수 있는 매력적인 곳이에요.

**칸에서 꼭 해봐야 할 것!**
* **레드 카펫 밟기 (Palais des Festivals et des Congrès):** 칸 국제영화제가 열리는 영화궁 앞에서 스타들처럼 레드 카펫을 밟아보는 특별한 경험을 해보세요!
* **크루아제트 거리 (La Croisette):** 고급 부티크와 호텔들이 늘어선 해변 산책로입니다. 지중해의 풍경을 감상하며 여유로운 시간을 보내보세요.
* **레렝 군도 (Îles de Lérins):** 페리를 타고 가까운 레렝 군도로 가서 자연 속에서 평화로운 시간을 보내거나, '철가면'의 전설이 깃든 생트 마르그리트 섬을 방문해보세요.
"""
        }
    }
}

# Streamlit 앱 구성
st.set_page_config(page_title="🇫🇷 프랑스 주요 관광지 가이드", layout="wide", initial_sidebar_state="expanded")

st.title("🇫🇷 프랑스 주요 관광지, 친절하고 자세한 가이드!")
st.markdown("""
안녕하세요! 아름다운 프랑스의 주요 관광지들을 여러분께 아주 친절하고 자세하게 소개해 드릴게요.
원하는 도시와 관광지를 선택하시면, 그곳의 매력과 함께 지도에서 위치를 확인할 수 있답니다.
자, 그럼 프랑스 여행을 떠나볼까요?
""")

# 사이드바에서 도시 선택
st.sidebar.header("🗺️ 여행지를 선택하세요!")
city_names = list(cities.keys())
selected_city = st.sidebar.selectbox(
    "어떤 도시로 떠나고 싶으신가요?",
    city_names,
    index=0 # 기본값으로 첫 번째 도시 선택
)

# 선택한 도시의 관광지 목록
spots_in_city = list(cities[selected_city].keys())
selected_spot = st.sidebar.selectbox(
    f"{selected_city}의 어떤 관광지를 보고 싶으신가요?",
    spots_in_city,
    index=0 # 기본값으로 첫 번째 관광지 선택
)

# 관광지 정보 가져오기
spot_info = cities[selected_city][selected_spot]
lat, lon = spot_info["location"]
description = spot_info["description"]

# 메인 콘텐츠 영역 (정보와 지도를 나란히 배치)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"✨ 여러분이 선택한 곳은 바로... **{selected_spot}** 입니다!")
    st.markdown(description)
    st.markdown(f"**😊 {selected_spot}에서 멋진 시간을 보내세요!**")

with col2:
    st.subheader(f"📍 {selected_spot}의 위치를 지도에서 확인해 보세요!")
    # Folium 지도 생성
    # 중심을 선택된 관광지로 설정하고, 초기 줌 레벨을 조정했습니다.
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # 마커 추가 (tooltip과 popup에 관광지 이름 표시)
    folium.Marker(
        [lat, lon],
        tooltip=f"**{selected_spot}**",
        popup=f"**{selected_spot}**",
        icon=folium.Icon(color='red', icon='info-sign') # 마커 아이콘 색상 변경
    ).add_to(m)

    # 선택된 도시의 다른 관광지들도 지도에 표시 (선택사항)
    # for spot_name, data in cities[selected_city].items():
    #     if spot_name != selected_spot:
    #         folium.Marker(
    #             data["location"],
    #             tooltip=spot_name,
    #             popup=spot_name,
    #             icon=folium.Icon(color='blue')
    #         ).add_to(m)

    # Streamlit에 Folium 지도 렌더링
    st_folium(m, width=700, height=500)

st.sidebar.markdown("---")
st.sidebar.info("이 가이드는 여러분의 즐거운 프랑스 여행을 돕기 위해 만들어졌습니다. 궁금한 점이 있다면 언제든지 문의해주세요!")
st.sidebar.markdown("© 2025 프랑스 여행 가이드")
