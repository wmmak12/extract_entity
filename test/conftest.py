import pytest


url_w_html = (
    'https://www.globenewswire.com/news-release/2021/04/23/2216303/0/en/Kessler-Topaz-Meltzer-Check-LLP-is-Investigating-Securities-Fraud-Claims-on-Behalf-of-Peloton-Interactive-Inc-Nasdaq-PTON-Investors.html',
    'https://www.globenewswire.com/en/news-release/2021/04/24/2216333/0/en/O2Gold-Closes-Acquisition-of-Colombian-Gold-Project.html'
)

url_w_no_entity = (
    'https://www.google.com',
    'https://www.google.com.sg/imghp?hl=en&authuser=0&ogbl'
)


@pytest.fixture(params=url_w_html)
def url_w_html(request):
    return request.param


@pytest.fixture(params=url_w_no_entity)
def url_w_no_entity(request):
    return request.param

