#!/usr/bin/env python
# ------------------------------------ merge_single_file.py ---------------------------------------
# A simple script to merge multiple lines from a singe file by preserving the key field 
# and concatenating the values of the desired field
#
# In order to work correctly the input file must be sorted on key
# 
# Written by:
#     Jonathan Gangi - javgan.tar.gz@gmail.com
#
# -------------------------------------------------------------------------------------------------
#  simpleMail.py
#  Copyright (C) 2021  Jonathan Gangi
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# -------------------------------------------------------------------------------------------------


# ------------------------------------------ Imports ----------------------------------------------
import argparse
import traceback
import os, sys

# ----------------------------------------- Functions ---------------------------------------------

# -- Function: merge_lines_single_file
# A function to perform the merge the keys into single lines
#
def merge_lines_single_file(options):
    try:
        # Initial parameters
        field_separator = options.input_separator
        input_stream = open(options.input_file,'r')
        key_field = int(options.key_field) - 1
        output_stream = open(options.output_file,'w') if options.output_file else None
        concat_list = [int(x) - 1 for x in options.concat_fields ] if options.concat_fields else [] 
        concat_separator = options.concat_separator
        skip_headers = True if str(options.skip_header).lower().find('true') != -1 else False
        add_merge_counter = True if str(options.append_counter.lower().find('true')) != -1 else False
        sum_field = int(options.sum_value[0]) - 1 if options.sum_value else None
        sum_lookup = options.sum_value[1] if options.sum_value else None  
        sum_field_required = True if sum_field and sum_lookup else False

        # Controllers
        last_line = None
        concat_dict = {}
        counter = 0
        merge_counter = 0
        concat_condition = lambda x: concat_separator.join(concat_dict[str(x)]) if (x in concat_list) else last_line[x]
        
        # Process data
        for line in input_stream:
            current_line = line.strip('\n').split(field_separator)
            
            # Just skip the first line of the iteration
            if skip_headers:
                skip_headers = False
                
            # If the current key has changed we should compute the values and dump the previous line
            elif last_line and last_line[key_field].find(current_line[key_field]) == -1:
                # Process the data from previous line
                last_line = [ concat_condition(x) for x in range(len(last_line)) ]
                _ = last_line.append(str(counter)) if sum_field_required else last_line
                _ = last_line.append(str(merge_counter)) if add_merge_counter else last_line
                merge_counter = 0
               
                # Print the formatted line
                dump_data(last_line, field_separator, output_stream)
             
                # Reset values
                concat_dict = {}
                counter = 0
                
            # Concatenate and sum fields for the current line
            concat_dict = concatenate_in_fields(concat_dict, concat_list, current_line)
            counter = counter + 1 if sum_field_required and current_line[sum_field].find(sum_lookup) != -1 else counter
            merge_counter += 1
                    
            # Next iteration
            last_line = current_line
            
        # Compute data for the final line
        if last_line:
            last_line = [ concat_condition(x) for x in range(len(last_line)) ]
            _ = last_line.append(str(counter)) if sum_field_required else last_line
            _ = last_line.append(str(merge_counter)) if add_merge_counter else last_line
            
        
            # Print the last line
            dump_data(last_line, field_separator, output_stream)

        # Close the streams
        input_stream.close()
        if output_stream:
            output_stream.close()
        
    except Exception as e:
        print ("Execution error: %s" % e)        
        traceback.print_exc()
        return 1
    return 0


# -- Function dump_data
# It will write the output data inside the file or on STDOUT
def dump_data(list_data, separator, output_stream):
    if not output_stream:
        print(separator.join(list_data))
    else:
        output_stream.write(separator.join(list_data) + '\n')


# -- Function: concatenate_in_fields
# It's an auxiliary function to build the concatenation list for each field
# in the concat_dict
def concatenate_in_fields(concat_dict, fields, data):
    for field in fields:
        if str(field) not in concat_dict.keys():
            concat_dict[str(field)] = [data[field]]
        else:
            concat_dict[str(field)].append(data[field])
    return concat_dict



# ------------------------------------------- Main ------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge multiple lines from a singe file by preserving the key field and concatenating the values of the desired field")

    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument("-t", "--separator", dest='input_separator', metavar="SEPARATOR", help="The field separator for input/output file", required=True)
    required.add_argument("-i", "--input", dest='input_file', metavar="FILE", help="The input file to be processed", required=True)
    required.add_argument("-k", "--key-field", dest='key_field', metavar="FIELD_NUM", help="The field num to be used as merging key", required=True)

    # Optional arguments
    parser.add_argument("-o", "--output", dest='output_file', metavar="FILE", help="The output file to be generated.")
    parser.add_argument("-m", "--merge-field", dest='concat_fields', metavar="FIELD", help="List of fields concatenate", nargs="*")
    parser.add_argument("-f", "--merge-separator", dest='concat_separator', metavar="SEPARATOR", help="The separator for concatenated lines")
    parser.add_argument("-v", "--sum-value", dest='sum_value', type=str, metavar=("FIELD","STRING"), help="The field to concatenate", nargs=2)
    parser.add_argument("-c", "--count-merged-lines", dest='append_counter', metavar=("true|false"), help="Whehter include a field with the counter of merged lines or not. Default = \"false\"", default="false")
    parser.add_argument("-s", "--skip-header", dest='skip_header', metavar="true|false", default='false', help="true to skip the first line of the file, false otherwise. Default = \"false\"")

    options = parser.parse_args()

    # Check the required together options
    if options.concat_fields and not options.concat_separator:
        parser.error("ERROR: You must provide a concatenation separator with the option \"-f\"")   

    if not os.path.isfile(options.input_file):
        print("ERROR: The input file provided \"%s\" cannot be read" % options.input_file)
        sys.exit(1)

    merge_lines_single_file(options)

