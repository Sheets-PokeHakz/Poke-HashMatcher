# Token : MTE5MjQ0ODgyODgwNTIyNjYyOA.GcZbfS.telV_M_p6RyVynLFYoWCdZSsvvT4Je0dnTqQqs

import os
import aiohttp
import discord
import imagehash
from PIL import Image
from io import BytesIO
from rembg import remove 
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

POKEMONS= './Pokemons'
TEMPLATES = './Templates'

@bot.event
async def on_ready():
    print(f' --------  {bot.user.name}')

@bot.command()
async def hash(ctx, file_name: str = None):
    if ctx.message.reference:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        if referenced_message.attachments:
            # Assuming you want to save the image in the "pokemons" folder
            folder_name = 'Pokemons'

            # Check if the folder exists, create it if not
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # Determine the file name based on user input or use a default unique name
            if file_name:
                file_name = os.path.join(folder_name, f"{file_name}.png")
            else:
                file_name = os.path.join(folder_name, f"{ctx.author.id}_{referenced_message.id}.png")

            # Download and save the image
            await referenced_message.attachments[0].save(file_name)

            input_image = Image.open(file_name)
            output = remove(input_image)

            new_file_name = os.path.join(TEMPLATES, f"{file_name}_edited.png")

            # Save the modified image with a new file name
            output.save(new_file_name)

            await ctx.send(f"Image Saved As {new_file_name}")

        elif referenced_message.embeds:
            # Handle messages with embeds containing images
            folder_name = 'Pokemons'

            for embed in referenced_message.embeds:
                if embed.image:
                    image_url = embed.image.url

                    # Determine the file name based on user input or use a default unique name
                    if file_name:
                        file_name = os.path.join(folder_name, f"{file_name}.png")
                    else:
                        file_name = os.path.join(folder_name, f"{ctx.author.id}_{referenced_message.id}.png")

                    # Download and save the image
                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_url) as response:
                            with open(file_name, 'wb') as f:
                                f.write(await response.read())

                    input_image = Image.open(file_name)
                    output = remove(input_image)

                    new_file_name = os.path.join(TEMPLATES, f"{file_name}_edited.png")

                    # Save the modified image with a new file name
                    output.save(new_file_name)

                    await ctx.send(f"Image Saved As {new_file_name}")

                    break

        else:
            await ctx.send("No Image Found")
    else:
        await ctx.send("Needs Reference Image")


@bot.event
async def on_message(message):
    owners = [727012870683885578, 1126502461155328122]

    if message.author.id in owners and message.attachments:
        attachment = message.attachments[0]
        if attachment.content_type.startswith("image/"):
            await attachment.save("Temp.png")

            input_image = Image.open("Temp.png")
            output = remove(input_image)

            # Save the modified image with the same file name
            output.save("Temp.png")

            try:
                sent_hash = imagehash.average_hash(output)

                for filename in os.listdir(TEMPLATES):
                    reference_image = Image.open(os.path.join(TEMPLATES, filename))
                    reference_hash = imagehash.average_hash(reference_image)

                    if sent_hash == reference_hash:
                        filename_without_ext = os.path.splitext(filename)[0].split(".")[-1]
                        await message.channel.send(f"Match Found : {filename_without_ext}")
                        return

                await message.channel.send("No Match Found")

            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send("An Error Occurred Processing The Image")

            finally:
                os.remove("Temp.png")


    elif message.author.id == 716390085896962058:
            if len(message.embeds) > 0:
                embed = message.embeds[0]
                if "appeared!" in embed.title:
                        if embed.image:
                            url = embed.image.url
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as response:
                                    with open('Temp.png', 'wb') as f:
                                        f.write(await response.read())

                                    try:
                                        sent_hash = imagehash.average_hash(Image.open("Temp.png"))

                                        for filename in os.listdir(POKEMONS):
                                            reference_image = Image.open(os.path.join(POKEMONS, filename))
                                            reference_hash = imagehash.average_hash(reference_image)

                                            if sent_hash == reference_hash:
                                                filename_without_ext = os.path.splitext(filename)[0].split(".")[-1]
                                                await message.channel.send(f"Match Found : {filename_without_ext}")
                                                return

                                        await message.channel.send("No Match Found")
                                        os.remove("Temp.png")

                                    except Exception as e:
                                        print(f"Error: {e}")
                                        await message.channel.send("An Error Occurred Processing The Image")

                                        


    await bot.process_commands(message)

bot.run('MTE5MjQ0ODgyODgwNTIyNjYyOA.GcZbfS.telV_M_p6RyVynLFYoWCdZSsvvT4Je0dnTqQqs')
