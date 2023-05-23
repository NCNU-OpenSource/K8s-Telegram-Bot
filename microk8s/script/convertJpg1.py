import cairo

def ascii_to_png(ascii_graph, output_file):
    # Calculate the dimensions of the graph
    lines = ascii_graph.strip().split('\n')
    max_line_length = max(len(line) for line in lines)
    width = max_line_length * 10  # Adjust the multiplier as needed
    height = len(lines) * 20  # Adjust the multiplier as needed

    # Create a PNG surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    # Create a PNG context
    context = cairo.Context(surface)

    # Set the background color
    context.set_source_rgb(1, 1, 1)  # White
    context.rectangle(0, 0, width, height)
    context.fill()

    # Set the text properties
    context.set_font_size(14)
    context.set_source_rgb(0, 0, 0)  # Black

    # Draw the ASCII graph
    y = 20
    for line in lines:
        context.move_to(10, y)
        context.show_text(line)
        y += 20

    # Save the image as PNG
    surface.write_to_png(output_file)

# Example usage
ascii_graph = '''
      +---------+
      |         |
 -----+         +-----
'''
output_file = 'output.png'

ascii_to_png(ascii_graph, output_file)

