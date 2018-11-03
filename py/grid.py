class Grid:
    border = True
    use_unicode = True

    def __init__(self, width, height, default=0):
        self.width = width
        self.height = height
        self.default = default
        self.init_array()

    def init_array(self, default=None):
        if default is None:
            default = self.default
        total_squares = self.width * self.height
        self.array = [default for __ in range(total_squares)]

    def get(self, row, col):
        index = self.convert_to_index(row, col)
        return self.array[index]

    def set(self, row, col, value):
        index = self.convert_to_index(row, col)
        self.array[index] = value

    def convert_to_index(self, row, col):
        return row*self.width + col

    def val_to_string(self, val):
        return str(val)

    def __str__(self):
        if self.border:
            if self.use_unicode:
                return self.display_unicode_border()
            else:
                return self.display_ascii_border()
        else:
            return self.display_no_border()

    def display_no_border(self):
        lines = []
        for row in range(self.height):
            line = []
            for col in range(self.width):
                index = self.convert_to_index(row, col)
                item = self.array[index]
                line.append(self.val_to_string(item))
            lines.append(' '.join(line))
        return '\n'.join(lines)

    def display_ascii_border(self):
        top_bot = '+' + (self.width*2 - 1) * '-' + '+'
        lines = []
        for row in range(self.height):
            line = []
            for col in range(self.width):
                index = self.convert_to_index(row, col)
                item = self.array[index]
                line.append(self.val_to_string(item))
            lines.append('|'+(' '.join(line)) + '|')
        lines = [top_bot] + lines + [top_bot]
        return '\n'.join(lines)

    def display_unicode_border(self):
        top_line = '╔' + (2*self.width-1)*'═' + '╗'
        bot_line = '╚' + (2*self.width-1)*'═' + '╝'
        lines = []
        for row in range(self.height):
            line = []
            for col in range(self.width):
                index = self.convert_to_index(row, col)
                item = self.array[index]
                line.append(self.val_to_string(item))
            lines.append('║'+(' '.join(line)) + '║')
        lines = [top_line] + lines + [bot_line]
        return '\n'.join(lines)

