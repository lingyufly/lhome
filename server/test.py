def f1():
    l=[]
    for v in range(1,4):
        def f2(vv):
            def f3():
                print(vv*vv)
            return f3
        l.append(f2(v))
    return l

a1,a2,a3=f1()
a1()
a2()
a3()