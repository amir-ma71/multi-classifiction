import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer , TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.externals import joblib
from pycm import *

import re


# read Data
data = pd.read_csv("data10classen.csv", encoding="utf-8")

# ########....pre processing....##########

stop_words = [ '!' , '!!' , '!!!' , '!!!!' , '!!!!!' , '!؟' , '#' , '$' , '%' , '&' , '(' , ')' , '*' , '+' , ',' , '-' , '.' , '/' ,
         '0' , '1' , '2' , '3' , '4' , '5' , '6' , '60' , '7' , '8' , '9' , ':' , ';' , '< ' , '<< ' , '<< ' , '< ' , '=' ,
         '> ' , '>> ' , '>> ' , '> ' , '?' , '@' , 'A' , 'B' , 'C' , 'D' , 'E' , 'F' , 'G' , 'H' , 'I' , 'J' , 'K' , 'L' ,
         'M' , 'N' , 'O' , 'P' , 'Q' , 'R' , 'S' , 'T' , 'U' , 'V' , 'W' , 'X' , 'Y' , 'Z' , '^' , '_' , '_-' , 'a' , 'b' ,
         'c' , 'd' , 'e' , 'f' , 'g' , 'h' , 'http' , 'https' , 'i' , 'j' , 'k' , 'l' , 'm' , 'n' , 'o' , 'p' , 'q' , 'r' ,
         's' , 't' , 'u' , 'v' , 'w' , 'www' , 'x' , 'y' , 'z' , '{' , '}' , '«' , '»' , '،' , '؛' , '؟' , '؟!' , '؟!!' ,
         '؟؟' , '؟؟؟' , '؟؟؟؟' , 'ء' , 'آ' , 'آخرین' , 'آخه' , 'آره' , 'آری' , 'آقای' , 'آمد' , 'آمدن' , 'آمدند' , 'آمده' ,
         'آمده_است' , 'آن' , 'آنان' , 'آنجا' , 'آنرا' , 'آنقدر' , 'آنكه' , 'آنها' , 'آنهایی' , 'آنهم' , 'آنوقت' , 'آنچه' ,
         'آنکه' , 'آن‌ها' , 'آور' , 'آورد' , 'آوردن' , 'آوردند' , 'آورده' , 'آوردیم' , 'آوری' , 'آی' , 'آیا' , 'آید' , 'أ' ,
         'ؤ' , 'إ' , 'ئ' , 'ا' , 'ابتدا' , 'ات' , 'اثر' , 'اثرِ' , 'اخیر' , 'اخیرا' , 'از' , 'ازت' , 'ازش' , 'ازشون' , 'ازین' ,
         'اس' , 'است' , 'استفاد' , 'استفاده' , 'اش' , 'اصن' , 'اغلب' , 'اف' , 'افتاد' , 'افتادم' , 'افتادن' , 'افتاده' ,
         'افزود' , 'اقای' , 'اكنون' , 'ال' , 'الآن' , 'الان' , 'الانم' , 'البته' , 'البتّه' , 'الف' , 'الی' , 'ام' , 'اما' ,
         'امر' , 'امروز' , 'امسال' , 'امور' , 'امکان' , 'ان' , 'انجام' , 'اند' , 'انداخته' , 'انقدر' , 'انها' , 'انکه' ,
         'انگار' , 'انگیز' , 'او' , 'اوست' , 'اول' , 'اولین' , 'اومد' , 'اومدن' , 'اومده' , 'اون' , 'اونا' , 'اونایی' ,
         'اونقدر' , 'اونم' , 'اونها' , 'اونوقت' , 'اونی' , 'اکنون' , 'اگر' , 'اگرچه' , 'اگه' , 'ای' , 'ایا' , 'ایشان' ,
         'ایشون' , 'ایم' , 'این' , 'اینا' , 'اینایی' , 'اینبار' , 'اینجا' , 'اینجاست' , 'اینجور' , 'اینجوری' , 'اینطور' ,
         'اینقدر' , 'اینقد' , 'اینكه' , 'اینم' , 'اینه' , 'اینها' , 'اینهمه' , 'اینو' , 'اینک' , 'اینکه' , 'اینگونه' , 'این‌ها' ,
         'ایی' , 'ای‌ها' , 'ب' , 'با' , 'بابت' , 'بار' , 'بارة' , 'باره' , 'باز' , 'بازخواهیم' , 'بازم' , 'باش' , 'باشد' ,
         'باشم' , 'باشند' , 'باشه' , 'باشی' , 'باشید' , 'باشیم' , 'باشین' , 'باعث' , 'بالا' , 'بالایِ' , 'بان' , 'باهم' ,
         'باید' , 'ببرد' , 'ببرن' , 'ببرند' , 'ببره' , 'ببرید' , 'ببریم' , 'ببینم' , 'ببینن' , 'ببینند' , 'ببینه' , 'ببینید' ,
         'ببینیم' , 'بتواند' , 'بتوانند' , 'بجز' , 'بخواد' , 'بخوان' , 'بخواهد' , 'بخواهند' , 'بخورن' , 'بخوره' , 'بداند' ,
         'بدانند' , 'بدانید' , 'بدانیم' , 'بدلیل' , 'بدم' , 'بده' , 'بدهد' , 'بدهند' , 'بدهید' , 'بدهیم' , 'بدون' , 'بدید' ,
         'بدیم' , 'بدین' , 'بذارن' , 'بذاره' , 'بر' , 'برا' , 'برابر' , 'برابرِ' , 'براساس' , 'براش' , 'براشون' , 'برامون' ,
         'برای' , 'برایت' , 'برایش' , 'برایِ' , 'برخوردار' , 'برخی' , 'برداری' , 'برداشتن' , 'بردن' , 'بردند' , 'برسد' ,
         'برسه' , 'برم' , 'برمی' , 'برن' , 'بره' , 'برو' , 'برود' , 'بروز' , 'بروند' , 'بروید' , 'برگرده' , 'بری' , 'برید' ,
         'بریم' , 'بزن' , 'بزنن' , 'بزنند' , 'بزنه' , 'بزنی' , 'بزنید' , 'بزنیم' , 'بس' , 'بستن' , 'بسیار' , 'بسیاری' ,
         'بشم' , 'بشه' , 'بشود' , 'بشیم' , 'بطور' , 'بعد' , 'بعداز' , 'بعری' , 'بعضی' , 'بفرستید' , 'بفرمایید' , 'بلكه' ,
         'بله' , 'بلکه' , 'بلی' , 'بماند' , 'بن' , 'بنا' , 'بنابراین' , 'بندازن' , 'بندی' , 'بنظرم' , 'بنی' , 'به' , 'بهت' ,
         'بهتر' , 'بهترین' , 'بهتون' , 'بهش' , 'بهشون' , 'بهم' , 'بود' , 'بودم' , 'بودن' , 'بودند' , 'بوده' , 'بوده_است' ,
         'بوده_اند' , 'بودید' , 'بودیم' , 'بکشند' , 'بکشه' , 'بکند' , 'بکنن' , 'بکنند' , 'بکنه' , 'بکنید' , 'بکنیم' ,
         'بگذارد' , 'بگذارند' , 'بگذارید' , 'بگذاریم' , 'بگم' , 'بگن' , 'بگه' , 'بگو' , 'بگوید' , 'بگویم' , 'بگویند' ,
         'بگویید' , 'بگوییم' , 'بگی' , 'بگید' , 'بگیر' , 'بگیرد' , 'بگیرم' , 'بگیرن' , 'بگیرند' , 'بگیره' , 'بگیری' ,
         'بگیرید' , 'بگیریم' , 'بگیم' , 'بی' , 'بیا' , 'بیاد' , 'بیارن' , 'بیاره' , 'بیان' , 'بیاورد' , 'بیاورند' , 'بیاید' ,
         'بیایند' , 'بیایید' , 'بیرون' , 'بیرونِ' , 'بیست' , 'بیش' , 'بیشتر' , 'بیشتری' , 'بیفته' , 'بین' , 'ة' , 'ت' ,
         'تا' , 'تازه' , 'تاكنون' , 'تان' , 'تاکنون' , 'تبدیل' , 'تحت' , 'ترتیب' , 'ترین' , 'تعیین' , 'تغییر' , 'تمام' ,
         'تمامی' , 'تن' , 'تو' , 'توان' , 'تواند' , 'توانست' , 'توانستن' , 'توانند' , 'توسط' , 'تولِ' , 'تون' , 'توی' ,
         'تویِ' , 'تی' , 'ث' , 'ج' , 'جا' , 'جای' , 'جایی' , 'جدا' , 'جدی' , 'جز' , 'جلویِ' , 'جناح' , 'جهت' , 'جوری' , 'ح' ,
         'حاضر' , 'حال' , 'حالا' , 'حالی' , 'حالیکه' , 'حتما' , 'حتی' , 'حد' , 'حداقل' , 'حدود' , 'حدودِ' , 'حل' , 'خ' , 'خاص' ,
         'خاطرنشان' , 'خان' , 'خب' , 'خصوص' , 'خواست' , 'خواستار' , 'خواستن' , 'خواستند' , 'خوانده' , 'خواه' , 'خواهد' ,
         'خواهد_بود' , 'خواهد_داد' , 'خواهد_داشت' , 'خواهد_شد' , 'خواهد_کرد' , 'خواهد_گرفت' , 'خواهند' , 'خواهند_شد' ,
         'خواهند_کرد' , 'خواهیم' , 'خواهیم_بود' , 'خواهیم_کرد' , 'خود' , 'خودت' , 'خودتون' , 'خودش' , 'خودشو' , 'خودشون' ,
         'خودم' , 'خودمون' , 'خور' , 'خورد' , 'خورده' , 'خوندن' , 'خویش' , 'خیاه' , 'خیلی' , 'د' , 'داد' , 'دادم' , 'دادن' ,
         'دادند' , 'داده' , 'داده_است' , 'داده_اند' , 'داده_بود' , 'داده_شد' , 'دادی' , 'دادید' , 'دادیم' , 'دار' , 'دارای' ,
         'دارد' , 'دارم' , 'دارند' , 'داره' , 'داری' , 'دارید' , 'داریم' , 'دارین' , 'داشت' , 'داشتم' , 'داشتن' , 'داشتند' ,
         'داشته' , 'داشته_است' , 'داشته_اند' , 'داشته_باشد' , 'داشته_باشند' , 'داشته_باشید' , 'داشته_باشیم' , 'داشتیم' ,
         'دانست' , 'دانند' , 'در' , 'دراین' , 'درباره' , 'درحالیکه' , 'درون' , 'دری' , 'دسته' , 'دنبالِ' , 'ده' , 'دهد' ,
         'دهند' , 'دهنده' , 'دهه' , 'دهید' , 'دهیم' , 'دو' , 'دوباره' , 'دور' , 'دوم' , 'دچار' , 'دیدن' , 'دیده' , 'دیدید' ,
         'دیدیم' , 'دیگر' , 'دیگران' , 'دیگری' , 'دیگه' , 'دیگه‌ای' , 'ذ' , 'ذیل' , 'ر' , 'را' , 'رابه' , 'راه' , 'رسانده' ,
         'رسید' , 'رسیدن' , 'رسیده_است' , 'رسیدیم' , 'رفت' , 'رفتم' , 'رفتن' , 'رفتند' , 'رفته' , 'رفته_است' , 'رفتی' ,
         'رفتیم' , 'ره' , 'رو' , 'روب' , 'روبه' , 'روز' , 'روزهای' , 'روش' , 'روند' , 'روی' , 'رویِ' , 'ز' , 'زاد' ,
         'زاده' , 'زد' , 'زدم' , 'زدن' , 'زدند' , 'زده' , 'زده_اند' , 'زدیم' , 'زمانی' , 'زمینه' , 'زیاد' , 'زیادی' ,
         'زیر' , 'زیرا' , 'زیرِ' , 'س' , 'ساختن' , 'ساخته' , 'ساز' , 'سازی' , 'ساله' , 'سال‌های' , 'سایر' , 'سبب' , 'ست' ,
         'سراسر' , 'سریِ' , 'سعی' , 'سمت' , 'سمتِ' , 'سه' , 'سهم' , 'سوم' , 'سوی' , 'سویِ' , 'سپس' , 'سی' , 'ش' , 'شامل' ,
         'شان' , 'شاید' , 'شد' , 'شدم' , 'شدن' , 'شدند' , 'شده' , 'شده_است' , 'شده_اند' , 'شده_بود' , 'شده_بودند' , 'شدگان' ,
         'شدی' , 'شش' ,'شما' , 'شمار' , 'شماها' , 'شنیدم' , 'شه' , 'شو' ,
         'شود' , 'شون' , 'شوند' , 'شوید' , 'شویم' , 'ص' , 'صرف' , 'ض' ,
         'ضدِّ' , 'ضمن' , 'ط' , 'طبق' , 'طبقِ' , 'طرف' , 'طریق' , 'طور' , 'طوری' , 'طول' , 'طی' , 'ظ' , 'ظاهرا' , 'ع' , 'عالی' ,
         'عدم' , 'عقبِ' , 'علاوه' , 'علت' , 'علّتِ' , 'علیه' , 'عنوان' , 'عنوانِ' , 'عهده' , 'عین' , 'غ' , 'غیر' , 'ف' , 'فرد' ,
         'فردی' , 'فرستاد' , 'فرمود' , 'فرمودند' , 'فرموده_اند' , 'فعلا' , 'فقط' , 'فهمید' , 'فهمیدم' , 'فوق' , 'ق' , 'قابل' ,
         'قبل' , 'قبلا' , 'قرار' , 'قصدِ' , 'ك' , 'كرد' , 'كردم' , 'كردن' , 'كردند' , 'كرده' , 'كسی' , 'كل' , 'كمتر' , 'كند' ,
         'كنم' , 'كنند' , 'كنید' , 'كنیم' , 'كه' , 'ل' , 'لازم' , 'لحاظ' , 'لذا' , 'لطفاً' , 'م' , 'ما' , 'مان' , 'ماند' ,
         'ماندن' , 'مانده' , 'مانند' , 'مانندِ' , 'مبنی' , 'متر' , 'متوجه' , 'مث' , 'مثل' , 'مثلا' , 'مثلِ' , 'مثه' , 'محسوب' ,
         'مختلف' , 'مدت' , 'مدّتی' , 'مرا' , 'مربوط' , 'مشخص' , 'مقابل' , 'ممکن' , 'من' , 'مناسب' , 'منظور' , 'منم' , 'منو' ,
         'مهم' , 'مواجه' , 'موارد' , 'موجب' , 'مورد' , 'مون' , 'موندم' , 'مونده' , 'مگر' , 'مگه' , 'می' , 'میاد' , 'میارن' ,
         'میاره' , 'میان' , 'میباشد' , 'میبره' , 'میبینم' , 'میتوان' , 'میتواند' , 'میتوانند' , 'میتوانیم' , 'میتونه' ,
         'میخواد' , 'میخواست' , 'میخوام' , 'میخوان' , 'میخواهد' , 'میخواهند' , 'میخواهید' , 'میخوای' , 'میخورن' , 'میخوره' ,
         'میداد' , 'میدادن' , 'میداند' , 'میدانند' , 'میدانید' , 'میدم' , 'میدن' , 'میده' , 'میدهد' , 'میدهند' , 'میدونم' ,
         'میدونن' , 'میدونه' , 'میدونید' , 'میدیم' , 'میذارن' , 'میرسد' , 'میرسه' , 'میرفت' , 'میرم' , 'میرن' , 'میره' ,
         'میرود' , 'میری' , 'میریم' , 'میزد' , 'میزند' , 'میزنن' , 'میزنند' , 'میزنه' , 'میزنی' , 'میشد' , 'میشن' ,
         'میشه' , 'میشود' , 'میشوند' , 'میشیم' , 'میفته' , 'میمونه' , 'میندازن' , 'میندازه' , 'میومد' , 'میکرد' , 'میکردم' ,
         'میکردن' , 'میکردند' , 'میکردیم' , 'میکشن' , 'میکشه' , 'میکند' , 'میکنم' , 'میکنن' , 'میکنند' , 'میکنه' , 'میکنی' ,
         'میکنید' , 'میکنیم' , 'میگفت' , 'میگفتن' , 'میگم' , 'میگن' , 'میگه' , 'میگوید' , 'میگویند' , 'میگی' , 'میگیرد' ,
         'میگیرن' , 'میگیرند' , 'میگیره' , 'میگیم' , 'می‌آورد' , 'می‌آید' , 'می‌افتد' , 'می‌باشد' , 'می‌باشند' , 'می‌برد' ,
         'می‌برند' , 'می‌بینند' , 'می‌توان' , 'می‌تواند' , 'می‌توانند' , 'می‌توانید' , 'می‌تونه' , 'می‌خواد' , 'می‌خواست' , 'می‌خوان' ,
         'می‌خواهد' , 'می‌خواهند' , 'می‌خواهیم' , 'می‌خورد' , 'می‌داد' , 'می‌دادند' , 'می‌داند' , 'می‌دانم' , 'می‌دانند' , 'می‌دانید' ,
         'می‌ده' , 'می‌دهد' , 'می‌دهم' , 'می‌دهند' , 'می‌دهیم' , 'می‌رسد' , 'می‌رفت' , 'می‌رود' , 'می‌روند' , 'می‌زند' , 'می‌زنند' ,
         'می‌شد' , 'می‌شه' , 'می‌شود' , 'می‌شوند' , 'می‌شویم' , 'می‌ماند' , 'می‌کرد' , 'می‌کردم' , 'می‌کردن' , 'می‌کردند' , 'می‌کردیم' ,
         'می‌کشد' , 'می‌کند' , 'می‌کنم' , 'می‌کنن' , 'می‌کنند' , 'می‌کنه' , 'می‌کنی' , 'می‌کنید' , 'می‌کنیم' , 'می‌گذرد' , 'می‌گردد' ,
         'می‌گفت' , 'می‌گفتند' , 'می‌گن' , 'می‌گه' , 'می‌گوید' , 'می‌گویم' , 'می‌گویند' , 'می‌گیرد' , 'می‌گیرند' , 'می‌گیره' , 'می‌یابد' ,
         'ن' , 'ناشی' , 'نام' , 'نباشد' , 'نباشند' , 'نباشه' , 'نباشید' , 'نباید' , 'نبود' , 'نبودن' , 'نبودند' , 'نبوده' ,
         'نبوده_است' , 'نتوانست' , 'نحوه' , 'نخریدن' , 'نخست' , 'نخواهد' , 'نخواهد_بود' , 'نخواهد_داشت' , 'نخواهد_شد' ,
         'نخواهد_کرد' , 'نداد' , 'ندادن' , 'ندادند' , 'نداده' , 'ندارد' , 'ندارم' , 'ندارن' , 'ندارند' , 'نداره' , 'نداری' ,
         'ندارید' , 'نداریم' , 'نداشت' , 'نداشتن' , 'نداشته' , 'نداشته_باشد' , 'نداشتیم' , 'نده' , 'ندهند' , 'ندهید' ,
         'ندید' , 'نرسیده' , 'نرفته' , 'نره' , 'نزدِ' , 'نزدیک' , 'نزدیکِ' , 'نسبت' , 'نشان' , 'نشد' , 'نشدن' , 'نشده' ,
         'نشده_است' , 'نشست' , 'نشه' , 'نشود' , 'نشوند' , 'نشین' , 'نشینی' , 'نظرم' , 'نظیر' , 'نكرده' , 'نماید' , 'نمایند' ,
         'نمایی' , 'نمایید' , 'نمود' , 'نمودن' , 'نمودند' , 'نموده' , 'نموده_است' , 'نموده_اند' , 'نمی' , 'نمیاد' ,
         'نمیتواند' , 'نمیتونه' , 'نمیخواد' , 'نمیدن' , 'نمیده' , 'نمیدونم' , 'نمیدونه' , 'نمیشد' , 'نمیشه' , 'نمیشود' ,
         'نمیکند' , 'نمیکنم' , 'نمیکنن' , 'نمیکنند' , 'نمیکنه' , 'نمیکنید' , 'نمی‌آید' , 'نمی‌توان' , 'نمی‌تواند' , 'نمی‌توانند' ,
         'نمی‌دانم' , 'نمی‌دانند' , 'نمی‌دهد' , 'نمی‌دهند' , 'نمی‌شد' , 'نمی‌شود' , 'نمی‌کرد' , 'نمی‌کند' , 'نمی‌کنم' , 'نمی‌کنند' ,
         'نمی‌کنه' , 'نمی‌کنید' , 'نمی‌کنیم' , 'نه' , 'نو' , 'نوشت' , 'نوشتن' , 'نکرد' , 'نکردم' , 'نکردن' , 'نکردند' ,
         'نکرده' , 'نکرده_است' , 'نکرده_اند' , 'نکردیم' , 'نکن' , 'نکند' , 'نکنن' , 'نکنند' , 'نکنید' , 'نکنیم' , 'نگاه' ,
         'نگفت' , 'نگو' , 'نگیرید' , 'نیا' , 'نیاد' , 'نیاز' , 'نیز' , 'نیس' , 'نیست' , 'نیستند' , 'نیستید' , 'نیستیم' ,
         'نیمه' , 'ه' , 'ها' , 'هارو' , 'هاست' , 'هاش' , 'های' , 'هایش' , 'هایشان' , 'هایی' , 'هبچ' , 'هر' , 'هرجا' ,
         'هرچند' , 'هرچه' , 'هرچی' , 'هرکس' , 'هرگز' , 'هرگونه' , 'هزار' , 'هست' , 'هستش' , 'هستم' , 'هستن' , 'هستند' ,
         'هستید' , 'هستیم' , 'هفت' , 'هفتم' , 'هم' , 'همان' , 'همش' , 'همه' , 'همه‌ی' , 'همواره' , 'همون' , 'همچنان' ,
         'همچنین' , 'همچون' , 'همچین' , 'همگی' , 'همیشه' , 'همین' , 'همینجوری' , 'همینه' , 'هنوز' , 'هنگامِ' , 'هنگامی' ,
         'هی' , 'هیچ' , 'و' , 'وارد' , 'وجود' , 'ور' , 'وسطِ' , 'وضع' , 'وقتی' , 'وقتیکه' , 'ول' , 'ولی' , 'وگرنه' , 'وگو' ,
         'وی' , 'ى' , 'ي' , 'پ' , 'پاعینِ' , 'پر' , 'پرسید' , 'پس' , 'پی' , 'پیدا' , 'پیش' , 'پیشِ' , 'چ' , 'چرا' , 'چطور' ,
         'چطوری' , 'چقدر' , 'چنان' , 'چند' , 'چندین' , 'چنین' , 'چه' , 'چهار' , 'چهارم' , 'چون' , 'چکار' , 'چگونه' , 'چی' ,
         'چیز' , 'چیزی' , 'چیست' , 'چیه' , 'چیکار' , 'ژ' , 'ک' , 'کامل' , 'کاملا' , 'کجا' , 'کجاست' , 'کجایی' , 'کدام' ,
         'کدوم' , 'کرد' , 'کردم' , 'کردن' , 'کردند' , 'کرده' , 'کرده_است' , 'کرده_اند' , 'کرده_اید' , 'کرده_ایم' ,
         'کرده_بود' , 'کرده_بودند' , 'کردید' , 'کردیم' , 'کردین' , 'کس' , 'کسانی' , 'کسی' , 'کشتن' , 'کشید' , 'کشیدن' ,
         'کشیدند' , 'کل' , 'کلا' , 'کلی' , 'کم' , 'کمتر' , 'کمی' , 'کن' , 'کنار' , 'کنارِ' , 'کند' , 'کنم' , 'کنن' , 'کنند' ,
         'کننده' , 'کنندگان' , 'کنه' , 'کنون' , 'کنونی' , 'کنی' , 'کنید' , 'کنیم' , 'کنین' , 'که' , 'کوچک' , 'کَی' , 'کی' ,
         'گ' , 'گاه' , 'گذاری' , 'گذاشتن' , 'گذاشتند' , 'گذاشته' , 'گذراند' , 'گذشت' , 'گر' , 'گرایی' , 'گردد' , 'گردید' ,
         'گردیده' , 'گرفت' , 'گرفتم' , 'گرفتن' , 'گرفتند' , 'گرفته' , 'گرفته_است' , 'گرفته_اند' , 'گرفته_بود' , 'گرفتیم' ,
         'گروهی' , 'گرچه' , 'گفت' , 'گفتم' , 'گفتن' , 'گفتند' , 'گفته' , 'گفته_است' , 'گفته_اند' , 'گفته_بود' , 'گفته_می‌شود' ,
         'گفتیم' , 'گم' , 'گو' , 'گونه' , 'گوی' , 'گوید' , 'گویند' , 'گیر' , 'گیرد' , 'گیری' , 'ۀ' , 'ی' , 'یا' , 'یابد' ,
         'یادتونه' , 'یادم' , 'یافت' , 'یافته' , 'یافته_است' , 'یعنی' , 'یك' , 'یكدیگر' , 'یكی' , 'یه' , 'یک' , 'یکدیگر' ,
         'یکی' , '0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '…'  , 'به', 'سال', 'عکس', 'به', 'دانلود']


data['text']=data['text'].apply((lambda x: re.sub('[^آ-یا-ی\s]', ' ', x)))   # delete any character except alphabet
data['text']=data['text'].apply((lambda x: re.sub("\s+", " ", x)))           # delete more than one space
data['text']=data['text'].apply((lambda x: re.sub('[\n]', '', x)))           # delete enter
data['text']=data['text'].apply((lambda x: re.sub('[\ـ]', '', x)))           # delete long word exp= ایــــــــران
data['text']=data['text'].apply((lambda x: re.sub(r'[^\w\s]', '', x)))       # delete weird character

# delete stop words
data['text']=data['text'].apply(lambda x: ' '.join([word for word in x.split(' ') if word not in (stop_words)]))

# ###########################################

X= data.text
y = data.jebhe
my_tags = data["jebhe"].unique()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42)
f=list(y_test)



sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])
sgd.fit(X_train, y_train)

y_pred = sgd.predict(X_test)
joblib.dump(sgd, 'SVM_model.pkl')
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred,target_names=my_tags))
print("*************confusion matrix*******************")
cm = ConfusionMatrix(actual_vector=f, predict_vector=y_pred)
print(cm)