Изначально на сайте можно выбрать темы (максимум 5) из изначально подготовленного датасета и количество слов в словаре. 
 
![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo1.png)

После нажатия кнопки «Преобразовать» начнется процесс очитски документов при помощи Hadoop и технологии MapReduce и по его окончанию внешний вид сайта изменится.

![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo2.png)
 
Появится просмотр изначального вида документа и преобразованный вид того же документа.
Кнопка «Посмотреть другие данные» изменит представленный документ.
Кнопки «Дерево решений» и «k Ближайших Соседей» отвечают за переключение метода обучения.
При нажатой кнопки «Дерево решений» нам доступен выбор гиперпараметров для обучения алгоритмом «Дерево решений», а также кнопка «Обучить».
При ее нажатии начнется процесс обучения дерева решений при помощи Hadoop и технологии MapReduce, а также кнопка «Обучить» изменится на кнопку «Остановить».
 
![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo3.png)

При ее нажатии процесс обучения остановится и его можно будет продолжить с того же момента на котором он был остановлен. Для этого нужно будет нажать на вновь появившуюся кнопку «Обучить». Если после нажатия кнопки «Остановить» и изменения гиперпараметров обучения, то обучение начнется с самого начала, а все предыдущие результаты будут удалены.
После окончания обучения внешний вид сайта изменится.
 
![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo4.png)

В появившемся поле можно ввести текст и при помощи кнопки «Определить тему» определить к какой теме относится введённой текст.
 
![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo5.png)

При нажатии кнопки «Использовать тестовую выборку» произойдет расчёт Precision и Recall для тестовой выборки.
 
![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo6.png)

При нажатой кнопки «k Ближайших Соседей» нам доступен выбор гиперпараметров для обучения алгоритмом «k Ближайших Соседей», кнопка «Определить тему» и «Использовать тестовую выборку». Данные кнопки работают аналогично тому как описано ранее.
 
![Image alt](https://raw.githubusercontent.com/Tempih/django_hadoop_ml/main/photo/photo7.png)

