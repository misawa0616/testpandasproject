from django.shortcuts import render
import pandas as pd
from .forms import DocumentForm
import io


def model_form_upload(request):

	# POSTメソッドの場合、True
    if request.method == 'POST':

    	# フォームに入力された値にエラーがない場合,TRUEとする。
        #form = DocumentForm(request.POST, request.FILES)

        # pandasでxlsxファイルを読み込む。
        img_read = request.FILES['image'].read()
        cc = io.BytesIO(img_read)
        df = pd.read_excel(cc, dtype=str, keep_default_na=False)

        # 1.時刻形式をYY:MM:DDに整形
        # 2.アップロードファイルから取得したカラムを、DBに登録できるよう修正
        # 3.jsonに変換
        df['お誕生日(せいれき)'] = df['お誕生日(せいれき)'].replace('(.*) 00:00:00(.*)', r'\1', regex=True)
        df = df.rename(columns={'お誕生日(せいれき)': 'birthday', '名': 'lastname', '姓': 'firstname'})
        print(df)
        after_json = df.to_json(orient='records', force_ascii=False)
        print(after_json)
        
        #if form.is_valid():
        result = 'アップロードに成功しました'
        form = DocumentForm()
        return render(request, 'testpandas/model_form_upload.html', { 'result': result, 'form': form} )
        #else:
        #    result = 'アップロードエラー'
        #    return render(request, 'inuneko3/model_form_upload.html', { 'result': result})
    else:
        form = DocumentForm()
        # POSTメソッド以外の場合、そのままmodel_form_upload.htmlへ移動する。
        return render(request, 'testpandas/model_form_upload.html', { 'form': form} )