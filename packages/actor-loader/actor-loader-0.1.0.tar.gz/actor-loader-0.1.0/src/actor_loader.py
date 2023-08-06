import json
import os
import shutil as file
import time
import requests
import zipfile

from bcml import util
from oead import byml, Sarc, yaz0, U32, S32
from pathlib import Path
from zlib import crc32

ignore = [
    "TwnObj_HyruleCastleObject_StandTorchOn_A_01"
]
"""List of actors to be ignored/skipped when 'fixing' the active mubin file."""

global_endian = True
"""True BE | False LE"""

global_actorinfo = {}
"""Dynamically adjusted actorinfo instance."""

class BasicIO:
    """Wraps commonly used In/Out functions in simple methods."""

    def handle_dynamic(file) -> dict:
        """Opens a pathlib.Path or bytes and handles it returning a dictionary with the file/bytes infomation."""
        data: bytes = []

        # If self is as file : read bytes
        try:
            if Path(file).is_file():
                data = file.read_bytes()
        except: data = file

        is_yaz0 = False

        if data[:4] == b'Yaz0':
            is_yaz0 = True
            data = yaz0.decompress(data)

        if data[:2] == b'BY':
            sub = 'BYML'
            if 'Objs' in byml.from_binary(data):
                sub = 'MUBIN'

            return {
                'content': byml.from_binary(data),
                'endian': True,
                'yaz0': yaz0,
                'type': 'BYML',
                'sub_type': sub
            }

        elif data[:2] == b'YB':
            sub = 'BYML'
            if 'Objs' in byml.from_binary(data):
                sub = 'MUBIN'

            return {
                'content': byml.from_binary(data),
                'endian': True,
                'yaz0': yaz0,
                'type': 'BYML',
                'sub_type': sub
            }

        elif data[:4] == b'SARC':
            return {
                'content': Sarc(data).get_files(),
                'endian': Sarc(data).get_endianness(),
                'yaz0': is_yaz0,
                'type': 'SARC'
            }

        else:
            print(f'The file {file} was not in a format recognized.')
            return {
                'ERROR': data[:4]
            }

    def write_byml(file: Path, data: dict):
        """Writes the passed data (oead.Hash/dict) to the file (Path)."""
        if not data['type'] == 'BYML':
            print(f'{file} was not a BYML file.')
            return

        # Convert BYML to binary
        write_data = byml.to_binary(data['content'], data['endian'])

        # Yaz0 compress
        if data['yaz0']:
            write_data = yaz0.compress(write_data)

        # Write bytes
        file.write_bytes(write_data)

    def write_actorinfo(actorinfo: dict = global_actorinfo):
        localized = {
            'content': actorinfo,
            'type': 'BYML',
            'yaz0': True,
            'endian': global_endian
        }

        if 'Actors' in actorinfo:
            content = util.get_content_path()
            actor_dir = f'{content}\\Actor'
            if not Path(actor_dir).is_dir(): os.makedirs(actor_dir)
            file = Path(f'{actor_dir}\\ActorInfo.product.sbyml')
            BasicIO.write_byml(file, localized)
        else: print('No changes were made.')

    def IS_projects() -> str:
        """Returns the Ice-Spear project folder as a Path object."""
        config = Path(f'{os.environ["USERPROFILE"]}\\.ice-spear\\config.json')

        if not config.is_file():
            print('The Ice-Spear config file was not found. Please install Ice-Spear.')
            return ''

        return json.loads(config.read_text())['projects']['path']

class ActorInfoIO:
    def transfer_entry(_from: dict, name: str, to: dict = {}) -> dict:
        global global_endian

        if not 'Actors' in to:
            file = BasicIO.handle_dynamic(util.get_game_file('Actor/ActorInfo.product.sbyml'))
            global_endian = file['endian']
            to = file['content']

        if 'Actors' in _from:
            for actor in _from['Actors']:
                if actor['name'] == name:
                    crc = crc32(actor['name'].encode())

                    if crc > 2147483647:
                        print(f'Appending !u {hex(crc)}')
                        crc = U32(crc)
                    else:
                        print(f'Appending {crc}')
                        crc = S32(crc)

                    if crc not in to['Hashes']:
                        to['Actors'].append(actor)
                        to['Hashes'].append(crc)
                    else:
                        print(f'{crc} already exists.')

                    return to

class ActorLoader:
    """Class for loading actors from/to mubin files."""

    def load_actor(name: str, parent: str) -> dict:
        global global_actorinfo
        actorpack_dir = f'content\\Actor\\Pack'
        c_actorpack_dir = f'{BasicIO.IS_projects()}\\Collision Actors\\content\\Actor\\Pack'

        print(f"Found '{name}' in {parent}")

        # Does the actor already exists in the mod? (w/C)
        if Path(f'{actorpack_dir}\\{name}.sbactorpack').is_file():
            return name

        # Does the actor already exists in the mod? (n/C)
        if Path(f'{actorpack_dir}\\{name}C.sbactorpack').is_file():
            return f'{name}C'
            
        # Does the provided name (actor) exists in the c-actors dump
        if Path(f'{c_actorpack_dir}\\{name}.sbactorpack').is_file():

            # Create the mod structure if it does not already exist
            if not Path(actorpack_dir).exists(): os.makedirs(actorpack_dir)
            
            # Copy the corresponding c-actor to the mod folder
            file.copy(f'{c_actorpack_dir}\\{name}.sbactorpack', f'{actorpack_dir}\\{name}.sbactorpack')

            # Add actor info entry
            global_actorinfo = ActorInfoIO.transfer_entry(BasicIO.handle_dynamic(Path(f'{c_actorpack_dir}..\\..\\ActorInfo.product.sbyml'))['content'], name, global_actorinfo)

            print(f'Loaded {name} from {parent}')
            return name

        # Does the provided name (actor) exists in the c-actors dump (append C)
        if Path(f'{c_actorpack_dir}\\{name}C.sbactorpack').is_file():
            # Ignore the actor if defined in ignore
            for ignore_name in ignore:
                if ignore_name == name:
                    return name

            # Create the mod structure if it does not already exist
            if not Path(actorpack_dir).exists(): os.makedirs(actorpack_dir)

            # Copy the corresponding c-actor to the mod folder 
            file.copy(f'{c_actorpack_dir}\\{name}C.sbactorpack', f'{actorpack_dir}\\{name}C.sbactorpack')

            # Add actor info entry
            global_actorinfo = ActorInfoIO.transfer_entry(BasicIO.handle_dynamic(Path(f'{c_actorpack_dir}..\\..\\ActorInfo.product.sbyml'))['content'], f'{name}C', global_actorinfo)

            print(f'Loaded {name}C from {parent}')
            return f'{name}C'

        return name

    def load_actors(file: Path):
        data = BasicIO.handle_dynamic(file)

        if 'ERROR' in data:
            return

        if data['type'] == 'BYML' and data['sub_type'] == 'MUBIN':
            # Look for mirror file for diffing
            mirror = {}
            mirror_path = Path(f'{util.get_aoc_dir()}\\Map\\MainField\\{file.name.split("_")[0]}\\{file.name}')

            if mirror_path.is_file():
                mirror = BasicIO.handle_dynamic(mirror_path)['content']

            for obj in data['content']['Objs']:
                if obj not in mirror['Objs'] and 'UnitConfigName' in obj:
                    obj['UnitConfigName'] = ActorLoader.load_actor(obj['UnitConfigName'], file)

            BasicIO.write_byml(file, data)

        elif data['type'] == 'SARC':
            for SARCfile in data['content']:
                if str(SARCfile).endswith('.mubin') or str(SARCfile).endswith('.smubin'):
                    data = BasicIO.handle_dynamic(SARCfile.data)

                    if data['type'] == 'MUBIN' and data['sub_type'] == 'MUBIN':
                        print(f'[HERE] {data} {file} {SARCfile}')
                        for obj in data['content']['Objs']:
                            if 'UnitConfigName' in obj:
                                ActorLoader.load_actor(obj['UnitConfigName'], f'{file}//{SARCfile}')

        return global_actorinfo

def main():
    print('Initializing...')

    if BasicIO.IS_projects() == '':
        input('')
        return

    if not Path(f'{BasicIO.IS_projects()}\\Collision Actors\\content\\Actor').is_dir():
        # download c-actors
        print('Downloading Collision Actors . . .')
        file_bytes = requests.get('https://onedrive.live.com/download?cid=74309C0E337BBADE&resid=74309C0E337BBADE%21312814&authkey=AN-usUBBhcDErYI')
        Path('.\\vawc.zip').write_bytes(file_bytes.content)
        os.makedirs(f'{BasicIO.IS_projects()}\\Collision Actors\\content')
        with zipfile.ZipFile('.\\vawc.zip', 'r') as zip_ref:
            zip_ref.extractall(f'{BasicIO.IS_projects()}\\Collision Actors\\content\\Actor')

        Path('.\\vawc.zip').unlink()

    start_time = time.time()

    if not Path('.\\aoc').is_dir() and Path('.\\content').is_dir():
        print('No aoc or content folder was found.')
        return

    local_actorinfo = {}

    formats = [
        ".pack",
        ".mubin",
        ".smubin"
    ]

    for file in Path('.\\').glob('**/*'):
        if file.is_file():
            if file.suffix in formats:
                try:
                    local_actorinfo = ActorLoader.load_actors(file)
                except Exception as e:
                    print(f'Error - {str(e.with_traceback())}')

    BasicIO.write_actorinfo(local_actorinfo)

    end_time = time.time()

    sec = end_time - start_time
    print(f'\nCompleted in {sec} seconds.')

if __name__ == "__main__":
    main()