from django import forms
class TreeForm(forms.Form):
     par1 = forms.IntegerField(initial=4,label='Минимальное число объектов', widget=forms.NumberInput(attrs={"class": "field__input"}))
     par2 = forms.IntegerField(initial=53, label='Максимальная глубина', widget=forms.NumberInput(attrs={"class": "field__input"}))

class kForm(forms.Form):
     par1 = forms.IntegerField(initial=121,label='Количество соседий', widget=forms.NumberInput(attrs={"class": "field__input"}))
class text(forms.Form):
     choices = (("alt.atheism", "Атеизм"), ("comp.graphics", "Графика"), ("comp.os.ms-windows.misc", "Windows разное") ,("comp.sys.ibm.pc.hardware","IBM железо"),('comp.sys.mac.hardware','Mac железо'),
                ('comp.windows.x','Windows X'),('misc.forsale','Распродажа'),("rec.autos",'Авто'),('rec.motorcycles','Мотоциклы'),('rec.sport.baseball','Бейсбол'),
                ('rec.sport.hockey','Хокей'),('sci.crypt','Криптография'),('sci.electronics','Электроника'),('sci.med','Медицина'),('sci.space','Космос'),('soc.religion.christian','Христианство'),
                ('talk.politics.guns','Оружие'),('talk.politics.mideast','Ближний восток'),('talk.politics.misc','Политика разное'),('talk.religion.misc','Религия разное'))
     categories = forms.MultipleChoiceField(choices=choices, label='Выберете темы')
     kol_slov_v_slovare = forms.IntegerField(label="Количество слов в словаре", widget=forms.NumberInput(attrs={"class": "field__input"}))
     required_css_class = "field"

# alt.atheism',
#  'comp.graphics',
#  'comp.os.ms-windows.misc',
#  'comp.sys.ibm.pc.hardware',
#  'comp.sys.mac.hardware',
#  'comp.windows.x',
#  'misc.forsale',
#  'rec.autos',
#  'rec.motorcycles',
#  'rec.sport.baseball',
#  'rec.sport.hockey',
#  'sci.crypt',
#  'sci.electronics',
#  'sci.med',
#  'sci.space',
#  'soc.religion.christian',
#  'talk.politics.guns',
#  'talk.politics.mideast',
#  'talk.politics.misc',
#  'talk.religion.misc']