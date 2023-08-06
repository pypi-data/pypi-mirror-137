#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This function can realize the following functions: in the case of a small number of samples, use the
traditional probability theory method(MLE) to generate data. When the distribution is "Auto", the optimal
distribution form will be selected according to the AIC criterion.
'''

import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math


def ProbabilityAuto(x, k):
    """
    Choose the best distribution form according to AIC
    :param x:original sample data
    :param k:number of data required
    :return: sample data generated under the chosen distribution
    """
    param1 = ProbabilityParam(x, 'Normal')
    AICNorm = 2*2 - 2*sum(stats.norm.logpdf(x, param1[0], param1[1]))
    param2 = ProbabilityParam(x, 'Lognormal')
    AICLognormal = 2*2 - 2 * sum(stats.lognorm.logpdf(x, param2[0], param2[1], param2[2]))
    param3 = ProbabilityParam(x, 'Weibull')
    AICWeibull = 2*2 - 2 * sum(stats.exponweib.logpdf(x, 1, param3[1], loc=0, scale=param3[3]))
    param4 = ProbabilityParam(x, 'Expon')
    AICExpon = 2*2 - 2*sum(stats.expon.logpdf(x, scale=param4[1]))
    minAIC = min(AICNorm, AICLognormal, AICWeibull, AICExpon)
    if minAIC == AICNorm:
        distribution = 'Normal'
    if minAIC == AICLognormal:
        distribution = 'Lognormal'
    if minAIC == AICWeibull:
        distribution = 'Weibull'
    if minAIC == AICExpon:
        distribution = 'Expon'

    return getProbability(x, distribution, k)


def ProbabilitySampling(x, distribution, k):
    """
    Sampling Algorithm
    :param x:original sample data
    :param distribution:distribution used in the MLE method,should be 'Uniform', 'Normal' , 'Weibull' , 'Expon' or 'Lognormal'
    :param k:number of data required
    :return:new data sample generated
    """
    min = np.min(x)
    max = np.max(x)
    if min == max:
        return [min for _ in range(k)]

    if distribution == 'Uniform':
        return [np.round(random.uniform(min, max), 2)for _ in range(k)]

    if distribution == 'Normal':
        param = ProbabilityParam(x, 'Normal')
        return [np.round(random.normalvariate(param[0], param[1]), 2)for _ in range(k)]

    if distribution == 'Lognormal':
        s, loc, scale = ProbabilityParam(x, 'Lognormal')
        return [np.round(random.lognormvariate(math.log(scale), s), 2)for _ in range(k)]

    if distribution == 'Weibull':
        param = ProbabilityParam(x, 'Weibull')
        return [np.round(random.weibullvariate(param[3], param[1]), 2)for _ in range(k)]

    if distribution == 'Expon':
        param = ProbabilityParam(x, 'Expon')
        return [np.round(random.expovariate(1/param[1]), 2)for _ in range(k)]


def ProbabilityParam(x, distribution):
    """
    Parametric Fitting Function
    :param x:original sample data
    :param distribution:distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' or 'Lognormal'
    :return:fitted parameter values
    """
    if distribution == 'Normal':
        return [np.mean(x), np.std(x)]

    if distribution == 'Lognormal':
        s, loc, scale = stats.lognorm.fit(x, floc=0)
        return [s, loc, scale]

    if distribution == 'Weibull':
        WeibullParam = stats.exponweib.fit(x, floc=0, f0=1)
        return WeibullParam

    if distribution == 'Expon':
        ExponParam = stats.expon.fit(x, floc=0)
        return ExponParam


def getProbability(x, distribution, k):
    """
    Main function, calculate and print the result.
    :param x: original sample data
    :param distribution: distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' , 'Lognormal' or 'Auto'
    :param k: number of data required
    :return: new data sample generated
    """
    if distribution == 'Auto':
        return ProbabilityAuto(x, k)

    print('选择的分布为: ', distribution)
    print('生成的样本为: ', ProbabilitySampling(x, distribution, k))
    return ProbabilitySampling(x, distribution, k)


if __name__ == '__main__':
    x = [77.05, 36.8, 114.07, 46.35, 44.41,
         35.1, 92.01, 197.42, 76.82, 16.95, 18.5]
    distribution = 'Auto'
    k = 11
    getProbability(x, distribution, k)
