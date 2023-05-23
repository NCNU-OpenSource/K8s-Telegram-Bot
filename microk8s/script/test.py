import matplotlib.pyplot as plt

def plot_graph(data, filename):
    timestamps = [d[0] for d in data]
    values = [float(d[1]) for d in data]

    plt.plot(timestamps, values)
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.title("Graph Title")
    
    # Save the graph as a PNG file
    plt.savefig(filename)
    
    # Display the graph (optional)
    plt.show()

# Example usage
data = [
    [1684567958.992, "6.899999999974767"],
    [1684568018.992, "9.000000000014552"],
    [1684568078.992, "15.31666666662204"],
    # ... rest of the data ...
    [1684571498.992, "7.683333333358561"],
    [1684571558.992, "7.633333333336239"]
]

filename = "output.png"

plot_graph(data, filename)

