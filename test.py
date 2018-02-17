import opencorpora
import pymorphy2

class countHelper:
    categories = [
        '_POS',  # Part of Speech, часть речи
        'animacy',  # одушевленность
        'aspect',  # вид: совершенный или несовершенный
        'case',  # падеж
        'gender',  # род (мужской, женский, средний)
        'involvement',  # включенность говорящего в действие
        'mood',  # наклонение (повелительное, изъявительное)
        'number',  # число (единственное, множественное)
        'person',  # лицо (1, 2, 3)
        'tense',  # время (настоящее, прошедшее, будущее)
        'transitivity',  # переходность (переходный, непереходный)
        'voice',  # залог (действительный, страдательный)
        'lemma'
    ]
    def __init__(self):
        self.categories = {}
        self.sentStatus = None
        for category in countHelper.categories:
            self.categories[category] = {'total': 0, 'correct': 0, 'sent': 0, 'correctSent': 0}

    def constructInitialSentDict(self):
        tmp = {}
        for category in countHelper.categories:
            tmp[category] = None
        return tmp

    def registerAssertion(self, category, status):
        self.categories[category]['total'] += 1
        self.categories[category]['correct'] += int(status)
        was = self.sentStatus.get(category, None)
        if was is None:
            self.sentStatus[category] = status
        else:
            if was:
                self.sentStatus[category] &= status
            else:
                pass

    def startSentence(self):
        if self.sentStatus is not None:
            for category in self.sentStatus:
                if self.sentStatus[category] is None:
                    continue
                else:
                    self.categories[category]['sent'] += 1
                    self.categories[category]['correctSent'] += int(self.sentStatus[category])
        self.sentStatus = self.constructInitialSentDict()



# from tokenizer.xtok.py import
morph = pymorphy2.MorphAnalyzer(result_type=None)
corpus = opencorpora.load('annot.opcorpora.no_ambig.xml')
print("Всего документов: ",len(corpus.docs))
counter = countHelper()
tokenCounter = 0
for doc in corpus.docs[1:]:
    # print(doc.source)
    for sentence in doc.sentences:
        counter.startSentence()
        for tokenCorpora in sentence.tokens:
            """:type tokenCorpora: opencorpora.Token"""
            tokenCounter += 1
            tokenMorphy = morph.parse(tokenCorpora.source)[0]
            corporaTagFromMorphy = tokenMorphy[1]
            counter.registerAssertion('lemma', tokenMorphy[2] == tokenCorpora.lemma)
            for cat in countHelper.categories:
                if cat == 'lemma':
                    continue
                attr = getattr(corporaTagFromMorphy, cat)
                if attr is not None:
                    status = str(attr) in tokenCorpora.grammemes
                    counter.registerAssertion(cat, status)
    # break
counter.startSentence()
map = {
    'lemma': 'Лемма',
    '_POS':'Часть речи',  # Part of Speech, часть речи
    'animacy': 'Одушевленность',  # одушевленность
    'aspect': 'Вид',  # вид: совершенный или несовершенный
    'case': 'Падеж',  # падеж
    'gender': 'Род',  # род (мужской, женский, средний)
    'involvement': 'включенность говорящего в действие',  # включенность говорящего в действие
    'mood':'Наклонение',  # наклонение (повелительное, изъявительное)
    'number':'Число',  # число (единственное, множественное)
    'person': 'Лицо',  # лицо (1, 2, 3)
    'tense': 'Время',  # время (настоящее, прошедшее, будущее)
    'transitivity': 'Переходность',  # переходность (переходный, непереходный)
    'voice':'Залог'  # залог (действительный, страдательный)
}
print("Всего токенов: "+str(tokenCounter))
for category in counter.categories:
    rez = counter.categories[category]
    print(map[category]+":")
    print("Всего токенов: "+str(rez['total'])+", всего предложений: "+str(rez['sent']))
    print("Правильно токенов: "+str(rez['correct'])+", правильно предложений: "+str(rez['correctSent']))
    accSent = round(rez['correctSent'] / rez['sent'], 3) if rez['sent'] != 0 else "не определена"
    accTokens = round(rez['correct'] / rez['total'],3) if rez['total'] != 0 else "не определена"
    print("Точность по токенам: "+str(accTokens)+", точность по предложениям: "+str(accSent))
    print("")
    print("")

print(counter.categories)
