from prettytable import PrettyTable

table = PrettyTable()
table.add_column("Pokemon Name", ['a','b','c'])
table.add_column("Pokemon Type", ['fire','water','earth'])
table.align='l'

print(table)