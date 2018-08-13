# -*- coding:utf-8 -*-
import Parent
from CompareUtil import EditDistance
def main():
    EditDistance.similarityDegree("黄鹤楼","i黄鹤楼van2")
    EditDistance.similarityDegree("黄鹤楼","黄黄鹤鹤楼")
    EditDistance.similarityDegree("黄鹤楼","鹤楼黄楼黄楼")
    EditDistance.similarityDegree("黄鹤楼","鹤鹤楼")
    EditDistance.similarityDegree("黄鹤楼","汤逊湖")
    EditDistance.similarityDegree("黄鹤楼","岳阳楼")

if __name__ == '__main__':
    main()