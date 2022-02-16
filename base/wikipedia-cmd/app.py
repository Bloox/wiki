from asyncio import exceptions
from hashlib import algorithms_guaranteed
from unittest.mock import patch
from xml.etree.ElementPath import prepare_parent
import requests as r
from bs4 import BeautifulSoup
import os,sys,webbrowser
from rich import print
try:
    base=sys.argv[1]
    baseLang=base.split('/')[2].split('.')[0]
except:
    baseLang="en"
    base="https://en.wikipedia.org/"
#/wiki/Special:Random
memo={42:"https://en.wikipedia.org/wiki/42_(number)",43:[],424224067:["https://en.wikipedia.org/wiki/42_(number)"],424224068:[[]]}
def url_gen(url):
    global memo
    if url=='_':
        site=r.get(memo[42])
    elif url in memo:
        try:
            site=r.get(memo[url])
        except:
            print("somthing is wrong!")
            return 0
        if site.status_code!=200:
            print("somthing is wrong! (fixing . . .)")
        return url_gen(memo[url])
    elif (url=="random")|(url=='r'):
            
            site=r.get(f"{base}/wiki/Special:Random")
    else:
        try:
            if url.startswith(base):
                site=r.get(url)
            elif url.startswith("/w"):
                    site=r.get(base+url)
            else:
                    site=r.get(f"{base}/wiki/"+url)
        except:
            print(f'[red]Invalid url schem[/] :"{url}"')
            return
    
    url=site.url
    memo[43].insert(0,memo[42])
    memo[42]=url
    return site

def link_extration(url):
    site=url_gen(url)
    print("SCAN!")
    print("\n\n")
    ctx=BeautifulSoup(site.text,'html.parser')
    linki=ctx.select("li > a, p > a, i > a")
    for i in linki:
        try:
            print(i.parent.text,": [rgb(0,100,255)]"+i.text+"[/]   ","link: "+i["href"])
        except KeyError:
            print(i.text,None)
def parser(ctx,d,ol_enumer=False,not_indent=False,show_url=False):

    if not_indent==True:
        d=0
    tooPrint=[]
    l=0
    for i in ctx:
        if i.name=="b":
            tooPrint.append(f'[bold]{i.text}[/]')
        elif i.name=="h2":
            tooPrint.append(f"[bold]# {i.text}[/]")
            i.clear()
        elif i.name=="p":
            
            c=parser(i,d,show_url=show_url)

            tooPrint.append("".join([j for j in c+['\n']]))
            i.clear()
        elif i.name=="div":
            c=parser(i,d,show_url=show_url)
            tooPrint.append("".join([j for j in c+['']]))
        elif i.name=="ol":
            c=parser(i,d+1,show_url=show_url)

            tooPrint.append("".join([(("  "*(d+1))+j) for j in c]))
            i.clear()
        elif i.name=="ul":
            c=parser(i,d+1,show_url=show_url)

            tooPrint.append("".join([(("  "*(d+1))+j) for j in c]))
            i.clear()
        elif i.name=="li":
            
            c=parser(i,d,show_url=show_url)
            if ol_enumer==True:
                tooPrint.append("".join([j for j in c+[f'{l}']]))
            else:
                tooPrint.append("".join([j for j in c]))
            [i.clear()]
            l+=1
        elif i.name=="strong":
            c=parser(i,d,show_url=show_url)
            tooPrint.append("[bold]"+"".join([j for j in c])+"[/]")
        elif i.name=="a":
            o=show_url

            c=parser(i,d,show_url=show_url)
            tooPrint.append(f'[link={base+i["href"]}]'+"".join([j for j in c])+"[/]"+f'{"  ("+i["href"]+")" if o==True else ""}')
        elif i.name=="span":
            c=parser(i,d,not_indent=False,show_url=show_url)
            tooPrint.append("".join([j for j in c+['']]))
            
            i.clear()
        elif i.name=="cite":
            c=parser(i,d,show_url=show_url)
            tooPrint.append("[italic]"+"".join([j for j in c])+"[/]")
        elif i.name=="i":
            tooPrint.append(i.text)
        elif i.name==None:
            tooPrint.append(i)


    return tooPrint
def save_text(ctx,pach,ai):
    print('tex save 3',pach,ctx.url)
    ctx=BeautifulSoup(ctx.text,'html.parser')
    ctx=ctx.select("#mw-content-text > div.mw-parser-output")
    o=parser(ctx,0,show_url=ai)
    
    f=open(pach,'a')
    f.close()
    f=open(pach,'wb')
    for i in o:
        f.write(bytes(i,'utf-16'))
    f.close()
    print("Saved as:"+pach)
    return
def site(url,si=(False,0),**args):
    w=os.get_terminal_size()[0]
    site=url_gen(url)
    url=site.url
    newsite=BeautifulSoup(site.text,"html.parser")
    if site.status_code!=200:
        print(site.url)
        print("[red bold]Error in url[/]")
        return
    if si[0]==True:
        patch=""
        if si[1]==0:
            patch="./"+newsite.select_one("#firstHeading").text.replace('\\','-').replace('/','-').replace(':','-').replace("*",'-').replace('?','-').replace('"','-').replace("<",'-').replace('>','-').replace(">",'-').replace("|",
            '-')+'.html'
        else:
            patch=si[1]+newsite.select_one("#firstHeading").text.replace('\\','-').replace('/','-').replace(':','-').replace("*",'-').replace('?','-').replace('"','-').replace("<",'-').replace('>','-').replace(">",'-').replace("|",
            '-')+'.html'
            
        f=open(patch,'a')
        f.close()
        f=open(patch,'wb')
        f.write(bytes(site.text,'utf-16'))
        f.close()
        print("Saved as:"+patch)
        return site.url
    elif si[0]==2:
        print("text save 2")
        patch=""
        if si[1]==0:
            patch="./"+newsite.select_one("#firstHeading").text.replace('\\','-').replace('/','-').replace(':','-').replace("*",'-').replace('?','-').replace('"','-').replace("<",'-').replace('>','-').replace(">",'-').replace("|",
            '-')+'.txt'
            if 'show_url' in args:
                save_text(site,patch,ai=True)
            else:
                save_text(site,patch,ai=False)
            return
    print("---"+"[bold]"+newsite.select_one("#firstHeading").text+"[/bold]"+"-"*(w-(len(newsite.select_one("#firstHeading").text)+3)))
    
    content=newsite.select("#mw-content-text > div.mw-parser-output")
    try:
        o=newsite.select_one("#mw-content-text > div.mw-parser-output > div.hatnote.navigation-not-searchable > a")
        print("For other uses see:",f"[link={o['href']}]{o.text}[/link] --> {o['href']}")
    except:
        pass
    print()
    o=parser(content[0],0,**args)
    for i in o:
        print(i,end='')
    print('\n')

def search(url,forceFind=False,use_link=False,no_prompt=False):
    global memo
    if use_link==False:
        res=r.get(f"{base}/w/index.php?search={url}{'&fulltext=1'if forceFind==True else ''}")
    else:
        res=r.get(url)
    if res.url.startswith(f"{base}wiki"):
        print("page found open??")
        if (input("y|n >")=='y') and (no_prompt==False):
            site(res.url)
        else:
            print("page url:  "+res.url)
    else:
        newsite=BeautifulSoup(res.text,'html.parser')
        d=newsite.select_one("#mw-content-text > div.searchresults.mw-searchresults-has-iw > p.mw-search-exists")
        try:
            a=d.select_one("a")['href']
            w=parser(d,0,False,show_url=True)
            for i in w:
                print(i,end='')
            print('   ('+a+')')
            if (input("open page? y/n ")=='y')and(no_prompt==False):
                site(a)
                return a
        except:
            pass
        o=newsite.select("#mw-content-text > div.searchdidyoumean")
        if len(o)!=0:
            o=o[0]
            print("[rgb(0,100,255)]"+o.text+"[/]",o.select_one('a')['href'])
            if (input("y / n  ")=='y') and (no_prompt==False):
                search(o.select_one('a')['href'])
        o=newsite.select("#mw-content-text > div.searchresults.mw-searchresults-has-iw > ul > li")
        print('')
        
        memo[424224067]=[]
        a=True
        for i in o:
            hed=i.select_one("div.mw-search-result-heading")
            print(f"# {hed.text} : {hed.select_one('a')['href']}")      
            for j in i.select("div.searchresult"):
                if j['class']=='searchmatch':
                    print("   "+"[bold]"+j.text+"[/]")
                else:
                    print("   "+j.text)
            print("")
            print("   "+i.select_one("div.mw-search-result-data").text)
            memo[424224067].append(hed.select_one('a')['href'])

            if a==True:
                p=input("open this result? y/n or 's' to stop asking! ")
                if p=='y':
                    site(hed.select_one('a')['href'])
                    return
                if p=='s':
                    a=False
        memo[424224068].insert(0,memo[424224067])
        
            
        


def app(base_url):
    global  base,baseLang,memo
    print(f"server:{base}")
    
    while True:
        cmd=input(">")
        cmd=cmd.split(" ")
        try:
            match cmd:
                
                    case ["exit",*o]:
                        return
                    case ["restart"|"r",*a]:
                        if "-c" in a:
                            os.system("cls")
                        if '-s' in a:
                            print("[rgb(200,200,50)]Restarting . . .[/]")
                            os.system(f"C:/Users/joach/pythonPatch2/python.exe d:/eksperymenty/wiki/app.py")
                            return
                        print("[rgb(200,200,50)]Restarting . . .[/]")
                        os.system(f"C:/Users/joach/pythonPatch2/python.exe d:/eksperymenty/wiki/app.py {base}")
                        return
                    case ["get",url,*a]:
                        args={}

                        if "-ai" in a:
                            args['show_url']=True

                        site(url,**args)
                        
                    case ["save",url,*p]:
                        print(url,'  |',*p,sep=',')
                        
                        if (len(p)==2) and ((p[0]=="text")|(p[0]=='txt')):
                            print('text save')
                            if p[1] in "_*.":
                                site(url,(2,0))
                            else:
                                site(url,(2,p[1]))
                        else:
                            p.append(0)
                            
                            site(url,(True,p[0]))

                    case ["cls"|'clear'|'c']:
                        os.system('cls')
                    case ["ping"]:
                        check(base,True)
                    case ["server",*args]:
                        if len(args)==0:
                            print("use -help to get help information")
                        elif (args[0]=="-h")|(args[0]=='-help'):
                            print("""
                            -g | -get :print curret server
                            -p | -ping:use os ping command to anelize performenc
                            -h | -help:this msg
                            -c | -chan: chenge server to next argument(first perfom check if True restart app witch new servver)
                            """)
                        elif (args[0]=='-g')|(args[0]=='-get'):
                            print(f"server:{base}")
                        elif (args[0]=='-p')|(args[0]=="-ping"):
                            os.system(f"ping {base.split('/')[2]}")
                        elif (len(args)>=2)and((args[0]=="-c")|(args[0]=="-chan"))and(check(args[1],noOpen=True)==True):
                            base=args[1]
                            os.system(f"C:/Users/joach/pythonPatch2/python.exe d:/eksperymenty/wiki/app.py {args[1]}")
                            return
                    case ['get_links',*url]:
                        for i in url:
                            link_extration(i)
                    case ["open",url]:
                        _=url_gen(url)
                        url=_.url
                        webbrowser.open(url,1)
                    case ["search"|"find",*l]:
                        url=" ".join(l)
                        print("searching:"+url)
                        search(url)
                    case ["lsearch"|'lfind',*a]:
                        if '-a' in a:
                            print(memo[424224068])
                        else:
                            print(memo[424224068][0])
                    case ["searchs"|"finds",*l]:
                        url=" ".join(l)
                        print("searching:"+url)
                        search(url,True)
                    case ["lang",*o]:
                        if len(o)==0:
                            print('-h for help')
                        elif (o[0]=="-g")|(o[0]=='-get'):
                            print(baseLang)
                        elif (o[0]in["-h","-help"]):
                            print("""
        -g    : get current language
        -h    : print this msg
        -c    : change current language server if valid                 
        """)
                        elif (len(o)>=2)and(o[0]in["-c","-chan"])and(o[1]in ["en","ja","de","fr","it","pl",'ru',"es","zh","pt"]):
                            base='https://'+o[1]+".wikipedia.org/"
                            if check(base,noOpen=True)==True:
                                os.system(f"C:/Users/joach/pythonPatch2/python.exe d:/eksperymenty/wiki/app.py {base}")
                                return
                    
                    case ["help",*o]:
                        print("""
        exit               : exit program
        restart|r          : re-open program with curret settings   
        get                : read wikipedia pages arg[0]=url *arg[1+]=flags (to get list of flags type get %f)
        clear|cls|c        : clear terminal
        ping               : re-check servers                 
        save               : save wikipedia site as html *arg[1]=patch (defult './') | arg[1]=='text' arg[2] as patch (save as txt)
        server             : server manager (-h for help)
        get_links          : extract link from wikipedia site with url:arg[0]
        open               : open link from wikipedia in webbrowser
        lang               : change lange server (-h for help)
        help               : print this msg
        find               : use search arg[0+]=term
        finds              : search but forcing to show all results
        lfind              : last finded urls
        history            : list of site that you visit
        v                  : check global varibles ! and modify them
        last               : check last url
        """)
                    case ["v",*e]:
                        l=len(e)
                        if l==0:
                            pass
                        elif l==1:
                            if e[0] in memo:
                                print(e,memo[e[0]])
                    case ['last',*a]:
                        if len(a)==1:
                            try:
                                print(memo[43][int(a)])
                            except IndexError:
                                print("You don't visit enought sits")
                        else:
                            print(memo[42])
                    case ['history']:
                        print(memo[43])
        except Exception as ro:
            print("I have troble\n","ERROR LOG:")
            print(ro)
def check(base,noOpen=False):
    res=r.get(base)
    if res.status_code==200:
        print(f"[green]WIKIPEDIA SERVERS ON[/]:{base}") 
        if noOpen==False:
            app(base)
        else:
            return True
    else: print(f"[red]WIKIPEDIA SERVERS OFF[/]:{base}");return False

if __name__ == '__main__':
    check(base)