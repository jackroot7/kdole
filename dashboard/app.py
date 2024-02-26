import streamlit as st
import sys
sys.path.insert(0, '../')
from utils import Utils
from streamlit_option_menu import option_menu


st.set_page_config(page_title='DataStream Analytics' ,layout="wide",page_icon='YO')

st.header('DataStream Analytics')
st.info("""Unlock the full potential of your YouTube content with DataStream Analytics. Dive deep into audience engagement, content performance, viewer sentiment, and keyword trends to craft videos that resonate and grow your channel. Experience the power of data-driven insights to elevate your strategy and connect with your audience like never before.""")


with st.sidebar:
    st.title(":blue[:computer: Dashboard] ", anchor=None, help=None)
    st.markdown("<span style='color:#8a7733'>Get Data and Sentimental Analysis powerd by AI models</span>", unsafe_allow_html=True)
    chanel_id = st.text_input('Youtube Channel ID',placeholder="ID", help='Get Youtube Channel ID from channel profile')
    st.button(":mag: Run Analysis", disabled=True if chanel_id=="" else False,  type="primary", use_container_width = True, on_click=Utils.submit_channel_id(chanel_id))
        

    st.header(":green[:globe_with_meridians: Apply Filters] ", anchor=None, help=None)
    add_radio = st.radio(
        "",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

side_panel, main_contents = st.columns([1, 3], gap="small")

with side_panel:
    selected = option_menu("Contents", [
        "Introduction", 
        'Useful Features',
        'Architecture',
        'Installation & Deployment',
        'Analytics & Presentations',
        'API & Integrations',
        'Licence',
        'Supports',
    ], icons=[
        'house', 'gear',
    ], menu_icon="cast", default_index=1)
    selected

with main_contents:
    st.title(":blue[:computer: Dashboard] ", anchor=None, help=None)




