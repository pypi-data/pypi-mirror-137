import Rahimcalc as r
import sys
def main():
    m=sys.argv[0]
    a=sys.argv[1]
    b=sys.argv[2]
    c=sys.argv[3]
    print(m,a,b,c)
    if a=='sum':
        print(r.sum(b,c))
    if a=='sub':
        print(r.sub(b,c))
    if a=='mul':
        print(r.mul(b,c))
    if a=='div':
        print(r.div(b,c))
    if a=='exp':
        print(r.exp(b,c))
    if a=='complex':
        print(r.complex(b,c))
if __name__=='__main__':
    main()
