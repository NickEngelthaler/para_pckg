import sys
import os 
import pandas as pd
sys.path.append("/Users/AaronXu/Research_Project/TPL/Extract_Features/step4_TPL_classifier/TPL_support_files")
os.chdir("/Users/AaronXu/Research_Project/TPL/Extract_Features/step4_TPL_classifier/TPL_support_files")



word_list_sb = pd.read_excel("Keyword_list_Without Symbol.xlsx")
word_list_nsb = pd.read_excel("Keyword List_With Symbol.xlsx")
word_list = pd.concat([word_list_sb, word_list_sb], axis=0)
word_list = list(word_list.loc[:,"keywords"])

word_list_nsb = list(word_list_nsb.loc[:,"with symbol"])



acr_list = pd.read_excel("/Users/AaronXu/Research_Project/TPL/Extract_Features/TPL_resource/Excluded Acronyms.xlsx")
acr_list = list(acr_list.iloc[:,1])
acr_list = list(set(acr_list))[1:]

word_list_sb = pd.read_excel("/Users/AaronXu/Research_Project/TPL/Extract_Features/TPL_resource/Keyword_list_Without Symbol.xlsx")
word_list_sb = list(word_list_sb.loc[:,"without symbol"])
word_list_nsb = pd.read_excel("/Users/AaronXu/Research_Project/TPL/Extract_Features/TPL_resource/Keyword List_With Symbol.xlsx")
word_list_nsb = list(word_list_nsb.loc[:,"with symbol"])

word_list = word_list_nsb + word_list_sb
word_list = list(set(word_list))
word_list = word_list[1:]
word_list = word_list[0:1] + word_list[3:]


import enchant
eng_dic = enchant.Dict("en_US")
word_list = [w for w in word_list if not eng_dic.check(w)]


import pandas as pd
file = pd.read_excel("/Users/AaronXu/Research_Project/TPL/Extract_Features/step4_TPL_classifier/TPL_support_files/Emoji Dictionary.xlsx")
file
file.groupby('TPL').nunique()

file = file[["No","TPL","Browser"]]
file = file.dropna(axis=0)

emoji_vq = file.loc[file.TPL=="VQ"]
emoji_vq = emoji_vq[["Browser"]]

emoji_vk = file.loc[file.TPL=="VK"]
emoji_vk = emoji_vk[["Browser"]]

emoji_tk = file.loc[file.TPL=="TK"]
emoji_tk = emoji_tk[["Browser"]]

emoji_a = file.loc[file.TPL=="A"]
emoji_a = emoji_a[["Browser"]]


emoticon_vk = [':‑)',':-Þ', ':‑Þ', ':Þ', ':-þ', ':‑þ', ':þ', ':)', ':-]', ':‑]', ':]', ':-3', ':‑3', ':3',
               ':->', ':‑>', ':>', '8-)', '8‑)', '8)', ':-}', ':‑}', ':}', ':o)', ':c)', ':^)', '=]',
               '=)', ':-D', ':‑D', ':D', '8-D', '8‑D', '8D', 'x-D', 'x‑D', 'xD', 'X-D', 'X‑D', 'XD',
               '=D', '=3', 'B^D', ':-))', ':‑))', ':-(', ':‑(', ':(', ':-c', ':‑c', ':c', ':-<', ':‑<',
               ':<', ':-[', ':‑[', ':[', ':-||', ':‑||', '>:[', ':{', ':@', '>:(', ":'-(", ":'‑(", ":'(",
               ":'-)", ":'‑)", ":')", "D-':", "D‑':", 'D:<', 'D:', 'D8', 'D;', 'D=', 'DX', ':-O', ':‑O',
               ':O', ':-o', ':‑o', ':o', ':-0', ':‑0', '8-0', '8‑0', '>:O', ':-*', ':‑*', ':*', ':×', ';-)',
               ';‑)', ';)', '*-)', '*‑)', '*)', ';-]', ';‑]', ';]', ';^)', ':-,', ':‑,', ';D', 'X‑P', 'XP',
               'x-p', 'x‑p', 'xp', ':-p', ':‑p', ':p', ':-b', ':‑b', ':b', 'd:', '=p', '>:P', ':-/', ':‑/',
               ':/', ':-.', ':‑.', '>:/', '=/', ':L', '=L', ':S', ':-|', ':‑|', ':|', ':$', ':-X', ':‑X',
               ':X', ':-#', ':‑#', ':#', ':-&', ':‑&', ':&', 'O:-)', 'O:‑)', 'O:)', '0:-3', '0:‑3', '0:3',
               '0:-)', '0:‑)', '0:)', '0;^)', '>:-)', '>:‑)', '>:)', '}:-)', '}:‑)', '}:)', '3:-)', '3:‑)',
               '3:)', '>;)', '|;-)', '|;‑)', '|-O', '|‑O', ':-J', ':‑J', '#-)', '#‑)', '%-)', '%‑)', '%)',
               ':-###..', ':‑###..', ':###..', '<:-|', '<:‑|', "',:-|", "',:‑|", "',:-l", "',:‑l", '<_<',
               '>_>', 'v.v', 'O_O', 'o-o', 'o‑o', 'O_o', 'o_O', 'o_o', 'O-O', 'O‑O', '( ͡° ͜ʖ ͡°)', '(>_<)',
               '(>_<)>', "(';')", '(^^ゞ', '(^_^;)', '(-_-;)', '(~_~;)', '(・.・;)', '(・_・;)', '(・・;)',
               '^^;', '^_^;', '(#^.^#)', '(^^;)', '(^.^)y-.o○', '(-.-)y-°°°', '(-_-)zzz', '(^_-)', '(^_-)-☆',
               '((+_+))', '(+o+)', '(°°)', '(°-°)', '(°.°)', '(°_°)', '(°_°>)', '(°レ°)', '<(｀^´)>', '^_^',
               '(°o°)', '(^_^)/', '(^O^)／', '(^o^)／', '(^^)/', '(≧∇≦)/', '(/◕ヮ◕)/', '(^o^)丿', '∩(·ω·)∩',
               '(·ω·)', '^ω^', '(__)', '_(._.)_', '_(_^_)_', '<(_ _)>', '<m(__)m>', 'm(__)m', 'm(_ _)m',
               '＼(°ロ＼)', '(／ロ°)／', "('_')", '(/_;)', '(T_T)', '(;_;)', '(;_;', '(;_:)', '(;O;)',
               '(:_;)', '(ToT)', '(Ｔ▽Ｔ)', ';_;', ';-;', ';n;', ';;', 'Q.Q', 'T.T', 'TnT', 'QQ', 'Q_Q',
               '(ー_ー)!!', '(-.-)', '(-_-)', '(一一)', '(；一_一)', '(=_=)', '(=^·^=)', '(=^··^=)', '=_^=',
               '(..)', '(._.)', '^m^', '(・・?', '(?_?)', '(－‸ლ)', '>^_^<', '<^!^>', '^/^', '（*^_^*）',
               '§^.^§', '(^<^)', '(^.^)', '(^ム^)', '(^·^)', '(^.^)', '(^_^.)', '(^_^)', '(^^)', '(^J^)',
               '(*^.^*)', '^_^', '(#^.^#)', '（^—^）', '(^^)/~~~', '(^_^)/~', '(;_;)/~~~', '(^.^)/~~~',
               '(-_-)/~~~', '($··)/~~~', '(@^^)/~~~', '(T_T)/~~~', '(ToT)/~~~', '(V)o￥o(V)', '＼(~o~)／',
               '＼(^o^)／', '＼(-o-)／', 'ヽ(^。^)ノ', 'ヽ(^o^)丿', '(*^0^*)', '(*_*)', '(*_*;', '(+_+)',
               '(@_@)', '(@_@。', '(＠_＠;)', '＼(◎o◎)／！', '!(^^)!', '(*^^)v', '(^^)v', '(^_^)v', '(’-’*)',
               '(＾ｖ＾)', '(＾▽＾)', '(・∀・)', '(´∀`)', '(⌒▽⌒）', '(~o~)', '(~_~)', '(^^ゞ', '(p_-)',
               '((d[-_-]b))', '(ーー゛)', '(^_^メ)', '(-_-メ)', '(~_~メ)', '(－－〆)', '(・へ・)', '(｀´)',
               '<`～´>', '<`ヘ´>', '(ーー;)', '(^0_0^)', '( ..)φφ(..)', '(●＾o＾●)', '(＾ｖ＾)', '(＾ｕ＾)',
               '(＾◇＾)', '( ^)o(^ )', '(^O^)', '(^o^)', '(^○^)', ')^o^(', '(*^▽^*)', '(✿◠‿◠)', '(￣ー￣)',
               '(￣□￣;)', '°o°', '°O°', ':O', 'o_O', 'o_0', 'o.O', '(o.o)', 'oO', '(*´▽｀*)', '(*°∀°)=3',
               '( ﾟ Дﾟ)', '(°◇°)', '(*￣m￣)', 'ヽ(´ー｀)┌', '(´･ω･`)', '(‘A`)', '(*^3^)/~☆', '.....φ(・∀・＊)',
               '@@','~~','^^']


with open("emoticon_vk.txt", "w", encoding = 'utf-8') as f:
    for s in emoticon_vk:
        f.write(str(s) +"\n")

with open("emoticon_vk.txt", "r") as f:
    for line in f:
    emoticon_vk.append(line)


import os
os.chdir("/Users/AaronXu/Research_Project/TPL/Extract_Features/step4_TPL_classifier/TPL_support_files")
emoticon_a = ['@};-', '@};‑', '@}->--', '@}‑>‑‑', "@}-;-'---", "@}‑;‑'‑‑‑", '@>-->--',
              '@>‑‑>‑‑', '*<|:-)', '*<|:‑)', '~(_8^(I)', '5:-)', '5:‑)', '=:o]', '7:^]', ',:-)',
              ',:‑)', '</3', '<3', '><>', '<*)))-{', '<*)))‑{', '><(((*>', '//0-0\\', '//0‑0\\',
              'ӽd̲̅a̲̅r̲̅w̲̅i̲̅ɳ̲̅ᕗ', 'Ӽd̲̅a̲̅r̲̅w̲̅i̲̅ɳ̲̅ᕗ', 'ӽe̲̅v̲̅o̲̅l̲̅u̲̅t̲̅i̲̅o̲̅ɳ̲̅ᕗ', 'Ӽe̲̅v̲̅o̲̅l̲̅u̲̅t̲̅i̲̅o̲̅ɳ̲̅ᕗ', '(o|o)', '(V)o￥o(V)', '.o○○o.',
              '( ^^)_U~~( ^^)_旦~~', '☆彡', '☆ミ', '>°)))彡', '(Q', '))', '><ヨヨ', '(°))<<', '>°))))彡',
              '<°)))彡', '>°))彡', '<+', '))><<', '<*))', '>=<', '<コ:彡', 'Ｃ:.ミ', '~>°)～～～',
              '～°·_·°～', '(°°)～', '●～*', '￣|○', 'STO', 'OTZ', 'OTL', 'orz',
              '$$$', '>>>','<<<', '^^^','~~>', '<~~']

with open("emoticon_a.txt", "w", encoding = 'utf-8') as f:
    for s in emoticon_a:
        f.write(str(s) +"\n")

with open("emoticon_a.txt", "r") as f:
    for line in f:
        emoticon_a.append(line)











