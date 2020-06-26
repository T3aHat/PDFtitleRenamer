# PDFtitleRenamer  
Rename pdf file name to article title.  
  
  
# 機能  
ウィンドウにDnDでファイルをリネーム候補に追加.フォルダをDnDすると,それ以下のフォルダ階層に含まれるすべての.pdfを追加.  
__add_folder__  
選択したフォルダ以下に含まれるpdfを探索して候補に追加.  
__add_file__  
選択した音声ファイルを候補に追加.  
__delete__  
候補のうち左クリックで選択したpdfを候補から除外.  
__clear__ 
候補をクリア.  
__save__  
pdfファイル名を`title`カラムにある通りにリネーム.  
__Drag and Drop__  
フレーム内にフォルダorファイルをDnDすると,`add_file`or`add_folder`の挙動をする.  
__shift+leftclick(or UpDown button)__  
あるpdfからクリックしたpdfまでを連続して全選択.  
__ctrl+shift+leftclick__  
複数選択したpdfのうち,クリックしたものだけ選択解除.  
__rightclick__  
選択したpdfを候補から削除.  