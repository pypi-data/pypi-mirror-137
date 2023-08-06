import os
import glob
import typer
import shutil
import tarfile
import requests
from itertools import repeat
from karaone.split import Dataset
from dotenv import load_dotenv
from typing import (List, Optional)

load_dotenv()

from karaone import (__author__,
                  __version__,
                  __app_name__)


app = typer.Typer()

KARA_URL = "http://www.cs.toronto.edu/~complingweb/data/karaOne/"

ALL_SUBJECTS = ["MM05","MM08","MM09","MM10","MM11","MM12",
                "MM14","MM15","MM16","MM18","MM19","MM20","MM21",
                "P02"]

def _get_version(value: bool) -> None:
    """Returns info from package

    Parametters
    ___________
    value: bool

    return None
    """
    if value:

        typer.echo(f"Package: {__app_name__}\nVersion: {__version__}\nAurhor: {__author__}")

        raise typer.Exit()

@app.callback()
def main(version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help = "Show the version of the application",
    callback = _get_version,
    is_eager = True
    )) -> None:
    """A simple utils tools for kara ona database eeg"""

    return None

@app.command()
def download(subjects: List[str] = typer.Option(ALL_SUBJECTS,
                                                "--subjects",
                                                "-s",
                                                help = "List of subject to download from Kara One databse"),
             url: Optional[str] = typer.Option(KARA_URL,
                                               "--url",
                                               "-u",
                                               help = "URL Kara One Databse"),
             path: Optional[str] = typer.Option("rawdata",
                                                "--path",
                                                "-p",
                                                help = "Path to save rawdata")) -> None:
    
    """Function to download Kara One Databse"""


    subjects = list(map(lambda subject: f"{subject}.tar.bz2", subjects))
    
    urls = list(map(lambda subject: f"{url}{subject}", subjects))

    print("Downloading files...")

    try:
        os.mkdir("rawdata")
    except FileExistsError:
        pass

    for index, url in enumerate(urls):

        try:

            with requests.get(url, stream = True, allow_redirects = True) as response:

                response.raise_for_status()

                for chunk in response.iter_content(chunk_size = 2048):

                    open(os.path.join(path, subjects[index]), "ab").write(chunk)
        
        except requests.exceptions.HTTPError:

            typer.echo(f"Invalid URL: {url} maybe the subject {subjects[index]} is not available or dosn't exist")

            continue

@app.command()
def extract(subjects: List[str] = typer.Option(ALL_SUBJECTS,
                                               "--subjects",
                                               "-s",
                                               help = "List of subject to extract from Kara One databse"),
            path: Optional[str] = typer.Option("rawdata",
                                               "--path",
                                               "-p",
                                               help = "Path to rawdata"),                                                 
            output: Optional[str] = typer.Option("rawextracted",
                                                 "--output",
                                                 "-o",
                                                 help = "Path to save extracted data")) -> None:
    """Function to extract Kara One Databse and move to new folder"""
    
    typer.echo("Extracting files...")

    subjects = list(subjects)

    check_if_file = lambda zip_file: os.path.exists(os.path.join(path, f"{zip_file}.tar.bz2")) == True

    exists = list(map(check_if_file, subjects))

    subjects = list(set([subjects[index] for index, value in enumerate(exists) if value]))

    subjects_zip = list(map(lambda subject: f"{subject}.tar.bz2", subjects))

    if subjects_zip:

        try:

            os.mkdir(output)
        
        except FileExistsError: 
            
            typer.echo(f"Folder {output} already exists, all files will be overwritten")

            shutil.rmtree(output)

            os.mkdir(output)

        typer.echo(f"Extracting {len(subjects)} subjects")

        for subject, subject_file in zip(subjects, subjects_zip):

            try:

                with tarfile.open(os.path.join(path, subject_file)) as tar:

                    tar.extractall(path = os.path.join(output, subject))
                                    
                tar.close()

            except IOError as e:

                typer.echo(f"Error extracting file: {subject}")
    
    typer.echo("Extraction finished")

    typer.echo("Moving files...")

    if len(subjects):

        join_new_folder = lambda subject: [folder[0] for folder in os.walk(os.path.join(output, subject)) if len(folder[2])] 
        
        move_files = lambda curretfolder, subject: shutil.move(curretfolder, os.path.join(output, subject))
        
        keep_files_to_move = lambda folder: glob.glob(folder + "/[!p]*")
        
        # remove_folders = lambda subject: shutil.rmtree(os.path.join(output, subject, "p"))

        folder_files = list(map(join_new_folder, subjects))
        
        for index_folder, datafolder in enumerate(folder_files):

            if len(subjects) == 1: files_keep = list(map(keep_files_to_move, datafolder))[0]
            
            else: files_keep = list(map(keep_files_to_move, datafolder))[0]

            try:

                list(map(move_files, files_keep, repeat(subjects[index_folder])))
                    
                # list(map(remove_folders, subjects[index_folder]))

            except FileNotFoundError:

                typer.echo("File does not exist because it was extracted")
            
            except shutil.Error as e:

                print(e)

                typer.echo(f"File already exists, {subjects[index_folder]} will be passed")

            else:
                
                typer.echo(f"Completed extracting files: {subjects[index_folder]}")
        
        typer.echo("Completed moving files")
    
    else: typer.echo("No files to extract")

@app.command()
def devide(subjects: List[str] = typer.Option(ALL_SUBJECTS,
                                                 "--subjects",
                                                 "-s",
                                                 help = "List of subject to extract from Kara One databse"),
              path: Optional[str] = typer.Option("rawextracted",
                                                 "--path",
                                                 "-p",
                                                 help = "Path to rawdata"),                                                 
              output: Optional[str] = typer.Option("cleandata",
                                                 "--output",
                                                 "-o",
                                                 help = "Path to save clean data")) -> None:
    
    """Function to extract raw .cnt file from subject and made it ml epochs """
    
    typer.echo("Extracting files...")

    subjects = list(subjects)
    
    check_if_files = lambda folder: len(glob.glob(os.path.join(path, folder, "*.cnt"))) == 1
    
    check_if_folder = lambda folder: os.path.exists(os.path.join(path, folder)) == True
    
    folders = list(map(check_if_folder, subjects))
    
    subjects = list(set([subjects[index] for index, value in enumerate(folders) if value]))
    
    files = list(map(check_if_files, subjects))
    
    only_cnt_subjects = list(set([subjects[index] for index, value in enumerate(files) if value]))
    
    cnt_files = list(map(lambda subject: glob.glob(os.path.join(path, subject, "*.cnt"))[0], only_cnt_subjects))
    
    if subjects:
        
        try:

            os.mkdir(output)
        
        except FileExistsError: 
            
            typer.echo(f"Folder {output} already exists, all files will be overwritten")

            shutil.rmtree(output)

            os.mkdir(output)
        
        if any(files):
            
            typer.echo(f"Spliting {len(only_cnt_subjects)} subjects")
            
            for subject, cnt_file in zip(only_cnt_subjects, cnt_files):
                
                typer.echo(f"Spliting files from {subject}")
                
                process = Dataset(subject, cnt_file, output = output, raw = path)
                
                try:
                    
                    process.make_dataset()
                
                except Exception as e: 
                    
                    typer.echo(f"Error processing subject: {subject}")
                    
                    print(e)

                else: typer.echo(f"Completed processing subject: {subject}")
            
            typer.echo("Completed processing subjects")
            
        else: typer.echo("You don't have any .cnt files in the folder")   
    
    else: typer.echo("You dont have any subjects to clean")