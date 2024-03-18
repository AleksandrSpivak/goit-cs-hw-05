# reading and coping files done by two different functions

import argparse
import logging
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile


parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source directory")
parser.add_argument("--output", "-o", help="Output directory", default="destination")

args = vars(parser.parse_args())
source = AsyncPath(args["source"])
output = AsyncPath(args["output"])

folders = []
file_number = 0


async def read_folder(path: AsyncPath):
    """
    Async function that recursively reads a folder and its subfolders.
    :param path: AsyncPath - the path of the folder to read
    :return: None
    """

    async for child in path.iterdir():

        if await child.is_dir():
            folders.append(child)
            await read_folder(child)
    return


async def copy_files(source: AsyncPath, output: AsyncPath):
    """
    Asynchronously copies files from the source directory to the output directory.
    Args:
        source (AsyncPath): The source directory path.
        output (AsyncPath): The output directory path.

    Returns:
        None
    """
    global file_number
    async for child in source.iterdir():
        if await child.is_file():
            folder = AsyncPath(output / child.suffix[1:])
            try:
                await folder.mkdir(exist_ok=True, parents=True)
                await copyfile(child, folder / child.name)
                file_number += 1
            except OSError as err:
                logging.error(err)
    return


async def main():

    await asyncio.gather(read_folder(source))

    for folder in folders:
        await copy_files(folder, output)


if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    folders.append(source)
    asyncio.run(main())

    print(f"{file_number} files were copied from '{source}' directory to '{output}' directory")
