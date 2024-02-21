import discord
from discord.ext import commands
import re
import requests
from bs4 import BeautifulSoup
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# Define o token do seu bot
TOKEN = 'MTIwNzc2MjQ1MTk4MzI0NTMxNA.Gu4B6l.sIqxxZxtB2CtMV62BBhP55M6eXOd6sKaJ6tRA0'

# Cria um objeto bot com o prefixo !
bot = commands.Bot(command_prefix='!', intents=intents)

async def get_profile_info(username):
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
        yield "Erro ao acessar a página."
        return

    # Extrai os links que contenham "/v/"
    soup = BeautifulSoup(response.content, 'html.parser')
    v_links = [link['href'] for link in soup.find_all('a', href=True) if "/v/" in link['href']]

    # Remove duplicatas
    v_links = list(set(v_links))

    # Loop através dos links e extrai informações do perfil
    profile_info_list = []
    for index, link in enumerate(v_links, start=1):
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

        # Cria uma string com as informações do perfil
        profile_info = (
            f"Perfil: https://greatfon.com{link}\n"
            f"Nome: {name}\n"
            f"Foto: {photo_url}\n"
            f"Bio: {bio}\n"
            f"Posts: {posts}\n"
            f"Seguidores: {followers}\n"
            f"Seguindo: {following}"
        )

        # Extrai os posts
        posts_section = soup.find('div', class_='profile_posts')
        if posts_section:
            posts = posts_section.find_all('div', class_='content__item')
            post_info = "\nPosts:"
            for post in posts:
                # Verifica se há uma imagem no post
                img_tag = post.find('img', class_='content__img')
                if img_tag:
                    img_url = img_tag['src']
                    post_info += f"\n- Imagem: {img_url}"

                # Verifica se há um vídeo no post
                video_tag = post.find('video', class_='content__video')
                if video_tag:
                    video_url = video_tag['src']
                    post_info += f"\n- Vídeo: {video_url}"

            # Adiciona as informações dos posts ao perfil
            profile_info += post_info

        # Adiciona as informações do perfil à lista
        profile_info_list.append(profile_info)

        # Envia cada informação do perfil individualmente
        yield profile_info, index, len(v_links)

@bot.command(name='instaSINT')
async def instaSINT(ctx, username: str):
    loading_message = await ctx.send("Obtendo informações do perfil...")

    async for profile_info, index, total in get_profile_info(username):
        await loading_message.edit(content=f"Obtendo informações do perfil... [{index}/{total}]")
        await ctx.send(profile_info)

    await loading_message.delete()

# Executa o bot com o token fornecido
bot.run(TOKEN)
