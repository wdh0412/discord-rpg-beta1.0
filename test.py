import discord
from dice import *
from state import *
import datetime
import time
from discord.ext import commands, tasks
from dungeon import *
from skullman import *
import math
import threading 
from user import *
from ctx import *
import tkinter
import asyncio

app = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@app.event
async def on_ready():
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)



@app.command(aliases=['따라하기', 'f'])
async def follow(ctx, *args):
    dddtv = checkUuser(ctx.author.name, ctx.author.id)
    await ctx.send('니얼굴')
    await asyncio.sleep(10)
    await ctx.send(', '.join(args))
    


async def follows(ctx):
    await ctx.send('니얼굴')
    
    




@app.command(aliases=['주사위', '다이스'])
async def d(ctx):
    result, _color, app, user = dice()
    embed = discord.Embed(title = "주사위 게임 결과", description = None, color = _color)
    embed.add_field(name = "Super Bot의 숫자", value = ":game_die: " + app, inline = True)
    embed.add_field(name = ctx.author.name+"의 숫자", value = ":game_die: " + user, inline = True)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)


@app.command(aliases=['회원가입', '가입'])
async def log(ctx):
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")

        Signup(ctx.author.name, ctx.author.id)

        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.")

@app.command(aliases=['탈퇴', '계정삭제'])
async def res(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    dddtt = checkstate(ctx.author.name, ctx.author.id)
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        Deletestate(dddtt)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")

        await ctx.send("탈퇴가 완료되었습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")

        await ctx.send("등록되지 않은 사용자입니다.")

@app.command(aliases=['내정보', '프로필'])
async def my(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        level, exp, money, ching, job  = userInfo(userRow)
        userNum = checkUserNum()
        expToUP = level*20
        boxes = int(exp/expToUP*20)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "칭호", value = ching)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "직업", value = job)
        embed.add_field(name = "XP: " + str(exp) + "/" + str(expToUP), value = boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.add_field(name = "보유 자산", value = money, inline = False)

        await ctx.send(embed=embed)
        
@app.command(aliases=['전직'])
async def swardman(ctx, jobd):
    print("전직이 가능한지 확인합니다.")
    userExistance, userRow = checkstat(ctx.author.name, ctx.author.id)
    senderRow = checkUuser(ctx.author.name, ctx.author.id) 
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미  전직하셨습니다.")
    else:
        if jobd == '검사':
            print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
            print("")
            statupz(ctx.author.name, ctx.author.id)
            jobmit(senderRow, jobd)
            print("검사 전직이 완료되었습니다.")
            print("------------------------------\n")
            await ctx.send("검사 전직이 완료되었습니다.")
        elif jobd == '레인저':
            print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
            print("")
            statupr(ctx.author.name, ctx.author.id)
            jobmit(senderRow, jobd)
            print("레인저 전직이 완료되었습니다.")
            print("------------------------------\n")
            await ctx.send("레인저 전직이 완료되었습니다.")
        elif jobd == '마법사':
            print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
            print("")
            statupb(ctx.author.name, ctx.author.id)
            jobmit(senderRow, jobd)
            print("마법사 전직이 완료되었습니다.")
            print("------------------------------\n")
            await ctx.send("마법사 전직이 완료되었습니다.")\
            
        else:
            await ctx.send("그런직업은 없음.")
        

@app.command(aliases=['내스텟', '내스탯'])
async def state(ctx):
    userExistance = checkstat(ctx.author.name, ctx.author.id)
    userRow = checkstate(ctx.author.name, ctx.author.id)
    statch = False, None
    if userExistance:
        hp, dd, db, dx, sp  = statInfo(userRow)
        statNum = checkstatNum()
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "HP", value = hp)
        embed.add_field(name = "물리공격력", value = dd)
        embed.add_field(name = "마법공격력", value = db)
        embed.add_field(name = "내구력: ", value = dx)
        embed.add_field(name = "회피율", value = sp)
        await ctx.send(embed=embed)
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("전직 후 자신의 스텟를 확인할 수 있습니다.")

@app.command(aliases=['스텟업', '스탯업'])
async def stateup(ctx, sstatssup, pointint):
    userExistance = checkstat(ctx.author.name, ctx.author.id)
    userRow = checkstate(ctx.author.name, ctx.author.id)
    senderRow = checkUuser(ctx.author.name, ctx.author.id)
    postpo = checkstatpoint(senderRow)
    if userExistance:
        if sstatssup == "hp":
            if int(pointint) > postpo:
                await ctx.send("스텟 포인트가 부족합니다")
            elif int(pointint) <= postpo:
                statlvlup(senderRow, userRow, 1, pointint)
        elif sstatssup == "dd":
            if int(pointint) > postpo:
                await ctx.send("스텟 포인트가 부족합니다")
            elif int(pointint) <= postpo:
                statlvlup(senderRow, userRow, 2, pointint)
        elif sstatssup == "db":
            if int(pointint) > postpo:
                await ctx.send("스텟 포인트가 부족합니다")
            elif int(pointint) <= postpo:
                statlvlup(senderRow, userRow, 3, pointint)
        elif sstatssup == "dx":
            if int(pointint) > postpo:
                await ctx.send("스텟 포인트가 부족합니다")
            elif int(pointint) <= postpo:
                statlvlup(senderRow, userRow, 4, pointint)
        elif sstatssup == "sp":
            if int(pointint) > postpo:
                await ctx.send("스텟 포인트가 부족합니다")
            elif int(pointint) <= postpo:  
                statlvlup(senderRow, userRow, 5, pointint)  


        
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("전직 후 자신의 스텟를 확인할 수 있습니다.")        

@app.command(aliases=['던'])
async def dungeonss(ctx):
    dgdg = checkdgd(ctx.author.name, ctx.author.id)
    dada = skullattack(dgdg)
    skullattackpow = skullattackpower(dgdg)
    print(dada)
    print(skullattackpow)

@app.command(aliases=['지하미궁입장'])
async def dungeon(ctx):
    userRow = checkstate(ctx.author.name, ctx.author.id)
    senderRow = checkUuser(ctx.author.name, ctx.author.id)
    checkmonsteris = checkmonster()
    if indgg(senderRow) == 1:
        if checkmonsteris == 1:
            await ctx.send("던전의 입구가 막혀있습니다 누군가의 기척이 느껴집니다..")
        else:
            if jobrow(senderRow) == '검사':
                skullman()
                hp, dd, db, dx, sp, atsp, sk1t, sk1cl, sk2t, sk3de, sk3cl1, sk3cl2, fnskt, fnskcl, _sk2cl, _sheild = warriorInfo(userRow)
                dgzup(ctx.author.name, ctx.author.id, hp, dd, db, dx, sp, atsp, sk1t, sk1cl, sk2t, sk3de, sk3cl1, sk3cl2, fnskt, fnskcl, _sk2cl, _sheild)
                indggch(senderRow)
                dgdg = checkdgd(ctx.author.name, ctx.author.id)
                await ctx.send("던전에 입장하셨습니다. 누군가의 시선이 느껴집니다...")
                while True:
                    fullhp = isuserfullhp(userRow)
                    ss = skullis()
                    if ss == True:
                        skullskillset = skullmanskill()
                        dgdgg = checkdgd(ctx.author.name, ctx.author.id)
                        if checkskullstun() == 1:
                            await asyncio.sleep(5)

                            if skullskillset == 1:
                                warpassivesk = warriorpassiveskull()
                                if warpassivesk == 3030:
                                    skat = skullattack(dgdgg)
                                    vsskullhp = skullvshp(dgdgg)
                                    skullattackpow = skullattackpower(dgdgg)
                                    skullhpp = skullhp()
                                    if skat == False:
                                        embed=discord.Embed(title="💀해골병사의 공격!💀", description="💭회피하는데 성공했다💭", color=0xff0000)
                                        embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                        embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                        embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                        embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                        await ctx.send(embed=embed)
                                    elif skat == 10:
                                        embed=discord.Embed(title="💀해골병사의 공격!💀", description="-"  + str(skullattackpow)  + "💥 의 데미지를 받았다!", color=0xff0000)
                                        embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                        embed.set_thumbnail(url="http://upload3.inven.co.kr/upload/2020/06/20/bbs/i015976418714.gif") 
                                        embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                        embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                        await ctx.send(embed=embed)
                                    elif skat == 9:
                                        embed=discord.Embed(title="💀해골병사의 공격!💀", description="🛡해골병사의 공격을 막아냈다!🛡", color=0xff0000)
                                        embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                        embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i13521511410.gif") 
                                        embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                        embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                        await ctx.send(embed=embed)
                                    elif skat == 444:
                                        resetDatadg()
                                        indggchrest(senderRow)
                                        await ctx.send("죽었당 ㅠ")  
                                elif warpassivesk == 1010:
                                    embed=discord.Embed(title="🗡검사 패시브 발동!🗡", description="🛡해골병사의 공격을 막아냈다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i14153243568.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif warpassivesk == 2020:
                                    embed=discord.Embed(title="✨검사 패시브 발동!✨", description="🛡해골병사의 공격을 쳐냈다. 해골병사가 1.5초간 기절합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i16264265597.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                    await asyncio.sleep(1.5)                                  
                            elif skullskillset == 2:
                                skullsh = skullsheld()
                                vsskullhp = skullvshp(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if skullsh == 2222:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="🛡해골병사가 방어태세를 취합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://img3.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202111/09/ruliweb/20211109162350838rwje.jpg") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsh == 3333:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="🛡해골병사가 방어태세를 취합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://img3.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202111/09/ruliweb/20211109162350838rwje.jpg") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                            elif skullskillset == 3:
                                warpassivesk = warriorpassiveskull()
                                if warpassivesk == 3030:
                                    skullsmash = skullsmashattack(dgdgg)
                                    vsskullhp = skullvshp(dgdgg)
                                    skullhpp = skullhp()
                                    skullsmashis = skullsmashattackis(dgdgg)
                                    if skullsmash == 10:
                                        embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="-" + str(skullsmashis) + "🗯 데미지!", color=0x780050)
                                        embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg") 
                                        embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i015281678920.gif") 
                                        embed.add_field(name="💀해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False) 
                                        embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                        await ctx.send(embed=embed)
                                    elif skullsmash == False:
                                        embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="💭회피하는데 성공했다💭", color=0x780050)
                                        embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                        embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                        embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                        embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                        await ctx.send(embed=embed)
                                    elif skullsmash == 9:
                                        embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="🛡해골병사의 공격을 막아냈다!🛡", color=0x780050)
                                        embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                        embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i13521511410.gif") 
                                        embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                        embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                        await ctx.send(embed=embed)
                                    elif skullsmash == 444:
                                        resetDatadg()
                                        indggchrest(senderRow)
                                        await ctx.send("뼈다귀 강타 맞고 죽었당 ㅠ")
                                elif warpassivesk == 1010:
                                    embed=discord.Embed(title="🗡검사 패시브 발동!🗡", description="🛡해골병사의 뼈다귀 강타를 막아냈다!🛡", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i14153243568.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif warpassivesk == 2020:
                                    embed=discord.Embed(title="✨검사 패시브 발동!✨", description="🛡해골병사의 뼈다귀 강타를 쳐냈다 해골병사가 1.5초간 기절합니다!🛡", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i16264265597.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                    await asyncio.sleep(1.5)     
                            elif skullskillset == 4:
                                hillskullp = hillskullisover()
                                hillhp = hillskull()
                                vsskullhp = skullvshp(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                
                                if hillhp == 39:
                                    
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="해골병사가 재조립을 시전합니다 hp를 회복합니다.", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://i3.ruliweb.com/ori/21/12/10/17da2a0217d48b822.gif") 
                                    embed.add_field(name="해골병사의 HP", value="+" + str(hillskullp) + "💗" +  "  " +   str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed) 
                                if hillhp == 40:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="해골병사가 재조립을 시전합니다 hp를 회복합니다.", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://i3.ruliweb.com/ori/21/12/10/17da2a0217d48b822.gif") 
                                    embed.add_field(name="해골병사의 HP", value="+40💗" +  "  " +   str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                        else:
                            print("해골병사는 스턴걸려서 움직일수없다.")
                    elif ss == False:
                        print("사망..")
                        break
                            
                        
                       
            elif jobrow(senderRow) == '레인저':
                skullman()
                _hp, _dd, _db, _dx, _sp, _critcaldameger, _critcallsetr, _atspr, _sk1cl, _sk2cl, _sk3ti, _sk3cl, _sk4cl, _miss = rainerInfo(userRow)
                dgrup(ctx.author.name, ctx.author.id, _hp, _dd, _db, _dx, _sp, _critcaldameger, _critcallsetr, _atspr, _sk1cl, _sk2cl, _sk3ti, _sk3cl, _sk4cl, _miss)
                indggch(senderRow)
                dgdg = checkdgd(ctx.author.name, ctx.author.id)
                await ctx.send("던전에 입장하셨습니다. 누군가의 시선이 느껴집니다...")
                while True:
                    fullhp = isuserfullhp(userRow)
                    ss = skullis()
                    if ss == True:
                        skullskillset = skullmanskill()
                        dgdgg = checkdgd(ctx.author.name, ctx.author.id)
                        if checkskullstun() == 1:
                            await asyncio.sleep(5)
                            if skullskillset == 1:
                                skat = skullattackrainer(dgdgg)
                                vsskullhp = skullvshp(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if skat == False:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="💭회피하는데 성공했다💭", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 10:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="-"  + str(skullattackpow)  + "💥 의 데미지를 받았다!", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="http://upload3.inven.co.kr/upload/2020/06/20/bbs/i015976418714.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 9:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="해골병사의 공격을 피했다💨", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 444:
                                    resetDatadg()
                                    indggchrest(senderRow)
                                    await ctx.send("죽었당 ㅠ")                                    
                            elif skullskillset == 2:
                                skullsh = skullsheld()
                                vsskullhp = skullvshp(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if skullsh == 2222:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="🛡해골병사가 방어태세를 취합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://img3.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202111/09/ruliweb/20211109162350838rwje.jpg") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                    
                                elif skullsh == 3333:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="🛡해골병사가 방어태세를 취합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://img3.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202111/09/ruliweb/20211109162350838rwje.jpg") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                            elif skullskillset == 3:
                                skullsmash = skullsmashattack(dgdgg)
                                vsskullhp = skullvshp(dgdgg)
                                skullhpp = skullhp()
                                skullsmashis = skullsmashattackrainer(dgdgg)
                                if skullsmash == 10:
                                    embed=discord.Embed(title="💀해골병사가 🦴뼈다귀 강타🦴를 사용합니다!💀", description="-" + str(skullsmashis) + "🗯 데미지!", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg") 
                                    embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i015281678920.gif") 
                                    embed.add_field(name="💀해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False) 
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsmash == False:
                                    embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="💭회피하는데 성공했다💭", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsmash == 9:
                                    embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="해골병사의 공격을 피했다💨", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsmash == 444:
                                    resetDatadg()
                                    indggchrest(senderRow)
                                    await ctx.send("뼈다귀 강타 맞고 죽었당 ㅠ")  
                            elif skullskillset == 4:
                                hillskullp = hillskullisover()
                                hillhp = hillskull()
                                vsskullhp = skullvshp(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if hillhp == 39:
                                    
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="해골병사가 재조립을 시전합니다 hp를 회복합니다.", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://i3.ruliweb.com/ori/21/12/10/17da2a0217d48b822.gif") 
                                    embed.add_field(name="해골병사의 HP", value="+" + str(hillskullp) + "💗" +  "  " +   str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                if hillhp == 40:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="해골병사가 재조립을 시전합니다 hp를 회복합니다.", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://i3.ruliweb.com/ori/21/12/10/17da2a0217d48b822.gif") 
                                    embed.add_field(name="해골병사의 HP", value="+40💗" +  "  " +   str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                        else:
                            print("해골병사는 스턴걸려서 움직일수없다.")
                    elif ss == False:
                        print("사망..")
                        break
                            
                        

                        
            elif jobrow(senderRow) == '마법사':
                skullman()
                _hp, _dd, _db, _dx, _sp, _atspb, _sk1fire, _sk1light, _sk1water, _sk2cl, _sk3tifire, _sk3clfire, _sk3tilight, _sk3cllight, _sk3tiwater, _sk3clwater, _sk4tmfire, _sk4clfire, _sk4tilight, _sk4cllight, _sk4tmwater, _sk4clwater, _sheldb, _bariar = bupsaInfo(userRow)
                dgbup(ctx.author.name, ctx.author.id, _hp, _dd, _db, _dx, _sp, _atspb, _sk1fire, _sk1light, _sk1water, _sk2cl, _sk3tifire, _sk3clfire, _sk3tilight, _sk3cllight, _sk3tiwater, _sk3clwater, _sk4tmfire, _sk4clfire, _sk4tilight, _sk4cllight, _sk4tmwater, _sk4clwater, _sheldb, _bariar)
                indggch(senderRow)
                dgdg = checkdgd(ctx.author.name, ctx.author.id)
                await ctx.send("던전에 입장하셨습니다. 누군가의 시선이 느껴집니다...")
                while True:
                    fullhp = isuserfullhp(userRow)
                    ss = skullis()
                    if ss == True:
                        skullskillset = skullmanskill()
                        dgdgg = checkdgd(ctx.author.name, ctx.author.id)
                        if checkskullstun() == 1:
                            await asyncio.sleep(5)
                            if skullskillset == 1:
                                skat = bupsaskullattack(dgdgg)
                                vsskullhp = skullvshp(dgdgg)
                                bariaris = dungeonbariar(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if skat == False:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="💭회피하는데 성공했다💭", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 10:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="-"  + str(skullattackpow)  + "💥 의 데미지를 받았다!", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="http://upload3.inven.co.kr/upload/2020/06/20/bbs/i015976418714.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 9:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="해골병사의 공격을 피했다💨", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 4:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="-"  + str(skullattackpow)  + "💥 의 데미지를 받았다!", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="http://upload3.inven.co.kr/upload/2020/06/20/bbs/i015976418714.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(bariaris) + "🤍"    + str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 3:
                                    embed=discord.Embed(title="💀해골병사의 공격!💀", description="-"  + str(skullattackpow)  + "💥 의 데미지를 받았다!", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="http://upload3.inven.co.kr/upload/2020/06/20/bbs/i015976418714.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(bariaris) + "🤍"    + str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)    
                                elif skat == 444:
                                    resetDatadg()
                                    indggchrest(senderRow)
                                    await ctx.send("죽었당 ㅠ")                                    
                            elif skullskillset == 2:
                                skullsh = skullsheld()
                                vsskullhp = skullvshp(dgdgg)
                                bariaris = dungeonbariar(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if skullsh == 2222:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="🛡해골병사가 방어태세를 취합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://img3.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202111/09/ruliweb/20211109162350838rwje.jpg") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                    await ctx.send("해골 병사가 방어태세를 취합니다.")
                                elif skullsh == 3333:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="🛡해골병사가 방어태세를 취합니다!🛡", color=0xff0000)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://img3.daumcdn.net/thumb/R658x0.q70/?fname=https://t1.daumcdn.net/news/202111/09/ruliweb/20211109162350838rwje.jpg") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                    await ctx.send("해골 병사가 방어태세를 취합니다.")
                            elif skullskillset == 3:
                                skullsmash = skullsmashattackbupsa(dgdgg)
                                vsskullhp = skullvshp(dgdgg)
                                bariaris = dungeonbariar(dgdgg)
                                skullhpp = skullhp()
                                skullsmashis = skullsmashattackis(dgdgg)
                                if skullsmash == 10:
                                    embed=discord.Embed(title="💀해골병사가 🦴뼈다귀 강타🦴를 사용합니다!💀", description="-" + str(skullsmashis) + "🗯 데미지!", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg") 
                                    embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i015281678920.gif") 
                                    embed.add_field(name="💀해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False) 
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsmash == False:
                                    embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="💭회피하는데 성공했다💭", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsmash == 9:
                                    embed=discord.Embed(title="💀해골병사💀의 🦴뼈다귀 강타🦴!", description="해골병사의 공격을 피했다💨", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://64.media.tumblr.com/e384973a23ab6dc7c8d6e36a432edaf4/tumblr_mzg50tP7wE1tpg9bro1_500.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 4:
                                    embed=discord.Embed(title="💀해골병사가 🦴뼈다귀 강타🦴를 사용합니다!💀", description="-" + str(skullsmashis) + "🗯 데미지!", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i015281678920.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(bariaris) + "🤍"    + str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skat == 3:
                                    embed=discord.Embed(title="💀해골병사가 🦴뼈다귀 강타🦴를 사용합니다!💀", description="-" + str(skullsmashis) + "🗯 데미지!", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i015281678920.gif") 
                                    embed.add_field(name="해골병사의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(bariaris) + "🤍"    + str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                elif skullsmash == 444:
                                    resetDatadg()
                                    indggchrest(senderRow)
                                    await ctx.send("뼈다귀 강타 맞고 죽었당 ㅠ")  
                            elif skullskillset == 4:
                                hillskullp = hillskullisover()
                                hillhp = hillskull()
                                vsskullhp = skullvshp(dgdgg)
                                skullattackpow = skullattackpower(dgdgg)
                                skullhpp = skullhp()
                                if hillhp == 39:
                                    
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="해골병사가 재조립을 시전합니다 hp를 회복합니다.", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://i3.ruliweb.com/ori/21/12/10/17da2a0217d48b822.gif") 
                                    embed.add_field(name="해골병사의 HP", value="+" + str(hillskullp) + "💗" +  "  " +   str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                                if hillhp == 40:
                                    embed=discord.Embed(title="💀해골병사 스킬발동!💀", description="해골병사가 재조립을 시전합니다 hp를 회복합니다.", color=0x780050)
                                    embed.set_author(name="전투", icon_url="https://wow.zamimg.com/uploads/screenshots/small/39410.jpg")
                                    embed.set_thumbnail(url="https://i3.ruliweb.com/ori/21/12/10/17da2a0217d48b822.gif") 
                                    embed.add_field(name="해골병사의 HP", value="+40💗" +  "  " +   str(skullhpp) + "/80☠", inline=False)
                                    embed.add_field(name=str(ctx.author.name) +  " 님의 HP", value=str(vsskullhp)  + "/" + str(fullhp) + "❤", inline=False)
                                    await ctx.send(embed=embed)
                        else:
                            print("스턴걸려있음")
                    elif ss == False:
                        print("사망..")
                        break
                            
                        

            else:            
                await ctx.send("개발중 입니다..ㅋ")
    else:
        await ctx.send("지금은 그럴떄가 아닌거같다.")
                    

@app.command(aliases=['공격', 'a'])
async def attack(ctx):
    userRow = checkstate(ctx.author.name, ctx.author.id)
    senderRow = checkUuser(ctx.author.name, ctx.author.id)
    if indgg(senderRow) == 2:
        if jobrow(senderRow) == '검사':
            dgdga = checkdgd(ctx.author.name, ctx.author.id)
            warriornn = warriorstun(dgdga)
            if warriornn == 1:
                collat = atspds(dgdga)
                if collat == 1:
                    swatcl = warrioratcl(dgdga)
                    swatsk = swardattackskull(dgdga)
                    warrioratclrestart(dgdga)
                    warriorskulldd = warriorvsskulldd(dgdga)
                    vsskullhp = skullvshp(dgdga)
                    skullhpp = skullhp()
                    fullhp = isuserfullhp(userRow)
                    if swatsk == False:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="💀해골병사💀에겐 맞지 않았다!💨", color=0xffff00)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                        embed.set_thumbnail(url="https://blog.kakaocdn.net/dn/pWPGp/btrTtk5BNtj/pGLfrhSphwRI77pTCX7Mw0/img.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(swatcl)
                        warrioratclredelet(dgdga)
                    elif swatsk == 10:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="-" + str(warriorskulldd) +  "💥 데미지!", color=0xffff00)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                        embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i15228566695.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(swatcl)
                        warrioratclredelet(dgdga)
                    elif swatsk == 9:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="🛡💀해골병사💀가 공격을 막았다!🛡", color=0xffff00)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                        embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i014005288588.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(swatcl)

                        warrioratclredelet(dgdga)
                    elif swatsk == 444:
                        resetDatadg()
                        indggchrest(senderRow)
                        lbl = lvlupskullman(senderRow)
                        maxexp = maxexpskull(senderRow)
                        eexxpp = userexp(senderRow)
                        lvlvl = userlv(senderRow)
                        if lbl == 000:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="💀해골병사💀를 쓰러뜨렸따!", color=0xffd000)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="경험치 + 10", value="돈 + 2000", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                        elif lbl == 999:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="💀해골병사💀를 쓰러뜨렸따!", color=0xffd000)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="lvlup!!", value="돈 + 2000, 스텟포인트 + 3!", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)

                elif collat == 2:
                    await ctx.send("쿨타임이 안지났습니다.")
            elif warriornn == 2:
                await ctx.send("기절상태입니다. 스킬사용이 불가합니다")
                
        elif jobrow(senderRow) == '레인저':
            dgdga = checkdgd(ctx.author.name, ctx.author.id)
            rainerst = rainerstun(dgdga)
            if rainerst == 1:
                ineratrego = raineratrego(dgdga)
                if ineratrego == 1:
                    riatcl = raineratsp(dgdga)
                    raatsk = rainerattackskull(dgdga)
                    raineratgo(dgdga)
                    warriorskulldd = warriorvsskulldd(dgdga)
                    vsskullhp = skullvshp(dgdga)
                    skullhpp = skullhp()
                    fullhp = isuserfullhp(userRow)
                    crit = raineratcritcaldd(dgdga)
                    if raatsk == False:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🏹", description="💀해골병사💀에겐 맞지 않았다!💨", color=0xb8ffe7)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/oVOSa.jpg")
                        embed.set_thumbnail(url="https://blog.kakaocdn.net/dn/pWPGp/btrTtk5BNtj/pGLfrhSphwRI77pTCX7Mw0/img.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(riatcl)
                        raineratreset(dgdga)
                    elif raatsk == 10:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🏹", description="-" + str(warriorskulldd) +  "🎯 데미지!", color=0xb8ffe7)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/oVOSa.jpg")
                        embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/16/bbs/i15151813644.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(riatcl)
                        raineratreset(dgdga)
                    elif raatsk == 9:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🏹", description="🛡💀해골병사💀가 공격을 막았다!🛡", color=0xb8ffe7)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/oVOSa.jpg")
                        embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i014005288588.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(riatcl)
                        raineratreset(dgdga)
                    elif raatsk == 444:
                        resetDatadg()
                        indggchrest(senderRow)
                        lbl = lvlupskullman(senderRow)
                        maxexp = maxexpskull(senderRow)
                        eexxpp = userexp(senderRow)
                        lvlvl = userlv(senderRow)
                        if lbl == 000:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🏹", description="💀해골병사💀를 쓰러뜨렸따!", color=0xb8ffe7)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="경험치 + 10", value="돈 + 2000", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                        elif lbl == 999:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🏹", description="💀해골병사💀를 쓰러뜨렸따!", color=0xb8ffe7)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="lvlup!!", value="돈 + 2000, 스텟포인트 + 3!", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                    elif raatsk == 777:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🏹", description="-" + str(crit) +  "🌟 크리티컬 데미지!", color=0x00fffb)
                        embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/oVOSa.jpg")
                        embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/16/bbs/i14377166465.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(riatcl)
                        raineratreset(dgdga)
                    elif raatsk == 77444:
                        resetDatadg()
                        indggchrest(senderRow)
                        lbl = lvlupskullman(senderRow)
                        maxexp = maxexpskull(senderRow)
                        eexxpp = userexp(senderRow)
                        lvlvl = userlv(senderRow)
                        if lbl == 000:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🌟", description="💀해골병사💀를 쓰러뜨렸따!", color=0x00fffb)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="경험치 + 10", value="돈 + 2000", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                        elif lbl == 999:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🌟", description="💀해골병사💀를 쓰러뜨렸따!", color=0x00fffb)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="lvlup!!", value="돈 + 2000, 스텟포인트 + 3!", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)

                elif ineratrego == 2:
                    await ctx.send("쿨타임이 안지났습니다.")
            elif rainerst == 2:
                await ctx.send("기절상태입니다. 스킬사용이 불가합니다")
                
            
        elif jobrow(senderRow) == '마법사':
            dgdga = checkdgd(ctx.author.name, ctx.author.id)
            bupsann = bupsastun(dgdga)
            if bupsann == 1:
                collat = bupsaatsprego(dgdga)
                if collat == 1:
                    bupsaatcll = bupsaatsp(dgdga)
                    swatsk = swardattackskull(dgdga)
                    bupsaatgo(dgdga)
                    warriorskulldd = warriorvsskulldd(dgdga)
                    vsskullhp = skullvshp(dgdga)
                    skullhpp = skullhp()
                    fullhp = isuserfullhp(userRow)
                    if swatsk == False:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🪄", description="💀해골병사💀에겐 맞지 않았다!💨", color=0xffffff)
                        embed.set_author(name="전투", icon_url="https://upload3.inven.co.kr/upload/2021/03/26/bbs/i15371837713.jpg")
                        embed.set_thumbnail(url="https://blog.kakaocdn.net/dn/pWPGp/btrTtk5BNtj/pGLfrhSphwRI77pTCX7Mw0/img.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(bupsaatcll)
                        bupsaatreset(dgdga)
                    elif swatsk == 10:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🪄", description="-" + str(warriorskulldd) +  "🎇 데미지!", color=0xffffff)
                        embed.set_author(name="전투", icon_url="https://upload3.inven.co.kr/upload/2021/03/26/bbs/i15371837713.jpg")
                        embed.set_thumbnail(url="https://i.pinimg.com/originals/c3/f0/de/c3f0de1af1ac02cc5a9c3bbc2a999bfe.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(bupsaatcll)
                        bupsaatreset(dgdga)
                    elif swatsk == 9:
                        embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🪄", description="🛡💀해골병사💀가 공격을 막았다!🛡", color=0xffffff)
                        embed.set_author(name="전투", icon_url="https://upload3.inven.co.kr/upload/2021/03/26/bbs/i15371837713.jpg")
                        embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2022/06/13/bbs/i014005288588.gif")
                        embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                        embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                        await ctx.send(embed=embed)
                        await asyncio.sleep(bupsaatcll)


                        bupsaatreset(dgdga)
                    elif swatsk == 444:
                        resetDatadg()
                        indggchrest(senderRow)
                        lbl = lvlupskullman(senderRow)
                        maxexp = maxexpskull(senderRow)
                        eexxpp = userexp(senderRow)
                        lvlvl = userlv(senderRow)
                        if lbl == 000:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🪄", description="💀해골병사💀를 쓰러뜨렸따!", color=0xffffff)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="경험치 + 10", value="돈 + 2000", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                        elif lbl == 999:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🪄", description="💀해골병사💀를 쓰러뜨렸따!", color=0xffffff)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="lvlup!!", value="돈 + 2000, 스텟포인트 + 3!", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                elif collat == 2:
                    await ctx.send("쿨타임이 안지났습니다.")
            elif bupsann == 2:
                await ctx.send("기절상태입니다. 스킬사용이 불가합니다")
    else:
        await ctx.send("지금은 그럴떄가 아닌거같다.")

@app.command(aliases=['스킬1', 's1'])
async def skill1(ctx): 
    userRow = checkstate(ctx.author.name, ctx.author.id)
    senderRow = checkUuser(ctx.author.name, ctx.author.id)
    if indgg(senderRow) == 2: 
        userlvskill = userlvofskll(senderRow)
        if userlvskill >= 5:
            if jobrow(senderRow) == '검사':
                dgdga = checkdgd(ctx.author.name, ctx.author.id)
                warriornn = warriorstun(dgdga)
                if warriornn == 1:
                    collat = skill1swardmanreis(dgdga)
                    if collat == 1:
                     
                        swatcl = skill1swardmancltime(dgdga)
                   
                        stunfaint = warriorskill1stun(dgdga)
                    
                        swatsk = swardskill1skull(dgdga)
              
                        skill1swardmanclrego(dgdga)
                 
                        warriorskulldd = swardskill1skulldamge(dgdga)
                
                        vsskullhp = skullvshp(dgdga)
                     
                        skullhpp = skullhp()
                        fullhp = isuserfullhp(userRow)
                        if swatsk == False:
                      
                            embed=discord.Embed(title=str(ctx.author.name) +  "님이 페인트를 사용! 🗡", description="💀해골병사💀가 공격을 피했다!", color=0xffff00)
                            embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                            embed.set_thumbnail(url="https://blog.kakaocdn.net/dn/pWPGp/btrTtk5BNtj/pGLfrhSphwRI77pTCX7Mw0/img.gif")
                            embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                            embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                            await ctx.send(embed=embed)
                            await asyncio.sleep(swatcl)
                            skill1swardmanclreset(dgdga)
                        elif swatsk == 10:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님이 페인트를 사용! 🗡", description="-" + str(warriorskulldd) +  "💥 데미지!", color=0xffff00)
                            embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2020/03/27/bbs/i015292836332.gif")
                            embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                            embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                            await ctx.send(embed=embed)
                            await asyncio.sleep(swatcl)
                            skill1swardmanclreset(dgdga)
                        elif swatsk == 9:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님이 페인트를 사용!✨", description="-" + str(warriorskulldd) +  "💥 데미지! 💫상대가 2초동안 기절합니다!💫", color=0xffc400)
                            embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                            embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/15/bbs/i14093240100.gif")
                            embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                            embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                            await ctx.send(embed=embed)
                            skill1stunff()
                            await asyncio.sleep(2)
                            skill1stunss()
                            await asyncio.sleep(stunfaint)
                            skill1swardmanclreset(dgdga)
                        elif swatsk == 444:
                            resetDatadg()
                            indggchrest(senderRow)
                            lbl = lvlupskullman(senderRow)
                            maxexp = maxexpskull(senderRow)
                            eexxpp = userexp(senderRow)
                            lvlvl = userlv(senderRow)
                            if lbl == 000:
                                embed=discord.Embed(title=str(ctx.author.name) +  "님이 페인트를 사용!✨", description="💀해골병사💀를 쓰러뜨렸따!", color=0xffc400)
                                embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                                embed.add_field(name="경험치 + 10", value="돈 + 2000", inline=False)
                                embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                                embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                                await ctx.send(embed=embed)
                        elif lbl == 999:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님이 페인트를 사용!✨", description="💀해골병사💀를 쓰러뜨렸따!", color=0xffc400)
                            embed.set_thumbnail(url="https://upload3.inven.co.kr/upload/2021/12/16/bbs/i015033845565.gif")
                            embed.add_field(name="lvlup!!", value="돈 + 2000, 스텟포인트 + 3!", inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 exp", value=str(eexxpp) + "/" + str(maxexp), inline=False)
                            embed.add_field(name=str(ctx.author.name) +  "님 의 lvl", value=str(lvlvl), inline=False)
                            await ctx.send(embed=embed)
                    elif collat == 2:
                        await ctx.send("쿨타임이 안지났습니다.")
                elif warriornn == 2:
                    await ctx.send("기절상태입니다. 스킬사용이 불가합니다")
                
            elif jobrow(senderRow) == '레인저':
                dgdga = checkdgd(ctx.author.name, ctx.author.id)
                rainerst = rainerstun(dgdga)
                if rainerst == 1:
                    ineratrego = skill1rainerreis(dgdga)
                    if ineratrego == 1:
                        riatcl = skill1rainercl(dgdga)
                        shiftskil = skill1rainer(dgdga)
                        skill1rainerrego(dgdga)
                        warriorskulldd = warriorvsskulldd(dgdga)
                        vsskullhp = skullvshp(dgdga)
                        skullhpp = skullhp()
                        fullhp = isuserfullhp(userRow)
                        if shiftskil == 0000:
                            await ctx.send("아직 피할수있다!.")
                            
                        elif shiftskil == 3333:
                            embed=discord.Embed(title=str(ctx.author.name) +  "님이 쉬프트를 사용! 🏹", description="🪵앞으로 3번의 공격을 회피합니다!🪵", color=0xb8ffe7)
                            embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/oVOSa.jpg")
                            embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i16190683397.gif")
                            embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                            embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                            await ctx.send(embed=embed)
                            await asyncio.sleep(riatcl)
                            skill1rainerreset(dgdga)
                    elif ineratrego == 2:
                        await ctx.send("아직 쿨타임이다 기다려라잇ㄱ.")
                elif rainerst == 2:
                    await ctx.send("기절상태입니다. 스킬사용이 불가합니다")
                
            
            elif jobrow(senderRow) == '마법사':
                dgdga = checkdgd(ctx.author.name, ctx.author.id)
                bupsann = bupsastun(dgdga)
                if bupsann == 1:
                    firelightwater = bupsafirelightwater(dgdga)
                    if firelightwater == 1:
                        collat = bupsaskill1clfirereis(dgdga)
                        if collat == 1:
                            bupsaatcll = bupsaskill1clfire(dgdga)
                            skillfire1 = skill1bupsafire(dgdga)
                            bupsaskill1firerego(dgdga)
                            warriorskulldd = warriorvsskulldd(dgdga)
                            vsskullhp = skullvshp(dgdga)
                            skullhpp = skullhp()
                            fullhp = isuserfullhp(userRow)
                            if skillfire1 == False:
                                await ctx.send("해골 병사가 공격을 회피하였다!.")
                                await asyncio.sleep(bupsaatcll)
                                bupsaskill1firereset(dgdga)
                            elif skillfire1 == 10:
                                embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="-" + str(warriorskulldd) +  "💥 데미지!", color=0xffff00)
                                embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                                embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i15228566695.gif")
                                embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                                embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                await ctx.send(embed=embed)
                                await asyncio.sleep(bupsaatcll)
                                bupsaskill1firereset(dgdga)
                            elif skillfire1 == 9:
                                await ctx.send("해골 병사가 공격을 막았다!.")
                                await asyncio.sleep(bupsaatcll)


                                bupsaatreset(dgdga)
                            elif skillfire1 == 444:
                                resetDatadg()
                                indggchrest(senderRow)
                                await ctx.send("해골 병사를 물리쳤다!")
                        elif collat == 2:
                            await ctx.send("쿨타임이 안지났습니다.")
                    elif firelightwater == 2:
                        collat = bupsaskill1cllightreis(dgdga)
                        if collat == 1:
                            bupsaatcll = bupsaskill1cllight(dgdga)
                            skilllight1 = skill1skulllight(dgdga)
                            bupsaskill1llightrego(dgdga)
                            warriorskulldd = warriorvsskulldd(dgdga)
                            vsskullhp = skullvshp(dgdga)
                            skullhpp = skullhp()
                            fullhp = isuserfullhp(userRow)
                            if skilllight1 == False:
                                await ctx.send("해골 병사가 공격을 회피하였다!.")
                                await asyncio.sleep(bupsaatcll)
                                bupsaskill1llightreset(dgdga)
                            elif skilllight1 == 10:
                                embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="-" + str(warriorskulldd) +  "💥 데미지!", color=0xffff00)
                                embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                                embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i15228566695.gif")
                                embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                                embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                await ctx.send(embed=embed)
                                await asyncio.sleep(bupsaatcll)
                                bupsaskill1llightreset(dgdga)
                            elif skilllight1 == 9:
                                await ctx.send("해골 병사가 공격을 막았다!.")
                                await asyncio.sleep(bupsaatcll)


                                bupsaskill1llightreset(dgdga)
                            elif skilllight1 == 444:
                                resetDatadg()
                                indggchrest(senderRow)
                                await ctx.send("해골 병사를 물리쳤다!")
                        elif collat == 2:
                            await ctx.send("쿨타임이 안지났습니다.")
                    elif firelightwater == 3:
                        collat = bupsaskill1clwaterreis(dgdga)
                        if collat == 1:
                            bupsaatcll = bupsaskill1clwater(dgdga)
                            skillwater1 = hilllight1(dgdga)
                            bupsaskill1lwaterrego(dgdga)
                            warriorskulldd = warriorvsskulldd(dgdga)
                            vsskullhp = skullvshp(dgdga)
                            skullhpp = skullhp()
                            fullhp = isuserfullhp(userRow)
                            if skillwater1 == 39:
                                await ctx.send("해골 병사가 공격을 회피하였다!.")
                                await asyncio.sleep(bupsaatcll)
                                bupsaskill1lwaterreset(dgdga)
                            elif skillwater1 == 40:
                                embed=discord.Embed(title=str(ctx.author.name) +  "님의 공격! 🗡", description="-" + str(warriorskulldd) +  "💥 데미지!", color=0xffff00)
                                embed.set_author(name="전투", icon_url="https://img.theqoo.net/img/hESlH.jpg")
                                embed.set_thumbnail(url="https://optimal.inven.co.kr/upload/2019/01/17/bbs/i15228566695.gif")
                                embed.add_field(name=str(ctx.author.name) +  "님 의 HP", value=str(vsskullhp) + "/" + str(fullhp) + "❤", inline=False)
                                embed.add_field(name="해골병사💀의 HP", value=str(skullhpp) + "/80☠", inline=False)
                                await ctx.send(embed=embed)
                                await asyncio.sleep(bupsaatcll)
                                bupsaskill1lwaterreset(dgdga)
                        elif collat == 2:
                            await ctx.send("쿨타임이 안지났습니다.")            
                elif bupsann == 2:
                    await ctx.send("기절상태입니다. 스킬사용이 불가합니다")
        else:
            await ctx.send("레벨이 부족하다.")

    else:
        await ctx.send("지금은 그럴떄가 아닌거같다.")


                        





@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다")

app.run('MTA3NTI3NDg5MzQwODYwODMxNw.Gab8Mh.kohpmzmB_X8dQ3RdAqumML53WDDqgavcSriGSc')