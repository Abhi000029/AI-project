import matplotlib.pyplot as plt
month =["jan","feb","mar"]
sales =[20,30,25]
plt.plot(month,sales)
plt.title("monthly sales")
plt.xlabel("month")
plt.ylabel("sales")
plt.show()

#create a bar chart
plt.bar(month,sales)   
plt.title("monthly sales")
plt.xlabel("month")
plt.ylabel("sales")
plt.show()  
