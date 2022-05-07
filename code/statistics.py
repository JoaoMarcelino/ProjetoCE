"""
statistics.py
Descriptive and inferential statistics in Python.
Uses numpy, scipy and matplotlib.
ernesto@dei.uc.pt
"""
__author__ = 'Ernesto Costa'
__date__ = 'March 2022'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import readStatisticsToFile
import seaborn as sns
import scipy.stats as st

# obtain data
def get_data(filename):
    """Simple: one column, no header. Returns an array"""
    data = np.loadtxt(filename)
    return data

def get_data_many(filename):
    """Many columns, no header. Transpose the data!"""
    data = np.loadtxt(filename, unpack=True)
    return data

# describing data

def describe_data(data):
    """ data is a numpy array of values"""
    min_ = np.amin(data)
    max_ = np.amax(data)
    mean_ = np.mean(data)
    median_ = np.median(data)
    mode_ = st.mode(data)
    std_ = np.std(data)
    var_ = np.var(data)
    skew_ = st.skew(data)
    kurtosis_ = st.kurtosis(data)
    q_25, q_50, q_75 = np.percentile(data, [25,50,75])
    basic = 'Min: %s\nMax: %s\nMean: %s\nMedian: %s\nMode: %s\nVar: %s\nStd: %s'
    other = '\nSkew: %s\nKurtosis: %s\nQ25: %s\nQ50: %s\nQ75: %s'
    all_ = basic + other
    print(all_ % (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75))
    return (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75)

# visualizing data
def histogram(data,title,xlabel,ylabel,bins=25):
    sns.set()
    plt.hist(data,bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def histogram_with_normal(data,title,xlabel,ylabel,bins=25):
    sns.set()
    plt.hist(data,bins=bins,density=True,alpha=0.6)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plot the PDF
    mu, std = st.norm.fit(data)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 1000)
    p = st.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    plt.show()
    
def box_plot(data, labels):
    sns.set()
    plt.boxplot(data,labels=labels)
    plt.show()


# Parametric??
def test_normal_ks(data):
    """Kolgomorov-Smirnov"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.kstest(norm_data,'norm')

def test_normal_sw(data):
    """Shapiro-Wilk"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.shapiro(norm_data)

def test_normal_and(data,dist='norm'):
    """Anderson-Darling test. Using dist='norm', tests for normality.
    output:
    @statistic
    @critical-values
    @significance level
    If the returned statistic is greater then the critical value for
    a significance level we can reject the null hypothesis that states
    that the data came from a a distribution of the type described.
    """
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.anderson(norm_data,dist)

def levene(data):
    """Test of equal variance."""
    W,pval = st.levene(*data)
    return(W,pval)

# hypothesis testing
# Parametric
def t_test_ind(data1,data2, eq_var=True):
    """
    parametric
    two samples
    independent
    """
    t,pval = st.ttest_ind(data1,data2, equal_var=eq_var)
    return (t,pval)

def t_test_dep(data1,data2):
    """
    parametric
    two samples
    dependent
    """
    t,pval = st.ttest_rel(data1,data2)
    return (t,pval)

def one_way_ind_anova(data):
    """
    parametric
    many samples
    independent
    """
    F,pval = st.f_oneway(*data)
    return (F,pval)

def one_way_dep_anova(data_frame):
    """
    --> Repeated measures one way ANOVA
    --> @data_frame: a  pandas DataFrame with the data
    parametric
    many samples
    dependent
    """
    grand_mean = data_frame.values.mean()
    #grand_variance = data_frame.values.var(ddof=1)
   
    row_means = data_frame.mean(axis=1)
    column_means = data_frame.mean(axis=0)
   
    # n = number of subjects; k = number of conditions/treatments
    n,k = len(data_frame.axes[0]), len(data_frame.axes[1])
    # total number of measurements
    N = data_frame.size # or n * k
   
    # degrees of freedom
    df_total = N - 1
    df_between = k - 1
    df_subject = n - 1
    df_within = df_total - df_between
    df_error = df_within - df_subject   
      
    # compute variances
    SS_between = sum(n*[(m - grand_mean)**2 for m in column_means])   
    SS_within = sum(sum([(data_frame[col] - column_means[i])**2 for i,col in enumerate(data_frame)]))  
    SS_subject = sum(k* [(m - grand_mean)**2 for m in row_means])  
    SS_error = SS_within - SS_subject  
    #SS_total = SS_between + SS_within
   
    # Compute Averages
    MS_between = SS_between/df_between
    MS_error = SS_error/df_error
    MS_subject = SS_subject/df_subject
   
    # F Statistics
    F = MS_between/MS_error
    # p-value
    p_value = st.f.sf(F,df_between,df_error)   
   
    return (F, p_value)


# Non Parametric
def mann_whitney(data1,data2):
    """
    non parametric
    two samples
    independent
    """    
    return st.mannwhitneyu(data1, data2)

def wilcoxon(data1,data2):
    """
    non parametric
    two samples
    dependent
    """     
    return st.wilcoxon(data1,data2)

def kruskal_wallis(data):
    """
    non parametric
    many samples
    independent
    """     
    H,pval = st.kruskal(*data)
    return (H,pval)

def friedman_chi(data):
    """
    non parametric
    many samples
    dependent
    """     
    F,pval = st.friedmanchisquare(*data)
    return (F,pval)    
    
# Effect size
def effect_size_t(stat,df):
    r = np.sqrt(stat**2/(stat**2 + df))
    return r

def effect_size_mw(stat,n1,n2):
    """
    n_ob: number of observations
    """
    n_ob = n1 + n2 
    mean = n1*n2/2
    std = np.sqrt(n1*n2*(n1+n2+1)/12)
    z_score = (stat - mean)/std
    print(z_score)
    return z_score/np.sqrt(n_ob)

def effect_size_wx(stat,n, n_ob):
    """
    n: size of effective sample (zero differences are excluded!)
    n_ob: number of observations
    """
    mean = n*(n+1)/4
    std = np.sqrt(n*(n+1)*(2*n+1)/24)
    z_score = (stat - mean)/std
    return z_score/np.sqrt(n_ob)

# Examples

def test_normality(data):

    alpha = 0.05

    #describe_data(data)

    #Kolgomorov-Smirnov
    statistic, pvalue = test_normal_ks(data)

    print(pvalue)
    
    if (pvalue <= alpha):
        return False  

    #Shapiro-Wilk
    statistic, pvalue = test_normal_sw(data)

    if (pvalue <= alpha):
        return False 
    
    #Anderson-Darling
    pvalue = test_normal_and(data)

    if (pvalue <= alpha):
        return False

    return True

def main():
    
    #ReadStatistics
    path = "/mnt/c/Users/j13ma/Desktop/Projetos/CE/projetoCE/results"
    seed = 50
    dataset = []
    #DP
    folder = 'test3DP'
    data = []
    for i in range(seed):
        filename = f"{path}/{folder}/run{i}.json"
        json = readStatisticsToFile(filename)
        fitness = json['bestIndiv'][1]
        data.append(fitness)
    
    dataset.append(data)
    #RI
    folder = 'test3RI'
    data = []
    for i in range(seed):
        filename = f"{path}/{folder}/run{i}.json"
        json = readStatisticsToFile(filename)
        fitness = json['bestIndiv'][1]
        data.append(fitness)

    dataset.append(data)

    #Test Normality

    for data in dataset:
        existsNormality = test_normality(data)
        if not existsNormality:
            print("We reject the null hypothesis - distribution not normal/guassian")

            return wilcoxon(dataset[0], dataset[1])

    print("We fail to reject the null hypothesis - distribution normal/guassian")
    #t_test_dep

    return 

if __name__ == "__main__":
    main()



def main_levene(filename):
    # get data
    data = get_data_many(filename)
    fake_sp = data[0,:]
    real_sp = data[1,:]
    stat, p_val = levene((fake_sp, real_sp))
    print(f'statistics: {stat}\t p_value: {p_val}')
    return (stat,p_val)
    
def main_1111(filename):
    # Pulse Rate example (one group)
    pr = get_data(filename)
    describe_data(pr)
    print(test_normal_and(pr,dist='norm'))    
    histogram(pr, 'Histogram','Pulse Rate', 'Frequency')

def main_1(filename):
    # Pulse Rate example (one group)
    pr = get_data(filename)
    describe_data(pr)
    print(test_normal_ks(pr))    
    histogram(pr, 'Histogram','Pulse Rate', 'Frequency')
    
def main_11(filename):
    # Pulse Rate example (one group)
    pr = get_data(filename)
    box_plot(pr,['PR'])
      
def main_111(filename):
    # Pulse Rate example (one group)
    pr = get_data(filename)
    describe_data(pr)
    print(test_normal_sw(pr)) 
    norm_data = (pr - np.mean(pr))/(np.std(pr)/np.sqrt(len(pr)))
    histogram_with_normal(norm_data, 'Histogram','Pulse Rate', 'Frequency')  
    
def main_2(filename):
    # Spider example (2 groups)
    sp = get_data_many(filename)
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    t,pval = t_test_dep(fake_sp,real_sp)
    print('t: %s   p_value: %s' % (t,pval))
    r = effect_size_t(t,len(fake_sp)-1)
    print('Effect size:  %s' % r)
    
    min_ = min([np.amin(sp[i,:]) for i in range(len(sp))])
    max_ = max([np.amax(sp[i,:]) for i in range(len(sp))])    
    plt.axis(ymin=min_ - 20, ymax=max_ + 20)
    plt.title('Anxiety to spiders')
    plt.ylabel('Level')
    
    box_plot([fake_sp,real_sp],['Fake','Real'])


def main_22(filename):
    # Spider example (2 groups)
    sp = get_data_many(filename)
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    t,pval = t_test_dep(fake_sp,real_sp)
    print('t: %s   p_value: %s' % (t,pval))
    r = effect_size_t(t,len(fake_sp)-1)
    print('Effect size:  %s' % r)
    histogram(fake_sp, 'Anxiety to spiders','Level','Value',bins=10 )


def main_222(filename):
    # Spider example (2 groups)
    sp = get_data_many(filename)
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    u, p = mann_whitney(fake_sp,real_sp)
    print('u= %f   p = %s' % (u, p))
    t,p = t_test_ind(fake_sp,real_sp)
    print('t= %f   p = %s' % (u, p))

def main_3(filename):
    #Sphere example (3 groups)
    sphere = get_data_many(filename)
    print('Kruskal-Wallis  --> ',kruskal_wallis(sphere))
    print("Friedman's Chi -->  ",friedman_chi(sphere))
    print('Levene -->  ',levene(sphere))    
    print('Indep. ANOVA -->  ', one_way_ind_anova(sphere))  
    
def main_33(filename):
    #Sphere example (3 groups)
    sphere = get_data_many(filename)
    print(levene(sphere))
    print(sphere)
    sphere_df = pd.DataFrame(sphere.T,columns= ['X_1','X_2','X_3'])
    print(sphere_df)
    print('Dep. ANOVA -->  ',one_way_dep_anova(sphere_df))  
    
def main_dep_anova():
    # example data (Andy Field (3rd ed), pg. 464
    insect = [8,9,6,5,8,7,10,12]
    kangaroo = [7,5,2,3,4,5,2,6]
    fish = [1,2,3,1,5,6,7,8]
    grub = [6,5,8,9,8,7,2,1]
   
    data_frame = pd.DataFrame({ "Insect":insect, "Kangaroo":kangaroo, "Fish":fish, "Grub": grub}) 
    f,p = one_way_dep_anova(data_frame)
    display_dep_anova(data_frame,f,p) 
    
def display_dep_anova(data_frame,f,p_val):
    print('Data: \n', data_frame,'\n')
    print('F-ratio: %6.4f\n'%f)
    print('p_value: %6.4f\n'%p_val)
    if p_val < 0.05:
        print('Reject the null hypothesis.[95%]')
    else:
        print('Cannot reject the null hypothesis. [95%]')    
     
if __name__ == '__main__':
    filename_1 = 'pulse_rate.txt'
    #main_1111(filename_1)
    #main_1(filename_1)
    #main_11(filename_1)
    #main_111(filename_1)
    filename_2 = 'spider.txt'
    #main_levene(filename_2)
    #main_2(filename_2)
    #main_22(filename_2)
    #main_222(filename_2)
    filename_3 = 'sphere.txt'
    #main_3(filename_3)
    #main_33(filename_3)
    #main_dep_anova()
    

    
 

  