unique_stat_names = {}

def format_key(key):
    key = key.replace(' ','_')
    return key

def main():
    with open("writefile.txt") as f:
        content = f.readlines()
        line_num = 0
        for line in content[1:]:
            line_num += 1
            columns = line.split(',')
            for stat_index in (5,6,7,8):
                key = format_key(columns[stat_index])
                unique_stat_names[key] = 0

    with open("writefile.txt") as input_file, open("normalized.txt","w") as output_file:
        file_string = "{},{},weapon".format(line_num, len(unique_stat_names)+2)
        for stat_name in unique_stat_names:
            file_string = file_string + ",{}".format(stat_name)
        file_string = file_string + ",price" + "\n"
        output_file.write(file_string)
        input_lines = input_file.readlines()
        for line in content[1:]:
            columns = line.split(',')
            line_stats = {}
            for stat_index in (5,6,7,8):
                key = format_key(columns[stat_index])
                value = float(columns[stat_index-4])
                value = stat_converter(value)
                line_stats[key] = value
            line_text = columns[0]
            for stat_name in unique_stat_names:
                if stat_name in line_stats:
                    line_text = line_text + "," + str(line_stats[stat_name])
                else:
                    line_text = line_text + ",{}".format(stat_converter(0))
            line_text = line_text + "," + columns[9]
            output_file.write(line_text)

def stat_converter(stat_input):
    if stat_input > 0.0:
        stat_input = 100
    if stat_input < 0.0:
        stat_input = 50
    if stat_input == 0.0:
        stat_input = -10000
    return stat_input






if __name__ == "__main__":
    main()