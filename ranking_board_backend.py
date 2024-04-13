# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 12:09:36 2024

@author: PC
"""
def msmain():
    import os
    import glob
    import pickle
    import numpy as np
    import pandas as pd
    
    current_path = os.getcwd()
    path = os.path.join(current_path, "saved_data")
    flist = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    
    for i in range(len(flist)):
        pattern = os.path.join(path, flist[i], "block1", "*.pkl")
        pkl_files = glob.glob(pattern)
        
        if len(pkl_files) == 60:
            _, msid = flist[i].rsplit('_', 1)
            date_text = flist[i].split('_', 1)[0]  # 언더바 기준으로 분할하여 좌측 부분(날짜와 시간)을 가져옴
            data = date_text[4:8] + date_text[8:12]      
            msid2 = msid + '_' + data
            
            df = pd.read_excel(os.path.join(current_path, 'ranking', 'ranking_data.xlsx'), index_col=0)
            if not msid2 in list(df['ID']):
                block_n = 0
                mssave_array = np.zeros((1, 3, 3)) * np.nan # block x group x fn
                mssave_dict = {}; blcok_name = 'block1'
                mssave_dict[blcok_name] = {} 
                accuracy = {'neutral':[], 'congruent':[], 'incongruent':[]}
                for j in range(len(pkl_files)):
                    with open(pkl_files[j], 'rb') as file:
                        msdict = pickle.load(file)
                    
                    label = None
                    if msdict['Correct'] and msdict['Response']=='Yes': label = 'TP'
                    elif msdict['Correct'] and msdict['Response']=='No': label = 'FP'
                    elif not(msdict['Correct']) and msdict['Response']=='Yes': label = 'FN'
                    elif not(msdict['Correct']) and msdict['Response']=='No': label = 'TN'
                    if msdict['Response Time'] == 1500: label = 'Noresponse'
            
                    accuracy[msdict['Condition']].append([label, msdict['Response Time']])
                
                keylist = list(accuracy.keys())
                for c in range(len(keylist)):
                    gn = keylist[c]
                    # rt_save[str(t)][gn] = []
                    
                    TP_vix = np.where(np.array(accuracy[gn])[:,0] == 'TP')[0]
                    TP_n = len(TP_vix)
                    TP_rts = np.array(np.array(accuracy[gn])[TP_vix,1], dtype=float)
            
                    FP_vix = np.where(np.array(accuracy[gn])[:,0] == 'FP')[0]
                    FP_n = len(FP_vix)
                    FP_rts = np.array(np.array(accuracy[gn])[FP_vix,1], dtype=float)
                    
                    TN_vix = np.where(np.array(accuracy[gn])[:,0] == 'TN')[0]
                    TN_n = len(TN_vix)
                    TN_rts = np.array(np.array(accuracy[gn])[TN_vix,1], dtype=float)
                    
                    FN_vix = np.where(np.array(accuracy[gn])[:,0] == 'FN')[0]
                    FN_n = len(FN_vix)
                    FN_rts = np.array(np.array(accuracy[gn])[FN_vix,1], dtype=float)
                    
                    if (TP_n + TN_n + FP_n + FN_n) != 0:
                        acc = (TP_n + TN_n) / (TP_n + TN_n + FP_n + FN_n)
                    else: acc = 0
                    
                    T_rt = np.nanmean(np.concatenate((TP_rts, TN_rts), axis=0))
                    F_rt = np.nanmean(np.concatenate((FP_rts, FN_rts), axis=0))
                    # nan 왜찍힘?
                    # print(t, n, keylist[c], acc, np.round([T_rt, F_rt]))
                    # rt_save[str(t)][keylist[c]] = [T_rt, F_rt, acc]
                    
                    mssave_dict[blcok_name][gn] = {}
                    mssave_dict[blcok_name][gn]['acc'] = acc
                    mssave_dict[blcok_name][gn]['true_reatction_time'] = T_rt
                    mssave_dict[blcok_name][gn]['false_reatction_time'] = F_rt
                    
                    mssave_array[block_n, c, 0] = acc
                    mssave_array[block_n, c, 1] = T_rt
                    mssave_array[block_n, c, 2] = F_rt
                    
                mssave_array[0,:,0][np.isnan(mssave_array[0,:,0])] = 0
                mssave_array[0,:,1:][np.isnan(mssave_array[0,:,1:])] = 2000
                    
                participant_data = np.reshape(mssave_array[0], (9,))
  
                def metric_stroop(participant_data):
                     # 가중치 설정
                     accuracy_weights = np.array([100, 100, 150])  # 정확도에 대한 가중치
                     response_time_weights = np.array([1, 1, 1.5])  # 반응 시간에 대한 가중치
                     wrong_response_penalty = 1.2  # 오답에 대한 추가 패널티
                     # 정확도와 반응 시간을 별도로 계산
                     accuracy_scores = participant_data[[0, 3, 6]] * accuracy_weights
                     response_time_scores = 1 / \
                         (participant_data[[1, 4, 7]] + participant_data[[2, 5, 8]] * \
                          wrong_response_penalty) * response_time_weights
                     # 최종 점수 계산: 정확도 점수와 반응 시간 점수의 합산
                     final_score = (np.sum(accuracy_scores) * 3) + (np.sum(response_time_scores) * 1e5)
                     final_score = np.round(final_score / 10, 3) - 54
                     print(f"Final score: {final_score}")
                     return final_score
                 
                final_score = metric_stroop(participant_data)
                
                df.loc[len(df)] = [msid2, final_score]
                df.to_excel(os.path.join(current_path, 'ranking', 'ranking_data.xlsx'))

