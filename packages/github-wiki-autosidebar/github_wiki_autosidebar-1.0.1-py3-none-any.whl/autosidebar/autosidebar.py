from os import walk


class AutoSidebar():
    def __init__(self):
        self.output = ''
        self.files = list(walk('.'))

    def add_to_output(self, string):
        self.output += string + '\n'

    def get_group(self, directory_name):
        group = [i for i in self.files if i[0] == directory_name]
        if len(group) > 0:
            return group[0]
        else:
            return []
    
    def add_group(self, group, h_level=''):
        if group[0] != '.':
            self.add_to_output((h_level + '* ' + group[0].split('\\')[-1])[4:])
        # first print all items
        for i in group[2]:
            hidden = i.startswith('_') or i.startswith('.')
            if not hidden and i.endswith('.md'):
                self.add_to_output((h_level + '    * [[' + i[:-3] + ']]')[4:])
        # get the individual groups
        parent = group[0]
        groups = [self.get_group(parent + '\\' + i)
                  for i in group[1] if not i.startswith('.')]
        for group in groups:
            self.add_group(group, h_level + '    ')

    def collate_output(self):
        self.add_group(self.files[0])

    def write_output_to_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(self.output)

    def run(self):
        self.collate_output()
        self.write_output_to_file('_Sidebar.md')


def main():
    auto_sidebar = AutoSidebar()
    auto_sidebar.run()


if __name__ == "__main__":
    main()
