import fasttext.util
# fasttext.util.download_model('fr', if_exists='ignore')  # English
ft = fasttext.load_model('cc.fr.300.bin')

ft.get_dimension()