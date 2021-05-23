import matplotlib.pyplot as plt

# x axis values
y = [1000, 230, 1000, 2323, 200, 2231]
# corresponding y axis values
x = [1, 2, 3, 4, 5, 6]

# plotting the points
plt.plot(x, y, color='#80cbcf', linestyle='dashed', linewidth=2,
         marker='o', markerfacecolor='#9aca64', markersize=12)

# setting x and y axis range
plt.ylim(0, 4000)
plt.xlim(1, len(x))

# naming the x axis
plt.xlabel('Packet (number)')
# naming the y axis
plt.ylabel('Delay (ms)')

# giving a title to my graph
plt.title('Delay per Packet')

# function to show the plot
plt.show()