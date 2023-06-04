###### without concurrent multi-thread
import sys 
import os
import time
import pandas as pd 
from nltk.corpus import brown

dir = "fill in your directory where you save the codes"

sys.path.append(dir)
os.chdir(dir)



brown_dic_ls = set(brown.words())
from TPL_Int_Score import TPL_Int_Score
from TPL_Int_Score import Prep
PARA = TPL_Int_Score("TPL_support_files/Keyword List_Without Symbol.xlsx", "TPL_support_files/Excluded Acronyms.xlsx","TPL_support_files/Keyword List_With Symbol.xlsx", "TPL_support_files/cursing_lexicon.txt", \
	"TPL_support_files/emoticon_a.txt", "TPL_support_files/emoticon_vk.txt", "TPL_support_files/emoticon_tk.txt","TPL_support_files/Emoji Dictionary.xlsx", brown_dic_ls)

data = pd.read_excel(dir +  '/test-sample/Classifier Test.xlsx')
start = time.time()
for i in range(data.shape[0]):
	temp = PARA.run(data['TEXT'].iloc[i])
	print(i)

duration = time.time() - start



###### with concurrent multi-thread
import sys 
import os
import time
import pandas as pd 
from nltk.corpus import brown
import concurrent.futures


dir = "fill in your directory where you save the codes"

sys.path.append(dir)
os.chdir(dir)



brown_dic_ls = set(brown.words())
from TPL_Int_Score import TPL_Int_Score
from TPL_Int_Score import Prep
PARA = TPL_Int_Score("TPL_support_files/Keyword List_Without Symbol.xlsx", "TPL_support_files/Excluded Acronyms.xlsx","TPL_support_files/Keyword List_With Symbol.xlsx", "TPL_support_files/cursing_lexicon.txt", \
	"TPL_support_files/emoticon_a.txt", "TPL_support_files/emoticon_vk.txt", "TPL_support_files/emoticon_tk.txt","TPL_support_files/Emoji Dictionary.xlsx", brown_dic_ls)


data = pd.read_excel(dir +  '/test-sample/Classifier Test.xlsx')
temp = []
results=[]
count = 0

start = time.time()
with concurrent.futures.ProcessPoolExecutor() as executor:
    for i in executor.map(PARA.run,data['TEXT']):
        results.append(i)
        count += 1     



duration = time.time() - start


