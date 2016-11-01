def levenshtein(s1, s2):
    """takes two strings S1 and S2 and compares them to return the Levenshtein distance"""
    
    import numpy as np    
    n = len(s1)
    m = len(s2)
    if (n == 0) or (m == 0):
        return n or m
    else:
        mat = np.zeros(shape = (n,m))
        for i in range(len(mat[0])):
            mat[0] = i
        for i in range(len(mat)):
            mat[i][0] = i
        #construct n*m matrix
        for i in range(n):
            for j in  range(m):
                if s1[i] == s2[j]:
                    cost = 0
                else:
                    cost = 1
                mat[i][j] = min( mat[i-1][j] + 1, mat[i][j-1] + 1,mat[i-1][j-1] + cost)
        return mat[n-1][m-1]
