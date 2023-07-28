import discord
import warnings
warnings.filterwarnings('ignore')
import emoji

from gensim.models.word2vec import Word2Vec
import gensim.downloader as api


def process_text(txt, guild):
    txt = has_arobase(txt, guild)
    txt = emotes(txt, guild)
    txt = txt + emoji.emojize(':thumbs_up:')
    return txt


def has_arobase(txt_unchanged: str, guild):
    txt_unchanged = txt_unchanged.replace('@', ' @ ')
    txt = txt_unchanged.replace('.','')
    # txt = txt.replace('@', ' @ ')
    
    l = txt.lower().split(' ')
    # if 'arobase' in l or 'ping' in l[-1] or '@' in l: # drop last to nerf "arobase."
    #     if 'arobase' in l:
    #         str_found = 'arobase'
    #     elif 'ping' in l:
    #         str_found = 'ping'
    #     elif '@' in l:
    #         str_found = '@'
    
    indices = [i for i, x in enumerate(l) if x == "arobase" or x=='ping' or x=='@']
    for ind in indices:
        # str_found = l[ind]
        idx_to_ping = ind + 1
        if len(l[idx_to_ping])<1:
            return txt_unchanged   #   + ' (bien tenté fdp mais non)'
        
        # find corresponding member
        if l[idx_to_ping]=='à':
            l[idx_to_ping]='a'
        if l[idx_to_ping].lower() == 'everyone':
            txt_unchanged += ' '
            txt_unchanged += '@everyone'

        for member in guild.members:
            if l[idx_to_ping] in (member.name.lower()):
                ping_str = member.mention
                txt_unchanged += ' '
                txt_unchanged += ping_str

        for member in guild.members:
            if member.nick:
                if l[idx_to_ping] in (member.nick.lower()):
                    ping_str = member.mention
                    txt_unchanged += ' '
                    txt_unchanged += ping_str
        
        for role in guild.roles:
            if l[idx_to_ping] in str(role).lower():
                txt_unchanged += role.mention

    return txt_unchanged # + '<:bourse:1058046211363446847>'



def add_relevant_emojis(txt):
    # download the model and return as object ready for use
    model_glove_twitter = api.load("glove-twitter-100")

    emoji_dict = 0
    print(model_glove_twitter.similarity("man", "network"))



    return txt





def emotes(txt, guild):
    emote_dict = {}
    server_emojis = guild.emojis
    for x in server_emojis:
        emote_dict[x.name.capitalize()] = x
        if x.name == "dokfun":
            emote_dict["Dock"] = x
            emote_dict["Duck"] = x
            emote_dict["Docs"] = x
            emote_dict["Doc"] = x
        
        if x.name == "pradelle":
            emote_dict["Pradel"] = x
        
        if x.name == "bilboum":
            emote_dict["Bill bon"] = x
            emote_dict["Bill boum"] = x
            emote_dict["Bill boom"] = x
        
        if x.name == "Francois":
            emote_dict["François"] = x

        if x.name == "hugodenizart":
            emote_dict["Hugo denizart"] = x
            emote_dict["Hugo denise"] = x
            emote_dict["Hugo de nizar"] = x
            emote_dict["Hugo de niz"] = x
            emote_dict["The pound"] = x
            emote_dict["The pooh"] = x
            
        if x.name == "volpi":
            emote_dict["Volpy"] = x
            
        
    for emote_str,emoji_object in emote_dict.items():
        if emote_str.lower() in txt and "<:"+emote_str.lower() not in txt:
            txt = txt.replace(emote_str.lower(), str(emoji_object))
        if emote_str.capitalize() in txt and "<:"+emote_str.capitalize() not in txt:
            txt = txt.replace(emote_str.capitalize(), str(emoji_object))
    return txt


