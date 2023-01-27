import os, traceback
import romtools as rt
from mml2mfvi import mml_to_akao

def akao_to_asm(data, channels, labels, filename):
    # create song label and output filename
    filename = os.path.splitext(filename)[0].lower()
    label_elems = filename.split("_")
    song_label = f'SongData_{label_elems[-1]}'
    asm_filename = f'{filename}.asm'

    # arrange and add channel pointers to the label references list
    for i in range(1, 17):
        labels[(i - 1) * 2 + 6] = channels[i]

    # add song start and song end label references
    labels[2] = 0x26
    labels[4] = len(data)

    # sort dict by label references
    labels = dict(sorted(labels.items()))

    # create list of unique sorted label declarations
    labels_decl = list(sorted(set(labels.values())))

    # create label declaration ranges
    ranges = []
    prev_value = 0
    for l in labels_decl:
        ranges.append(rt.Range(prev_value, l))
        prev_value = l

    # add label declaration index to label reference
    for k, v in labels.items():
        labels[k] = labels_decl.index(v)

    # file header with song label
    asm_string = '; this file is generated automatically,' \
        + ' do not modify manually\n\n'
    asm_string += '.list off\n'
    asm_string += f'\n\n{song_label}:\n'

    # song data size
    song_size = rt.hex_string(len(data) - 2, 4, '$').lower()
    asm_string += f'\n        .word   {song_size}'
    offset = 2

    for i in range(len(labels_decl)):
        # label references in the label range
        label_refs = dict((k, v) for k, v in labels.items() if k > ranges[i].begin and k <= ranges[i].end)
        for k, v in label_refs.items():
            data_block_size = k - offset
            if data_block_size > 0:
                # bytes before the label reference
                data_block = data[offset: k]
                for j in range(len(data_block)):
                    if j % 16 == 0:
                        asm_string += '\n        .byte   '
                    else:
                        asm_string += ','
                    asm_string += rt.hex_string(data_block[j], 2, '$').lower()
                    offset += 1
            # label reference
            label = rt.hex_string(labels_decl[v], 4, '@').lower()
            asm_string += f'\n        .addr   {label}'
            offset += 2
        data_block_size = ranges[i].end - offset
        if data_block_size > 0:
            # bytes after the label reference and before the next declaration
            data_block = data[offset: ranges[i].end]
            for j in range(len(data_block)):
                if j % 16 == 0:
                    asm_string += '\n        .byte   '
                else:
                    asm_string += ','
                asm_string += rt.hex_string(data_block[j], 2, '$').lower()
                offset += 1
        # label declaration
        decl = rt.hex_string(labels_decl[i], 4, '@').lower()
        asm_string += f'\n\n{decl}:'
    asm_string += '\n\n.list on\n'

    return asm_filename, asm_string
        
if __name__ == '__main__':
    asm_dir = os.path.join(os.getcwd(), 'src', 'assets')
    mml_dir = os.path.join(asm_dir, 'mml')

    for file in os.listdir(mml_dir):
        file_path = os.path.join(mml_dir, file)
        mml = []
        # read mml file
        try:
            with open(file_path, 'r') as f:
                mml = f.readlines()
        except IOError as e:
            print(f'Error reading file {file_path}')
            print(e)

        # convert mml file to binary and create asm string
        try:
            variants = mml_to_akao(mml)
            def_variant = variants['_default_']
            asm_filename, asm_string = akao_to_asm(def_variant[0], def_variant[1], def_variant[2], file)
        except Exception:
            traceback.print_exc()

        # write asm file
        try:
            asm_path = os.path.join(asm_dir, asm_filename)        
            os.makedirs(os.path.dirname(asm_path), exist_ok=True)
            with open(asm_path, 'w') as f:
                f.write(asm_string)              
            print(f'{asm_filename} created.')
        except IOError as e:
            print(f'Error writing file {asm_path}')
            print(e)