import click
import os

GITCHANGELOG_PLACEHOLDER = '_Next_Version_Number_'

def replace_string_in_file(file_name, old_string, new_string):
    #read input file
    with open(file_name, "rt") as fin:
        #read file contents to string
        data = fin.read()
    #replace all occurrences of the required string
    data = data.replace(old_string, new_string)
    #open the input file in write mode
    with open(file_name, "wt") as fin:
        #overrite the input file with the resulting data
        fin.write(data)

def get_version(bumptype=None):
    new_version_valid = True
    if bumptype is None:
        new_version_valid = False
        bumptype = 'patch'
    version_info_str = os.popen(f'bumpversion {bumptype} --dry-run --allow-dirty --list').read()
    version_info = {pair[0]: pair[1] for pair in [s.split('=') for s in version_info_str.split('\n')] if len(pair)>1}
    curr_version = version_info['current_version']
    new_version = version_info['new_version'] if new_version_valid else ''
    return curr_version, new_version

def new_changes_from_changelog(prev_version):
    with open('CHANGELOG.md') as fid:
        textdata = fid.read()
    prev_version_pos = textdata.find(f'# {prev_version}')
    end_of_new_changes_pos = textdata[:prev_version_pos].rfind('\n')
    return textdata[:end_of_new_changes_pos]

@click.command()
@click.option('-b', '--bumptype', type=click.Choice(['major', 'minor', 'patch'], case_sensitive=False), required=True, prompt=True, help='Whether to bump the version to a major, minor, or patch release')
def release(bumptype):
    curr_version, new_version = get_version(bumptype)
    release_branch = f'release/{new_version}'
    os.system(f'git checkout -b {release_branch}')
    os.system(f'gitchangelog {curr_version}..')
    replace_string_in_file('CHANGELOG.md', GITCHANGELOG_PLACEHOLDER, new_version)
    os.system('git add CHANGELOG.md')
    os.system('git commit -m"updated changelog"')
    os.system(f'bumpversion {bumptype}')
    os.system(f'git push --set-upstream origin {release_branch}')

if __name__ == "__main__":
    release()
