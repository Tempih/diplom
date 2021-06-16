import joblib
from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this
from django.http import JsonResponse
from django.shortcuts import render
from .forms import text,TreeForm,kForm
from django.views.generic import View
import sklearn.datasets
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_distances
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from django.http import HttpResponseRedirect
from .tasks import create_task, random_data, learning, prediction, del_dir
from celery.result import AsyncResult
from celery.result import ResultBase
import os
text_clf_2 = False
par1_g, par2_g = 0, 0
text_clf_2_status = 0
status = ''
class_dict ={'alt.atheism': 'Атеизм', 'comp.graphics': 'Графика', 'comp.os.ms-windows.misc': 'Windows разное', 'comp.sys.ibm.pc.hardware': 'IBM железо', 'comp.sys.mac.hardware': 'Mac железо', 'comp.windows.x': 'Windows X', 'misc.forsale': 'Распродажа', 'rec.autos': 'Авто', 'rec.motorcycles': 'Мотоциклы', 'rec.sport.baseball': 'Бейсбол', 'rec.sport.hockey': 'Хокей', 'sci.crypt': 'Криптография', 'sci.electronics': 'Электроника', 'sci.med': 'Медицина', 'sci.space': 'Космос', 'soc.religion.christian': 'Христианство', 'talk.politics.guns': 'Оружие', 'talk.politics.mideast': 'Ближний восток', 'talk.politics.misc': 'Политика разное', 'talk.religion.misc': 'Религия разное'}
class AjaxHandlerView(View):
  def post(self, request):
    global status,twenty_train,z,train_data_tfidf,vect, tfidf, form, twenty_test
    status = request.POST.get("status")
    # if request.is_ajax():
    if status == '0':
        max_features = int(request.POST.get("max_features"))
        form = eval(request.POST.get("categories"))
        print(form)
        pars = create_task.delay(form, max_features)
        return JsonResponse(
                {'text_for': str(pars.get()[0]),
                 'text_preobraz': str(pars.get()[1])})
    elif status == '3':
        z = eval(os.popen("head -n 1 check.txt").read())
        if z[0] == 1:
            dist_for_paste = []
            for i in z[1]:
               dist_for_paste.append(class_dict[i])
            print(dist_for_paste)
            pars = random_data.delay()
            return JsonResponse({"dist_for_paste": dist_for_paste,'text_for': str(pars.get()[0]),
             'text_preobraz': str(pars.get()[1])})
    elif status == '1':
        pars = random_data.delay()
        return JsonResponse(
            {'text_for': str(pars.get()[0]),

             'text_preobraz': str(pars.get()[1])})
    else:
         return JsonResponse(
            {'stat':'ok'})

    # temp = form.cleaned_data.get("categories")
    # print(temp)
    # return JsonResponse({'review': status, "star": int(star)})
  def get(self, request):
    form = text(initial={'kol_slov_v_slovare': 3000})
    context = {'form': form}
    return render(request, 'train.html',context)

def ml(request):
    global text_clf, text_clf_2_status, text_clf_2, par1_g, par2_g
    # form = request.POST.get("status")
    # if form == "Дерево решений":
    #     form_1 = TreeForm(request.POST or None)
    # elif form == "k Ближайших Соседей":
    if request.method == 'GET':
        if status == 'Дерево решений' or status == '0' or status == '3':
            form_1 = TreeForm(request.GET or None)
        elif status == 'k Ближайших Соседей':
            form_1 = kForm(request.GET or None)
        context = {'form': form_1}
        response = render(
            request,
            'k_or_tree.html',
            context
        )
        return response
    if request.method == 'POST':
        stat = request.POST.get("status")
        if stat == '4':
            z = eval(os.popen("head -n 1 check.txt").read())
            if z[2] == 1:
                return JsonResponse(
                    {'stat': 'ok'})
            else:
                if text_clf_2_status == 1:
                    if text_clf_2.ready():
                        text_clf_2_status = 0
                        return JsonResponse(
                            {'stat': 0})
                    return JsonResponse(
                        {'stat': 1})
                elif text_clf_2_status == 2:
                    return JsonResponse(
                        {'stat': 2})
                elif text_clf_2_status == 0:
                    return JsonResponse(
                        {'stat': 0})
        elif stat == 'Дерево решений' or status == 'k Ближайших Соседей':
            pars = request.POST.get("par1")
            par1, par2 = pars.split(",")
            laerning_stat = 0
            if par1_g != par1 or par2_g != par2:
                par1_g, par2_g = par1, par2
                laerning_stat = 1
            text_clf_2 = learning.delay(status, par1, par2, laerning_stat)
            # print(text_clf_2.ready())
            if text_clf_2.ready():
                text_clf_2_status = 2
                return JsonResponse(
                {'stat': 2})
            else:
                text_clf_2_status = 1
                return JsonResponse(
                    {'stat': 1})
def predict(request):
        metod = request.POST.get("metod")
        status = request.POST.get("status")
        pars = request.POST.get("par1")
        text_for_prediction = request.POST.get("text_for_prediction")
        par1, par2 = pars.split(",")
        z = eval(os.popen("head -n 1 check.txt").read())
        if status == "1" and z[3] == 1 and metod == 'Дерево решений':
                result = os.popen("hdfs dfs -cat hdfs://localhost:9000/tree_result/part-00000").read().split('\n')
                result = [eval(result[0]), eval(result[1])]
        elif status == '1' and int(z[4]) == int(par1) and int(z[4]) != 0 and metod == 'k Ближайших Соседей':
                cmd = "rm part-00000"
                os.system(cmd)
                cmd = "hadoop fs -get /knn_test_full/part-00000"
                os.system(cmd)
                res = []
                f = open('/Users/artemmihajlov/PycharmProjects/diplom_web/part-00000', 'r')
                for line in f:
                    res.append(eval(line))
                f.close()
                trans_result = list(map(list, zip(*res)))
                result =  [(metrics.recall_score(trans_result[0], trans_result[1], average="weighted")) * 100,
                        (metrics.precision_score(trans_result[0], trans_result[1], average="weighted")) * 100]
        else:
            result = prediction.delay('''{0}'''.format(text_for_prediction), status, par1, metod)
            result = result.get()
        print(result)
        if status == '0':
            result = class_dict[z[1][int(result)]]
            return JsonResponse(
            {'prediction': result})
        else:
            return JsonResponse(
                {"recall": str(result[0]),"precision": str(result[1])})

def stop(request):
    text_clf_2_status = 0
    job_id = os.popen("mapred job -list  | awk 'NR > 2 { print $1 }'").read()
    cmd = ('hadoop job -kill '+str(job_id).replace('\n',''))
    os.system(cmd)
    del_dir.delay()
    return JsonResponse(
        {'status': "stop"})