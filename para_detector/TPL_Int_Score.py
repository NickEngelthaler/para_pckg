import os 
import pandas as pd 
import re 
import sys 
import numpy as np
import regex
from collections import Counter
from Detect_Wordbased_TPL.Detect_Wordbased_TPL import Detect_Wordbased_TPL
from Detect_Silence import Detect_Silence
from Detect_Emphasis import Detect_Emphasis
from Detect_Asterisk_TPL.Detect_Asterisk_TPL import Detect_Asterisk_TPL
from Detect_Rhythm import Detect_Rhythm
from Detect_Censorship import Detect_Censorship
from Detect_Spelling import Detect_Spelling
from Detect_Emojicon_TPL.Detect_Emojicon_TPL import Detect_Emojicon_TPL
from Detect_Formatting import Detect_Formatting
from nltk.corpus import brown
from multiprocessing import Process
import traceback

class Prep:
    def __init__(self, keyword_no_symbol_path, acron_path,keyword_symbol_path, curse_path, emoticon_a_path, emoticon_vk_path, emoticon_tk_path,emoji_path, brown_dic):
        self.brown_dic = brown_dic

        self.word_list = pd.read_excel(keyword_no_symbol_path)  # "TPL_support_files/Keyword List_Without Symbol.xlsx"

        self.word_list.function[self.word_list.function == "Detect_Alternants"] = 'alternant'
        self.word_list.function[self.word_list.function == "Detect_Differentiators"] = 'differentiator'
        self.word_list.function[self.word_list.function == "Detect_alphahaptics"] = 'alphahaptics'

        self.keyword_dic = self.word_list.groupby('function')['keywords'].apply(lambda x: x.values.tolist()).to_dict()

        self.acron_list = pd.read_excel(acron_path) # "TPL_support_files/Excluded Acronyms.xlsx"
        self.acron_list = list(self.acron_list.loc[:,"Acronyms"])
        self.acron_list = self.acron_list + [w+"s" for w in self.acron_list]


        self.word_list_S =  pd.read_excel(keyword_symbol_path) #"TPL_support_files/Keyword List_With Symbol.xlsx"
        self.word_list_sb = self.word_list_S.copy()
        self.word_list_sb.function[self.word_list_sb.function=="Detect_Differentiators"] ='vs'
        self.word_list_sb.function[self.word_list_sb.function=="Detect_Volume"] ='vq'
        self.word_list_sb.function[self.word_list_sb.function=="Detect_alphakinesics"] ='vk'
        self.word_list_sb.function[self.word_list_sb.function=="Detect_alphahaptics"] ='tk'

        self.word_list_sb2 = self.word_list_S.copy()
        self.word_list_sb2.function[self.word_list_sb2.function!="Detect_alphakinesics"] ='nvk'
        self.word_list_sb2 = self.word_list_sb2.loc[self.word_list_sb2.function=='nvk',]

        self.word_list_sb3 = self.word_list_S.copy()
        self. word_list_sb3.function ='na'
        self.word_list_sb4 = pd.DataFrame({'TPL':["artifact"], 'keywords':["emoji"], 'function':["a"]})


        self.word_list_sb = pd.concat([self.word_list_sb, self.word_list_sb2,self.word_list_sb3, self.word_list_sb4])
        self.keyword_dic_sb = self.word_list_sb.groupby('function')['keywords'].apply(lambda x: x.values.tolist()).to_dict()


        self.word_list_comb = pd.concat([self.word_list_S, self.word_list], axis=0)
        self.word_list_comb = list(self.word_list_comb.loc[:,"keywords"])
        self.word_list_comb = [w.lower() for w in self.word_list_comb]


        self.censor_list = []
        with open(curse_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/cursing_lexicon.txt"
            for line in f:
                self.censor_list.append(line)
            self.censor_list = [re.sub(r"\n","", w) for w in self.censor_list]



        self.emoticon_a = []
        with open(emoticon_a_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/emoticon_a.txt"
            for line in f:
                self.emoticon_a.append(line)
            self.emoticon_a = [re.sub(r"\n","", w) for w in self.emoticon_a]

        self.emoticon_vk = []
        with open(emoticon_vk_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/emoticon_vk.txt"
            for line in f:
                self.emoticon_vk.append(line)
            self.emoticon_vk = [re.sub(r"\n","", w) for w in self.emoticon_vk]

        self.emoticon_tk = []
        with open(emoticon_tk_path, "r", encoding = 'utf-8') as f: #"TPL_support_files/emoticon_tk.txt"
            for line in f:
                self.emoticon_tk.append(line)
            
            self.emoticon_tk = [re.sub(r"\n","", w) for w in self.emoticon_tk]


        self.key_emoticon = {"a":self.emoticon_a, "na": self.emoticon_vk+ self.emoticon_tk, 
                    "vk":self.emoticon_vk, "nvk": self.emoticon_a + self.emoticon_tk,
                    "tk":self.emoticon_tk, "ntk": self.emoticon_a + self.emoticon_vk}


        self.key_emoji = pd.read_excel(emoji_path) #"TPL_support_files/Emoji Dictionary.xlsx"
        self.key_emoji['TPL'] = self.key_emoji['TPL'].str.lower()
        self.key_emoji = self.key_emoji.groupby('TPL')['Browser'].apply(lambda x: x.values.tolist()).to_dict()
        self.key_emoji['a'] = [w for w in self.key_emoji['a'] if w!='*️⃣']




    def emoticon_hierachy(self, type):
            ### pre-processing emoticon list ###
        if type == "tk":
            target_emoticon = self.key_emoticon["tk"]
        elif type == "vk":
            target_emoticon = self.key_emoticon["vk"]
        elif type == "a":
            target_emoticon = self.key_emoticon["a"]

        if "x" in target_emoticon:
            target_emoticon = [w for w in target_emoticon if (w not in ['x', 'xx', 'xxx', 'XXX', 'XX', 'X'])]


        emoticon = target_emoticon
        
        emoticon_top =[]
        emoticon_mid =[]
        emoticon_mid2 =[]
        emoticon_btm =[]
        # delete any duplication in the emoticon list 
        emoticon = list(set(emoticon))
        emoticon2 = []
        emoticon3 = []
        emoticon4 = []
        
        ### create four-layer hierachy in emoticon due to the nested characteristics of emoticon e.g. :D *:D ###
        # putting \\ before any symbol in the emoticon for the sake of regular expression search
        for k in emoticon: 
            k_hat = ""  
            for i in k:
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    k_hat = k_hat + i
                else:
                    k_hat = k_hat + "\\"+ i
            # create hierachy in emoticon 
            # the top(leaf) is emoticon only found once in the emoticon list        
            if (len(re.findall(k_hat, " ".join(emoticon))))==1:
                emoticon_top = emoticon_top + [k];
            else:
            # list of emoticon found more than once -- building units of top
                emoticon2 = emoticon2 + [k];

        # putting \\ before any symbol of the building unit of top for search purpose
        for k in emoticon2:
            k_hat = ""
            for i in k:
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    k_hat = k_hat + i
                else:
                    k_hat = k_hat + "\\"+ i
            # the mid is emoticon found once in the building units list
            if (len(re.findall(k_hat, " ".join(emoticon2))))==1:
                emoticon_mid = emoticon_mid + [k];
            else:
                # emoticon found more than once building units of mid 
                emoticon3 = emoticon3 + [k];

        # putting \\ before any symbol of the building unit of mid for search purpose
        for k in emoticon3:
            k_hat = ""
            for i in k:
                if len(re.findall(r"[0-9A-Za-z ]",i))!=0:
                    k_hat = k_hat + i
                else:
                    k_hat = k_hat + "\\"+ i
            # the mid2 is emoticon found once in the building units of mid list
            if (len(re.findall(k_hat, " ".join(emoticon3))))==1:
                emoticon_mid2 = emoticon_mid2 + [k];
            else:
            # emoticon found more than once in the building units of mid2 list
                emoticon_btm = emoticon_btm + [k];
        return emoticon_top, emoticon_mid2, emoticon_mid, emoticon_btm




class TPL_Int_Score:
    def __init__(self, keyword_no_symbol_path, acron_path,keyword_symbol_path, curse_path, emoticon_a_path, emoticon_vk_path, emoticon_tk_path,emoji_path, brown_dic):
        self.keyword_symbol_path = keyword_symbol_path
        self.keyword_no_symbol_path = keyword_no_symbol_path
        self.acron_path = acron_path
        self.curse_path = curse_path
        self.emoticon_a_path = emoticon_a_path
        self.emoticon_vk_path = emoticon_vk_path
        self.emoticon_tk_path = emoticon_tk_path
        self.emoji_path = emoji_path
        self.brown_dic = brown_dic

        self.Prep = Prep(self.keyword_no_symbol_path, self.acron_path,self.keyword_symbol_path, self.curse_path, self.emoticon_a_path, self.emoticon_vk_path, self.emoticon_tk_path,self.emoji_path, self.brown_dic)
        self.emoticon_hier_tk = self.Prep.emoticon_hierachy('tk')
        self.emoticon_hier_vk = self.Prep.emoticon_hierachy('vk')
        self.emoticon_hier_a = self.Prep.emoticon_hierachy('a')

    def all_modules(self, textline):
        ## Function Detect_Wordbased_TPL
        temp = Detect_Wordbased_TPL(textline, self.Prep.keyword_dic, self.Prep.acron_list, self.Prep.brown_dic)
        vq_stress = temp[0]
        vq_pitch = temp[1]
        vq_tempo = temp[2]
        vq_emphasis = temp[3]
        vs_alternants = temp[4]
        vs_differentiators = temp[5]
        tk_alphahaptics = temp[6]
        vq_intst_tempo = temp[7]
        vq_intst_emphasis = temp[8]


        ## Function Detect_Silence
        temp = Detect_Silence(textline)
        vq_silence = temp[0]
        vq_intst_silence = temp[1]



        ############### Apply Function --  Detect_Emphasis ####################

        ## Function Detect_Emphasis
        temp = Detect_Emphasis(textline)
        vq_emphasis = vq_emphasis + temp[0]
        vq_intst_emphasis = vq_intst_emphasis + temp[1]


        ############### Apply function -- Detect_Asterisk_TPL ###############

        temp = Detect_Asterisk_TPL(textline, self.Prep.keyword_dic_sb)
        vq_volume = temp[0]
        vs_differentiators_asterisk = temp[1]
        tk_alphahaptics_asterisk = temp[2]
        vk_alphakinesics = temp[3]
        a_emoji_symbol = temp[4]

        ############### Apply Function --  Detect_Rhythm ####################


        vq_rhythm = Detect_Rhythm(textline, self.Prep.word_list_comb, self.Prep.brown_dic)

        ############### Apply Function -- Detect_Censorship ####################


        vq_censorship = Detect_Censorship(textline, self.Prep.censor_list)


        ############### Apply Function -- Detect_Spelling ####################
         
        ## Function Detect_Spelling
        
        vq_spelling = Detect_Spelling(textline, self.Prep.word_list,self.Prep.brown_dic, self.Prep.acron_list)

        ############### Apply Function -- Detect_Emojicon_TPL ####################


        temp = Detect_Emojicon_TPL(textline, self.Prep.key_emoji, self.Prep.key_emoticon, self.emoticon_hier_tk, self.emoticon_hier_vk, self.emoticon_hier_a )
        tk_tactileemojis = temp[0]
        vk_bodilyemojis = temp[1]
        a_nonbodilyemojis = temp[2]
        tk_bodilyemoticons = temp[3]
        vk_bodilyemoticons = temp[4]
        a_nonbodilyemoticons = temp[5]

        tk_intst_tactileemojis = temp[6]
        vk_intst_bodilyemojis = temp[7]
        a_intst_nonbodilyemojis = temp[8]
        tk_intst_bodilyemoticons = temp[9]
        vk_intst_bodilyemoticons = temp[10]
        a_intst_nonbodilyemoticons = temp[11]



        ############### Apply Function -- Detect_Formatting  ####################
        # applicable for A

        a_formatting  = Detect_Formatting([textline])


    ############### Add them up ##########
        TPL_raw_count = vq_stress + vq_pitch + vq_tempo + vq_emphasis + vq_volume  + vq_rhythm + vq_censorship + vq_spelling + vq_silence + \
        vs_alternants + vs_differentiators + vs_differentiators_asterisk + \
        tk_alphahaptics  + tk_alphahaptics_asterisk + tk_tactileemojis + tk_bodilyemoticons + \
        vk_alphakinesics + vk_bodilyemojis + vk_bodilyemoticons + \
        a_emoji_symbol + a_nonbodilyemojis + a_nonbodilyemoticons + a_formatting


        vs_differentiators = vs_differentiators_asterisk + vs_differentiators
        tk_alphahaptics = tk_alphahaptics  + tk_alphahaptics_asterisk
        a_nonbodilyemoticons = a_nonbodilyemoticons + a_emoji_symbol
        vq_tempo = vq_tempo + vq_silence
        total_emoticon_count = tk_bodilyemoticons + vk_bodilyemoticons + a_nonbodilyemoticons
        total_emoji_count = tk_tactileemojis + vk_bodilyemojis + a_nonbodilyemojis
        total_emoji_raw_count = tk_intst_tactileemojis + vk_intst_bodilyemojis + a_intst_nonbodilyemojis



        return vq_pitch, vq_rhythm, vq_stress, vq_emphasis, vq_tempo, vq_volume, vq_censorship, vq_spelling, vs_alternants, vs_differentiators, tk_alphahaptics, vk_alphakinesics, a_formatting, tk_bodilyemoticons, vk_bodilyemoticons, a_nonbodilyemoticons, tk_tactileemojis, vk_bodilyemojis, a_nonbodilyemojis, total_emoji_raw_count, total_emoji_count, total_emoticon_count, TPL_raw_count

    def run(self, textline):
        try:
            if type(textline) == str and len(textline.strip()) > 0:                                        
                res = self.all_modules(textline)
                return res
        except Exception:
            print(traceback.print_exc())
