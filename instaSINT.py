import re
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def get_profile_info(username):
    # Define os cookies necessários para acesso à página
    cookies = {
        '_inst_key': 'SFMyNTY.g3QAAAADbQAAAAtfY3NyZl90b2tlbm0AAAAYUGtERzFSakpEbmRMWnFzekQwd1doYlhobQAAAAJleG0AAAABMW0AAAADdHRrbQAAACBHaTZ6aEZ3eVR3VWZZQjFmc1hrSGk0bWVibWpUX3hQeQ.RJ7Og3wZOVdOGdwAoeYdMWyn_B8oVptKCReF8nHN2as',
        '_ga': 'GA1.1.44733741.1708380384',
        '__gads': 'ID=260fc4f010652bf4:T=1708380384:RT=1708380384:S=ALNI_MY2XGnyHJUYYeysUXnUHht-h9guJA',
        '__gpi': 'UID=00000a0e608aef20:T=1708380384:RT=1708380384:S=ALNI_MacSFIIrbwoKjHkqm5p3bjgFkUDdQ',
        '__eoi': 'ID=94fd1ff0831e60ec:T=1708380384:RT=1708380384:S=AA-AfjZexqosE0dlhI7NNmByqh3j',
        '_ym_uid': '1708380386203591861',
        '_ym_d': '1708380386',
        '_ym_isad': '2',
        '_ga_T410N8PBE5': 'GS1.1.1708380383.1.1.1708380515.0.0.0',
        'cf_clearance': 'pWKv0gjCH77aixYAgce37UnNH2lWLS2wT5o2xHASRUk-1708383602-1.0-AXV7ezLQXvGQk5ndx9NmH1AAgusxEM3W715+cX5rnIHBCDBuMwfP6xPx7MvHi4SwKFo8yX3qghO5ou8LlZfxnfI='
    }

    # Realiza a requisição HTTP para a URL
    url = f"https://greatfon.com/search?query={username}"
    headers = {
        'authority': 'greatfon.com',
        'referer': f'https://greatfon.com/search?query={username}',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        print(f"{Fore.RED}Erro ao acessar a página.{Style.RESET_ALL}")
        return

    # Extrai os links que contenham "/v/"
    soup = BeautifulSoup(response.content, 'html.parser')
    v_links = [link['href'] for link in soup.find_all('a', href=True) if "/v/" in link['href']]

    # Remove duplicatas
    v_links = list(set(v_links))

    # Loop através dos links e extrai informações do perfil
    for link in v_links:
        profile_page = requests.get(f"https://greatfon.com{link}", headers=headers, cookies=cookies)
        if profile_page.status_code != 200:
            continue

        soup = BeautifulSoup(profile_page.content, 'html.parser')
        name = soup.find('h1', class_='user__title').text.strip()
        
        # Extrai a URL da foto corretamente
        photo_style = soup.find('div', class_='user__img')['style']
        photo_url = re.search(r"url\('([^']*)'\)", photo_style).group(1)
        
        bio = soup.find('div', class_='user__info-desc').text.strip()
        posts = soup.find_all('li', class_='user__item')[0].text.strip()
        followers = soup.find_all('li', class_='user__item')[1].text.strip()
        following = soup.find_all('li', class_='user__item')[2].text.strip()

        print(f"{Fore.CYAN}################################################################################################################################################################################################")
        print(f"\nPerfil: https://greatfon.com{link}")
        print(f"Nome: {name}")
        print(f"Foto: {photo_url}")
        print(f"Bio: {bio}")
        print(f"Posts: {posts}")
        print(f"Seguidores: {followers}")
        print(f"Seguindo: {following}{Style.RESET_ALL}")

        # Extrai informações sobre os posts
        posts_container = soup.find_all('div', class_='content__item grid-item card')
        print("\nPosts:")
        for post in posts_container:
            description = post.find('div', class_='content__text')
            if description:
                description = description.text.strip()
            else:
                description = "Nenhuma descrição disponível."

            image_or_video = post.find('img', class_='content__img')
            if image_or_video:
                image_or_video = image_or_video['src']
            else:
                image_or_video = "Nenhuma imagem ou vídeo disponível."

            likes = post.find('div', class_='content__like-text').text.strip()
            comments = post.find('div', class_='content__comment-text').text.strip()
            date = post.find('div', class_='content__time-text').text.strip()

            print(f"[+] {Fore.YELLOW}Descrição: {description}")
            print(f"- Imagem ou vídeo: {image_or_video}")
            print(f"- Likes: {likes}")
            print(f"- Comentários: {comments}")
            print(f"- Data do post: {date}{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Uso: python3 {sys.argv[0]} <username>{Style.RESET_ALL}")
    else:
        username = sys.argv[1]
        get_profile_info(username)

# Créditos
print("Script desenvolvido por Mr_ofcodyx (https://github.com/mrofcodyx) - instaSINT.py")
