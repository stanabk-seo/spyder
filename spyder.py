import os
from google.cloud import storage
import advertools as adv
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import csv
import unicodedata

#Crawling the website

st.title("""Spyder""")
st.header('Crawl your website and detect SEO issues!')

#list-mode

st.subheader('List Mode')
crawl_list_data_df = pd.DataFrame()
clean_list_df = pd.DataFrame()

file = st.file_uploader('', type='csv')
if file is not None:
    url_list = list(file)
clean_url = []

try:
    if url_list is not None:

        for s in url_list:
            url = s.decode('utf-8')
            clean_url.append(url)
        
        # st.write(url)
        adv.crawl(clean_url, output_file='list_mode.jl', follow_links=False)
        crawl_list_data_df = pd.read_json('list_mode.jl', lines = True)
        clean_list_df = crawl_list_data_df.drop(['og:image:width','og:image:height','twitter:card','twitter:image','jsonld_@context','jsonld_headline','jsonld_url','jsonld_datePublished','jsonld_dateModified','jsonld_keywords','jsonld_description','jsonld_publisher.@type','jsonld_publisher.name','jsonld_publisher.url','jsonld_publisher.logo.@type','jsonld_publisher.logo.url','jsonld_publisher.logo.width','jsonld_publisher.logo.height','jsonld_author.@type','jsonld_author.name','jsonld_author.image.@type','jsonld_author.image.url','jsonld_author.image.width','jsonld_author.image.height','jsonld_author.url','jsonld_author.sameAs','jsonld_image.@type','jsonld_image.url','jsonld_image.width','jsonld_image.height','jsonld_mainEntityOfPage.@type','jsonld_mainEntityOfPage.@id','download_slot','download_latency','ip_address','resp_headers_server','resp_headers_date','resp_headers_x-powered-by','resp_headers_cache-control','resp_headers_etag','resp_headers_vary','resp_headers_strict-transport-security','resp_headers_x-frame-options','resp_headers_x-content-type-options','request_headers_accept','request_headers_accept-language'], axis=1)

    st.write(clean_list_df)

    csv = clean_list_df.to_csv(index=False)
    st.download_button('Download CSV', csv, 'list_mode.csv', 'text/csv')

except:
    print('Ignore errors')


#spidermode

st.subheader('Spider Mode')

with st.form(key='my_form'):
    website_name = st.text_input(label = 'Enter website name here')
    website_path = st.text_input(label = 'Type your domain URL here')
    submit_button = st.form_submit_button(label = 'Start Crawling')

#Crawl settings

st.sidebar.subheader('Crawl Settings')

st.sidebar.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

#including subdomains

include_subdomains = st.sidebar.checkbox("Include Sub-domains")

max_subdomains =[]

if include_subdomains:
    # max_subdomains = st.sidebar.slider('Number of Sub-domains:', 0, 20, 3)
    subdomains = st_tags_sidebar(label = 'Enter Sub-domains:', text = 'Type sub-domains and hit Enter', value = ['subdomain.example.com'],maxtags=20,key='1')

#limit crawl total

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

limit_url = st.sidebar.checkbox("Limit Crawl Total")

if limit_url:
    url_limit = st.sidebar.number_input('',min_value=10)
else:
    url_limit = 1000000

#switching user agents

google_bot_phone = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.120 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
google_bot_desktop = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
bing_bot_desktop = 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
bing_bot_phone = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
default = 'abkbot/0.1'

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

user_agent = st.sidebar.selectbox('Select User Agent: ', (google_bot_desktop,google_bot_phone,bing_bot_desktop,bing_bot_phone,default))

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

#obey or disobey robots.txt

disobey_robots_txt = st.sidebar.checkbox("Disobey robots.txt")
if disobey_robots_txt:
    disobey_robots = False

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

#max speed limit

max_speed = st.sidebar.checkbox("Limit Maximum Speed (URLs/sec)")

if max_speed:
    max_speed_limit = st.sidebar.number_input('',min_value=0.5, step=0.5)

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

#download_delay

download_delay = st.sidebar.checkbox("Add Download Delay (in secs)")

if download_delay:
    delay = st.sidebar.number_input('',min_value=1, step=1)

#depth_limit

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

crawl_depth = st.sidebar.checkbox("Limit Crawl Depth")

if crawl_depth:
    depth_limit = st.sidebar.number_input('',min_value=1, step=1)

#crawling

if website_path is not None:

    try:
        crawl_data_df = pd.DataFrame()
        sub_domain_list = []

        file_name = website_name+'.jl'

        if sub_domain_list:
            adv.crawl(website_path, file_name, follow_links = True, allowed_domains=sub_domain_list, custom_settings={'CLOSESPIDER_PAGECOUNT': url_limit, 'USER_AGENT': user_agent, 'CLOSESPIDER_ERRORCOUNT': 10, 'ROBOTSTXT_OBEY': disobey_robots, 'CONCURRENT_REQUESTS': max_speed_limit, 'DOWNLOAD_DELAY': delay, 'DEPTH_LIMIT': depth_limit})
        else:
            adv.crawl(website_path, file_name, follow_links = True, custom_settings={'CLOSESPIDER_PAGECOUNT': url_limit, 'USER_AGENT': user_agent, 'CLOSESPIDER_ERRORCOUNT': 10, 'ROBOTSTXT_OBEY': disobey_robots, 'CONCURRENT_REQUESTS': max_speed_limit, 'DOWNLOAD_DELAY': delay, 'DEPTH_LIMIT': depth_limit})

        crawl_spider_data_df = pd.read_json(file_name, lines = True)

        try:

            new_crawl_data_df = crawl_spider_data_df.drop(['jsonld_@graph','og:image:width','og:image:height','twitter:card','twitter:image','jsonld_@context','jsonld_headline','jsonld_url','jsonld_datePublished','jsonld_dateModified','jsonld_keywords','jsonld_description','jsonld_publisher.@type','jsonld_publisher.name','jsonld_publisher.url','jsonld_publisher.logo.@type','jsonld_publisher.logo.url','jsonld_publisher.logo.width','jsonld_publisher.logo.height','jsonld_author.@type','jsonld_author.name','jsonld_author.image.@type','jsonld_author.image.url','jsonld_author.image.width','jsonld_author.image.height','jsonld_author.url','jsonld_author.sameAs','jsonld_image.@type','jsonld_image.url','jsonld_image.width','jsonld_image.height','jsonld_mainEntityOfPage.@type','jsonld_mainEntityOfPage.@id','download_slot','download_latency','ip_address','resp_headers_server','resp_headers_date','resp_headers_x-powered-by','resp_headers_cache-control','resp_headers_etag','resp_headers_vary','resp_headers_strict-transport-security','resp_headers_x-frame-options','resp_headers_x-content-type-options','request_headers_accept','request_headers_accept-language'], axis=1)
            st.write(new_crawl_data_df)

        except:
            try:
                new_crawl_data_df = crawl_spider_data_df
                # st.write('We faced some issues, this is the minimum data we could get -')
                st.write(new_crawl_data_df)
            except:
                new_crawl_data_df = crawl_spider_data_df[['url','title','meta_desc','viewport','charset','h1','h2','canonical','alt_href','body_text','size','depth','status','links_url','links_text','links_nofollow','nav_links_url','nav_links_text','nav_links_nofollow','header_links_url','header_links_text','header_links_nofollow','crawl_time','resp_headers_content-type','request_headers_user-agent','request_headers_accept-encoding']]
                st.write('There were some issues, we could only get following data:')
                st.write(new_crawl_data_df)


        csv1 = new_crawl_data_df.to_csv(index=False)

        st.download_button('Download CSV', csv1, 'spider_mode.csv', 'text/csv')

    except Exception as e:
        print(e)
        # st.write(e)


#Uploading the Data to Google Cloud Storage

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\ABShukla\Documents\Python_projects\Python\advert_tools\Crawler\google_service_account_key.json'

# storage_client = storage.Client()

# #Creating New Bucket
# # bucket_name = 'crawl_data_bucket'
# # bucket = storage_client.bucket(bucket_name)
# # bucket.location = 'US'
# # bucket = storage_client.create_bucket(bucket)

# #Accessing the bucket
# my_bucket = storage_client.get_bucket('crawl_data_bucket')

# #Uploading files
# def upload_to_bucket(blob_name, file_path, bucket_name):
#     try:
#         bucket = storage_client.get_bucket(bucket_name)
#         blob = bucket.blob(blob_name)
#         blob.upload_from_filename(file_path)
#         return True
#     except Exception as e:
#         print(e)
#         return False

# file_path = r'C:\Users\ABShukla\Documents\Python_projects\Python\advert_tools\Crawler'

# upload_to_bucket('simple_snippet_data.csv', os.path.join(file_path, 'crawl_data_simple_snippets.csv'), 'crawl_data_bucket')
# upload_to_bucket('/document/simple_snippet_data.csv', os.path.join(file_path, 'crawl_data_simple_snippets.csv'), 'crawl_data_bucket')



