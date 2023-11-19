from bs4 import BeautifulSoup
import os
import requests
import json
MAIN_URL = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
# member_dict = {}
MEMBER_LIST = []


def get_data(url, page):
    # for i in range(0, 745, 12):  # 745

    url = f"{url}{page}"
    req = requests.get(url, headers=HEADERS)
    src = req.text

    get_list_links(src)

    # if not os.path.isdir(f"data/page_{page}"):
    #     os.mkdir(f"data/page_{page}")
    # with open(f"data/page_{page}/members.html", 'w', encoding="utf-8") as file:
    #     file.write(src)
    # with open(f"data/page_{page}/members.html", 'r', encoding="utf-8") as file:
    #     src = file.read()


def get_list_links(page_text):
    soup = BeautifulSoup(page_text, 'lxml')
    members_info = soup.find_all('div', class_='bt-slide-content')

    for member in members_info:
        member_title = member.find('a')['title']
        member_href = member.find('a')['href']
        for el in [',', ' ']:
            if el in member_title:
                member_title = member_title.replace(el, '_')

        # member_dict[member_title] = member_href
        MEMBER_LIST.append(member_href)


def get_data_member_card(members_list):
    main_dict = {}
    main_list = []
    count = 1
    for url in members_list:
        req = requests.get(url, headers=HEADERS)
        src = req.text
        # if not os.path.isdir(f"data/page_{i}/{title}"):
        #     os.mkdir(f"data/page_{i}/{title}")
        # with open(f"data/page_{i}/{title}/page.html", "w", encoding="utf-8") as file:
        #     file.write(src)
        # with open(f"data/page_{i}/{title}/page.html", "r", encoding="utf-8") as file:
        #     src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        card_info = soup.find("div", class_='bt-profil')

        member_img = "https://www.bundestag.de"+card_info.find(
            class_='bt-bild-standard').find('img')['data-img-md-normal']
        name_and_political_party = card_info.find(
            'div', class_='bt-biografie-name').find('h3').text
        name_and_political_party_list = name_and_political_party.strip().split(',')
        member_name = name_and_political_party_list[0]
        member_party = name_and_political_party_list[1].strip()
        social_network = soup.find('ul', class_='bt-linkliste').find_all('li')
        social_network_dict = {}
        for item in social_network:
            social_network_dict[item.find('a')['title']] = item.find('a')[
                'href']

        main_list.append({
            'member_name': member_name,
            'image_url': member_img,
            'political_party': member_party,
            'social_network': social_network_dict})

        print(f"{count}: {url} \n запись окончена")
        count += 1
    return main_list
    # social_network_dict['title'] =

    # print(member_img)
    # print(member_name)
    # print(member_party)
    # print(social_network_dict)


for i in range(0, 745, 12):
    get_data(MAIN_URL, i)
with open("data/members_list.txt", "a", encoding="utf-8") as file:
    for link in MEMBER_LIST:
        file.write(f"{link}\n")
with open("data/members_list.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file.readlines()]

result_dict = get_data_member_card(lines)

with open(f"data/result.json", 'w', encoding='utf-8') as file:
    json.dump(result_dict, file, indent=4, ensure_ascii=False)
