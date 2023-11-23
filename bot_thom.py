import datetime

import discord
import discord.utils
from discord.ext import commands

import correction

token = 'ODQzODYxNjc5OTM3NjgzNDk4.GKcrOD.g6pm_wTUcDsF73fpVEpAmD_mRBDZh5WlIitlf4'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.correction = correction

    async def on_ready(self):
        print('Connecté')
        print(self.user.name)
        print(self.user.id)
        print('------')
        activity = discord.Activity(type=discord.ActivityType.listening,name="Mon !aide risque de vous être précieuse...")
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        print(message.author, message.content)
        try:
            print(message.author.roles, message.channel.id)
        except:
            pass
        if message.content.startswith('!aide'):
            argument = message.content
            current_channel = self.get_channel(message.channel.id)
            embed = discord.Embed(title="**__Menu d'aide !__**",description="Dans ce menu vous pouvez retrouver les différentes commande à votre disposition !\n\n",url='https://cas.mon-ent-occitanie.fr/', color=15548997)
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_thumbnail(url='https://emoji.gg/assets/emoji/5374-iruma-wiggle-dizzy-dance.gif')
            embed.add_field(name="!correction <Nom_De_L'exercice>",value="Cet commande vous permet de vérifier si vous avez juste a la réalisation de votre exercice !(Faites réelement l'exercice et n'essayez pas de tricher :p)\n",inline=False)
            embed.add_field(name="!evenement",value="Grâce a cet commande vous pouvez savoir tout les évènements scolaire de cette année en NSI ou SNT !\n\n",inline=False)
            embed.add_field(name="!ping",value="Je m'ennuie souvant alors fait une petite partie avec moi de temps en temps :) !\n\n\n",inline=False)
            await current_channel.send(embed=embed)

        if message.content.startswith('!correction'):
            argument = message.content
            current_channel = self.get_channel(message.channel.id)
            if argument.split(' ')[1] in self.correction.liste:
                await current_channel.send(
                    f"{message.author.mention} la correction de l'exercice {argument.split(' ')[1]} vous a été envoyée par message !")
                await message.author.send(self.correction.liste_correction(argument.split(' ')[1]))
            else:
                await current_channel.send(
                    f"{message.author.mention} la correction de l'exercice {argument.split(' ')[1]} n'est soit pas disponible ou l'exercice n'exite pas !")

        if "!ping" in message.content.lower():
            emoji_ping = '\U0001F3D3'
            await message.add_reaction(emoji_ping)
            current_channel = self.get_channel(message.channel.id)
            await current_channel.send(f'!pong')

        if message.content.startswith('!evenement'):
            current_channel = self.get_channel(message.channel.id)
            await  current_channel.send("Voici la liste des évenements de votre lycée :\n>>> Date | Evenement\n10/06 | Nuit du code")

        if message.content.startswith('!message'):
            current_channel = self.get_channel(message.channel.id)
            argument = message.content
            now = datetime.datetime.now()
            p = now.strftime("%Y-%m-%d")
            file = open("message.csv", "a")
            file.write(f"{message.author},{argument[9:len(argument)]},{p}\n")
            file.close()
            await  current_channel.send(f"{message.author.mention} , votre message a bien été enregistré !")

    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        liste_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']
        role_emoji = {
            '1️⃣': discord.utils.get(guild.roles, name='Les Bases'),
            '2️⃣': discord.utils.get(guild.roles, name='Les Conditions'),
            '3️⃣': discord.utils.get(guild.roles, name='Les Listes'),
            '4️⃣': discord.utils.get(guild.roles, name='Les Dictionnaires'),
            '5️⃣': discord.utils.get(guild.roles, name='Les Boucles'),
            '6️⃣': discord.utils.get(guild.roles, name='Les Fonctions')
        }
        membre = payload.member
        channel = 976932657713774602
        message = 976950475003944990
        if payload.channel_id == channel:
            print(self.get_channel(payload.channel_id))
            if payload.message_id == message:
                print("message", payload.emoji.name)
                if payload.emoji.name in liste_emoji:
                    await membre.add_roles(role_emoji[payload.emoji.name])


client = MyClient()
client.run(token)
