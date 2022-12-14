import discord
from discord.ext import commands

from ..utility import embed_builder, values

class Utility(commands.Cog):

    def __init__(self, client):
        self.client: discord.Client = client
        self.embeds = embed_builder.EmbedBuilder()
        self.values = values.Values()

    @commands.command(aliases=['u', 'uinfo', 'user'])
    async def userinfo(self, ctx, *user: discord.Member):
        if len(user) == 0:
            user = ctx.author
        else:
            user = user[0]
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered",
                        value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1),
                            value=role_string,
                            inline=False)
        perm_string = ', '.join([
            str(p[0]).replace("_", " ").title() for p in user.guild_permissions
            if p[1]
        ])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        await ctx.send(embed=embed)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *reason):
        if not reason:
            reason = "No reason"
        await member.ban(reason=reason)
        await ctx.send(embed=self.embeds.good(f"{member.mention} has been banned from the server."))
        embed = self.embeds.moderation([1, "b", reason, member])
        channel = await self.client.fetch_channel(self.values.get_channel("moderation_log"))
        await channel.send(embed=embed)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *reason):
        if not reason:
            reason = "No reason"
        await member.kick(reason=reason)
        await ctx.send(embed=self.embeds.good(f"{member.mention} has been kicked from the server."))
        embed = self.embeds.moderation([1, "k", reason, member])
        channel = await self.client.fetch_channel(self.values.get_channel("moderation_log"))
        await channel.send(embed=embed)

    @commands.command()
    async def unban(self, ctx: discord.Guild, member: discord.User):
        bans = await ctx.guild.bans()
        await ctx.guild.unban([x.user for x in bans if x.user.id == member.id][0])
        await ctx.send(embed=self.embeds.good(f"{member.mention} has been unbanned from the server."))
        embed = self.embeds.moderation([1, "ub", member])
        channel = await self.client.fetch_channel(self.values.get_channel("moderation_log"))
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Utility(client))