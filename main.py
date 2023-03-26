
import os
import keep_alive
from discord import app_commands
import discord
from Phigros import phigros_songs
keep_alive.keep_alive()
intents = discord.Intents.all()
client=discord.Client(intents=intents)
tree= app_commands.CommandTree(client)
my_secret = os.environ['token']
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Phigros"))

    await tree.sync()


#楽曲入力やっとけ
@tree.command(name="phigros")
async def Phigros(ctx, *, song_name:str):
    for song in phigros_songs:
        if song['title'].lower() == song_name.lower():
            # Embedを作成して、情報を追加する
            embed = discord.Embed(title=song['title'], color=discord.Color.green())
            embed.add_field(name='BPM', value=song['bpm'], inline=False)
            for diff in song['difficulty']:
                embed.add_field(name=diff, value=f"Level: {song['difficulty'][diff]['level']}, Combo: {song['difficulty'][diff]['combo']}, Charter:{song['difficulty'][diff]['charter']}",inline=False)
            embed.add_field(name='Composer', value=song['composer'], inline=False)
            embed.add_field(name='Song chapter', value=song['song chapter'], inline=False)
            await ctx.response.send_message(embed=embed)
            return

    # 楽曲が見つからない場合はエラーメッセージを表示する
    await ctx.response.send_message('楽曲が見つかりませんでした。')

#ACC計算用100%超えないようにするのは後でやる
@tree.command(name="acc",description="p,パーフェクト数、g,グッド数、tn,総ノーツ数")
async def acc(ctx,*, p: int, g: int, tn: int):
    acc = (p + g * 0.65) / tn * 100
    await ctx.response.send_message(f"Accuracy: {acc:.2f}%")

client.run(my_secret)