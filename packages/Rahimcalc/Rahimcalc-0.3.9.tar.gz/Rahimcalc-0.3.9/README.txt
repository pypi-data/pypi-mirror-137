# Rahimcalc
___

### Package Name:
- Rahimcalc

### Author 
- Abdurrahim
- Abdurrazzak

### Package install comment

- type in cmd(command prompt)

  - > Python -m pip install Rahimcalc

### Image:

![image](https://blogger.googleusercontent.com/img/a/AVvXsEi5flFGPlq1YL2SQ-TxJKoeYAKxM6vzZmDSXSDaqYy0xU7qGRh5qOMugPwN42h8G2vXjwXi6PIMXZVJO28P4JD_ctXoWjgPOZ_yE2tvoVdVEAJzL7R_3PStxBi6m0CD_n6GE30-Asn-gAg1LqiJm0wqaKlnR5eMDa2LhB1hapQu_x2x-DVkiPeH53xV=w945-h600-p-k-no-nu))

### Code:

```python
import Rahimcalc as r
print(dir(r))
a=int(input("Enter a:"))
b=-int(input("Enter b:"))
print("Addition:",r.sum(a,b))
print("Subtraction:",r.sub(a,b))
print("Multiplication:",r.mul(a,b))
print("Division:",r.div(a,b))
print("Complex Numbers:",r.complex(a,b))
print("Exponent:",r.exp(a,b))
```

### Package uninstall comment
- type in cmd(command prompt)

  - >pip uninstall Rahimcalc