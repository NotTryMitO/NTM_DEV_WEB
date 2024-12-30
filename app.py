from quart import Quart, redirect, request, session, render_template, send_from_directory
import requests
import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv


app = Quart(__name__, template_folder='site/templates')
app.secret_key = 'bananaazul'

load_dotenv()

# Configurações do Discord
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://ntm-dev-web.onrender.com/discord/callback"

# cenas do bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot1_token = os.getenv("bot1_token") #bot main
bot2_token = os.getenv("bot2_token") #bot ticket
bot1 = commands.Bot(command_prefix="!", intents=intents) #bot main
bot2 = commands.Bot(command_prefix=".", intents=intents) #bot ticket

#informacoes gerais
member_role = 1303727367901941822
REQUIRED_ROLE_ID = 1303726904569892884

# Rota para autenticação com Discord
@app.route("/")
async def home():
    if "user_id" in session:
        username = session["username"]
        avatar_url = session["avatar_url"]
        return await render_template("index-PT.html", username=username, avatar_url=avatar_url)
    return await render_template("login-PT.html")

@app.route("/discord/login")
async def login():
    return redirect(f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

# Callback do OAuth2
@app.route("/discord/callback")
async def callback():
    code = request.args.get("code")
    if not code:
        return "Erro ao autenticar: código ausente.", 400

    # Trocar o código por um token de acesso
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

    if response.status_code != 200:
        print("Erro ao obter token:", response.text)
        return "Erro ao obter token. Verifique as configurações.", 400

    token = response.json().get("access_token")
    if not token:
        return "Erro ao obter o token de acesso.", 400

    # Obter informações do usuário
    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {token}"},
    )
    if user_response.status_code != 200:
        return "Erro ao obter dados do usuário.", 400

    user_data = user_response.json()
    user_id = user_data["id"]
    username = user_data["username"]
    discriminator = user_data["discriminator"]
    avatar_hash = user_data["avatar"]

    # Construir a URL do avatar
    if avatar_hash:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
    else:
        avatar_url = f"https://cdn.discordapp.com/embed/avatars/{int(discriminator) % 5}.png"

    # Armazenar na sessão
    session["user_id"] = user_id
    session["username"] = username
    session["avatar_url"] = avatar_url

    # Redirecionar para a página index
    return redirect("/")

# Página de login para a versão PT
@app.route("/login-PT")
async def login_PT():
    return await render_template("login-PT.html")

# Página de login para a versão US
@app.route("/login-US")
async def login_US():
    return await render_template("login-US.html")


# Página principal para a versão PT
@app.route("/index-PT")
async def index_PT():
    if "user_id" in session:
        username = session["username"]
        avatar_url = session["avatar_url"]
        return await render_template("index-PT.html", username=username, avatar_url=avatar_url)
    return redirect("/")


# Página principal para a versão US
@app.route("/index-US")
async def index_US():
    if "user_id" in session:
        username = session["username"]
        avatar_url = session["avatar_url"]
        return await render_template("index-US.html", username=username, avatar_url=avatar_url)
    return redirect("/")


# Rota para mudança de idioma
@app.route("/change_language")
async def change_language():
    language = request.args.get('lang')
    if language == "US":
        return redirect("/index-US")
    else:
        return redirect("/index-PT")

# Rota para mudança de idioma
@app.route("/change_language_login")
async def change_language_login():
    language = request.args.get('lang')
    if language == "US":
        return redirect("/login-US")  # Redireciona para o login em inglês
    else:
        return redirect("/login-PT")  # Redireciona para o login em português

# Rota para arquivos estáticos
@app.route('/site/templates/<path:filename>')
async def templates_path(filename):
    return await send_from_directory('site/templates', filename)

# Rota para arquivos template
@app.route('/site/static/<path:filename>')
async def static_files(filename):
    return await send_from_directory('site/static', filename)

@app.route("/comprar1", methods=["POST"])
async def comprar1():
    if "user_id" not in session:
        return {"success": False, "message": "Usuário não autenticado."}, 401

    user_id = int(session["user_id"])
    user = bot1.get_user(user_id)

    if not user:
        try:
            user = await bot1.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "Usuário não encontrado no Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Erro ao buscar usuário no Discord."}, 500

    try:
        mensagem = f"Olá, {session['username']}! Para fazer a compra do bot de sugestões entre no nosso discord, https://discord.gg/Yau8FUsq e abra um ticket em https://discord.com/channels/1290074291047632919/1303725153934381090. Se tiver dúvidas, entre em contato com nossa equipe de suporte."
        await user.send(mensagem)
        return {"success": True, "message": "Mensagem enviada com sucesso."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Não foi possível enviar mensagem. O usuário pode ter bloqueado mensagens diretas."}, 403
    except discord.HTTPException as e:
        print(f"Erro ao enviar mensagem para {user_id}: {e}")
        return {"success": False, "message": "Erro ao enviar a mensagem."}, 500

@app.route("/comprar2", methods=["POST"])
async def comprar2():
    if "user_id" not in session:
        return {"success": False, "message": "Usuário não autenticado."}, 401

    user_id = int(session["user_id"])
    user = bot1.get_user(user_id)

    if not user:
        try:
            user = await bot1.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "Usuário não encontrado no Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Erro ao buscar usuário no Discord."}, 500

    try:
        mensagem = f"Olá, {session['username']}! Para fazer a compra do bot de comandos personalizado entre no nosso discord, https://discord.gg/Yau8FUsq e abra um ticket em https://discord.com/channels/1290074291047632919/1303725153934381090. Se tiver dúvidas, entre em contato com nossa equipe de suporte."
        await user.send(mensagem)
        return {"success": True, "message": "Mensagem enviada com sucesso."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Não foi possível enviar mensagem. O usuário pode ter bloqueado mensagens diretas."}, 403
    except discord.HTTPException as e:
        print(f"Erro ao enviar mensagem para {user_id}: {e}")
        return {"success": False, "message": "Erro ao enviar a mensagem."}, 500

@app.route("/comprar3", methods=["POST"])
async def comprar3():
    if "user_id" not in session:
        return {"success": False, "message": "Usuário não autenticado."}, 401

    user_id = int(session["user_id"])
    user = bot1.get_user(user_id)

    if not user:
        try:
            user = await bot1.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "Usuário não encontrado no Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Erro ao buscar usuário no Discord."}, 500

    try:
        mensagem = f"Olá, {session['username']}! Para fazer a compra do bot de Anti-Links entre no nosso discord, https://discord.gg/Yau8FUsq e abra um ticket em https://discord.com/channels/1290074291047632919/1303725153934381090. Se tiver dúvidas, entre em contato com nossa equipe de suporte."
        await user.send(mensagem)
        return {"success": True, "message": "Mensagem enviada com sucesso."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Não foi possível enviar mensagem. O usuário pode ter bloqueado mensagens diretas."}, 403
    except discord.HTTPException as e:
        print(f"Erro ao enviar mensagem para {user_id}: {e}")
        return {"success": False, "message": "Erro ao enviar a mensagem."}, 500

@app.route("/buy1", methods=["POST"])
async def buy1():
    if "user_id" not in session:
        return {"success": False, "message": "User not authenticated."}, 401

    user_id = int(session["user_id"])
    user = bot1.get_user(user_id)

    if not user:
        try:
            user = await bot1.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "User not found on Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Error fetching user on Discord."}, 500

    try:
        message = (
            f"Hello, {session['username']}! To purchase the suggestion bot, join our Discord at https://discord.gg/Yau8FUsq and open a ticket at "
            "https://discord.com/channels/1290074291047632919/1303725153934381090. If you have any questions, please contact our support team."
        )
        await user.send(message)
        return {"success": True, "message": "Message sent successfully."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Could not send message. The user may have blocked direct messages."}, 403
    except discord.HTTPException as e:
        print(f"Error sending message to {user_id}: {e}")
        return {"success": False, "message": "Error sending the message."}, 500

@app.route("/buy2", methods=["POST"])
async def buy2():
    if "user_id" not in session:
        return {"success": False, "message": "User not authenticated."}, 401

    user_id = int(session["user_id"])
    user = bot1.get_user(user_id)

    if not user:
        try:
            user = await bot1.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "User not found on Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Error fetching user on Discord."}, 500

    try:
        message = (
            f"Hello, {session['username']}! To purchase the custom command bot, join our Discord at https://discord.gg/Yau8FUsq and open a ticket at "
            "https://discord.com/channels/1290074291047632919/1303725153934381090. If you have any questions, please contact our support team."
        )
        await user.send(message)
        return {"success": True, "message": "Message sent successfully."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Could not send message. The user may have blocked direct messages."}, 403
    except discord.HTTPException as e:
        print(f"Error sending message to {user_id}: {e}")
        return {"success": False, "message": "Error sending the message."}, 500

@app.route("/buy3", methods=["POST"])
async def buy3():
    if "user_id" not in session:
        return {"success": False, "message": "User not authenticated."}, 401

    user_id = int(session["user_id"])
    user = bot1.get_user(user_id)

    if not user:
        try:
            user = await bot1.fetch_user(user_id)
        except discord.NotFound:
            return {"success": False, "message": "User not found on Discord."}, 404
        except discord.HTTPException as e:
            return {"success": False, "message": "Error fetching user on Discord."}, 500

    try:
        message = (
            f"Hello, {session['username']}! To purchase the Anti-Links bot, join our Discord at https://discord.gg/Yau8FUsq and open a ticket at "
            "https://discord.com/channels/1290074291047632919/1303725153934381090. If you have any questions, please contact our support team."
        )
        await user.send(message)
        return {"success": True, "message": "Message sent successfully."}, 200
    except discord.Forbidden:
        return {"success": False, "message": "Could not send message. The user may have blocked direct messages."}, 403
    except discord.HTTPException as e:
        print(f"Error sending message to {user_id}: {e}")
        return {"success": False, "message": "Error sending the message."}, 500

@app.route("/logout")
async def logout():
    session.clear()
    return redirect("/")

async def start_quart_app():
    await app.run_task(host="127.0.0.1", port=5000)

'''bot main - bot1 - starts'''
#role automatica
@bot1.event
async def on_member_join(member):
    ROLE_ID = 1303727367901941822
    guild = member.guild
    role = guild.get_role(ROLE_ID)
    
    if role:
        try:
            await member.add_roles(role)
            print('-----------------------------------')
            print(f'Adicionada a role "{role.name}" ao membro {member.name}.')
            print('-----------------------------------')
        except discord.Forbidden:
            print(f"Permissão insuficiente para adicionar a role '{role.name}' ao membro {member.name}.")
        except discord.HTTPException as e:
            print(f"Erro ao tentar adicionar a role: {e}")
    else:
        print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")

#contadores
@tasks.loop(seconds=30)
async def atualizar_canal_members():
    CANAL_ID = 1303520594649677894
    try:
        canal = bot1.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            membros_reais = [m for m in guild.members if not m.bot]
            numero_membros_reais = len(membros_reais)
            novo_nome = f'members-{numero_membros_reais}'
            await canal.edit(name=novo_nome)
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@tasks.loop(seconds=30)
async def atualizar_canal_clients():
    CANAL_ID = 1303719327601655828
    ROLE_ID = 1303727484965224509
    try:
        canal = bot1.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            role = guild.get_role(ROLE_ID)
            if role:
                numero_membros_com_role = len(role.members)
                novo_nome = f'clients-{numero_membros_com_role}'
                await canal.edit(name=novo_nome)
            else:
                print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@tasks.loop(seconds=30)
async def atualizar_canal_bots():
    CANAL_ID = 1307465880745017366
    try:
        canal = bot1.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            bots = [m for m in guild.members if m.bot]
            numero_bots = len(bots)
            novo_nome = f'bots-{numero_bots}'
            await canal.edit(name=novo_nome)
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

#bot1 on_ready
@bot1.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="™ NTM DEV")
    print(f'Logged in as {bot1.user}')
    try:
        synced = await bot1.tree.sync()
        print(f'{bot1.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot1.change_presence(activity=activity)
    atualizar_canal_members.start()
    atualizar_canal_clients.start()
    atualizar_canal_bots.start()
'''bot main - bot1 - ends'''

'''bot ticket - bot2 - starts'''
#bot2 on_ready
@bot2.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="Desenvolvido por NTM DEV")
    print(f'Logged in as {bot2.user}')
    try:
        synced = await bot2.tree.sync()
        print(f'{bot2.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot2.change_presence(activity=activity)

#ticket
class TicketButton(discord.ui.Button):
    def __init__(self, label, ticket_option=None, image_url=None, ticket_text=None):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.ticket_option = ticket_option
        self.image_url = image_url
        self.ticket_text = ticket_text

    async def callback(self, interaction: discord.Interaction):
        if self.ticket_option:
            ticket_name = f"{self.ticket_option}"
            role_to_mention = discord.utils.get(interaction.guild.roles, name="NTM DEV")
            role_mention = role_to_mention.mention
            user = interaction.user
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                role_to_mention: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
            ticket_message = f"📩 **|** Hi {user.mention}! You opened the ticket {self.ticket_option}. Send all possible information about your case and wait until the {role_mention} reply."
            if self.ticket_text:
                ticket_message += f"\n\n{self.ticket_text}"
            if self.image_url:
                ticket_message += f"\n{self.image_url}"
            await ticket_channel.send(ticket_message)
            await interaction.response.send_message(f"You opened the ticket {self.ticket_option} in {ticket_channel.mention}", ephemeral=True)
            view = discord.ui.View()
            close_button = CloseButton("Close", ticket_channel.id)
            view.add_item(close_button)
            await ticket_channel.send("Click the button below to close this ticket:", view=view)
        else:
            await interaction.response.send_message("Invalid ticket option.", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, label, channel_id):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        ticket_channel = interaction.guild.get_channel(self.channel_id)
        if ticket_channel:
            await ticket_channel.delete()
            await interaction.response.send_message("The ticket was closed successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Unable to find ticket channel.", ephemeral=True)

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="shopping", label="Shopping", emoji="🛒", description='Ticket for shopping'),
            discord.SelectOption(value="support", label="Support", emoji="💳", description='Ticket for support'),
            discord.SelectOption(value="doubts", label="Doubts", emoji="❔", description='Ticket for doubts'),
            discord.SelectOption(value="bugs", label="Bugs", emoji="🐌", description='Ticket for bugs'),
            discord.SelectOption(value='partners', label='Partners', emoji='🤝', description='Ticket to close partnership')
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] in ["shopping", "support", "doubts", "bugs", 'partners']:
            selected_option = self.values[0]
            await interaction.response.defer()
            view = discord.ui.View()
            open_button = TicketButton(label=f"Open {selected_option} Ticket", ticket_option=selected_option)
            view.add_item(open_button)
            await interaction.followup.send(content=f"Press the button below to open a {selected_option} ticket", view=view, ephemeral=True)

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

@bot2.command()
async def ticket(ctx, interaction = None):
    embed = discord.Embed(
        title="**SERVICE**",
        description="➡️ - To open a ticket, select one of the options below:",
        color=0x2f336b
    )
    embed.add_field(name="", value="```ㅤㅤㅤㅤㅤㅤㅤㅤ! 𝘽𝙀𝙁𝙊𝙍𝙀 𝙊𝙋𝙀𝙉𝙄𝙉𝙂 !ㅤㅤㅤ```", inline=False)
    embed.add_field(name="", value="➡️ - Do not open a ticket without **NECESSITY**", inline=False)
    embed.add_field(name="", value="➡️ - Don't tag the MODERATORS, they are aware of your ticket", inline=False)
    embed.set_image(url="https://i.imgur.com/b1dqBpP.png")
    message = await ctx.send(embed=embed)
    await ctx.send(view=PersistentView())
    
    if any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!")
    else:
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)

'''bot ticket - bot2 - ends'''

async def main():
    await asyncio.gather(
        start_quart_app(),
        bot1.start(bot1_token),
        bot2.start(bot2_token)
    )

if __name__ == "__main__":
    asyncio.run(main())
