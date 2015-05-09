#coding:utf-8
import jieba.posseg as pseg
import pymongo
class InfoHandle(object):

    def __init__(self, sentense):
        self.sentense = sentense
        self.segment = []
        self.segmentpos = []
        self.operation = 0.0
        self.emotion = []
        self.emotiontypedict = {
            'PA': '快乐',
            'PE': '安心',
            'PD': '尊敬',
            'PH': '赞扬',
            'PG': '相信',
            'PB': '喜爱',
            'PK': '祝愿',
            'NA': '愤怒',
            'NB': '悲伤',
            'NJ': '失望',
            'NH': '疚',
            'PF': '思',
            'NI': '慌',
            'NC': '恐惧',
            'NG': '羞',
            'NE': '烦闷',
            'ND': '憎恶',
            'NN': '贬责',
            'NK': '妒忌',
            'NL': '怀疑',
            'PC': '惊奇',
        }
        #数据库连接
        self.conn = pymongo.Connection('202.113.78.6', 27017)
        self.db = self.conn['POASYS']
        self.emotiondict = self.db['emotiondict']

    def sentensemark(self):
        for item in pseg.cut(self.sentense):
            self.segment.append(item.word)
            #词性标注
            dictmark = self.dictwordmark(item.word)
            if(dictmark!=None):
                worddict = {
                    'word': item.word,
                    'flag': item.flag,
                    'meansnum': dictmark['dwordmeans'],
                    'emotiontype': dictmark['demotiontype'],
                    'polar': dictmark['dpolar'],
                    'strength': dictmark['dstength'],
                }
                self.segmentpos.append(worddict) #字典型放入List

                #倾向性标注
                if(worddict['polar']==1):
                    self.operation += worddict['strength']
                if(worddict['polar']==2):
                    self.operation -= worddict['strength']
                #情感类型标注
                self.emotion.append(self.emotiontypedict[worddict['emotiontype']])
            else:
                self.segmentpos.append({'word': item.word, 'flag': item.flag})

    def dictwordmark(self, word):
        if word!=None:
            dictitem = self.emotiondict.find_one({'dword': word})
            return dictitem
        else:
            return None


    '''情感标注'''
    def emotionmark(self, word):
        if self.segment:
            pass








