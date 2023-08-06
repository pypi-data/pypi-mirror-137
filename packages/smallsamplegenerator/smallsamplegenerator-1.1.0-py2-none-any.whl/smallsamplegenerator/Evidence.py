#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This function can achieve the following functions: in the case of a small number of samples, combined
with expert scoring, the method of evidence theory is used to generate data. When the distribution is
"Auto", the optimal distribution form will be selected according to the AIC criterion to calculate the
maximum likelihood estimation and the least square estimation. Compared with the traditional method,
this method can obtain better parameter data under the condition that the number of parameter samples
is small by combining subjective information.
'''

import numpy as np
import scipy.stats as s
from scipy.optimize import fmin
from scipy.optimize import leastsq
from scipy.interpolate import lagrange
import matplotlib.pyplot as plt
import math as math
import sys as sys
import seaborn as sns


def voluntarilyPick(distribution, x, parini):
    """
    choose the best distribution form according to AIC
    :param distribution:distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' , 'LogNorm' or 'Auto'
    :param x:original sample data
    :param parini:initial estimation of the model parameters,should be a binary one-dimensional array
    :return:actual distribution
    """
    exactDistribution = distribution
    if distribution == 'Normal':
        exactDistribution = 'Normal'
    elif distribution == 'Weibull':
        exactDistribution = 'Weibull'
    elif distribution == 'Expon':
        exactDistribution = 'Expon'
    elif distribution == 'LogNorm':
        exactDistribution = 'LogNorm'
    elif distribution == 'Auto':
        parOutWeibull = parMle(x, parini, 'Weibull')
        aicWeibull = -2 * sum(s.exponweib.logpdf(x, 1, parOutWeibull[-1], loc=0, scale=parOutWeibull[0] / math.gamma(1 + 1 / parOutWeibull[-1]))) + 2 * 2
        parOutNormal = parMle(x, parini, 'Normal')
        aicNorm = -2 * sum(s.norm.logpdf(x, parOutNormal[0], parOutNormal[-1])) + 2 * 2
        parOutExpon = parMle(x, parini, 'Expon')
        aicExpon = -2 * sum(s.expon.logpdf(x, scale=1 / parOutExpon[0])) + 2 * 2
        parOutLogNorm = parMle(x, parini, 'LogNorm')
        aicLogNorm = -2 * sum(s.lognorm.logpdf(x, parOutLogNorm[-1], loc=0, scale=1 / np.exp(parOutLogNorm[0]))) + 2 * 2
        if aicNorm == min(aicWeibull, aicNorm, aicExpon, aicLogNorm):
            exactDistribution = 'Normal'
        elif aicWeibull == min(aicWeibull, aicNorm, aicExpon, aicLogNorm):
            exactDistribution = 'Weibull'
        elif aicExpon == min(aicWeibull, aicNorm, aicExpon, aicLogNorm):
            exactDistribution = 'Expon'
        elif aicLogNorm == min(aicWeibull, aicNorm, aicExpon, aicLogNorm):
            exactDistribution = 'LogNorm'
    else:
        print('请输入正确的分布')
        sys.exit(0)
        
    return exactDistribution


def parMle(x, parInitial, distribution):
    """
    parameters extraction using the maximum likelihood method
    :param x:original sample data
    :param parInitial:initial estimation of the model parameters,should be a binary one-dimensional array
    :param distribution:distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' or 'LogNorm'
    :return:optimal values of the model parameters using MLE
    """
    def likelihoodFunction(pars):
        if distribution == 'Normal':
            logmle = - sum(s.norm.logpdf(x, pars[0], pars[-1]))
        elif distribution == 'Weibull':
            logmle = - sum(s.exponweib.logpdf(x, 1,
                          pars[-1], loc=0, scale=pars[0] / math.gamma(1 + 1 / pars[-1])))
        elif distribution == 'Expon':
            logmle = - sum(s.expon.logpdf(x, scale=1 / pars[0]))
        elif distribution == 'LogNorm':
            logmle = - sum(s.lognorm.logpdf(x, pars[-1], loc=0, scale=1 / np.exp(pars[0])))
        else:
            print('请输入正确的分布')
            sys.exit(0)
        return logmle
    parOutMle = fmin(likelihoodFunction, parInitial, disp=False)

    return parOutMle


def parLeastsq(x, parInitial, distribution):
    """
    parameters extraction using the least squares method
    :param x:original sample data
    :param parInitial:initial estimation of the model parameters,should be a binary one-dimensional array
    :param distribution:distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' or 'LogNorm'
    :return:optimal values of the model parameters using Leastsqures
    """
    x = np.array(x)
    x.sort()
    parInitial = np.asarray(parInitial)

    def F(x, distribution):
        if distribution == 'Weibull':
            x1 = np.log(x)
            F = np.log(
                np.log(1 / (1 - (np.arange(0, len(x), 1) + 0.5) / len(x))))
        elif distribution == 'Normal':
            F = x
            x1 = s.norm.ppf(q=((np.arange(0, len(x), 1) + 0.5) / len(x)))
        elif distribution == 'Expon':
            F = np.log(
                np.log(1 / (1 - (np.arange(0, len(x), 1) + 0.5) / len(x))))
            x1 = np.log(x)
        elif distribution == 'LogNorm':
            x = np.log(x)
            F = x
            x1 = s.norm.ppf(q=((np.arange(0, len(x), 1) + 0.5) / len(x)))
        else:
            print('请输入正确的分布')
            sys.exit(0)
        return (x1, F)

    def error(pars, x, y):
        return pars[0] * x + pars[1] - y

    def errorExpon(b1, x, y):
        return x + b1 - y

    parOutIni = leastsq(error, parInitial, args=F(x, distribution))
    parOutIniExpon = leastsq(
        errorExpon, parInitial[1], args=F(x, distribution))
    if distribution == 'Normal':
        parOutLeastsq = (parOutIni[0][-1], parOutIni[0][0])
    elif distribution == 'Weibull':
        parOutLeastsq = (
            np.exp((-parOutIni[0][-1]) / parOutIni[0][0]), parOutIni[0][0])
    elif distribution == 'Expon':
        parOutLeastsq = (np.exp(parOutIniExpon[0]), 1)
    elif distribution == 'LogNorm':
        parOutLeastsq = (-parOutIni[0][-1], parOutIni[0][0])

    return parOutLeastsq


def dempster(x, distribution, parOutMle, parOutLeastsq, y, mode):
    """
    using evidence theory for evidence synthesis
    :param x:original sample data
    :param distribution:distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' or 'LogNorm'
    :param parOutMle:optimal values of the model parameters using MLE
    :param parOutLeastsq:optimal values of the model parameters using Leastsqures
    :param y:expert score,if not, use [1, 1, 1] instead
    :param mode:selection of synthesis method,should be [0,0,0], [1,0,0], [0,1,0], [0,0,1], [1,1,0],
    [1,0,1], [0,1,1] or [1,1,1].Corresponding to [maximum likelihood method information source, least
    square method information source, expert scoring information source], 1 is included, 0 is not included.
    :return:synthetic reliability
    """
    if distribution == 'Normal':
        dataMle = s.norm.pdf(x, parOutMle[0], parOutMle[-1])
        dataLeastsq = s.norm.pdf(x, parOutLeastsq[0], parOutLeastsq[-1])
    elif distribution == 'Weibull':
        dataMle = s.exponweib.pdf(
            x, 1, parOutMle[-1], loc=0, scale=parOutMle[0] / math.gamma(1 + 1 / parOutMle[-1]))
        dataLeastsq = s.exponweib.pdf(
            x, 1, parOutLeastsq[-1], loc=0, scale=parOutLeastsq[0])
    elif distribution == 'Expon':
        dataMle = s.expon.pdf(x, scale=1 / parOutMle[0])
        dataLeastsq = s.expon.pdf(x, scale=1 / parOutLeastsq[0])
    elif distribution == 'LogNorm':
        dataMle = s.lognorm.pdf(
            x, parOutMle[-1], loc=0, scale=1 / np.exp(parOutMle[0]))
        dataLeastsq = s.lognorm.pdf(
            x, parOutLeastsq[-1], loc=0, scale=1 / np.exp(parOutLeastsq[0]))
    else:
        print('请输入正确的分布')
        sys.exit(0)
    dataMle = dataMle / sum(dataMle)
    dataLeastsq = dataLeastsq / sum(dataLeastsq)
    y = np.array(y)
    y = y / sum(y)
    if mode == [0, 0, 0]:
        print('请输入正确的合成方式')
        finalSyntheticReliability = dataMle * dataLeastsq / sum(dataMle * dataLeastsq)
    elif mode == [1, 0, 0]:
        finalSyntheticReliability = dataMle
    elif mode == [0, 1, 0]:
        finalSyntheticReliability = dataLeastsq
    elif mode == [0, 0, 1]:
        finalSyntheticReliability = y
    elif mode == [1, 1, 0]:
        finalSyntheticReliability = dataMle * dataLeastsq / sum(dataMle * dataLeastsq)
    elif mode == [1, 0, 1]:
        finalSyntheticReliability = dataMle * y / sum(dataMle * y)
    elif mode == [0, 1, 1]:
        finalSyntheticReliability = dataLeastsq * y / sum(dataLeastsq * y)
    elif mode == [1, 1, 1]:
        syntheticReliability = dataMle * dataLeastsq / sum(dataMle * dataLeastsq)
        finalSyntheticReliability = syntheticReliability * y / sum(syntheticReliability * y)
    else:
        print('合成方式录入错误')


    return finalSyntheticReliability


def interLagrange(x, finalSyntheticReliability):
    """
    interpolate using Lagrangian interpolation algorithm
    added processing steps for duplicate samples
    :param x:original sample data
    :param finalSyntheticReliability:synthetic reliability
    :return:interpolated point set
    """
    aZero = np.zeros(len(set(x)))
    finalSyntheticReliability = np.array(finalSyntheticReliability)
    t = np.arange(min(np.array(x)), max(np.array(x)), 0.01)
    nonrepeatReliability = []
    num = 0
    for i in set(x):
        for j in range(len(x)):
            if i == x[j]:
                aZero[num] = aZero[num] + finalSyntheticReliability[j]
        num = num+1
    for i in set(x):
        nonrepeatReliability .append(i)
    y = np.maximum(
        lagrange(np.array(nonrepeatReliability), np.array(aZero))(t), 0)

    return (t, y)


def samplingEvcidence(t, y, n):
    """
    sampling algorithm
    :param t:the abscissa of the point set obtained by interpolation
    :param y:the ordinate of the point set obtained by interpolation
    :param n:number of data required
    :return:new data sample generated
    """
    y = y / np.sum(y)
    generatedSample = np.zeros(n)
    sum = np.cumsum(y)
    for i in range(0, n):
        randonNum = np.random.random()
        for j in range(0, len(y)):
            if sum[j] >= randonNum:
                generatedSample[i] = t[j]
                break

    return generatedSample



def getEvidence(x, parInitial, distribution, y, n, mode):
    """
    Main Function
    :param x: original sample data
    :param parInitial: initial estimation of the model parameters,should be a binary one-dimensional array
    :param distribution: distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' or 'LogNorm'
    :param y:expert score,if not, use [1, 1, 1] instead
    :param n:number of data required
    :param mode:selection of synthesis method,should be [0,0,0], [1,0,0], [0,1,0], [0,0,1], [1,1,0],
    [1,0,1], [0,1,1] or [1,1,1].Corresponding to [maximum likelihood method information source, least
    square method information source, expert scoring information source], 1 is included, 0 is not included.
    :return:new data sample generated
    """
    exactDistribution = voluntarilyPick(distribution, x, parInitial)
    parOutMle = parMle(x, parInitial, exactDistribution)
    parOutLeastsq = parLeastsq(x, parInitial, exactDistribution)
    finalSyntheticReliability = dempster(x, exactDistribution, parOutMle, parOutLeastsq, y, mode)
    (a, b) = interLagrange(x, finalSyntheticReliability)
    generatedSample = np.round(samplingEvcidence(a, b, n), 2)
    print('选择的分布为: ', exactDistribution)
    print('生成的样本为: ', generatedSample)

    return generatedSample


if __name__ == '__main__':
    x = [1, 2, 3]
    parini = [1, 1]
    distribution = 'Auto'
    y = [1, 1, 1]
    n = 20
    mode = [1, 1, 1]
    getEvidence(x, parini, distribution, y, n, mode)