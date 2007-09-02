import pygame
from pygame.locals import *

def convert_event_to_key(event):
    if event.type==KEYDOWN:
        if event.key == K_BACKSPACE:
            return "BACK"
        elif event.key == K_DELETE:
            return "DEL"
        elif event.key == K_HOME: 
            return "HOME"
        elif event.key == K_END:
            return "END"
        elif event.key == K_LEFT:
            return "LEFT"
        elif event.key == K_RIGHT:
            return "RIGHT"
        elif event.key == K_RETURN:
            return "RETURN"
        elif event.key == K_TAB:
            return "TAB"
        else:
            return event.unicode.encode('latin-1')
    return None

def split_word(font, text, wrap):
        letters=[i for i in text]
        nw=""
        words=[]
        for i in letters:
            if font.size(nw+" "+i)[0]<=wrap:
                nw=" ".join([nw, i])
            else:
                words.append(nw+" -")
                nw=" ".join(["",i])
        if nw:
            words.append(nw)
        return words

def wrap_text(font, text, wrap):
    new=text.split("\n")
    if wrap:
        new_lines=[]
        for line in new:
            if font.size(line)<=wrap:
                new_lines.append(line)
            else:
                words=line.split(" ")
                ok=""
                for word in words:
                    if font.size(ok+ " "+word)[0]<=wrap:
                        ok=" ".join([ok,word])
                    else:
                        if ok:
                            new_lines.append(ok)
                        ok=""
                        if font.size(ok+word)[0]<=wrap:
                            ok=" ".join([ok,word])
                        else:
                            for i in split_word(word):
                                new_lines.append(i)
                if ok:
                    new_lines.append(ok)
        new=new_lines

    lines=new
    width=0
    for i in lines:
        if font.size(i)[0]>width:width=font.size(i)[0]
    height=int(font.fsize*len(lines))

    return lines, (width, height)
