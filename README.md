# PARA
Codes used to develop the PARA GUI 

- TPL_UI.py generates the PARA GUI. On top of the PARA codes, it utilizes multi-thread input processing in parallel. This improves the computational speed by 4 times (e.g., it takes around 3.6 seconds to process 100 texts with each less than 20 tokens)

- TPL_Int_Score.py compiles all the PARA modules into one. 
- test.py can be used to directly call TPL_Int_Score and test its performance. We provide two versions of test, one with multiprocessing, the other without multiprocessing. 

- Detect_Wordbased_TPL is a whole folder that contains the detection of TPL elements that are word / phrase based, including VQ stress, pitch, tempo, emphasis, VS alternants, differentiators, TK alphahaptics.   
Its main function is in Detect_Wordbased_TPL.py and five supporting functions: check_emphasis.py (detect emphasis TPL pattern), check_temp.py (detect tempo TPL pattern), check_pitch.py (detect pitch TPL pattern), check_stress.py (detect stress TPL pattern), separate_str.py (determine whether string with symbols shall be separated into words e.g. this*is*great v.s. g*r*e*a*t, the former should be [this, is, great] but not the latter).   

- Detect_Silence is a function module that detects the repetition usage of dot, or other silence symbol. The output of this module will be added into calculating the final output of VQ tempo. 

- Detect_Emphasis is a function module that detects word/phrase repetition as well as exclamation and/or question mark repetition. 

- Detect_Spelling is a function module that detects words whose letters are connected by the same symbol e.g. s-l-o-w

- Detect_Rhythm is a function module that detects word-symbol alternations e.g. Best. Food. Ever

- Detect_Censorship is a function module that detects censorship  

- Detect_Asterisk_TPL is a whole folder that contains the detection of TPL elements that are characterized by the asterisk pattern, including VQ volume, VS differentiators, TK alphahaptics, VK alphakinesics, Artifact emoji symbol. 
Its main function is in Detect_Asterisk_TPL.py and one supporting function: check_asterisk.py (detect the asterisk pattern) 

- Detect_Emojicon_TPL is a whole folder that contains the detection of TPL elements that are emoji / emoticon based, including TK tactile emoji, tactile emoticon, VK bodily emoji, bodily emoticon, Artifact nonbodily emoji, nonbodily emoticon
Its main function is in Detect_Emojicon_TPL.py and two supporting functions: check_emoji.py (detect emoji pattern), and check_emoticon.py (detect emoticon pattern and has its own supporting function block_emoticon.py to set restriction on what detected emoticon to count) 

- Detect_Formatting is a function module that detects formatting 


