import time #line:1
from time import strftime #line:3
from time import gmtime #line:4
import pandas as pd #line:6
class cleverminer :#line:8
    version_string ="0.0.88"#line:10
    def __init__ (O00O00OO0OO0000O0 ,**O00OO0O0O0000OOO0 ):#line:12
        O00O00OO0OO0000O0 ._print_disclaimer ()#line:13
        O00O00OO0OO0000O0 .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:21
        O00O00OO0OO0000O0 ._init_data ()#line:22
        O00O00OO0OO0000O0 ._init_task ()#line:23
        if len (O00OO0O0O0000OOO0 )>0 :#line:24
            O00O00OO0OO0000O0 .kwargs =O00OO0O0O0000OOO0 #line:25
            O00O00OO0OO0000O0 ._calc_all (**O00OO0O0O0000OOO0 )#line:26
    def _init_data (O000O00O0OOO000O0 ):#line:28
        O000O00O0OOO000O0 .data ={}#line:30
        O000O00O0OOO000O0 .data ["varname"]=[]#line:31
        O000O00O0OOO000O0 .data ["catnames"]=[]#line:32
        O000O00O0OOO000O0 .data ["vtypes"]=[]#line:33
        O000O00O0OOO000O0 .data ["dm"]=[]#line:34
        O000O00O0OOO000O0 .data ["rows_count"]=int (0 )#line:35
        O000O00O0OOO000O0 .data ["data_prepared"]=0 #line:36
    def _init_task (OO00O00O0O0OOO0O0 ):#line:38
        OO00O00O0O0OOO0O0 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:47
        OO00O00O0O0OOO0O0 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:51
        OO00O00O0O0OOO0O0 .hypolist =[]#line:52
        OO00O00O0O0OOO0O0 .stats ['total_cnt']=0 #line:54
        OO00O00O0O0OOO0O0 .stats ['total_valid']=0 #line:55
        OO00O00O0O0OOO0O0 .stats ['control_number']=0 #line:56
        OO00O00O0O0OOO0O0 .result ={}#line:57
    def _get_ver (OO0O0O0OOOO00O0OO ):#line:59
        return OO0O0O0OOOO00O0OO .version_string #line:60
    def _print_disclaimer (OO0O0OO0O000000OO ):#line:62
        print ("***********************************************************************************************************************************************************************")#line:63
        print ("Cleverminer version ",OO0O0OO0O000000OO ._get_ver ())#line:64
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:65
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:66
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:67
        print ("This version is for personal and educational use only.")#line:68
        print ("***********************************************************************************************************************************************************************")#line:69
    def _prep_data (OOO00O000OOOO00OO ,O00OO000000O00000 ):#line:71
        print ("Starting data preparation ...")#line:72
        OOO00O000OOOO00OO ._init_data ()#line:73
        OOO00O000OOOO00OO .stats ['start_prep_time']=time .time ()#line:74
        OOO00O000OOOO00OO .data ["rows_count"]=O00OO000000O00000 .shape [0 ]#line:75
        for OOOOOOOOOO00O0O0O in O00OO000000O00000 .select_dtypes (exclude =['category']).columns :#line:76
            O00OO000000O00000 [OOOOOOOOOO00O0O0O ]=O00OO000000O00000 [OOOOOOOOOO00O0O0O ].apply (str )#line:77
        O0O0OOOO0O0OOOO00 =pd .DataFrame .from_records ([(OO0O00OOOO0O0OOOO ,O00OO000000O00000 [OO0O00OOOO0O0OOOO ].nunique ())for OO0O00OOOO0O0OOOO in O00OO000000O00000 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:79
        print ("Unique value counts are:")#line:80
        print (O0O0OOOO0O0OOOO00 )#line:81
        for OOOOOOOOOO00O0O0O in O00OO000000O00000 .columns :#line:82
            if O00OO000000O00000 [OOOOOOOOOO00O0O0O ].nunique ()<100 :#line:83
                O00OO000000O00000 [OOOOOOOOOO00O0O0O ]=O00OO000000O00000 [OOOOOOOOOO00O0O0O ].astype ('category')#line:84
            else :#line:85
                print (f"WARNING: attribute {OOOOOOOOOO00O0O0O} has more than 100 values, will be ignored.")#line:86
                del O00OO000000O00000 [OOOOOOOOOO00O0O0O ]#line:87
        print ("Encoding columns into bit-form...")#line:88
        OO0OO0OOOO0O00OOO =0 #line:89
        O00OO0O0O000000O0 =0 #line:90
        for OOO0000O0OOO0000O in O00OO000000O00000 :#line:91
            print ('Column: '+OOO0000O0OOO0000O )#line:93
            OOO00O000OOOO00OO .data ["varname"].append (OOO0000O0OOO0000O )#line:94
            O00OOO0O0OO0OOO0O =pd .get_dummies (O00OO000000O00000 [OOO0000O0OOO0000O ])#line:95
            OO00O00000O0000OO =0 #line:96
            if (O00OO000000O00000 .dtypes [OOO0000O0OOO0000O ].name =='category'):#line:97
                OO00O00000O0000OO =1 #line:98
            OOO00O000OOOO00OO .data ["vtypes"].append (OO00O00000O0000OO )#line:99
            O0OOO00000000OOO0 =0 #line:102
            OO00OO00O0OO0OOOO =[]#line:103
            O00000O0O000OOOOO =[]#line:104
            for O00O0OO000O00O00O in O00OOO0O0OO0OOO0O :#line:106
                print ('....category : '+str (O00O0OO000O00O00O )+" @ "+str (time .time ()))#line:108
                OO00OO00O0OO0OOOO .append (O00O0OO000O00O00O )#line:109
                O0OOOOO0O0OO0O00O =int (0 )#line:110
                OO00OO000OOO00000 =O00OOO0O0OO0OOO0O [O00O0OO000O00O00O ].values #line:111
                for O00O0OO0O0O0OO00O in range (OOO00O000OOOO00OO .data ["rows_count"]):#line:113
                    if OO00OO000OOO00000 [O00O0OO0O0O0OO00O ]>0 :#line:114
                        O0OOOOO0O0OO0O00O +=1 <<O00O0OO0O0O0OO00O #line:115
                O00000O0O000OOOOO .append (O0OOOOO0O0OO0O00O )#line:116
                O0OOO00000000OOO0 +=1 #line:126
                O00OO0O0O000000O0 +=1 #line:127
            OOO00O000OOOO00OO .data ["catnames"].append (OO00OO00O0OO0OOOO )#line:129
            OOO00O000OOOO00OO .data ["dm"].append (O00000O0O000OOOOO )#line:130
        print ("Encoding columns into bit-form...done")#line:132
        print ("Encoding columns into bit-form...done")#line:133
        print (f"List of attributes for analysis is: {OOO00O000OOOO00OO.data['varname']}")#line:134
        print (f"List of category names for individual attributes is : {OOO00O000OOOO00OO.data['catnames']}")#line:135
        print (f"List of vtypes is (all should be 1) : {OOO00O000OOOO00OO.data['vtypes']}")#line:136
        OOO00O000OOOO00OO .data ["data_prepared"]=1 #line:138
        print ("Data preparation finished ...")#line:139
        print ('Number of variables : '+str (len (OOO00O000OOOO00OO .data ["dm"])))#line:140
        print ('Total number of categories in all variables : '+str (O00OO0O0O000000O0 ))#line:141
        OOO00O000OOOO00OO .stats ['end_prep_time']=time .time ()#line:142
        print ('Time needed for data preparation : ',str (OOO00O000OOOO00OO .stats ['end_prep_time']-OOO00O000OOOO00OO .stats ['start_prep_time']))#line:143
    def bitcount (O0OOOO0OOO0OO0OO0 ,OO0OOO0O0OOO0OOO0 ):#line:146
        O00OOOOO000OO0O00 =0 #line:147
        while OO0OOO0O0OOO0OOO0 >0 :#line:148
            if (OO0OOO0O0OOO0OOO0 &1 ==1 ):O00OOOOO000OO0O00 +=1 #line:149
            OO0OOO0O0OOO0OOO0 >>=1 #line:150
        return O00OOOOO000OO0O00 #line:151
    def _verifyCF (O00O0OOOO000OOOO0 ,_O0O0OOO000OOO000O ):#line:154
        OOO00OO00O0OOOO00 =bin (_O0O0OOO000OOO000O ).count ("1")#line:155
        O0O000OOOOOO00000 =[]#line:156
        OOO0OO00O0O0OOO00 =[]#line:157
        O000O0O000000000O =0 #line:158
        O00O0O00OO0OOO00O =0 #line:159
        OOOO000000O0OO0OO =0 #line:160
        OOO0000OOO0O0OO0O =0 #line:161
        OO00O0O0OO0O0OO00 =0 #line:162
        OOO000O0OO0000O00 =0 #line:163
        OOO00OO0OO0OOOOO0 =0 #line:164
        O000000OOO000O000 =0 #line:165
        OOO00OO00O0OOO00O =0 #line:166
        O00OO0O00000OO0OO =O00O0OOOO000OOOO0 .data ["dm"][O00O0OOOO000OOOO0 .data ["varname"].index (O00O0OOOO000OOOO0 .kwargs .get ('target'))]#line:167
        for O000OO00000O0OO00 in range (len (O00OO0O00000OO0OO )):#line:168
            O00O0O00OO0OOO00O =O000O0O000000000O #line:169
            O000O0O000000000O =bin (_O0O0OOO000OOO000O &O00OO0O00000OO0OO [O000OO00000O0OO00 ]).count ("1")#line:170
            O0O000OOOOOO00000 .append (O000O0O000000000O )#line:171
            if O000OO00000O0OO00 >0 :#line:172
                if (O000O0O000000000O >O00O0O00OO0OOO00O ):#line:173
                    if (OOOO000000O0OO0OO ==1 ):#line:174
                        O000000OOO000O000 +=1 #line:175
                    else :#line:176
                        O000000OOO000O000 =1 #line:177
                    if O000000OOO000O000 >OOO0000OOO0O0OO0O :#line:178
                        OOO0000OOO0O0OO0O =O000000OOO000O000 #line:179
                    OOOO000000O0OO0OO =1 #line:180
                    OOO000O0OO0000O00 +=1 #line:181
                if (O000O0O000000000O <O00O0O00OO0OOO00O ):#line:182
                    if (OOOO000000O0OO0OO ==-1 ):#line:183
                        OOO00OO00O0OOO00O +=1 #line:184
                    else :#line:185
                        OOO00OO00O0OOO00O =1 #line:186
                    if OOO00OO00O0OOO00O >OO00O0O0OO0O0OO00 :#line:187
                        OO00O0O0OO0O0OO00 =OOO00OO00O0OOO00O #line:188
                    OOOO000000O0OO0OO =-1 #line:189
                    OOO00OO0OO0OOOOO0 +=1 #line:190
                if (O000O0O000000000O ==O00O0O00OO0OOO00O ):#line:191
                    OOOO000000O0OO0OO =0 #line:192
                    OOO00OO00O0OOO00O =0 #line:193
                    O000000OOO000O000 =0 #line:194
        OOOO0000OOO0O0000 =True #line:197
        for O0OO00OO0OO0OO00O in O00O0OOOO000OOOO0 .quantifiers .keys ():#line:198
            if O0OO00OO0OO0OO00O =='Base':#line:199
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=OOO00OO00O0OOOO00 )#line:200
            if O0OO00OO0OO0OO00O =='RelBase':#line:201
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=OOO00OO00O0OOOO00 *1.0 /O00O0OOOO000OOOO0 .data ["rows_count"])#line:202
            if O0OO00OO0OO0OO00O =='S_Up':#line:203
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=OOO0000OOO0O0OO0O )#line:204
            if O0OO00OO0OO0OO00O =='S_Down':#line:205
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=OO00O0O0OO0O0OO00 )#line:206
            if O0OO00OO0OO0OO00O =='S_Any_Up':#line:207
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=OOO0000OOO0O0OO0O )#line:208
            if O0OO00OO0OO0OO00O =='S_Any_Down':#line:209
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=OO00O0O0OO0O0OO00 )#line:210
            if O0OO00OO0OO0OO00O =='Max':#line:211
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=max (O0O000OOOOOO00000 ))#line:212
            if O0OO00OO0OO0OO00O =='Min':#line:213
                OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=min (O0O000OOOOOO00000 ))#line:214
            if O0OO00OO0OO0OO00O =='Relmax':#line:215
                if sum (O0O000OOOOOO00000 )>0 :#line:216
                    OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=max (O0O000OOOOOO00000 )*1.0 /sum (O0O000OOOOOO00000 ))#line:217
                else :#line:218
                    OOOO0000OOO0O0000 =False #line:219
            if O0OO00OO0OO0OO00O =='Relmin':#line:220
                if sum (O0O000OOOOOO00000 )>0 :#line:221
                    OOOO0000OOO0O0000 =OOOO0000OOO0O0000 and (O00O0OOOO000OOOO0 .quantifiers .get (O0OO00OO0OO0OO00O )<=min (O0O000OOOOOO00000 )*1.0 /sum (O0O000OOOOOO00000 ))#line:222
                else :#line:223
                    OOOO0000OOO0O0000 =False #line:224
        OO0OOOO000OOO0O0O ={}#line:225
        if OOOO0000OOO0O0000 ==True :#line:226
            O00O0OOOO000OOOO0 .stats ['total_valid']+=1 #line:228
            OO0OOOO000OOO0O0O ["base"]=OOO00OO00O0OOOO00 #line:229
            OO0OOOO000OOO0O0O ["rel_base"]=OOO00OO00O0OOOO00 *1.0 /O00O0OOOO000OOOO0 .data ["rows_count"]#line:230
            OO0OOOO000OOO0O0O ["s_up"]=OOO0000OOO0O0OO0O #line:231
            OO0OOOO000OOO0O0O ["s_down"]=OO00O0O0OO0O0OO00 #line:232
            OO0OOOO000OOO0O0O ["s_any_up"]=OOO000O0OO0000O00 #line:233
            OO0OOOO000OOO0O0O ["s_any_down"]=OOO00OO0OO0OOOOO0 #line:234
            OO0OOOO000OOO0O0O ["max"]=max (O0O000OOOOOO00000 )#line:235
            OO0OOOO000OOO0O0O ["min"]=min (O0O000OOOOOO00000 )#line:236
            OO0OOOO000OOO0O0O ["rel_max"]=max (O0O000OOOOOO00000 )*1.0 /O00O0OOOO000OOOO0 .data ["rows_count"]#line:237
            OO0OOOO000OOO0O0O ["rel_min"]=min (O0O000OOOOOO00000 )*1.0 /O00O0OOOO000OOOO0 .data ["rows_count"]#line:238
            OO0OOOO000OOO0O0O ["hist"]=O0O000OOOOOO00000 #line:239
        return OOOO0000OOO0O0000 ,OO0OOOO000OOO0O0O #line:241
    def _verify4ft (OO0OO0OO0O0OOOOOO ,_O0O0O0OO0O0O00OOO ):#line:243
        OOOOOOOOO0OOOO0OO ={}#line:244
        O00O00OO000O0OOOO =0 #line:245
        for OOOO000OO0O0OOOOO in OO0OO0OO0O0OOOOOO .task_actinfo ['cedents']:#line:246
            OOOOOOOOO0OOOO0OO [OOOO000OO0O0OOOOO ['cedent_type']]=OOOO000OO0O0OOOOO ['filter_value']#line:248
            O00O00OO000O0OOOO =O00O00OO000O0OOOO +1 #line:249
        O00O0000O0OOO000O =bin (OOOOOOOOO0OOOO0OO ['ante']&OOOOOOOOO0OOOO0OO ['succ']&OOOOOOOOO0OOOO0OO ['cond']).count ("1")#line:251
        O0O0O000O0O00O0O0 =None #line:252
        O0O0O000O0O00O0O0 =0 #line:253
        if O00O0000O0OOO000O >0 :#line:262
            O0O0O000O0O00O0O0 =bin (OOOOOOOOO0OOOO0OO ['ante']&OOOOOOOOO0OOOO0OO ['succ']&OOOOOOOOO0OOOO0OO ['cond']).count ("1")*1.0 /bin (OOOOOOOOO0OOOO0OO ['ante']&OOOOOOOOO0OOOO0OO ['cond']).count ("1")#line:263
        O00000O0O0OO0O00O =1 <<OO0OO0OO0O0OOOOOO .data ["rows_count"]#line:265
        OOO0OOOO0O0O000OO =bin (OOOOOOOOO0OOOO0OO ['ante']&OOOOOOOOO0OOOO0OO ['succ']&OOOOOOOOO0OOOO0OO ['cond']).count ("1")#line:266
        O0000O0OO000OOO0O =bin (OOOOOOOOO0OOOO0OO ['ante']&~(O00000O0O0OO0O00O |OOOOOOOOO0OOOO0OO ['succ'])&OOOOOOOOO0OOOO0OO ['cond']).count ("1")#line:267
        OOOO000OO0O0OOOOO =bin (~(O00000O0O0OO0O00O |OOOOOOOOO0OOOO0OO ['ante'])&OOOOOOOOO0OOOO0OO ['succ']&OOOOOOOOO0OOOO0OO ['cond']).count ("1")#line:268
        OO0OO0OO00000O000 =bin (~(O00000O0O0OO0O00O |OOOOOOOOO0OOOO0OO ['ante'])&~(O00000O0O0OO0O00O |OOOOOOOOO0OOOO0OO ['succ'])&OOOOOOOOO0OOOO0OO ['cond']).count ("1")#line:269
        OO00O0OOOO000OO0O =0 #line:270
        if (OOO0OOOO0O0O000OO +O0000O0OO000OOO0O )*(OOO0OOOO0O0O000OO +OOOO000OO0O0OOOOO )>0 :#line:271
            OO00O0OOOO000OO0O =OOO0OOOO0O0O000OO *(OOO0OOOO0O0O000OO +O0000O0OO000OOO0O +OOOO000OO0O0OOOOO +OO0OO0OO00000O000 )/(OOO0OOOO0O0O000OO +O0000O0OO000OOO0O )/(OOO0OOOO0O0O000OO +OOOO000OO0O0OOOOO )-1 #line:272
        else :#line:273
            OO00O0OOOO000OO0O =None #line:274
        OOOO0O00000O0OO0O =0 #line:275
        if (OOO0OOOO0O0O000OO +O0000O0OO000OOO0O )*(OOO0OOOO0O0O000OO +OOOO000OO0O0OOOOO )>0 :#line:276
            OOOO0O00000O0OO0O =1 -OOO0OOOO0O0O000OO *(OOO0OOOO0O0O000OO +O0000O0OO000OOO0O +OOOO000OO0O0OOOOO +OO0OO0OO00000O000 )/(OOO0OOOO0O0O000OO +O0000O0OO000OOO0O )/(OOO0OOOO0O0O000OO +OOOO000OO0O0OOOOO )#line:277
        else :#line:278
            OOOO0O00000O0OO0O =None #line:279
        O0OO0OO000O0000OO =True #line:280
        for OO0OOOOOOOOOOO000 in OO0OO0OO0O0OOOOOO .quantifiers .keys ():#line:281
            if OO0OOOOOOOOOOO000 =='Base':#line:282
                O0OO0OO000O0000OO =O0OO0OO000O0000OO and (OO0OO0OO0O0OOOOOO .quantifiers .get (OO0OOOOOOOOOOO000 )<=O00O0000O0OOO000O )#line:283
            if OO0OOOOOOOOOOO000 =='RelBase':#line:284
                O0OO0OO000O0000OO =O0OO0OO000O0000OO and (OO0OO0OO0O0OOOOOO .quantifiers .get (OO0OOOOOOOOOOO000 )<=O00O0000O0OOO000O *1.0 /OO0OO0OO0O0OOOOOO .data ["rows_count"])#line:285
            if OO0OOOOOOOOOOO000 =='pim':#line:286
                O0OO0OO000O0000OO =O0OO0OO000O0000OO and (OO0OO0OO0O0OOOOOO .quantifiers .get (OO0OOOOOOOOOOO000 )<=O0O0O000O0O00O0O0 )#line:287
            if OO0OOOOOOOOOOO000 =='aad':#line:288
                if OO00O0OOOO000OO0O !=None :#line:289
                    O0OO0OO000O0000OO =O0OO0OO000O0000OO and (OO0OO0OO0O0OOOOOO .quantifiers .get (OO0OOOOOOOOOOO000 )<=OO00O0OOOO000OO0O )#line:290
                else :#line:291
                    O0OO0OO000O0000OO =False #line:292
            if OO0OOOOOOOOOOO000 =='bad':#line:293
                if OOOO0O00000O0OO0O !=None :#line:294
                    O0OO0OO000O0000OO =O0OO0OO000O0000OO and (OO0OO0OO0O0OOOOOO .quantifiers .get (OO0OOOOOOOOOOO000 )<=OOOO0O00000O0OO0O )#line:295
                else :#line:296
                    O0OO0OO000O0000OO =False #line:297
            OOO00O0OOOO0OOOOO ={}#line:298
        if O0OO0OO000O0000OO ==True :#line:299
            OO0OO0OO0O0OOOOOO .stats ['total_valid']+=1 #line:301
            OOO00O0OOOO0OOOOO ["base"]=O00O0000O0OOO000O #line:302
            OOO00O0OOOO0OOOOO ["rel_base"]=O00O0000O0OOO000O *1.0 /OO0OO0OO0O0OOOOOO .data ["rows_count"]#line:303
            OOO00O0OOOO0OOOOO ["pim"]=O0O0O000O0O00O0O0 #line:304
            OOO00O0OOOO0OOOOO ["aad"]=OO00O0OOOO000OO0O #line:305
            OOO00O0OOOO0OOOOO ["bad"]=OOOO0O00000O0OO0O #line:306
            OOO00O0OOOO0OOOOO ["fourfold"]=[OOO0OOOO0O0O000OO ,O0000O0OO000OOO0O ,OOOO000OO0O0OOOOO ,OO0OO0OO00000O000 ]#line:307
        return O0OO0OO000O0000OO ,OOO00O0OOOO0OOOOO #line:311
    def _verifysd4ft (O0O000OOO00O000OO ,_O0OOO0O0OOOOO0O0O ):#line:313
        OOO0OO00OO0O00O00 ={}#line:314
        O00O0O00OO000O0OO =0 #line:315
        for OOOOOOO0O000OOOOO in O0O000OOO00O000OO .task_actinfo ['cedents']:#line:316
            OOO0OO00OO0O00O00 [OOOOOOO0O000OOOOO ['cedent_type']]=OOOOOOO0O000OOOOO ['filter_value']#line:318
            O00O0O00OO000O0OO =O00O0O00OO000O0OO +1 #line:319
        O0O0OOO00O0OO0OO0 =bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")#line:321
        OO00O00O00O00O000 =bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")#line:322
        OO0OOO0000OOOOO0O =None #line:323
        O00O0OO0OO0OOO00O =0 #line:324
        OO00OOO0O0O0OOO00 =0 #line:325
        if O0O0OOO00O0OO0OO0 >0 :#line:334
            O00O0OO0OO0OOO00O =bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")*1.0 /bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")#line:335
        if OO00O00O00O00O000 >0 :#line:336
            OO00OOO0O0O0OOO00 =bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")*1.0 /bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")#line:337
        OOOO0OOOO000OO000 =1 <<O0O000OOO00O000OO .data ["rows_count"]#line:339
        O0O00OO0O0OO0O000 =bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")#line:340
        O0O000O00O000O0O0 =bin (OOO0OO00OO0O00O00 ['ante']&~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['succ'])&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")#line:341
        O0O00O0O00OO0OOOO =bin (~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['ante'])&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")#line:342
        OOOO0O0O00OO00O0O =bin (~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['ante'])&~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['succ'])&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['frst']).count ("1")#line:343
        OOO0000OO0O0O0000 =bin (OOO0OO00OO0O00O00 ['ante']&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")#line:344
        OO0O0O00O0OO0O0O0 =bin (OOO0OO00OO0O00O00 ['ante']&~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['succ'])&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")#line:345
        OOO0O0O0OO0000OOO =bin (~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['ante'])&OOO0OO00OO0O00O00 ['succ']&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")#line:346
        OOO0OO0OO0OO0OO0O =bin (~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['ante'])&~(OOOO0OOOO000OO000 |OOO0OO00OO0O00O00 ['succ'])&OOO0OO00OO0O00O00 ['cond']&OOO0OO00OO0O00O00 ['scnd']).count ("1")#line:347
        OOO0OO0OO0OOO0OOO =True #line:348
        for OOO0000O0OO00OOOO in O0O000OOO00O000OO .quantifiers .keys ():#line:349
            if (OOO0000O0OO00OOOO =='FrstBase')|(OOO0000O0OO00OOOO =='Base1'):#line:350
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=O0O0OOO00O0OO0OO0 )#line:351
            if (OOO0000O0OO00OOOO =='ScndBase')|(OOO0000O0OO00OOOO =='Base2'):#line:352
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=OO00O00O00O00O000 )#line:353
            if (OOO0000O0OO00OOOO =='FrstRelBase')|(OOO0000O0OO00OOOO =='RelBase1'):#line:354
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=O0O0OOO00O0OO0OO0 *1.0 /O0O000OOO00O000OO .data ["rows_count"])#line:355
            if (OOO0000O0OO00OOOO =='ScndRelBase')|(OOO0000O0OO00OOOO =='RelBase2'):#line:356
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=OO00O00O00O00O000 *1.0 /O0O000OOO00O000OO .data ["rows_count"])#line:357
            if (OOO0000O0OO00OOOO =='Frstpim')|(OOO0000O0OO00OOOO =='pim1'):#line:358
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=O00O0OO0OO0OOO00O )#line:359
            if (OOO0000O0OO00OOOO =='Scndpim')|(OOO0000O0OO00OOOO =='pim2'):#line:360
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=OO00OOO0O0O0OOO00 )#line:361
            if OOO0000O0OO00OOOO =='Deltapim':#line:362
                OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=O00O0OO0OO0OOO00O -OO00OOO0O0O0OOO00 )#line:363
            if OOO0000O0OO00OOOO =='Ratiopim':#line:366
                if (OO00OOO0O0O0OOO00 >0 ):#line:367
                    OOO0OO0OO0OOO0OOO =OOO0OO0OO0OOO0OOO and (O0O000OOO00O000OO .quantifiers .get (OOO0000O0OO00OOOO )<=O00O0OO0OO0OOO00O *1.0 /OO00OOO0O0O0OOO00 )#line:368
                else :#line:369
                    OOO0OO0OO0OOO0OOO =False #line:370
        O0000O000OO00O000 ={}#line:371
        if OOO0OO0OO0OOO0OOO ==True :#line:372
            O0O000OOO00O000OO .stats ['total_valid']+=1 #line:374
            O0000O000OO00O000 ["base1"]=O0O0OOO00O0OO0OO0 #line:375
            O0000O000OO00O000 ["base2"]=OO00O00O00O00O000 #line:376
            O0000O000OO00O000 ["rel_base1"]=O0O0OOO00O0OO0OO0 *1.0 /O0O000OOO00O000OO .data ["rows_count"]#line:377
            O0000O000OO00O000 ["rel_base2"]=OO00O00O00O00O000 *1.0 /O0O000OOO00O000OO .data ["rows_count"]#line:378
            O0000O000OO00O000 ["pim1"]=O00O0OO0OO0OOO00O #line:379
            O0000O000OO00O000 ["pim2"]=OO00OOO0O0O0OOO00 #line:380
            O0000O000OO00O000 ["deltapim"]=O00O0OO0OO0OOO00O -OO00OOO0O0O0OOO00 #line:381
            if (OO00OOO0O0O0OOO00 >0 ):#line:382
                O0000O000OO00O000 ["ratiopim"]=O00O0OO0OO0OOO00O *1.0 /OO00OOO0O0O0OOO00 #line:383
            else :#line:384
                O0000O000OO00O000 ["ratiopim"]=None #line:385
            O0000O000OO00O000 ["fourfold1"]=[O0O00OO0O0OO0O000 ,O0O000O00O000O0O0 ,O0O00O0O00OO0OOOO ,OOOO0O0O00OO00O0O ]#line:386
            O0000O000OO00O000 ["fourfold2"]=[OOO0000OO0O0O0000 ,OO0O0O00O0OO0O0O0 ,OOO0O0O0OO0000OOO ,OOO0OO0OO0OO0OO0O ]#line:387
        if OOO0OO0OO0OOO0OOO :#line:389
            print (f"DEBUG : ii = {O00O0O00OO000O0OO}")#line:390
        return OOO0OO0OO0OOO0OOO ,O0000O000OO00O000 #line:391
    def _verifynewact4ft (OOOOOOO00O0OOOO0O ,_OOO0000O000OO000O ):#line:393
        OO00O0O000O000O00 ={}#line:394
        for O0OO0OO00000O0O00 in OOOOOOO00O0OOOO0O .task_actinfo ['cedents']:#line:395
            OO00O0O000O000O00 [O0OO0OO00000O0O00 ['cedent_type']]=O0OO0OO00000O0O00 ['filter_value']#line:397
        O0O0OOO000O000O00 =bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']).count ("1")#line:399
        O0OO0OO00OOO0OOO0 =bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']&OO00O0O000O000O00 ['antv']&OO00O0O000O000O00 ['sucv']).count ("1")#line:400
        OOO0OOOOO0O0OO000 =None #line:401
        OO0OO000O0OOO00O0 =0 #line:402
        O0O0OOOO0OO0OOO0O =0 #line:403
        if O0O0OOO000O000O00 >0 :#line:412
            OO0OO000O0OOO00O0 =bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']).count ("1")*1.0 /bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['cond']).count ("1")#line:414
        if O0OO0OO00OOO0OOO0 >0 :#line:415
            O0O0OOOO0OO0OOO0O =bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']&OO00O0O000O000O00 ['antv']&OO00O0O000O000O00 ['sucv']).count ("1")*1.0 /bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['cond']&OO00O0O000O000O00 ['antv']).count ("1")#line:417
        OO0OO000000OOOO0O =1 <<OOOOOOO00O0OOOO0O .rows_count #line:419
        OOO0O00000OO0000O =bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']).count ("1")#line:420
        OOOOOOOOO0O00O0O0 =bin (OO00O0O000O000O00 ['ante']&~(OO0OO000000OOOO0O |OO00O0O000O000O00 ['succ'])&OO00O0O000O000O00 ['cond']).count ("1")#line:421
        OO00OOOO00OOO00O0 =bin (~(OO0OO000000OOOO0O |OO00O0O000O000O00 ['ante'])&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']).count ("1")#line:422
        OO00OOO0O0000OOO0 =bin (~(OO0OO000000OOOO0O |OO00O0O000O000O00 ['ante'])&~(OO0OO000000OOOO0O |OO00O0O000O000O00 ['succ'])&OO00O0O000O000O00 ['cond']).count ("1")#line:423
        O0000OO0O0O000O0O =bin (OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']&OO00O0O000O000O00 ['antv']&OO00O0O000O000O00 ['sucv']).count ("1")#line:424
        OOOO0OOOO0OO0O000 =bin (OO00O0O000O000O00 ['ante']&~(OO0OO000000OOOO0O |(OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['sucv']))&OO00O0O000O000O00 ['cond']).count ("1")#line:425
        O0O0OO0000O0O0O00 =bin (~(OO0OO000000OOOO0O |(OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['antv']))&OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['cond']&OO00O0O000O000O00 ['sucv']).count ("1")#line:426
        O0OOOOO0OOOOOO00O =bin (~(OO0OO000000OOOO0O |(OO00O0O000O000O00 ['ante']&OO00O0O000O000O00 ['antv']))&~(OO0OO000000OOOO0O |(OO00O0O000O000O00 ['succ']&OO00O0O000O000O00 ['sucv']))&OO00O0O000O000O00 ['cond']).count ("1")#line:427
        OO000OO000O00O0OO =True #line:428
        for O0O0OOOOO0OO0000O in OOOOOOO00O0OOOO0O .quantifiers .keys ():#line:429
            if (O0O0OOOOO0OO0000O =='PreBase')|(O0O0OOOOO0OO0000O =='Base1'):#line:430
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=O0O0OOO000O000O00 )#line:431
            if (O0O0OOOOO0OO0000O =='PostBase')|(O0O0OOOOO0OO0000O =='Base2'):#line:432
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=O0OO0OO00OOO0OOO0 )#line:433
            if (O0O0OOOOO0OO0000O =='PreRelBase')|(O0O0OOOOO0OO0000O =='RelBase1'):#line:434
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=O0O0OOO000O000O00 *1.0 /OOOOOOO00O0OOOO0O .data ["rows_count"])#line:435
            if (O0O0OOOOO0OO0000O =='PostRelBase')|(O0O0OOOOO0OO0000O =='RelBase2'):#line:436
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=O0OO0OO00OOO0OOO0 *1.0 /OOOOOOO00O0OOOO0O .data ["rows_count"])#line:437
            if (O0O0OOOOO0OO0000O =='Prepim')|(O0O0OOOOO0OO0000O =='pim1'):#line:438
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=OO0OO000O0OOO00O0 )#line:439
            if (O0O0OOOOO0OO0000O =='Postpim')|(O0O0OOOOO0OO0000O =='pim2'):#line:440
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=O0O0OOOO0OO0OOO0O )#line:441
            if O0O0OOOOO0OO0000O =='Deltapim':#line:442
                OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=OO0OO000O0OOO00O0 -O0O0OOOO0OO0OOO0O )#line:443
            if O0O0OOOOO0OO0000O =='Ratiopim':#line:446
                if (O0O0OOOO0OO0OOO0O >0 ):#line:447
                    OO000OO000O00O0OO =OO000OO000O00O0OO and (OOOOOOO00O0OOOO0O .quantifiers .get (O0O0OOOOO0OO0000O )<=OO0OO000O0OOO00O0 *1.0 /O0O0OOOO0OO0OOO0O )#line:448
                else :#line:449
                    OO000OO000O00O0OO =False #line:450
        OO0OO0O0O0O00OOO0 ={}#line:451
        if OO000OO000O00O0OO ==True :#line:452
            OOOOOOO00O0OOOO0O .stats ['total_valid']+=1 #line:454
            OO0OO0O0O0O00OOO0 ["base1"]=O0O0OOO000O000O00 #line:455
            OO0OO0O0O0O00OOO0 ["base2"]=O0OO0OO00OOO0OOO0 #line:456
            OO0OO0O0O0O00OOO0 ["rel_base1"]=O0O0OOO000O000O00 *1.0 /OOOOOOO00O0OOOO0O .data ["rows_count"]#line:457
            OO0OO0O0O0O00OOO0 ["rel_base2"]=O0OO0OO00OOO0OOO0 *1.0 /OOOOOOO00O0OOOO0O .data ["rows_count"]#line:458
            OO0OO0O0O0O00OOO0 ["pim1"]=OO0OO000O0OOO00O0 #line:459
            OO0OO0O0O0O00OOO0 ["pim2"]=O0O0OOOO0OO0OOO0O #line:460
            OO0OO0O0O0O00OOO0 ["deltapim"]=OO0OO000O0OOO00O0 -O0O0OOOO0OO0OOO0O #line:461
            if (O0O0OOOO0OO0OOO0O >0 ):#line:462
                OO0OO0O0O0O00OOO0 ["ratiopim"]=OO0OO000O0OOO00O0 *1.0 /O0O0OOOO0OO0OOO0O #line:463
            else :#line:464
                OO0OO0O0O0O00OOO0 ["ratiopim"]=None #line:465
            OO0OO0O0O0O00OOO0 ["fourfoldpre"]=[OOO0O00000OO0000O ,OOOOOOOOO0O00O0O0 ,OO00OOOO00OOO00O0 ,OO00OOO0O0000OOO0 ]#line:466
            OO0OO0O0O0O00OOO0 ["fourfoldpost"]=[O0000OO0O0O000O0O ,OOOO0OOOO0OO0O000 ,O0O0OO0000O0O0O00 ,O0OOOOO0OOOOOO00O ]#line:467
        return OO000OO000O00O0OO ,OO0OO0O0O0O00OOO0 #line:469
    def _verifyact4ft (O0O0OOO0O00000O0O ,_OO0O0O000O0OO0O00 ):#line:471
        O00O00O000O00OO00 ={}#line:472
        for OOO0OOOOOO0OO00O0 in O0O0OOO0O00000O0O .task_actinfo ['cedents']:#line:473
            O00O00O000O00OO00 [OOO0OOOOOO0OO00O0 ['cedent_type']]=OOO0OOOOOO0OO00O0 ['filter_value']#line:475
        OO0OOO0O0O00O0O0O =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv-']&O00O00O000O00OO00 ['sucv-']).count ("1")#line:477
        OOOO00O00OOOO0OOO =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv+']&O00O00O000O00OO00 ['sucv+']).count ("1")#line:478
        O00O0O000OOO00000 =None #line:479
        O000OO000OOO0000O =0 #line:480
        OOO00OOOO0000OO0O =0 #line:481
        if OO0OOO0O0O00O0O0O >0 :#line:490
            O000OO000OOO0000O =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv-']&O00O00O000O00OO00 ['sucv-']).count ("1")*1.0 /bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv-']).count ("1")#line:492
        if OOOO00O00OOOO0OOO >0 :#line:493
            OOO00OOOO0000OO0O =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv+']&O00O00O000O00OO00 ['sucv+']).count ("1")*1.0 /bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv+']).count ("1")#line:495
        O00OO0OOO0OO0O0O0 =1 <<O0O0OOO0O00000O0O .data ["rows_count"]#line:497
        OOOO000O0OOOOOOOO =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv-']&O00O00O000O00OO00 ['sucv-']).count ("1")#line:498
        O000OO0OO0OO0OOOO =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['antv-']&~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['sucv-']))&O00O00O000O00OO00 ['cond']).count ("1")#line:499
        OOO00O0O00OOO0OOO =bin (~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['antv-']))&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['sucv-']).count ("1")#line:500
        OOO0O0OO00O0O000O =bin (~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['antv-']))&~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['sucv-']))&O00O00O000O00OO00 ['cond']).count ("1")#line:501
        OO00000O0OO0OO0O0 =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['antv+']&O00O00O000O00OO00 ['sucv+']).count ("1")#line:502
        OOOOO00OOO0OO0O00 =bin (O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['antv+']&~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['sucv+']))&O00O00O000O00OO00 ['cond']).count ("1")#line:503
        OO00000O00OO0000O =bin (~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['antv+']))&O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['cond']&O00O00O000O00OO00 ['sucv+']).count ("1")#line:504
        O000OOO0OOO000OOO =bin (~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['ante']&O00O00O000O00OO00 ['antv+']))&~(O00OO0OOO0OO0O0O0 |(O00O00O000O00OO00 ['succ']&O00O00O000O00OO00 ['sucv+']))&O00O00O000O00OO00 ['cond']).count ("1")#line:505
        O0000O0OO0O0O0000 =True #line:506
        for O0OOO0O00O0OOOOO0 in O0O0OOO0O00000O0O .quantifiers .keys ():#line:507
            if (O0OOO0O00O0OOOOO0 =='PreBase')|(O0OOO0O00O0OOOOO0 =='Base1'):#line:508
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=OO0OOO0O0O00O0O0O )#line:509
            if (O0OOO0O00O0OOOOO0 =='PostBase')|(O0OOO0O00O0OOOOO0 =='Base2'):#line:510
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=OOOO00O00OOOO0OOO )#line:511
            if (O0OOO0O00O0OOOOO0 =='PreRelBase')|(O0OOO0O00O0OOOOO0 =='RelBase1'):#line:512
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=OO0OOO0O0O00O0O0O *1.0 /O0O0OOO0O00000O0O .data ["rows_count"])#line:513
            if (O0OOO0O00O0OOOOO0 =='PostRelBase')|(O0OOO0O00O0OOOOO0 =='RelBase2'):#line:514
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=OOOO00O00OOOO0OOO *1.0 /O0O0OOO0O00000O0O .data ["rows_count"])#line:515
            if (O0OOO0O00O0OOOOO0 =='Prepim')|(O0OOO0O00O0OOOOO0 =='pim1'):#line:516
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=O000OO000OOO0000O )#line:517
            if (O0OOO0O00O0OOOOO0 =='Postpim')|(O0OOO0O00O0OOOOO0 =='pim2'):#line:518
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=OOO00OOOO0000OO0O )#line:519
            if O0OOO0O00O0OOOOO0 =='Deltapim':#line:520
                O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=O000OO000OOO0000O -OOO00OOOO0000OO0O )#line:521
            if O0OOO0O00O0OOOOO0 =='Ratiopim':#line:524
                if (O000OO000OOO0000O >0 ):#line:525
                    O0000O0OO0O0O0000 =O0000O0OO0O0O0000 and (O0O0OOO0O00000O0O .quantifiers .get (O0OOO0O00O0OOOOO0 )<=OOO00OOOO0000OO0O *1.0 /O000OO000OOO0000O )#line:526
                else :#line:527
                    O0000O0OO0O0O0000 =False #line:528
        OO0OOOOO0OO00OO00 ={}#line:529
        if O0000O0OO0O0O0000 ==True :#line:530
            O0O0OOO0O00000O0O .stats ['total_valid']+=1 #line:532
            OO0OOOOO0OO00OO00 ["base1"]=OO0OOO0O0O00O0O0O #line:533
            OO0OOOOO0OO00OO00 ["base2"]=OOOO00O00OOOO0OOO #line:534
            OO0OOOOO0OO00OO00 ["rel_base1"]=OO0OOO0O0O00O0O0O *1.0 /O0O0OOO0O00000O0O .data ["rows_count"]#line:535
            OO0OOOOO0OO00OO00 ["rel_base2"]=OOOO00O00OOOO0OOO *1.0 /O0O0OOO0O00000O0O .data ["rows_count"]#line:536
            OO0OOOOO0OO00OO00 ["pim1"]=O000OO000OOO0000O #line:537
            OO0OOOOO0OO00OO00 ["pim2"]=OOO00OOOO0000OO0O #line:538
            OO0OOOOO0OO00OO00 ["deltapim"]=O000OO000OOO0000O -OOO00OOOO0000OO0O #line:539
            if (O000OO000OOO0000O >0 ):#line:540
                OO0OOOOO0OO00OO00 ["ratiopim"]=OOO00OOOO0000OO0O *1.0 /O000OO000OOO0000O #line:541
            else :#line:542
                OO0OOOOO0OO00OO00 ["ratiopim"]=None #line:543
            OO0OOOOO0OO00OO00 ["fourfoldpre"]=[OOOO000O0OOOOOOOO ,O000OO0OO0OO0OOOO ,OOO00O0O00OOO0OOO ,OOO0O0OO00O0O000O ]#line:544
            OO0OOOOO0OO00OO00 ["fourfoldpost"]=[OO00000O0OO0OO0O0 ,OOOOO00OOO0OO0O00 ,OO00000O00OO0000O ,O000OOO0OOO000OOO ]#line:545
        return O0000O0OO0O0O0000 ,OO0OOOOO0OO00OO00 #line:547
    def _verify_opt (O0OOOOOO0OO0OO00O ,OO00O000O0OO0O00O ,OO0OO0O0OO0000OO0 ):#line:549
        O00O0000OO000000O =False #line:550
        if not (OO00O000O0OO0O00O ['optim'].get ('only_con')):#line:553
            return False #line:554
        O0O00O000O0OOO000 ={}#line:555
        for OOO000OO00OOOOO0O in O0OOOOOO0OO0OO00O .task_actinfo ['cedents']:#line:556
            O0O00O000O0OOO000 [OOO000OO00OOOOO0O ['cedent_type']]=OOO000OO00OOOOO0O ['filter_value']#line:558
        OO00O0OOO0OO00O00 =1 <<O0OOOOOO0OO0OO00O .data ["rows_count"]#line:560
        O0000O00O0000O0OO =OO00O0OOO0OO00O00 -1 #line:561
        OO0OOOO0O000O00OO =""#line:562
        O00OO000O00OO0O0O =0 #line:563
        if (O0O00O000O0OOO000 .get ('ante')!=None ):#line:564
            O0000O00O0000O0OO =O0000O00O0000O0OO &O0O00O000O0OOO000 ['ante']#line:565
        if (O0O00O000O0OOO000 .get ('succ')!=None ):#line:566
            O0000O00O0000O0OO =O0000O00O0000O0OO &O0O00O000O0OOO000 ['succ']#line:567
        if (O0O00O000O0OOO000 .get ('cond')!=None ):#line:568
            O0000O00O0000O0OO =O0000O00O0000O0OO &O0O00O000O0OOO000 ['cond']#line:569
        OOOOO0O00O0O00O00 =None #line:572
        if (O0OOOOOO0OO0OO00O .proc =='CFMiner')|(O0OOOOOO0OO0OO00O .proc =='4ftMiner'):#line:597
            O00000O000O000000 =bin (O0000O00O0000O0OO ).count ("1")#line:598
            for OOOO000OOO0O0O00O in O0OOOOOO0OO0OO00O .quantifiers .keys ():#line:599
                if OOOO000OOO0O0O00O =='Base':#line:600
                    if not (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 ):#line:601
                        O00O0000OO000000O =True #line:602
                if OOOO000OOO0O0O00O =='RelBase':#line:604
                    if not (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 *1.0 /O0OOOOOO0OO0OO00O .data ["rows_count"]):#line:605
                        O00O0000OO000000O =True #line:606
        return O00O0000OO000000O #line:609
        if O0OOOOOO0OO0OO00O .proc =='CFMiner':#line:612
            if (OO0OO0O0OO0000OO0 ['cedent_type']=='cond')&(OO0OO0O0OO0000OO0 ['defi'].get ('type')=='con'):#line:613
                O00000O000O000000 =bin (O0O00O000O0OOO000 ['cond']).count ("1")#line:614
                O00O0OO0OO0OOO0OO =True #line:615
                for OOOO000OOO0O0O00O in O0OOOOOO0OO0OO00O .quantifiers .keys ():#line:616
                    if OOOO000OOO0O0O00O =='Base':#line:617
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 )#line:618
                        if not (O00O0OO0OO0OOO0OO ):#line:619
                            print (f"...optimization : base is {O00000O000O000000} for {OO0OO0O0OO0000OO0['generated_string']}")#line:620
                    if OOOO000OOO0O0O00O =='RelBase':#line:621
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 *1.0 /O0OOOOOO0OO0OO00O .data ["rows_count"])#line:622
                        if not (O00O0OO0OO0OOO0OO ):#line:623
                            print (f"...optimization : base is {O00000O000O000000} for {OO0OO0O0OO0000OO0['generated_string']}")#line:624
                O00O0000OO000000O =not (O00O0OO0OO0OOO0OO )#line:625
        elif O0OOOOOO0OO0OO00O .proc =='4ftMiner':#line:626
            if (OO0OO0O0OO0000OO0 ['cedent_type']=='cond')&(OO0OO0O0OO0000OO0 ['defi'].get ('type')=='con'):#line:627
                O00000O000O000000 =bin (O0O00O000O0OOO000 ['cond']).count ("1")#line:628
                O00O0OO0OO0OOO0OO =True #line:629
                for OOOO000OOO0O0O00O in O0OOOOOO0OO0OO00O .quantifiers .keys ():#line:630
                    if OOOO000OOO0O0O00O =='Base':#line:631
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 )#line:632
                        if not (O00O0OO0OO0OOO0OO ):#line:633
                            print (f"...optimization : base is {O00000O000O000000} for {OO0OO0O0OO0000OO0['generated_string']}")#line:634
                    if OOOO000OOO0O0O00O =='RelBase':#line:635
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 *1.0 /O0OOOOOO0OO0OO00O .data ["rows_count"])#line:636
                        if not (O00O0OO0OO0OOO0OO ):#line:637
                            print (f"...optimization : base is {O00000O000O000000} for {OO0OO0O0OO0000OO0['generated_string']}")#line:638
                O00O0000OO000000O =not (O00O0OO0OO0OOO0OO )#line:639
            if (OO0OO0O0OO0000OO0 ['cedent_type']=='ante')&(OO0OO0O0OO0000OO0 ['defi'].get ('type')=='con'):#line:640
                O00000O000O000000 =bin (O0O00O000O0OOO000 ['ante']&O0O00O000O0OOO000 ['cond']).count ("1")#line:641
                O00O0OO0OO0OOO0OO =True #line:642
                for OOOO000OOO0O0O00O in O0OOOOOO0OO0OO00O .quantifiers .keys ():#line:643
                    if OOOO000OOO0O0O00O =='Base':#line:644
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 )#line:645
                        if not (O00O0OO0OO0OOO0OO ):#line:646
                            print (f"...optimization : ANTE: base is {O00000O000O000000} for {OO0OO0O0OO0000OO0['generated_string']}")#line:647
                    if OOOO000OOO0O0O00O =='RelBase':#line:648
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O00000O000O000000 *1.0 /O0OOOOOO0OO0OO00O .data ["rows_count"])#line:649
                        if not (O00O0OO0OO0OOO0OO ):#line:650
                            print (f"...optimization : ANTE:  base is {O00000O000O000000} for {OO0OO0O0OO0000OO0['generated_string']}")#line:651
                O00O0000OO000000O =not (O00O0OO0OO0OOO0OO )#line:652
            if (OO0OO0O0OO0000OO0 ['cedent_type']=='succ')&(OO0OO0O0OO0000OO0 ['defi'].get ('type')=='con'):#line:653
                O00000O000O000000 =bin (O0O00O000O0OOO000 ['ante']&O0O00O000O0OOO000 ['cond']&O0O00O000O0OOO000 ['succ']).count ("1")#line:654
                OOOOO0O00O0O00O00 =0 #line:655
                if O00000O000O000000 >0 :#line:656
                    OOOOO0O00O0O00O00 =bin (O0O00O000O0OOO000 ['ante']&O0O00O000O0OOO000 ['succ']&O0O00O000O0OOO000 ['cond']).count ("1")*1.0 /bin (O0O00O000O0OOO000 ['ante']&O0O00O000O0OOO000 ['cond']).count ("1")#line:657
                OO00O0OOO0OO00O00 =1 <<O0OOOOOO0OO0OO00O .data ["rows_count"]#line:658
                O0O0OO0OOOOO000OO =bin (O0O00O000O0OOO000 ['ante']&O0O00O000O0OOO000 ['succ']&O0O00O000O0OOO000 ['cond']).count ("1")#line:659
                O000OOO000O0OOOOO =bin (O0O00O000O0OOO000 ['ante']&~(OO00O0OOO0OO00O00 |O0O00O000O0OOO000 ['succ'])&O0O00O000O0OOO000 ['cond']).count ("1")#line:660
                OOO000OO00OOOOO0O =bin (~(OO00O0OOO0OO00O00 |O0O00O000O0OOO000 ['ante'])&O0O00O000O0OOO000 ['succ']&O0O00O000O0OOO000 ['cond']).count ("1")#line:661
                O0O0OO00OOOO0OO0O =bin (~(OO00O0OOO0OO00O00 |O0O00O000O0OOO000 ['ante'])&~(OO00O0OOO0OO00O00 |O0O00O000O0OOO000 ['succ'])&O0O00O000O0OOO000 ['cond']).count ("1")#line:662
                O00O0OO0OO0OOO0OO =True #line:663
                for OOOO000OOO0O0O00O in O0OOOOOO0OO0OO00O .quantifiers .keys ():#line:664
                    if OOOO000OOO0O0O00O =='pim':#line:665
                        O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=OOOOO0O00O0O00O00 )#line:666
                    if not (O00O0OO0OO0OOO0OO ):#line:667
                        print (f"...optimization : SUCC:  pim is {OOOOO0O00O0O00O00} for {OO0OO0O0OO0000OO0['generated_string']}")#line:668
                    if OOOO000OOO0O0O00O =='aad':#line:670
                        if (O0O0OO0OOOOO000OO +O000OOO000O0OOOOO )*(O0O0OO0OOOOO000OO +OOO000OO00OOOOO0O )>0 :#line:671
                            O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=O0O0OO0OOOOO000OO *(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO +OOO000OO00OOOOO0O +O0O0OO00OOOO0OO0O )/(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO )/(O0O0OO0OOOOO000OO +OOO000OO00OOOOO0O )-1 )#line:672
                        else :#line:673
                            O00O0OO0OO0OOO0OO =False #line:674
                        if not (O00O0OO0OO0OOO0OO ):#line:675
                            OO0OOO0OO00OO0OO0 =O0O0OO0OOOOO000OO *(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO +OOO000OO00OOOOO0O +O0O0OO00OOOO0OO0O )/(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO )/(O0O0OO0OOOOO000OO +OOO000OO00OOOOO0O )-1 #line:676
                            print (f"...optimization : SUCC:  aad is {OO0OOO0OO00OO0OO0} for {OO0OO0O0OO0000OO0['generated_string']}")#line:677
                    if OOOO000OOO0O0O00O =='bad':#line:678
                        if (O0O0OO0OOOOO000OO +O000OOO000O0OOOOO )*(O0O0OO0OOOOO000OO +OOO000OO00OOOOO0O )>0 :#line:679
                            O00O0OO0OO0OOO0OO =O00O0OO0OO0OOO0OO and (O0OOOOOO0OO0OO00O .quantifiers .get (OOOO000OOO0O0O00O )<=1 -O0O0OO0OOOOO000OO *(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO +OOO000OO00OOOOO0O +O0O0OO00OOOO0OO0O )/(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO )/(O0O0OO0OOOOO000OO +OOO000OO00OOOOO0O ))#line:680
                        else :#line:681
                            O00O0OO0OO0OOO0OO =False #line:682
                        if not (O00O0OO0OO0OOO0OO ):#line:683
                            O0OO0OOOOO00OO00O =1 -O0O0OO0OOOOO000OO *(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO +OOO000OO00OOOOO0O +O0O0OO00OOOO0OO0O )/(O0O0OO0OOOOO000OO +O000OOO000O0OOOOO )/(O0O0OO0OOOOO000OO +OOO000OO00OOOOO0O )#line:684
                            print (f"...optimization : SUCC:  bad is {O0OO0OOOOO00OO00O} for {OO0OO0O0OO0000OO0['generated_string']}")#line:685
                O00O0000OO000000O =not (O00O0OO0OO0OOO0OO )#line:686
        if (O00O0000OO000000O ):#line:687
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {OO0OO0O0OO0000OO0['cedent_type']}")#line:688
        return O00O0000OO000000O #line:689
    def _print (O0OO0000000O00O00 ,OOO0O0O0000O0O0OO ,_OO0OOOOOO00O0O0O0 ,_OO0OOOOOO0O0O0OOO ):#line:692
        if (len (_OO0OOOOOO00O0O0O0 ))!=len (_OO0OOOOOO0O0O0OOO ):#line:693
            print ("DIFF IN LEN for following cedent : "+str (len (_OO0OOOOOO00O0O0O0 ))+" vs "+str (len (_OO0OOOOOO0O0O0OOO )))#line:694
            print ("trace cedent : "+str (_OO0OOOOOO00O0O0O0 )+", traces "+str (_OO0OOOOOO0O0O0OOO ))#line:695
        O00O00000000O00OO =''#line:696
        for O0O0OOOO000OO0OO0 in range (len (_OO0OOOOOO00O0O0O0 )):#line:697
            OO000O00O0O0OO0OO =O0OO0000000O00O00 .data ["varname"].index (OOO0O0O0000O0O0OO ['defi'].get ('attributes')[_OO0OOOOOO00O0O0O0 [O0O0OOOO000OO0OO0 ]].get ('name'))#line:698
            O00O00000000O00OO =O00O00000000O00OO +O0OO0000000O00O00 .data ["varname"][OO000O00O0O0OO0OO ]+'('#line:700
            for O0OO0000O0O0000O0 in _OO0OOOOOO0O0O0OOO [O0O0OOOO000OO0OO0 ]:#line:701
                O00O00000000O00OO =O00O00000000O00OO +O0OO0000000O00O00 .data ["catnames"][OO000O00O0O0OO0OO ][O0OO0000O0O0000O0 ]+" "#line:702
            O00O00000000O00OO =O00O00000000O00OO +')'#line:703
            if O0O0OOOO000OO0OO0 +1 <len (_OO0OOOOOO00O0O0O0 ):#line:704
                O00O00000000O00OO =O00O00000000O00OO +' & '#line:705
        return O00O00000000O00OO #line:709
    def _print_hypo (OOOOO0O0O00OO00OO ,O000O0O00O0OOOO00 ):#line:711
        print ('Hypothesis info : '+str (O000O0O00O0OOOO00 ['params']))#line:712
        for O000O000O0OOOO00O in OOOOO0O0O00OO00OO .task_actinfo ['cedents']:#line:713
            print (O000O000O0OOOO00O ['cedent_type']+' = '+O000O000O0OOOO00O ['generated_string'])#line:714
    def _genvar (OO0OOO0OO0O0O0OOO ,OOOOOOOO0O0OOO0OO ,O00OO0000O0O0O00O ,_OOO0OO000O0O000O0 ,_O00OOOO0OOOO0OO00 ,_OO0OOOO0O0OO0000O ,_OO00OO0O0O00O0OOO ,_OO0OOOO00OO0O000O ):#line:716
        for OOOOO0O0O0OOO0OO0 in range (O00OO0000O0O0O00O ['num_cedent']):#line:717
            if len (_OOO0OO000O0O000O0 )==0 or OOOOO0O0O0OOO0OO0 >_OOO0OO000O0O000O0 [-1 ]:#line:718
                _OOO0OO000O0O000O0 .append (OOOOO0O0O0OOO0OO0 )#line:719
                OOOO0OOOO0000OO0O =OO0OOO0OO0O0O0OOO .data ["varname"].index (O00OO0000O0O0O00O ['defi'].get ('attributes')[OOOOO0O0O0OOO0OO0 ].get ('name'))#line:720
                _O0OO0OO0OO00000OO =O00OO0000O0O0O00O ['defi'].get ('attributes')[OOOOO0O0O0OOO0OO0 ].get ('minlen')#line:721
                _O0OO0O0OO00O000OO =O00OO0000O0O0O00O ['defi'].get ('attributes')[OOOOO0O0O0OOO0OO0 ].get ('maxlen')#line:722
                _OO0OOOO0000O0O0O0 =O00OO0000O0O0O00O ['defi'].get ('attributes')[OOOOO0O0O0OOO0OO0 ].get ('type')#line:723
                O0O00OOO000000OO0 =len (OO0OOO0OO0O0O0OOO .data ["dm"][OOOO0OOOO0000OO0O ])#line:724
                _O0O000OO00O0OO0OO =[]#line:725
                _O00OOOO0OOOO0OO00 .append (_O0O000OO00O0OO0OO )#line:726
                _OOOOOOOOO0O0000OO =int (0 )#line:727
                OO0OOO0OO0O0O0OOO ._gencomb (OOOOOOOO0O0OOO0OO ,O00OO0000O0O0O00O ,_OOO0OO000O0O000O0 ,_O00OOOO0OOOO0OO00 ,_O0O000OO00O0OO0OO ,_OO0OOOO0O0OO0000O ,_OOOOOOOOO0O0000OO ,O0O00OOO000000OO0 ,_OO0OOOO0000O0O0O0 ,_OO00OO0O0O00O0OOO ,_OO0OOOO00OO0O000O ,_O0OO0OO0OO00000OO ,_O0OO0O0OO00O000OO )#line:728
                _O00OOOO0OOOO0OO00 .pop ()#line:729
                _OOO0OO000O0O000O0 .pop ()#line:730
    def _gencomb (OOOOOO0OO0O0OOO00 ,O0O000O0O0O000O0O ,OO000O0OOOOO000O0 ,_O00OO0O000O000000 ,_O00O00000OOOO0O00 ,_O0OO0000O0O0O00OO ,_OOO0OOO00O0000000 ,_OO00O000OO0000O0O ,O000000OOOOOOO00O ,_O00000O0OO000OOO0 ,_OOO0O00O000OO00OO ,_OOOO00OOO0O000OO0 ,_OO0O000000O00O000 ,_OO0OOOO0O0OOOO000 ):#line:732
        _O00OO000O000O00O0 =[]#line:733
        if _O00000O0OO000OOO0 =="subset":#line:734
            if len (_O0OO0000O0O0O00OO )==0 :#line:735
                _O00OO000O000O00O0 =range (O000000OOOOOOO00O )#line:736
            else :#line:737
                _O00OO000O000O00O0 =range (_O0OO0000O0O0O00OO [-1 ]+1 ,O000000OOOOOOO00O )#line:738
        elif _O00000O0OO000OOO0 =="seq":#line:739
            if len (_O0OO0000O0O0O00OO )==0 :#line:740
                _O00OO000O000O00O0 =range (O000000OOOOOOO00O -_OO0O000000O00O000 +1 )#line:741
            else :#line:742
                if _O0OO0000O0O0O00OO [-1 ]+1 ==O000000OOOOOOO00O :#line:743
                    return #line:744
                O0O000O0O0O0O0000 =_O0OO0000O0O0O00OO [-1 ]+1 #line:745
                _O00OO000O000O00O0 .append (O0O000O0O0O0O0000 )#line:746
        elif _O00000O0OO000OOO0 =="lcut":#line:747
            if len (_O0OO0000O0O0O00OO )==0 :#line:748
                O0O000O0O0O0O0000 =0 ;#line:749
            else :#line:750
                if _O0OO0000O0O0O00OO [-1 ]+1 ==O000000OOOOOOO00O :#line:751
                    return #line:752
                O0O000O0O0O0O0000 =_O0OO0000O0O0O00OO [-1 ]+1 #line:753
            _O00OO000O000O00O0 .append (O0O000O0O0O0O0000 )#line:754
        elif _O00000O0OO000OOO0 =="rcut":#line:755
            if len (_O0OO0000O0O0O00OO )==0 :#line:756
                O0O000O0O0O0O0000 =O000000OOOOOOO00O -1 ;#line:757
            else :#line:758
                if _O0OO0000O0O0O00OO [-1 ]==0 :#line:759
                    return #line:760
                O0O000O0O0O0O0000 =_O0OO0000O0O0O00OO [-1 ]-1 #line:761
            _O00OO000O000O00O0 .append (O0O000O0O0O0O0000 )#line:763
        elif _O00000O0OO000OOO0 =="one":#line:764
            if len (_O0OO0000O0O0O00OO )==0 :#line:765
                O0O0000OOO0OO0O00 =OOOOOO0OO0O0OOO00 .data ["varname"].index (OO000O0OOOOO000O0 ['defi'].get ('attributes')[_O00OO0O000O000000 [-1 ]].get ('name'))#line:766
                try :#line:767
                    O0O000O0O0O0O0000 =OOOOOO0OO0O0OOO00 .data ["catnames"][O0O0000OOO0OO0O00 ].index (OO000O0OOOOO000O0 ['defi'].get ('attributes')[_O00OO0O000O000000 [-1 ]].get ('value'))#line:768
                except :#line:769
                    print (f"ERROR: attribute '{OO000O0OOOOO000O0['defi'].get('attributes')[_O00OO0O000O000000[-1]].get('name')}' has not value '{OO000O0OOOOO000O0['defi'].get('attributes')[_O00OO0O000O000000[-1]].get('value')}'")#line:770
                    exit (1 )#line:771
                _O00OO000O000O00O0 .append (O0O000O0O0O0O0000 )#line:772
                _OO0O000000O00O000 =1 #line:773
                _OO0OOOO0O0OOOO000 =1 #line:774
            else :#line:775
                print ("DEBUG: one category should not have more categories")#line:776
                return #line:777
        else :#line:778
            print ("Attribute type "+_O00000O0OO000OOO0 +" not supported.")#line:779
            return #line:780
        for OOO0O0OO0O0O000OO in _O00OO000O000O00O0 :#line:783
                _O0OO0000O0O0O00OO .append (OOO0O0OO0O0O000OO )#line:785
                _O00O00000OOOO0O00 .pop ()#line:786
                _O00O00000OOOO0O00 .append (_O0OO0000O0O0O00OO )#line:787
                _OOO0O00000O0OOO00 =_OO00O000OO0000O0O |OOOOOO0OO0O0OOO00 .data ["dm"][OOOOOO0OO0O0OOO00 .data ["varname"].index (OO000O0OOOOO000O0 ['defi'].get ('attributes')[_O00OO0O000O000000 [-1 ]].get ('name'))][OOO0O0OO0O0O000OO ]#line:791
                _O0OOOO00O00O0OOOO =1 #line:793
                if (len (_O00OO0O000O000000 )<_OOO0O00O000OO00OO ):#line:794
                    _O0OOOO00O00O0OOOO =-1 #line:795
                if (len (_O00O00000OOOO0O00 [-1 ])<_OO0O000000O00O000 ):#line:797
                    _O0OOOO00O00O0OOOO =0 #line:798
                _OO0OO0O0OO00000O0 =0 #line:800
                if OO000O0OOOOO000O0 ['defi'].get ('type')=='con':#line:801
                    _OO0OO0O0OO00000O0 =_OOO0OOO00O0000000 &_OOO0O00000O0OOO00 #line:802
                else :#line:803
                    _OO0OO0O0OO00000O0 =_OOO0OOO00O0000000 |_OOO0O00000O0OOO00 #line:804
                OO000O0OOOOO000O0 ['trace_cedent']=_O00OO0O000O000000 #line:805
                OO000O0OOOOO000O0 ['traces']=_O00O00000OOOO0O00 #line:806
                OO000O0OOOOO000O0 ['generated_string']=OOOOOO0OO0O0OOO00 ._print (OO000O0OOOOO000O0 ,_O00OO0O000O000000 ,_O00O00000OOOO0O00 )#line:807
                OO000O0OOOOO000O0 ['filter_value']=_OO0OO0O0OO00000O0 #line:808
                O0O000O0O0O000O0O ['cedents'].append (OO000O0OOOOO000O0 )#line:809
                O00OO0O0O0OOOO000 =OOOOOO0OO0O0OOO00 ._verify_opt (O0O000O0O0O000O0O ,OO000O0OOOOO000O0 )#line:810
                if not (O00OO0O0O0OOOO000 ):#line:816
                    if _O0OOOO00O00O0OOOO ==1 :#line:817
                        if len (O0O000O0O0O000O0O ['cedents_to_do'])==len (O0O000O0O0O000O0O ['cedents']):#line:819
                            if OOOOOO0OO0O0OOO00 .proc =='CFMiner':#line:820
                                O00OOO0OOOO00OOOO ,OOO0000OO00000O0O =OOOOOO0OO0O0OOO00 ._verifyCF (_OO0OO0O0OO00000O0 )#line:821
                            elif OOOOOO0OO0O0OOO00 .proc =='4ftMiner':#line:822
                                O00OOO0OOOO00OOOO ,OOO0000OO00000O0O =OOOOOO0OO0O0OOO00 ._verify4ft (_OOO0O00000O0OOO00 )#line:823
                            elif OOOOOO0OO0O0OOO00 .proc =='SD4ftMiner':#line:824
                                O00OOO0OOOO00OOOO ,OOO0000OO00000O0O =OOOOOO0OO0O0OOO00 ._verifysd4ft (_OOO0O00000O0OOO00 )#line:825
                            elif OOOOOO0OO0O0OOO00 .proc =='NewAct4ftMiner':#line:826
                                O00OOO0OOOO00OOOO ,OOO0000OO00000O0O =OOOOOO0OO0O0OOO00 ._verifynewact4ft (_OOO0O00000O0OOO00 )#line:827
                            elif OOOOOO0OO0O0OOO00 .proc =='Act4ftMiner':#line:828
                                O00OOO0OOOO00OOOO ,OOO0000OO00000O0O =OOOOOO0OO0O0OOO00 ._verifyact4ft (_OOO0O00000O0OOO00 )#line:829
                            else :#line:830
                                print ("Unsupported procedure : "+OOOOOO0OO0O0OOO00 .proc )#line:831
                                exit (0 )#line:832
                            if O00OOO0OOOO00OOOO ==True :#line:833
                                O00OOO00OO000O0O0 ={}#line:834
                                O00OOO00OO000O0O0 ["hypo_id"]=OOOOOO0OO0O0OOO00 .stats ['total_valid']#line:835
                                O00OOO00OO000O0O0 ["cedents"]={}#line:836
                                for O0OO0OO0O0OOOO00O in O0O000O0O0O000O0O ['cedents']:#line:837
                                    O00OOO00OO000O0O0 ['cedents'][O0OO0OO0O0OOOO00O ['cedent_type']]=O0OO0OO0O0OOOO00O ['generated_string']#line:838
                                O00OOO00OO000O0O0 ["params"]=OOO0000OO00000O0O #line:840
                                O00OOO00OO000O0O0 ["trace_cedent"]=_O00OO0O000O000000 #line:841
                                OOOOOO0OO0O0OOO00 ._print_hypo (O00OOO00OO000O0O0 )#line:842
                                O00OOO00OO000O0O0 ["traces"]=_O00O00000OOOO0O00 #line:845
                                OOOOOO0OO0O0OOO00 .hypolist .append (O00OOO00OO000O0O0 )#line:846
                            OOOOOO0OO0O0OOO00 .stats ['total_cnt']+=1 #line:847
                    if _O0OOOO00O00O0OOOO >=0 :#line:848
                        if len (O0O000O0O0O000O0O ['cedents_to_do'])>len (O0O000O0O0O000O0O ['cedents']):#line:849
                            OOOOOO0OO0O0OOO00 ._start_cedent (O0O000O0O0O000O0O )#line:850
                    O0O000O0O0O000O0O ['cedents'].pop ()#line:851
                    if (len (_O00OO0O000O000000 )<_OOOO00OOO0O000OO0 ):#line:852
                        OOOOOO0OO0O0OOO00 ._genvar (O0O000O0O0O000O0O ,OO000O0OOOOO000O0 ,_O00OO0O000O000000 ,_O00O00000OOOO0O00 ,_OO0OO0O0OO00000O0 ,_OOO0O00O000OO00OO ,_OOOO00OOO0O000OO0 )#line:853
                else :#line:854
                    O0O000O0O0O000O0O ['cedents'].pop ()#line:855
                if len (_O0OO0000O0O0O00OO )<_OO0OOOO0O0OOOO000 :#line:856
                    OOOOOO0OO0O0OOO00 ._gencomb (O0O000O0O0O000O0O ,OO000O0OOOOO000O0 ,_O00OO0O000O000000 ,_O00O00000OOOO0O00 ,_O0OO0000O0O0O00OO ,_OOO0OOO00O0000000 ,_OOO0O00000O0OOO00 ,O000000OOOOOOO00O ,_O00000O0OO000OOO0 ,_OOO0O00O000OO00OO ,_OOOO00OOO0O000OO0 ,_OO0O000000O00O000 ,_OO0OOOO0O0OOOO000 )#line:857
                _O0OO0000O0O0O00OO .pop ()#line:858
    def _start_cedent (OOOO0O00O0O000000 ,O00OOO0000OOO0O0O ):#line:860
        if len (O00OOO0000OOO0O0O ['cedents_to_do'])>len (O00OOO0000OOO0O0O ['cedents']):#line:861
            _O0O0O000O0000OO0O =[]#line:862
            _O0000O0000OOOOO0O =[]#line:863
            OOOOO0OOO000O00O0 ={}#line:864
            OOOOO0OOO000O00O0 ['cedent_type']=O00OOO0000OOO0O0O ['cedents_to_do'][len (O00OOO0000OOO0O0O ['cedents'])]#line:865
            OO000OOO0OOO00OOO =OOOOO0OOO000O00O0 ['cedent_type']#line:866
            if ((OO000OOO0OOO00OOO [-1 ]=='-')|(OO000OOO0OOO00OOO [-1 ]=='+')):#line:867
                OO000OOO0OOO00OOO =OO000OOO0OOO00OOO [:-1 ]#line:868
            OOOOO0OOO000O00O0 ['defi']=OOOO0O00O0O000000 .kwargs .get (OO000OOO0OOO00OOO )#line:870
            if (OOOOO0OOO000O00O0 ['defi']==None ):#line:871
                print ("Error getting cedent ",OOOOO0OOO000O00O0 ['cedent_type'])#line:872
            _OO0O0OOO0O0O00000 =int (0 )#line:873
            OOOOO0OOO000O00O0 ['num_cedent']=len (OOOOO0OOO000O00O0 ['defi'].get ('attributes'))#line:878
            if (OOOOO0OOO000O00O0 ['defi'].get ('type')=='con'):#line:879
                _OO0O0OOO0O0O00000 =(1 <<OOOO0O00O0O000000 .data ["rows_count"])-1 #line:880
            OOOO0O00O0O000000 ._genvar (O00OOO0000OOO0O0O ,OOOOO0OOO000O00O0 ,_O0O0O000O0000OO0O ,_O0000O0000OOOOO0O ,_OO0O0OOO0O0O00000 ,OOOOO0OOO000O00O0 ['defi'].get ('minlen'),OOOOO0OOO000O00O0 ['defi'].get ('maxlen'))#line:881
    def _calc_all (OOOO000OOO00OO000 ,**O0O000OOOOO000O00 ):#line:884
        OOOO000OOO00OO000 ._prep_data (OOOO000OOO00OO000 .kwargs .get ("df"))#line:885
        OOOO000OOO00OO000 ._calculate (**O0O000OOOOO000O00 )#line:886
    def _check_cedents (O000OOOO00OOOOOOO ,O0OOO0OO0O00OOO00 ,**O0000OO00OOOOOOOO ):#line:888
        OO00OOOOO0OO0OO0O =True #line:889
        if (O0000OO00OOOOOOOO .get ('quantifiers',None )==None ):#line:890
            print (f"Error: missing quantifiers.")#line:891
            OO00OOOOO0OO0OO0O =False #line:892
            return OO00OOOOO0OO0OO0O #line:893
        if (type (O0000OO00OOOOOOOO .get ('quantifiers'))!=dict ):#line:894
            print (f"Error: quantifiers are not dictionary type.")#line:895
            OO00OOOOO0OO0OO0O =False #line:896
            return OO00OOOOO0OO0OO0O #line:897
        for OOOO0O0000O0O0O00 in O0OOO0OO0O00OOO00 :#line:899
            if (O0000OO00OOOOOOOO .get (OOOO0O0000O0O0O00 ,None )==None ):#line:900
                print (f"Error: cedent {OOOO0O0000O0O0O00} is missing in parameters.")#line:901
                OO00OOOOO0OO0OO0O =False #line:902
                return OO00OOOOO0OO0OO0O #line:903
            O000OOO0OO0OO0O0O =O0000OO00OOOOOOOO .get (OOOO0O0000O0O0O00 )#line:904
            if (O000OOO0OO0OO0O0O .get ('minlen'),None )==None :#line:905
                print (f"Error: cedent {OOOO0O0000O0O0O00} has no minimal length specified.")#line:906
                OO00OOOOO0OO0OO0O =False #line:907
                return OO00OOOOO0OO0OO0O #line:908
            if not (type (O000OOO0OO0OO0O0O .get ('minlen'))is int ):#line:909
                print (f"Error: cedent {OOOO0O0000O0O0O00} has invalid type of minimal length ({type(O000OOO0OO0OO0O0O.get('minlen'))}).")#line:910
                OO00OOOOO0OO0OO0O =False #line:911
                return OO00OOOOO0OO0OO0O #line:912
            if (O000OOO0OO0OO0O0O .get ('maxlen'),None )==None :#line:913
                print (f"Error: cedent {OOOO0O0000O0O0O00} has no maximal length specified.")#line:914
                OO00OOOOO0OO0OO0O =False #line:915
                return OO00OOOOO0OO0OO0O #line:916
            if not (type (O000OOO0OO0OO0O0O .get ('maxlen'))is int ):#line:917
                print (f"Error: cedent {OOOO0O0000O0O0O00} has invalid type of maximal length.")#line:918
                OO00OOOOO0OO0OO0O =False #line:919
                return OO00OOOOO0OO0OO0O #line:920
            if (O000OOO0OO0OO0O0O .get ('type'),None )==None :#line:921
                print (f"Error: cedent {OOOO0O0000O0O0O00} has no type specified.")#line:922
                OO00OOOOO0OO0OO0O =False #line:923
                return OO00OOOOO0OO0OO0O #line:924
            if not ((O000OOO0OO0OO0O0O .get ('type'))in (['con','dis'])):#line:925
                print (f"Error: cedent {OOOO0O0000O0O0O00} has invalid type. Allowed values are 'con' and 'dis'.")#line:926
                OO00OOOOO0OO0OO0O =False #line:927
                return OO00OOOOO0OO0OO0O #line:928
            if (O000OOO0OO0OO0O0O .get ('attributes'),None )==None :#line:929
                print (f"Error: cedent {OOOO0O0000O0O0O00} has no attributes specified.")#line:930
                OO00OOOOO0OO0OO0O =False #line:931
                return OO00OOOOO0OO0OO0O #line:932
            for O0O00OOOOO0000OOO in O000OOO0OO0OO0O0O .get ('attributes'):#line:933
                if (O0O00OOOOO0000OOO .get ('name'),None )==None :#line:934
                    print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO} has no 'name' attribute specified.")#line:935
                    OO00OOOOO0OO0OO0O =False #line:936
                    return OO00OOOOO0OO0OO0O #line:937
                if not ((O0O00OOOOO0000OOO .get ('name'))in O000OOOO00OOOOOOO .data ["varname"]):#line:938
                    print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} not in variable list. Please check spelling.")#line:939
                    OO00OOOOO0OO0OO0O =False #line:940
                    return OO00OOOOO0OO0OO0O #line:941
                if (O0O00OOOOO0000OOO .get ('type'),None )==None :#line:942
                    print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} has no 'type' attribute specified.")#line:943
                    OO00OOOOO0OO0OO0O =False #line:944
                    return OO00OOOOO0OO0OO0O #line:945
                if not ((O0O00OOOOO0000OOO .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:946
                    print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} has unsupported type {O0O00OOOOO0000OOO.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:947
                    OO00OOOOO0OO0OO0O =False #line:948
                    return OO00OOOOO0OO0OO0O #line:949
                if (O0O00OOOOO0000OOO .get ('minlen'),None )==None :#line:950
                    print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} has no minimal length specified.")#line:951
                    OO00OOOOO0OO0OO0O =False #line:952
                    return OO00OOOOO0OO0OO0O #line:953
                if not (type (O0O00OOOOO0000OOO .get ('minlen'))is int ):#line:954
                    if not (O0O00OOOOO0000OOO .get ('type')=='one'):#line:955
                        print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} has invalid type of minimal length.")#line:956
                        OO00OOOOO0OO0OO0O =False #line:957
                        return OO00OOOOO0OO0OO0O #line:958
                if (O0O00OOOOO0000OOO .get ('maxlen'),None )==None :#line:959
                    print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} has no maximal length specified.")#line:960
                    OO00OOOOO0OO0OO0O =False #line:961
                    return OO00OOOOO0OO0OO0O #line:962
                if not (type (O0O00OOOOO0000OOO .get ('maxlen'))is int ):#line:963
                    if not (O0O00OOOOO0000OOO .get ('type')=='one'):#line:964
                        print (f"Error: cedent {OOOO0O0000O0O0O00} / attribute {O0O00OOOOO0000OOO.get('name')} has invalid type of maximal length.")#line:965
                        OO00OOOOO0OO0OO0O =False #line:966
                        return OO00OOOOO0OO0OO0O #line:967
        return OO00OOOOO0OO0OO0O #line:968
    def _calculate (OOO000O000O0O00O0 ,**OO000OO00O00OO0O0 ):#line:970
        if OOO000O000O0O00O0 .data ["data_prepared"]==0 :#line:971
            print ("Error: data not prepared")#line:972
            return #line:973
        OOO000O000O0O00O0 .kwargs =OO000OO00O00OO0O0 #line:974
        OOO000O000O0O00O0 .proc =OO000OO00O00OO0O0 .get ('proc')#line:975
        OOO000O000O0O00O0 .quantifiers =OO000OO00O00OO0O0 .get ('quantifiers')#line:976
        OOO000O000O0O00O0 ._init_task ()#line:978
        OOO000O000O0O00O0 .stats ['start_proc_time']=time .time ()#line:979
        OOO000O000O0O00O0 .task_actinfo ['cedents_to_do']=[]#line:980
        OOO000O000O0O00O0 .task_actinfo ['cedents']=[]#line:981
        if OO000OO00O00OO0O0 .get ("proc")=='CFMiner':#line:984
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do']=['cond']#line:985
            if OO000OO00O00OO0O0 .get ('target',None )==None :#line:986
                print ("ERROR: no target variable defined for CF Miner")#line:987
                return #line:988
            if not (OOO000O000O0O00O0 ._check_cedents (['cond'],**OO000OO00O00OO0O0 )):#line:989
                return #line:990
            if not (OO000OO00O00OO0O0 .get ('target')in OOO000O000O0O00O0 .data ["varname"]):#line:991
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:992
                return #line:993
        elif OO000OO00O00OO0O0 .get ("proc")=='4ftMiner':#line:995
            if not (OOO000O000O0O00O0 ._check_cedents (['ante','succ'],**OO000OO00O00OO0O0 )):#line:996
                return #line:997
            _OOOO0OOOO0O0000O0 =OO000OO00O00OO0O0 .get ("cond")#line:999
            if _OOOO0OOOO0O0000O0 !=None :#line:1000
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1001
            else :#line:1002
                OOO00OOOOO0O0OOOO =OOO000O000O0O00O0 .cedent #line:1003
                OOO00OOOOO0O0OOOO ['cedent_type']='cond'#line:1004
                OOO00OOOOO0O0OOOO ['filter_value']=(1 <<OOO000O000O0O00O0 .data ["rows_count"])-1 #line:1005
                OOO00OOOOO0O0OOOO ['generated_string']='---'#line:1006
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1008
                OOO000O000O0O00O0 .task_actinfo ['cedents'].append (OOO00OOOOO0O0OOOO )#line:1009
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1013
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1014
        elif OO000OO00O00OO0O0 .get ("proc")=='NewAct4ftMiner':#line:1015
            _OOOO0OOOO0O0000O0 =OO000OO00O00OO0O0 .get ("cond")#line:1018
            if _OOOO0OOOO0O0000O0 !=None :#line:1019
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1020
            else :#line:1021
                OOO00OOOOO0O0OOOO =OOO000O000O0O00O0 .cedent #line:1022
                OOO00OOOOO0O0OOOO ['cedent_type']='cond'#line:1023
                OOO00OOOOO0O0OOOO ['filter_value']=(1 <<OOO000O000O0O00O0 .data ["rows_count"])-1 #line:1024
                OOO00OOOOO0O0OOOO ['generated_string']='---'#line:1025
                print (OOO00OOOOO0O0OOOO ['filter_value'])#line:1026
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1027
                OOO000O000O0O00O0 .task_actinfo ['cedents'].append (OOO00OOOOO0O0OOOO )#line:1028
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('antv')#line:1029
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1030
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1031
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1032
        elif OO000OO00O00OO0O0 .get ("proc")=='Act4ftMiner':#line:1033
            _OOOO0OOOO0O0000O0 =OO000OO00O00OO0O0 .get ("cond")#line:1036
            if _OOOO0OOOO0O0000O0 !=None :#line:1037
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1038
            else :#line:1039
                OOO00OOOOO0O0OOOO =OOO000O000O0O00O0 .cedent #line:1040
                OOO00OOOOO0O0OOOO ['cedent_type']='cond'#line:1041
                OOO00OOOOO0O0OOOO ['filter_value']=(1 <<OOO000O000O0O00O0 .data ["rows_count"])-1 #line:1042
                OOO00OOOOO0O0OOOO ['generated_string']='---'#line:1043
                print (OOO00OOOOO0O0OOOO ['filter_value'])#line:1044
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1045
                OOO000O000O0O00O0 .task_actinfo ['cedents'].append (OOO00OOOOO0O0OOOO )#line:1046
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1047
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1048
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1049
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1050
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1051
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1052
        elif OO000OO00O00OO0O0 .get ("proc")=='SD4ftMiner':#line:1053
            if not (OOO000O000O0O00O0 ._check_cedents (['ante','succ','frst','scnd'],**OO000OO00O00OO0O0 )):#line:1056
                return #line:1057
            _OOOO0OOOO0O0000O0 =OO000OO00O00OO0O0 .get ("cond")#line:1058
            if _OOOO0OOOO0O0000O0 !=None :#line:1059
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1060
            else :#line:1061
                OOO00OOOOO0O0OOOO =OOO000O000O0O00O0 .cedent #line:1062
                OOO00OOOOO0O0OOOO ['cedent_type']='cond'#line:1063
                OOO00OOOOO0O0OOOO ['filter_value']=(1 <<OOO000O000O0O00O0 .data ["rows_count"])-1 #line:1064
                OOO00OOOOO0O0OOOO ['generated_string']='---'#line:1065
                print (OOO00OOOOO0O0OOOO ['filter_value'])#line:1066
                OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1067
                OOO000O000O0O00O0 .task_actinfo ['cedents'].append (OOO00OOOOO0O0OOOO )#line:1068
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('frst')#line:1069
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1070
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1071
            OOO000O000O0O00O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1072
        else :#line:1073
            print ("Unsupported procedure")#line:1074
            return #line:1075
        print ("Will go for ",OO000OO00O00OO0O0 .get ("proc"))#line:1076
        OOO000O000O0O00O0 .task_actinfo ['optim']={}#line:1079
        OOO00OO0000000O0O =True #line:1080
        for OOOOO00O0O0O0O0O0 in OOO000O000O0O00O0 .task_actinfo ['cedents_to_do']:#line:1081
            try :#line:1082
                O00000OOO00O0OO00 =OOO000O000O0O00O0 .kwargs .get (OOOOO00O0O0O0O0O0 )#line:1083
                if O00000OOO00O0OO00 .get ('type')!='con':#line:1086
                    OOO00OO0000000O0O =False #line:1087
            except :#line:1088
                O0O0O0000OO0OO0O0 =1 <2 #line:1089
        if "opts"in OO000OO00O00OO0O0 :#line:1091
            if "no_optimizations"in OO000OO00O00OO0O0 .get ('opts'):#line:1092
                OOO00OO0000000O0O =False #line:1093
                print ("No optimization will be made.")#line:1094
        O0O0000OO0O00OOO0 ={}#line:1096
        O0O0000OO0O00OOO0 ['only_con']=OOO00OO0000000O0O #line:1097
        OOO000O000O0O00O0 .task_actinfo ['optim']=O0O0000OO0O00OOO0 #line:1098
        print ("Starting to mine rules.")#line:1106
        OOO000O000O0O00O0 ._start_cedent (OOO000O000O0O00O0 .task_actinfo )#line:1107
        OOO000O000O0O00O0 .stats ['end_proc_time']=time .time ()#line:1109
        print ("Done. Total verifications : "+str (OOO000O000O0O00O0 .stats ['total_cnt'])+", hypotheses "+str (OOO000O000O0O00O0 .stats ['total_valid'])+",control number:"+str (OOO000O000O0O00O0 .stats ['control_number'])+", times: prep "+str (OOO000O000O0O00O0 .stats ['end_prep_time']-OOO000O000O0O00O0 .stats ['start_prep_time'])+", processing "+str (OOO000O000O0O00O0 .stats ['end_proc_time']-OOO000O000O0O00O0 .stats ['start_proc_time']))#line:1112
        OOO0OO000000O0OO0 ={}#line:1113
        OO0OO0O0OOOO0OOOO ={}#line:1114
        OO0OO0O0OOOO0OOOO ["task_type"]=OO000OO00O00OO0O0 .get ('proc')#line:1115
        OO0OO0O0OOOO0OOOO ["target"]=OO000OO00O00OO0O0 .get ('target')#line:1117
        OO0OO0O0OOOO0OOOO ["self.quantifiers"]=OOO000O000O0O00O0 .quantifiers #line:1118
        if OO000OO00O00OO0O0 .get ('cond')!=None :#line:1120
            OO0OO0O0OOOO0OOOO ['cond']=OO000OO00O00OO0O0 .get ('cond')#line:1121
        if OO000OO00O00OO0O0 .get ('ante')!=None :#line:1122
            OO0OO0O0OOOO0OOOO ['ante']=OO000OO00O00OO0O0 .get ('ante')#line:1123
        if OO000OO00O00OO0O0 .get ('succ')!=None :#line:1124
            OO0OO0O0OOOO0OOOO ['succ']=OO000OO00O00OO0O0 .get ('succ')#line:1125
        if OO000OO00O00OO0O0 .get ('opts')!=None :#line:1126
            OO0OO0O0OOOO0OOOO ['opts']=OO000OO00O00OO0O0 .get ('opts')#line:1127
        OOO0OO000000O0OO0 ["taskinfo"]=OO0OO0O0OOOO0OOOO #line:1128
        O00OO0O00OOO0OOOO ={}#line:1129
        O00OO0O00OOO0OOOO ["total_verifications"]=OOO000O000O0O00O0 .stats ['total_cnt']#line:1130
        O00OO0O00OOO0OOOO ["valid_hypotheses"]=OOO000O000O0O00O0 .stats ['total_valid']#line:1131
        O00OO0O00OOO0OOOO ["time_prep"]=OOO000O000O0O00O0 .stats ['end_prep_time']-OOO000O000O0O00O0 .stats ['start_prep_time']#line:1132
        O00OO0O00OOO0OOOO ["time_processing"]=OOO000O000O0O00O0 .stats ['end_proc_time']-OOO000O000O0O00O0 .stats ['start_proc_time']#line:1133
        O00OO0O00OOO0OOOO ["time_total"]=OOO000O000O0O00O0 .stats ['end_prep_time']-OOO000O000O0O00O0 .stats ['start_prep_time']+OOO000O000O0O00O0 .stats ['end_proc_time']-OOO000O000O0O00O0 .stats ['start_proc_time']#line:1134
        OOO0OO000000O0OO0 ["summary_statistics"]=O00OO0O00OOO0OOOO #line:1135
        OOO0OO000000O0OO0 ["hypotheses"]=OOO000O000O0O00O0 .hypolist #line:1136
        OOO00OOO00OO000O0 ={}#line:1137
        OOO00OOO00OO000O0 ["varname"]=OOO000O000O0O00O0 .data ["varname"]#line:1138
        OOO00OOO00OO000O0 ["catnames"]=OOO000O000O0O00O0 .data ["catnames"]#line:1139
        OOO0OO000000O0OO0 ["datalabels"]=OOO00OOO00OO000O0 #line:1140
        OOO000O000O0O00O0 .result =OOO0OO000000O0OO0 #line:1143
    def print_summary (O00O0000O000O00O0 ):#line:1145
        print ("")#line:1146
        print ("CleverMiner task processing summary:")#line:1147
        print ("")#line:1148
        print (f"Task type : {O00O0000O000O00O0.result['taskinfo']['task_type']}")#line:1149
        print (f"Number of verifications : {O00O0000O000O00O0.result['summary_statistics']['total_verifications']}")#line:1150
        print (f"Number of hypotheses : {O00O0000O000O00O0.result['summary_statistics']['valid_hypotheses']}")#line:1151
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O00O0000O000O00O0.result['summary_statistics']['time_total']))}")#line:1152
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O00O0000O000O00O0.result['summary_statistics']['time_prep']))}")#line:1154
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O00O0000O000O00O0.result['summary_statistics']['time_processing']))}")#line:1155
        print ("")#line:1156
    def print_hypolist (O00O0O0OO000OOO0O ):#line:1158
        print ("")#line:1159
        print ("List of hypotheses:")#line:1160
        if O00O0O0OO000OOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1161
            print ("HYPOID BASE  PIM   AAD    Hypothesis")#line:1162
        elif O00O0O0OO000OOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1163
            print ("HYPOID BASE  S_UP  S_DOWN Condition")#line:1164
        elif O00O0O0OO000OOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1165
            print ("HYPOID BASE1 BASE2 RatioPIM DeltaPIM Hypothesis")#line:1166
        else :#line:1167
            print ("Unsupported task type for hypolist")#line:1168
            return #line:1169
        for OO000OOOO0O00000O in O00O0O0OO000OOO0O .result ["hypotheses"]:#line:1170
            O0OO0OOOO00000O00 ="{:6d}".format (OO000OOOO0O00000O ["hypo_id"])#line:1171
            if O00O0O0OO000OOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1172
                O0OO0OOOO00000O00 =O0OO0OOOO00000O00 +" "+"{:5d}".format (OO000OOOO0O00000O ["params"]["base"])+" "+"{:.3f}".format (OO000OOOO0O00000O ["params"]["pim"])+" "+"{:+.3f}".format (OO000OOOO0O00000O ["params"]["aad"])#line:1173
                O0OO0OOOO00000O00 =O0OO0OOOO00000O00 +" "+OO000OOOO0O00000O ["cedents"]["ante"]+" => "+OO000OOOO0O00000O ["cedents"]["succ"]+" | "+OO000OOOO0O00000O ["cedents"]["cond"]#line:1174
            elif O00O0O0OO000OOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1175
                O0OO0OOOO00000O00 =O0OO0OOOO00000O00 +" "+"{:5d}".format (OO000OOOO0O00000O ["params"]["base"])+" "+"{:5d}".format (OO000OOOO0O00000O ["params"]["s_up"])+" "+"{:5d}".format (OO000OOOO0O00000O ["params"]["s_down"])#line:1176
                O0OO0OOOO00000O00 =O0OO0OOOO00000O00 +" "+OO000OOOO0O00000O ["cedents"]["cond"]#line:1177
            elif O00O0O0OO000OOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1178
                O0OO0OOOO00000O00 =O0OO0OOOO00000O00 +" "+"{:5d}".format (OO000OOOO0O00000O ["params"]["base1"])+" "+"{:5d}".format (OO000OOOO0O00000O ["params"]["base2"])+"    "+"{:.3f}".format (OO000OOOO0O00000O ["params"]["ratiopim"])+"   "+"{:+.3f}".format (OO000OOOO0O00000O ["params"]["deltapim"])#line:1179
                O0OO0OOOO00000O00 =O0OO0OOOO00000O00 +" "+OO000OOOO0O00000O ["cedents"]["ante"]+" => "+OO000OOOO0O00000O ["cedents"]["succ"]+" | "+OO000OOOO0O00000O ["cedents"]["cond"]+" : "+OO000OOOO0O00000O ["cedents"]["frst"]+" x "+OO000OOOO0O00000O ["cedents"]["scnd"]#line:1180
            print (O0OO0OOOO00000O00 )#line:1182
        print ("")#line:1183
    def print_hypo (O00O0O00O0OO0OOO0 ,O00O000O0O0O0OOO0 ):#line:1185
        print ("")#line:1186
        if (O00O000O0O0O0OOO0 <=len (O00O0O00O0OO0OOO0 .result ["hypotheses"])):#line:1187
            if O00O0O00O0OO0OOO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1188
                print ("")#line:1189
                OO00OO0OOO0000O0O =O00O0O00O0OO0OOO0 .result ["hypotheses"][O00O000O0O0O0OOO0 -1 ]#line:1190
                print (f"Hypothesis id : {OO00OO0OOO0000O0O['hypo_id']}")#line:1191
                print ("")#line:1192
                print (f"Base : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['base'])}  Relative base : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['rel_base'])}  PIM : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['pim'])}  AAD : {'{:+.3f}'.format(OO00OO0OOO0000O0O['params']['aad'])}  BAD : {'{:+.3f}'.format(OO00OO0OOO0000O0O['params']['bad'])}")#line:1193
                print ("")#line:1194
                print ("Cedents:")#line:1195
                print (f"  antecedent : {OO00OO0OOO0000O0O['cedents']['ante']}")#line:1196
                print (f"  succcedent : {OO00OO0OOO0000O0O['cedents']['succ']}")#line:1197
                print (f"  condition  : {OO00OO0OOO0000O0O['cedents']['cond']}")#line:1198
                print ("")#line:1199
                print ("Fourfold table")#line:1200
                print (f"    |  S  |  ¬S |")#line:1201
                print (f"----|-----|-----|")#line:1202
                print (f" A  |{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold'][0])}|{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold'][1])}|")#line:1203
                print (f"----|-----|-----|")#line:1204
                print (f"¬A  |{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold'][2])}|{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold'][3])}|")#line:1205
                print (f"----|-----|-----|")#line:1206
            elif O00O0O00O0OO0OOO0 .result ['taskinfo']['task_type']=="CFMiner":#line:1207
                print ("")#line:1208
                OO00OO0OOO0000O0O =O00O0O00O0OO0OOO0 .result ["hypotheses"][O00O000O0O0O0OOO0 -1 ]#line:1209
                print (f"Hypothesis id : {OO00OO0OOO0000O0O['hypo_id']}")#line:1210
                print ("")#line:1211
                print (f"Base : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['base'])}  Relative base : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['max'])}  Histogram minimum : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['rel_min'])}")#line:1213
                print ("")#line:1214
                print (f"Condition  : {OO00OO0OOO0000O0O['cedents']['cond']}")#line:1215
                print ("")#line:1216
                print (f"Histogram {OO00OO0OOO0000O0O['params']['hist']}")#line:1217
            elif O00O0O00O0OO0OOO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1218
                print ("")#line:1219
                OO00OO0OOO0000O0O =O00O0O00O0OO0OOO0 .result ["hypotheses"][O00O000O0O0O0OOO0 -1 ]#line:1220
                print (f"Hypothesis id : {OO00OO0OOO0000O0O['hypo_id']}")#line:1221
                print ("")#line:1222
                print (f"Base1 : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['base1'])} Base2 : {'{:5d}'.format(OO00OO0OOO0000O0O['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['rel_base2'])} PIM1 : {'{:.3f}'.format(OO00OO0OOO0000O0O['params']['pim1'])}  PIM2 : {'{:+.3f}'.format(OO00OO0OOO0000O0O['params']['pim2'])}  Delta PIM : {'{:+.3f}'.format(OO00OO0OOO0000O0O['params']['deltapim'])} Ratio PIM : {'{:+.3f}'.format(OO00OO0OOO0000O0O['params']['ratiopim'])}")#line:1223
                print ("")#line:1224
                print ("Cedents:")#line:1225
                print (f"  antecedent : {OO00OO0OOO0000O0O['cedents']['ante']}")#line:1226
                print (f"  succcedent : {OO00OO0OOO0000O0O['cedents']['succ']}")#line:1227
                print (f"  condition  : {OO00OO0OOO0000O0O['cedents']['cond']}")#line:1228
                print (f"  first set  : {OO00OO0OOO0000O0O['cedents']['frst']}")#line:1229
                print (f"  second set : {OO00OO0OOO0000O0O['cedents']['scnd']}")#line:1230
                print ("")#line:1231
                print ("Fourfold tables:")#line:1232
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1233
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1234
                print (f" A  |{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold1'][0])}|{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold2'][0])}|{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold2'][1])}|")#line:1235
                print (f"----|-----|-----|  ----|-----|-----|")#line:1236
                print (f"¬A  |{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold1'][2])}|{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold2'][2])}|{'{:5d}'.format(OO00OO0OOO0000O0O['params']['fourfold2'][3])}|")#line:1237
                print (f"----|-----|-----|  ----|-----|-----|")#line:1238
            else :#line:1239
                print ("Unsupported task type for hypo details")#line:1240
            print ("")#line:1244
        else :#line:1245
            print ("No such hypothesis.")#line:1246
