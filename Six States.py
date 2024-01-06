#importing necessary libraries
from qiskit import QuantumCircuit, Aer, transpile
from qiskit_aer import AerSimulator
import numpy as np

n=int(input("Enter length of initial string: "))

#Preparing string and basis for Alice

Initial_string=[]
for i in range(n):
    String=np.random.randint(2)
    Initial_string.append(String)
    
Alice_basis=[]
for i in range(n):
    basis=np.random.randint(3)
    Alice_basis.append(basis)
print("Alice's basis: ",Alice_basis)

created_key=[]
def creating_key(basis,string):
    for i in range(n):   
        qc=QuantumCircuit(1,1)
        if string[i]==1:
            qc.x(0)
            
            
        if basis[i]==0:
            pass
        if basis[i]==1:
            qc.h(0)
        if basis[i]==2:
            qc.h(0)
            qc.rz(np.pi/2,0)
        qc.barrier()
        created_key.append(qc)
    return created_key
message=creating_key(Alice_basis,Initial_string)
print("Initial string: ",Initial_string)

#Generating basis for Bob
Bob_basis=[]
for i in range(n):
    basis=np.random.randint(3)
    Bob_basis.append(basis)
print("Bob's basis: ",Bob_basis)
    
#measurement by Bob
def measure(sent_key, basis):
    backend=Aer.get_backend('aer_simulator')
    aer_sim=Aer.get_backend('aer_simulator')
    measurements=[]
    for b in range(n):
        if basis[b]==0:
            sent_key[b].measure(0,0)
        if basis[b]==1:
            sent_key[b].h(0)
            sent_key[b].measure(0,0)
        if basis[b]==2:
            sent_key[b].rz(np.pi/2,0)
            sent_key[b].h(0)
            sent_key[b].measure(0,0)
        qobj=transpile(sent_key[b],backend=backend)
        result= aer_sim.run(qobj,shots=2000,memory=True).result()
        measured_bit= result.get_memory(qobj)[0]
        measurements.append(int(measured_bit))
    return measurements
Bob_results=measure(created_key, Bob_basis)
print("Bob's measured key: ",Bob_results)



        
    
#Defining the protocol
def Protocol(basis1,basis2,result):
    final_key=[]
    for i in range(n):
        if basis1[i]==basis2[i]:
            final_key.append(result[i])
    return final_key

order=[]
for i in range(n):
    if Alice_basis[i]==Bob_basis[i]:
        order.append(i)
Bob_key=Protocol(Alice_basis,Bob_basis,Bob_results)
print("Bob's final key: ",Bob_key)
x=len(order)
Final_string=[]
print(order)
for i in range(x):
    Final_string.append(Initial_string[order[i]])
#Testing
if Bob_key==Final_string:
    print("The keys match, hence the protocol is working")
else:
    print("Error in string")

    
print("length of initial key:",n)
print("length of final key:",x)
print(Final_string)
