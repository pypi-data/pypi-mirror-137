#!/usr/bin/env python
"""
   Call DMseg.
"""
from __future__ import print_function
import numpy as np
from time import localtime, strftime
import pandas as pd
import sys
import os.path as op

def clustermaker(chr, pos, assumesorted=False, maxgap=500):
    tmp2 = chr.groupby(by=chr, sort=False)
    tmp3 = tmp2.count()
    Indexes = tmp3.cumsum().to_list()
    Indexes.insert(0, 0)
    clusterIDs = pd.Series(data=[None]*pos.shape[0], index=chr.index)
    Last = 0
    for i in range(len(Indexes)-1):
        i1 = Indexes[i]
        i2 = Indexes[i+1]
        Index = range(i1, i2)
        x = pos.iloc[Index]
        if (not(assumesorted)):
            tmp = [j-1 for j in x.rank()]
            x = x.iloc[tmp]
        y = np.diff(x) > maxgap
        y = np.insert(y, 0, 1)
        z = np.cumsum(y)
        clusterIDs.iloc[i1:i2] = z + Last
        Last = max(z) + Last
    return clusterIDs


def fit_model_probes1(beta, design):
    #use np array to save time
    beta1 = np.array(beta)
    design1 = np.array(design)
    M = np.delete(design1,1,axis=1)
    M_QR_q, M_QR_r = np.linalg.qr(M)
    S = np.diag([1] * M.shape[0]) - np.matmul(M_QR_q, M_QR_q.transpose())
    V = design1[:, 1]
    SV = np.matmul(S, V)
    coef = np.matmul(beta1, np.matmul(S.transpose(), V)) / np.matmul(V.transpose(), SV)
    # Calculate residuals
    QR_X_q, QR_X_r = np.linalg.qr(design)
  
    resids = np.diag([1] * design.shape[0]) - np.matmul(QR_X_q, QR_X_q.transpose())
    resids = np.matmul(resids, beta1.transpose())
 
    # Calculate SE
    tmp1 = np.linalg.inv(design1.T.dot(design1))[1, 1] / (beta.shape[1] - np.linalg.matrix_rank(M) - 1)
    SE = np.sqrt(np.multiply(resids, resids).sum(axis=0) * tmp1)
    result = np.array([coef,SE]).T
    #result = dict(Coef=pd.Series(coef,index=beta.index),SE=pd.Series(SE,index=beta.index),fit_x=design)
    return result

# vectorize part of the fit_model process for simulation, save 20% of time
def fit_model_probes_sim1(beta,design,seed=1000,B=500):
    beta1 = np.array(beta)
    design1 = np.array(design)
    M = np.delete(design1,1,axis=1)
    M_QR_q, M_QR_r = np.linalg.qr(M)
    S = np.diag([1] * M.shape[0]) - np.matmul(M_QR_q, M_QR_q.transpose())
    np.random.seed(seed)
    design_permute = np.array(design.copy())
    group_mat = np.zeros((design.shape[0],B))

    for i in range(B):
        idx = np.random.permutation(range(design.shape[0]))
        group_mat[:,i]=design[idx,1]
    #V = group_mat[:,100]
    V = group_mat
    SV = np.matmul(S, V)

    coef = np.matmul(beta1, np.matmul(S.transpose(), V)) / np.diag(np.matmul(V.transpose(), SV))
    allSE = np.zeros((beta.shape[0],B))
    # Calculate residuals
    #strftime("%Y-%m-%d %H:%M:%S", localtime())
    term1 = np.diag([1] * design.shape[0])
    term2 = np.linalg.matrix_rank(M)
    #this takes time
    for i in range(B):
        design_permute[:,1]=group_mat[:,i]
        QR_X_q, QR_X_r = np.linalg.qr(design_permute)
        #np.allclose(design, np.matmul(QR_X_q, QR_X_r))
        resids = term1 - np.matmul(QR_X_q, QR_X_q.transpose())
        resids = np.matmul(resids, beta1.transpose())
        # Calculate SE
        tmp1 = np.linalg.inv(design_permute.T.dot(design_permute))[1, 1] / (beta.shape[1] - term2 -1)
        allSE[:,i] = np.sqrt(np.multiply(resids,resids).sum(axis=0) * tmp1)
    #strftime("%Y-%m-%d %H:%M:%S", localtime())
    #result = dict(Coef=pd.DataFrame(coef,index=beta.index),SE=pd.DataFrame(allSE,index=beta.index),group_mat=group_mat)
    result = np.concatenate((coef,allSE),axis=1)
    return result


#Search peak segments
def Search_segments1(DMseg_stats, cutoff=1.96):
    zscore = DMseg_stats['Coef']/DMseg_stats['SE']
    #DMseg_stats['Zscore'] = zscore
    cutoff = abs(cutoff)
    
    #direction: 1 if cpg has zscore > cutoff, 0 abs(zscore) < cutoff, -1 if zscore < -cutoff 
    direction = np.zeros(DMseg_stats.shape[0])
    direction = np.where(zscore >= cutoff, 1, direction)
    direction = np.where(zscore <= -cutoff, -1, direction)
    #direction = pd.Series(direction, index=zscore.index)
    #direction1 is based on the absolute zscores.
    direction1 = np.zeros(DMseg_stats.shape[0])
    direction1 = np.where(abs(zscore) >= cutoff, 1, direction)
    

    #segments are segments based on direction1 (a segment includes all connected CpGs with different direction); a segment can cross the border of a cluster
    tmp0 = 1*(np.diff(direction1) != 0)
    tmp0 = np.insert(tmp0, 0, 1)
    segments = np.cumsum(tmp0)
    #segments = pd.Series(segments, index=DMseg_stats.index)
    #split a segment if it covers multiple clusters; a segment should be within a cluster
    allsegments = segments + DMseg_stats['cluster']
    tmp0 = 1*(np.diff(allsegments) != 0)
    tmp0 = np.insert(tmp0, 0, 1)
    allsegments = np.cumsum(tmp0)
    #len(allsegments.unique())
    #allsegments are the final segments
    DMseg_stats['segment'] = allsegments
    DMseg_stats['direction'] = direction

    tmp0 = 1*(np.diff(direction) != 0)
    tmp0 = np.insert(tmp0, 0, 1)
    segments1 = np.cumsum(tmp0)
    allsegments1 = segments1 + DMseg_stats['cluster']
    tmp0 = 1*(np.diff(allsegments1) != 0)
    tmp0 = np.insert(tmp0, 0, 1)
    allsegments1 = np.cumsum(tmp0)
    DMseg_stats['segment1'] = allsegments1

    return DMseg_stats
    

#LRT function
def LRT_segment_nocorr1(DMseg_stats):
    csegments = DMseg_stats.segment
    bdiff = DMseg_stats.Coef
    bvar= 1/pow(DMseg_stats.SE,2)
    bb0 = bvar.groupby(csegments).sum()
    bb1 = (bdiff*bvar).groupby(csegments).sum()
    groupcounts= csegments.groupby(csegments).count()
    seg_mean=bb1/bb0
    seg_mean_vec = np.repeat(seg_mean,groupcounts)
    lrt1=pow(bdiff-seg_mean_vec,2)*bvar
    lrt0=pow(bdiff,2)*bvar
    lrt= lrt0.groupby(csegments).sum() - lrt1.groupby(csegments).sum()
    result = dict(lrt=lrt, seg_mean=seg_mean)
    return result

#LRT function considering switches in a peak
def LRT_segment_nocorr2(DMseg_stats):
    csegments = DMseg_stats.segment
    bdiff = np.abs(DMseg_stats.Coef)
    bvar= 1/pow(DMseg_stats.SE,2)
    DMseg_stats["bvar"] = bvar
    DMseg_stats['bdiff_bvar'] = bvar * bdiff
    #first compute b0,b1 based on segments using zscore (not absolute values)
    tmp = DMseg_stats.groupby(by="segment1")
    b0 = tmp['bvar'].sum()
    b1 = tmp["bdiff_bvar"].sum()
    sign = tmp['direction'].first()
    #the segment id using absolute zscore
    mysegment = tmp['segment'].first()
    #include the sign here
    tmp1 = pd.DataFrame({"b0":b0,"b1_sign":b1*sign,"bb1_divid_bb0_sign":b1/b0*sign,"segment":mysegment},index=b0.index)
    tmp1_groupby = tmp1.groupby(by="segment")
    bb0 = tmp1_groupby['b0'].sum()
    bb1 = tmp1_groupby['b1_sign'].sum()
    seg_mean = bb1/bb0
    tmp1["bb1_divid_bb0_sign"] = round(tmp1["bb1_divid_bb0_sign"],3)
    tmp1["bb1_divid_bb0_sign"] = tmp1["bb1_divid_bb0_sign"].astype(str)
    tmp1_groupby = tmp1.groupby(by="segment")
    #for segmean if there are swiches, show all
    seg_mean_all = tmp1_groupby.agg({"bb1_divid_bb0_sign": ";".join})
 
    groupcounts= csegments.groupby(csegments).count()
    seg_mean_vec = np.repeat(seg_mean,groupcounts)
    lrt1=pow(bdiff-seg_mean_vec,2)*bvar
    lrt0=pow(bdiff,2)*bvar
    lrt= lrt0.groupby(csegments).sum() - lrt1.groupby(csegments).sum()
    result = dict(lrt=lrt, seg_mean=seg_mean_all)
    return result

#wrap Search_segments + LRT
def Segment_satistics2(Pstats1,clusterindex,pos,chr,beta_diff_cutoff,zscore_cutoff):
    # Check ROI, region of interest, both: coef.cutoff, zsocre.cutoff ---------
    # clusters meet beta_diff_cutoff and zscore_cutoff
    #cluster_grp = clusterindex.groupby(clusterindex)
    Pstats1 = pd.DataFrame(Pstats1,index=clusterindex.index,columns=["Coef","SE"])
    Pstats1["Zscore"] = Pstats1["Coef"]/Pstats1["SE"]
    mycoef = 1*(Pstats1['Coef'].abs()>beta_diff_cutoff)
    myzscore = 1*(Pstats1['Zscore'].abs()>zscore_cutoff)

    coef_select=mycoef.groupby(clusterindex).sum()>1
    zscore_select=myzscore.groupby(clusterindex).sum()>1

    groupcounts = clusterindex.groupby(clusterindex).count()
    coef_select_vec = np.repeat(coef_select, groupcounts)
    zscore_select_vec = np.repeat(zscore_select, groupcounts)
    ROIcluster=clusterindex[clusterindex.index[np.logical_and(coef_select_vec,zscore_select_vec)]]
    #print(len(ROIcluster.unique()), " ROI clusters detected.")
    
    DMseg_sd = Pstats1['SE'].loc[ROIcluster.index]
    DMseg_coef = Pstats1['Coef'].loc[ROIcluster.index]
   
    DMseg_pos = pos[ROIcluster.index]
    DMseg_chr = chr[ROIcluster.index]
    
    DMseg_stats = pd.concat([DMseg_coef, DMseg_sd, DMseg_chr, DMseg_pos, ROIcluster], axis=1)
    DMseg_stats.columns = ["Coef", "SE", "chr", "pos", "cluster"]

    DMseg_stats = Search_segments1(DMseg_stats,zscore_cutoff)
    
    #peaks
    DMseg_stats1 = DMseg_stats[DMseg_stats.segment *DMseg_stats.direction != 0]
    DMseg_stats1_groupby = DMseg_stats1.groupby(by="segment")
    # #peak should have #cpg>1
    tmp = DMseg_stats1_groupby['cluster'].transform('count').gt(1)
    DMseg_stats1 = DMseg_stats1.loc[tmp.index[tmp==True]]
    #DMseg_stats1 = DMseg_stats1_groupby.filter(lambda x: len(x) > 1)
    
    ## compute the LRT statistics

    tmp = LRT_segment_nocorr2(DMseg_stats=DMseg_stats1)
    segid = np.unique(DMseg_stats1.segment)

    DMseg_out = pd.DataFrame(columns=["Chr","start_cpg","start_pos","end_cpg","end_pos","n_cpgs","seg_mean","LRT"])
    DMseg_out["seg_mean"]=tmp['seg_mean']
    DMseg_out["LRT"]=tmp['lrt']

    DMseg_stats1["cpgname"] = DMseg_stats1.index
    DMgroup = DMseg_stats1.groupby("segment")
    DMseg_out["n_cpgs"]=DMgroup["segment"].count()
    DMseg_out["Chr"]=DMgroup["chr"].first()
    DMseg_out["start_cpg"]=DMgroup["cpgname"].first()
    DMseg_out["end_cpg"]=DMgroup["cpgname"].last()
    DMseg_out["start_pos"] = DMgroup["pos"].first()
    DMseg_out["start_pos"] = DMseg_out["start_pos"].astype(int)
    DMseg_out["end_pos"] = DMgroup["pos"].last()
    DMseg_out["end_pos"] = DMseg_out["end_pos"].astype(int)
    #DMseg_out["numswitches"] = DMgroup["segment1"].last()-DMgroup["segment1"].first()
    DMseg_out = DMseg_out.reset_index(drop=True)
    return DMseg_out


#do simulation based on permutation, use fit_model_probe
def do_simulation2(beta,design,clusterindex,pos,chr,seed=1000,beta_diff_cutoff=0.05,zscore_cutoff=1.96,B=500):

    print("Start " + str(B) + " simulation: " + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    allsimulation_maxLRT=np.zeros((B,1))
    beta1 = np.array(beta)
    design1 = np.array(design)
    print("Start linear model fitting: " + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    Pstatsall =  fit_model_probes_sim1(beta=beta1,design=design1,seed=seed,B=B)
    #strftime("%Y-%m-%d %H:%M:%S", localtime())
    print("Start peak finding and LRT computing: " + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    for i in range(B):
        if (i+1) % 100 == 0:
            print("Iteration " + str(i+1) + ":  " + strftime("%Y-%m-%d %H:%M:%S", localtime()))

        Pstats2 = np.array((Pstatsall[:,i],Pstatsall[:,i+B])).T
        DMseg_out1 = Segment_satistics2(Pstats1=Pstats2,clusterindex=clusterindex,pos=pos,chr=chr,beta_diff_cutoff=beta_diff_cutoff,zscore_cutoff=zscore_cutoff)
        #DMseg_out1['simulationidx'] = i
        allsimulation_maxLRT[i]=np.max(DMseg_out1.LRT)
    
    print("Simulation ends " + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    return allsimulation_maxLRT

# DMseg_out1=compute_fwer(DMseg_out,DMseg_sim_LRTmax1)
# DMseg_out2=compute_fwer(DMseg_out,DMseg_sim_LRTmax2)

def compute_fwer(DMseg_out,DMseg_sim_LRTmax):
    LRT_alt = DMseg_out['LRT']
    LRT_max = DMseg_sim_LRTmax.tolist()
    LRT_max1 = [x for y in LRT_max for x in y]
    LRT_alt_rank = pd.DataFrame(-np.array(LRT_alt.to_list() + LRT_max1))
    LRT_alt_rank = LRT_alt_rank.rank(axis=0, na_option='bottom')[
        0:len(LRT_alt)]
    LRT_alt_rank = LRT_alt_rank - LRT_alt_rank.rank(axis=0)

    FWER = LRT_alt_rank / len(LRT_max)
    DMseg_out["FWER"] = FWER.iloc[:,0].to_list()
    DMseg_out["LRT"] = round(DMseg_out["LRT"],3)
    DMseg_out = DMseg_out.sort_values(by=['LRT'], ascending=False)
    DMseg_out = DMseg_out.reset_index(drop=True) 
    np.sum(DMseg_out["FWER"]<0.05)
    idx = np.where(DMseg_out["FWER"]<0.05)[0]
    print(DMseg_out.iloc[idx,:])
    return DMseg_out

def pieline (betafile, colDatafile, postionfile, maxgap=500, sd_cutoff=0.025, beta_diff_cutoff=0.05, zscore_cutoff=1.96, seed=1000, B=500):
    sys.path.insert(0, op.join(op.dirname(__file__), ".."))
    #sys.path.insert(0, '/fh/fast/dai_j/Programs/DMseg_python/')
    print("program starts--------")
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    beta = pd.read_csv(betafile, delimiter=',', index_col=0)
    colData = pd.read_csv(colDatafile)
    position = pd.read_csv(postionfile, delimiter=',', index_col=0)
    chr = position['chr']
    pos = position['position']
    #call cluster
    cluster = clustermaker(chr=chr, pos=pos, maxgap=maxgap)
    
    #in case there are missing beta values
    if beta.isnull().sum().sum() > 0:
        for i in beta.index[beta.isnull().any(axis=1)]:     
            beta.loc[i].fillna(beta.loc[i].mean(),inplace=True)

    clustergrp = cluster.groupby(cluster)
    len(clustergrp)  # 170156
    sum(clustergrp.value_counts()==1)   # 117604, most of clusters have 1 CpG
    clusterlen=clustergrp.filter(lambda x:len(x) > 1)
    beta = beta.loc[clusterlen.index]
    #print(len(clusterlen.unique()), "clusters have more than 1 CpG.")
    # next filter out low SD
    allsd = beta.T.std()
    #print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    tmp = clusterlen.groupby(clusterlen)
    maxsd=allsd.groupby(clusterlen).max()
    maxsd_vec=np.repeat(maxsd,tmp.count())
    clustersd=clusterlen[clusterlen.index[maxsd_vec>sd_cutoff]]
    #print(len(clustersd.unique()), "clusters pass sd.cluster filter.")
    #print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    beta = beta.loc[clustersd.index]
    pos=pos[clustersd.index]
    chr=chr[clustersd.index]

    #work on design matrix
    intercept = pd.Series([1]*beta.shape[1], index=beta.columns)
    group_dummy = pd.get_dummies(data=colData.iloc[:, 0], drop_first=True)
    group_dummy.set_index(beta.columns, inplace=True)
    ## need to check if there are other dummy
    other_dummy = pd.get_dummies(data=colData.iloc[:, 1:], drop_first=True)
    other_dummy.set_index(beta.columns, inplace=True)
    design = pd.concat([intercept, group_dummy, other_dummy], axis=1)
    
    #work on observed data
    Pstats = fit_model_probes1(beta, design)
    DMseg_out = Segment_satistics2(Pstats,clustersd,pos=pos,chr=chr,beta_diff_cutoff=beta_diff_cutoff,zscore_cutoff=zscore_cutoff)

    #work on simulation data
    DMseg_sim_LRTmax2 = do_simulation2(beta,design,clustersd,pos=pos,chr=chr)
    DMseg_out1=compute_fwer(DMseg_out,DMseg_sim_LRTmax2)

    print("Program ends")
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    return DMseg_out1


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__,
                   formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument("-betafile", dest="betafile", help="beta matrix", required=True)
    p.add_argument("-colDatafile", dest="colDatafile", help="colData matrix", required=True)
    p.add_argument("-positionfile", dest="positionfile", help="position of CpGs", required=True)
    p.add_argument("-maxgap", dest="maxgap", help="max gap to deterine clusters", default=500)
    p.add_argument("-sd_cutoff", dest="sd_cutoff", help="SD cutoff to filter clusters", default=0.025)
    p.add_argument("-beta_diff_cutoff", dest="beta_diff_cutoff", help="Beta difference cutoff to filter clusters", default=0.05)
    p.add_argument("-zscore_cutoff", dest="zscore_cutoff", help="Z score cutoff to detect peaks", default=1.96)
    p.add_argument("-seed", dest="seed", help="random seed for simulation", default=1000)
    p.add_argument("-B", dest="B", help="number of simulation", default=100)
    args = p.parse_args()
    return pieline(args.betafile, args.colDatafile, args.positionfile, args.maxgap, args.sd_cutoff, args.beta_diff_cutoff, args.zscore_cutoff, args.seed, args.B)


if __name__ == "__main__":
    main()





