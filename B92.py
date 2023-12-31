#importing necessary libraries
from qiskit import QuantumCircuit, Aer, transpile
from qiskit_aer import AerSimulator
import numpy as np
n=int(input("Enter length of initial string: "))

#Preparing string and basis for Alice
Initial_string=[]
Alice_basis=[]
for i in range(n):
    String=np.random.randint(2)
    Initial_string.append(String)
created_key=[]
def creating_key(bit):
    for i in range(n):   
        qc=QuantumCircuit(1,1)
        if bit[i]==0:
            pass
        if bit[i]==1:
            qc.h(0)
        qc.barrier()
        created_key.append(qc)
    return created_key
message=creating_key(Initial_string)

#Generating basis for Bob
Bob_basis=[]
for i in range(n):
    basis=np.random.randint(2)
    Bob_basis.append(basis)
    
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
        qobj=transpile(sent_key[b],backend=backend)
        result= aer_sim.run(qobj,shots=10,memory=True).result()
        measured_bit= result.get_memory(qobj)[0]
        measurements.append(int(measured_bit))
    return measurements
Bob_results=measure(created_key, Bob_basis)

#Defining the protocol
def Protocol(result,basis):
    key=[]
    for i in range(n):
        if result[i]==1:
            if basis[i]==0:
                key.append(1)
            if basis[i]==1:
                key.append(0)
    return key
order=[]
for i in range(n):
    if Bob_results[i]==1:
        order.append(i)
Bob_key=Protocol(Bob_results,Bob_basis)
x=len(order)
Final_string=[]


for i in range(x):
    Final_string.append(Initial_string[order[i]])

#Testing
if Bob_key==Final_string:
    print("The keys match, hence the protocol is working")
else:
    print("Error in string")
    
print("length of initial key:",n)
print("length of final key:",x)
        

    




    
    
