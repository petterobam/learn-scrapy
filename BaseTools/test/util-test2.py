# -*- coding:utf-8 -*-
import Parent
from MyUtil import FileTool
from MyUtil import MyStr
def html2markdown(input_file_path, output_file_path):
    html = FileTool.read_utf8(input_file_path)
    mdTxt = MyStr.html2markdown(html)
    FileTool.overwrite(output_file_path, mdTxt)
    

if __name__ == '__main__':
    html2markdown('data/test-file.html', 'data/result.md')