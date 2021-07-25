# import matplotlib.pyplot as plt
#
# # x axis values
# x = [1, 2, 3]
# # corresponding y axis values
# y = [2, 4, 1]
#
# # plotting the points
# plt.plot(x, y)
#
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
#
# # giving a title to my graph
# plt.title('My first graph!')
#
# # function to show the plot
# plt.savefig('test.png')

from PIL import ImageDraw, Image

pic = Image.new("RGB", (1000, 1000), (255, 255, 255))
draw = ImageDraw.Draw(pic)
draw.point((100, 100), fill=128)
draw.point((300, 300), fill=128)
draw.line((15, 25, 35, 45), fill=128)
pic.show()
