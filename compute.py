import shutil
from private import SUBTITLES_CHANNEL_ID


from speech_rec import get_large_audio_transcription
from txt_processing import process_text


async def send_text_asap_from_onlyfiles(onlyfiles, audio_chunks_dir, tmpdirname, language, bot, channel, ctx):
    for f in onlyfiles:
            if f.startswith("unc_"):
                whole_text = get_large_audio_transcription(audio_chunks_dir, tmpdirname+'/'+f, language)
                if len(whole_text)<2:
                    continue
                sender_id = int(f.split('.')[0].split('_')[-1])
                try:
                    truc_muche = await bot.fetch_user(sender_id)
                    sender_name = truc_muche.name
                except Exception as e:
                    print(f'exception:  {e}')
                    sender_name = str(sender_id)
                
                if len(whole_text) > 0:
                    whole_text = process_text(whole_text, ctx.guild)

                    current_text = str(sender_name) + " : " + str(whole_text) + '\n'
                    subtitles_channel = await bot.fetch_channel(SUBTITLES_CHANNEL_ID)

                    if len(current_text)>=1999:
                        current_text = current_text[:1999]
                    await subtitles_channel.send(current_text)
        
    shutil.rmtree(tmpdirname)