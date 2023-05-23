import cairo

# Your ASCII graph as a string
ascii_graph = '''
      +---------+
      |         |
 -----+         +-----
'''

# Set the desired output image dimensions
width, height = 200, 100

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
context.move_to(10, 50)
context.show_text(ascii_graph)

# Save the image as PNG
surface.write_to_png('output.png')

