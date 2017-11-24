# coding:utf-8
import os
import random
import sys


'''
不知道采样个数n时，想要均匀采样k个的方法！
(只有k个存储空间限制的情况下)
若sample各不相同，则最终被选取的概率应为k/n

假设:
1. k<=n
2. 第i次的sample，最终接受它的概率为p(i)
3. 若已经有k个samples采用，则随机选一个剔除然后接受新的sample

采样方法:
1. i<=k, approve
2. i>k, approve with the probability of  k/i

证明：
对于前k个sample中任意一个sample，最终approved的概率为：
k/n = [1-p(k+1)/k] * [1-p(k+2)/k] ... * [1-p(n)/k]   ... (1)
注： p(i)*((k-1)/k)+1-p(i) 化简得 1-p(i)/k

对于i>k的任意一个sample，最终approved的概率为：
k/n = p(i) * [1-p(i+1)/k] * ... * [1-p(n)/k]         ... (2)

连立(1),(2),得
p(k+1)=k/(k+1)
...
p(n)=k/n

第i次的sample，最终接受它的概率为:
    p(i) = k/i

决定了p(i),则无论采样个数多少，则最终采用的

'''


class Sampling(object):

    def __init__(self, k):
        self.samples = []
        self.k = k
        self.tick = 0

    def sampling(self):
        return self.samples

    def read(self, sample):
        # processing
        self.processing(sample)
        assert len(self.samples) <= self.k, "Overflow"

    def approve(self, sample):
        idx = random.randint(0, self.k - 1)
        self.samples[idx] = sample

    def processing(self, sample):
        self.tick += 1
        if len(self.samples) < self.k:
            self.samples.append(sample)
        elif random.randint(1, self.tick) <= self.k:
            self.approve(sample)
        else:
            pass


class Stat(object):

    def __init__(self, T, N, k):
        """ Repeat T trials,
        each trial will read N characters and return k samples
        """
        self.T = T
        self.N = N
        assert 1 <= k <= 25
        assert k <= N
        self.k = k
        self.source = {}

    def stream(self):
        sampler = Sampling(self.k)
        for i in range(self.N):
            delta = random.randint(0, 10)
            c = chr(ord('A') + delta)
            if c not in self.source:
                self.source[c] = 1
            else:
                self.source[c] += 1
            sampler.read(c)
        return sampler

    def count(self):
        cnt = {}
        for t in range(self.T):
            sampler = self.stream()
            samples = sampler.sampling()
            for s in samples:
                if s in cnt:
                    cnt[s] += 1
                else:
                    cnt[s] = 1
        return cnt

    def statistic(self):

        cnt = self.count()
        total = sum(cnt.values())
        print "total: ", total
        for k, v in sorted(cnt.items()):
            print "%c %d %0.3f" % (k, v, float(v) / total)

        total = sum(self.source.values())
        print "source total: ", total
        for k, v in sorted(self.source.items()):
            print "%c %d %0.3f" % (k, v, float(v) / total)

if __name__ == '__main__':
    stat_char = Stat(100000, 10, 5)
    stat_char.statistic()
