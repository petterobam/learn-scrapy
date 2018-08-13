# -*- coding:utf-8 -*-

class EditDistance():

    @classmethod
    def minEditDist(cls, sm, sn):
        '''
        计算两个字符串的最小莱温斯坦距离
        '''
        m,n = len(sm)+1,len(sn)+1

        # create a matrix (m*n)
        matrix = [[0]*n for i in range(m)]

        matrix[0][0]=0
        for i in range(1,m):
            matrix[i][0] = matrix[i-1][0] + 1

        for j in range(1,n):
            matrix[0][j] = matrix[0][j-1]+1


        for i in range(m):
            print(matrix[i])

        print("********************")

        cost = 0

        for i in range(1,m):
            for j in range(1,n):
                if sm[i-1]==sn[j-1]:
                    cost = 0
                else:
                    cost = 1

                matrix[i][j]=min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+cost)

        for i in range(m):
            print(matrix[i])

        return matrix[m-1][n-1]

    @classmethod
    def similarityDegree(cls, str1, str2):
        '''
        计算两个字符串的相似度
        '''
        mindist = 0
        if str1 == None and str2 != None:
            mindist = len(str2)
            return 0
        elif str1 != None and str2 == None:
            mindist = len(str1)
            return 0
        elif str1 != None and str2 != None:
            mindist = cls.minEditDist(str1,str2)
        else:
            return 0
        maxLength = min(len(str1), len(str2))
        similarityDegree = 1-mindist/maxLength
        print(str1, "和", str2, "的相似度为：", similarityDegree)
        return similarityDegree
