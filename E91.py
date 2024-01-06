#importing necessary libraries
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
import numpy as np

n=int(input("Enter no. of bits:"))

#Creating Qubits
Qubits=[]
for i in range(n):
    Qubits+=[QuantumCircuit(2,2)]
    Qubits[i].h(0)
    Qubits[i].cx(0,1)
    Qubits[i].x(0)
    Qubits[i].z(0)

#Alice's options
A_choices=[]
A_circuits=[]

for i in range(n):
    choices=np.random.randint(3)
    A_choices+=[choices]
    
    Alice_option1=QuantumCircuit(1,1)
    Alice_option1.h(0)
    Alice_option1.measure(0,0)
    Alice_option2=QuantumCircuit(1,1)
    Alice_option2.rz(np.pi/4,0)
    Alice_option2.h(0)
    Alice_option2.measure(0,0)
    Alice_option3=QuantumCircuit(1,1)
    Alice_option3.rz(np.pi/2,0)
    Alice_option3.h(0)  
    Alice_option3.measure(0,0)
    Alice_options=[Alice_option1,Alice_option2,Alice_option3]
    A_circuits+=[Alice_options[choices]]
for i in range(n):
    Qubits[i]=Qubits[i].compose(A_circuits[i],qubits=0,clbits=0)

#Bob's options
B_choices=[]
B_circuits=[]

for i in range(n):
    choices=np.random.randint(3)
    B_choices+=[choices]
    Bob_option1=QuantumCircuit(1,1)
    Bob_option1.rz(np.pi/4,0)
    Bob_option1.h(0)
    Bob_option1.measure(0,0)
    Bob_option2=QuantumCircuit(1,1)
    Bob_option2.rz(np.pi/2,0)
    Bob_option2.h(0)  
    Bob_option2.measure(0,0)
    Bob_option3=QuantumCircuit(1,1)
    Bob_option3.rz(3*(np.pi/4),0)
    Bob_option3.h(0)
    Bob_option3.measure(0,0)
    Bob_options=[Bob_option1,Bob_option2,Bob_option3]
    B_circuits+=[Bob_options[choices]]
for i in range(n):
    Qubits[i]=Qubits[i].compose(B_circuits[i],qubits=1,clbits=1)
    
backend=Aer.get_backend('aer_simulator')
job = execute(Qubits, backend = backend, shots = 1024)
result = job.result()
counts = result.get_counts()

alice_bits = []
bob_bits = []
for i in range(n):
  bits = list(counts[i].keys())[0]
  alice_bits += [bits[0]]
  bob_bits += [bits[1]]
  
Alice_key=[]
Bob_key=[]

for i in range(n):
  if Alice_options[A_choices[i]] == Bob_options[B_choices[i]]:
    Alice_key += [int(alice_bits[i])]
    Bob_key += [1-int(bob_bits[i])]
print("Alice's key= ",Alice_key)
print("Bob's key= ",Bob_key)
